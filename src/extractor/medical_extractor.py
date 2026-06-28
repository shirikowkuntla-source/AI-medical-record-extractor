import re
import logging
from typing import Dict, List, Optional, Any
from dataclasses import dataclass

logger = logging.getLogger(__name__)


@dataclass
class MedicalExtractor:
    """Extract structured medical information from text.
    
    Uses pattern matching and rule-based extraction for CPU-only inference.
    Designed to work completely offline without external API calls.
    """
    
    def extract(self, text: str) -> Dict[str, Any]:
        """Extract medical information from text.
        
        Args:
            text: Raw text from medical document
            
        Returns:
            Dictionary with extracted medical information
        """
        if not text or not text.strip():
            raise ValueError("Empty text provided for extraction")
        
        text = self._clean_text(text)
        
        return {
            "patient_name": self._extract_patient_name(text),
            "age": self._extract_age(text),
            "gender": self._extract_gender(text),
            "symptoms": self._extract_symptoms(text),
            "diagnosis": self._extract_diagnosis(text),
            "medications": self._extract_medications(text),
            "medical_history": self._extract_medical_history(text),
            "doctor_name": self._extract_doctor_name(text),
            "hospital_name": self._extract_hospital_name(text),
            "summary": self._generate_summary(text)
        }
    
    @staticmethod
    def _clean_text(text: str) -> str:
        """Clean and normalize text.
        
        Args:
            text: Raw text
            
        Returns:
            Cleaned text
        """
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text)
        # Remove special characters but keep medical relevant ones
        text = re.sub(r'[^\w\s\.\,\;\:\-\(\)\/\%\@\#\*\+\=\<\>\!]', '', text)
        return text.strip()
    
    def _extract_patient_name(self, text: str) -> Optional[str]:
        """Extract patient name from text.
        
        Args:
            text: Medical document text
            
        Returns:
            Patient name or None
        """
        # Common patterns for patient name
        patterns = [
            r'Patient\s*Name[:\s]+([A-Z][a-z]+(?:\s+[A-Z][a-z]+)+)',
            r'Name[:\s]+([A-Z][a-z]+(?:\s+[A-Z][a-z]+)+)',
            r'Patient[:\s]+([A-Z][a-z]+(?:\s+[A-Z][a-z]+)+)',
            r'Mr\.?\s+([A-Z][a-z]+(?:\s+[A-Z][a-z]+)+)',
            r'Mrs\.?\s+([A-Z][a-z]+(?:\s+[A-Z][a-z]+)+)',
            r'Ms\.?\s+([A-Z][a-z]+(?:\s+[A-Z][a-z]+)+)',
        ]
        
        for pattern in patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                name = match.group(1).strip()
                # Validate it's not a common word
                if len(name.split()) >= 2 and name.split()[0].lower() not in ['the', 'this', 'that']:
                    return name
        
        return None
    
    def _extract_age(self, text: str) -> Optional[int]:
        """Extract patient age from text.
        
        Args:
            text: Medical document text
            
        Returns:
            Age as integer or None
        """
        patterns = [
            r'Age[:\s]+(\d{1,3})',
            r'(\d{1,3})\s*(?:years?|yrs?|y\.?o\.?)',
            r'(\d{1,3})\s*(?:year\s+old)',
        ]
        
        for pattern in patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                age = int(match.group(1))
                if 0 < age < 150:  # Reasonable age range
                    return age
        
        return None
    
    def _extract_gender(self, text: str) -> Optional[str]:
        """Extract patient gender from text.
        
        Args:
            text: Medical document text
            
        Returns:
            Gender (Male/Female/Other) or None
        """
        text_lower = text.lower()
        
        if re.search(r'\b(male|man|boy|gentleman|mr\.?)\b', text_lower):
            return "Male"
        elif re.search(r'\b(female|woman|girl|lady|mrs\.?|ms\.?)\b', text_lower):
            return "Female"
        
        return None
    
    def _extract_symptoms(self, text: str) -> List[str]:
        """Extract symptoms from text.
        
        Args:
            text: Medical document text
            
        Returns:
            List of symptoms
        """
        symptoms = []
        
        # Common symptom patterns
        symptom_keywords = [
            'pain', 'fever', 'cough', 'headache', 'nausea', 'vomiting',
            'diarrhea', 'fatigue', 'weakness', 'dizziness', 'chest pain',
            'shortness of breath', 'sore throat', 'runny nose', 'congestion',
            'body ache', 'joint pain', 'swelling', 'rash', 'itching',
            'bleeding', 'bruising', 'numbness', 'tingling', 'anxiety',
            'depression', 'insomnia', 'loss of appetite', 'weight loss',
            'weight gain', 'blurred vision', 'hearing loss', 'tinnitus'
        ]
        
        text_lower = text.lower()
        
        for symptom in symptom_keywords:
            if symptom in text_lower:
                # Find the context around the symptom
                pattern = rf'\b\w*\s*{re.escape(symptom)}\s*\w*\b'
                matches = re.findall(pattern, text_lower)
                for match in matches[:2]:  # Limit to 2 variations per symptom
                    if match not in symptoms:
                        symptoms.append(match.strip())
        
        return symptoms[:10]  # Limit to top 10 symptoms
    
    def _extract_diagnosis(self, text: str) -> Optional[str]:
        """Extract diagnosis from text.
        
        Args:
            text: Medical document text
            
        Returns:
            Diagnosis or None
        """
        patterns = [
            r'Diagnosis[:\s]+([^\.]+)',
            r'Diagnosed\s+(?:with\s+)?([^\.]+)',
            r'Condition[:\s]+([^\.]+)',
            r'Disease[:\s]+([^\.]+)',
        ]
        
        for pattern in patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                diagnosis = match.group(1).strip()
                if len(diagnosis) > 3 and len(diagnosis) < 200:
                    return diagnosis
        
        return None
    
    def _extract_medications(self, text: str) -> List[str]:
        """Extract medications from text.
        
        Args:
            text: Medical document text
            
        Returns:
            List of medications
        """
        medications = []
        
        # Look for medication section
        med_section = re.search(
            r'(?:Medications?|Medicine|Drugs?|Rx|Prescription)[:\s]+(.*?)(?:\n\n|\Z)',
            text,
            re.IGNORECASE | re.DOTALL
        )
        
        if med_section:
            med_text = med_section.group(1)
            # Extract medication names (usually capitalized or specific patterns)
            med_patterns = [
                r'\b([A-Z][a-z]+(?:cin|mycin|prazole|statin|sartan|pril|olol|pine|zone|mab|xaban|dipine))\b',
                r'\b(\d+\s*(?:mg|mcg|ml|g)\s+[A-Z][a-z]+)\b',
                r'Tab\.?\s+([A-Z][a-z]+)',
                r'Cap\.?\s+([A-Z][a-z]+)',
            ]
            
            for pattern in med_patterns:
                matches = re.findall(pattern, med_text)
                medications.extend(matches)
        
        # Common medication keywords
        common_meds = [
            'aspirin', 'paracetamol', 'ibuprofen', 'amoxicillin', 'metformin',
            'lisinopril', 'atorvastatin', 'omeprazole', 'amlodipine', 'metoprolol',
            'losartan', 'gabapentin', 'hydrochlorothiazide', 'furosemide',
            'prednisone', 'cephalexin', 'ciprofloxacin', 'azithromycin'
        ]
        
        text_lower = text.lower()
        for med in common_meds:
            if med in text_lower:
                if med not in medications:
                    medications.append(med)
        
        return medications[:15]  # Limit to 15 medications
    
    def _extract_medical_history(self, text: str) -> List[str]:
        """Extract medical history from text.
        
        Args:
            text: Medical document text
            
        Returns:
            List of medical history items
        """
        history = []
        
        # Look for history section
        history_section = re.search(
            r'(?:Medical History|Past History|History|Previous Conditions?)[:\s]+(.*?)(?:\n\n|\Z)',
            text,
            re.IGNORECASE | re.DOTALL
        )
        
        if history_section:
            history_text = history_section.group(1)
            # Split by common delimiters
            items = re.split(r'[,;\n•\-]', history_text)
            for item in items:
                item = item.strip()
                if item and len(item) > 2 and len(item) < 100:
                    history.append(item)
        
        # Common medical conditions
        conditions = [
            'diabetes', 'hypertension', 'asthma', 'heart disease', 'cancer',
            'arthritis', 'thyroid', 'kidney disease', 'liver disease', 'stroke',
            'heart attack', 'bypass surgery', 'appendectomy', 'tonsillectomy'
        ]
        
        text_lower = text.lower()
        for condition in conditions:
            if condition in text_lower and condition not in history:
                history.append(condition)
        
        return history[:10]  # Limit to 10 items
    
    def _extract_doctor_name(self, text: str) -> Optional[str]:
        """Extract doctor name from text.
        
        Args:
            text: Medical document text
            
        Returns:
            Doctor name or None
        """
        patterns = [
            r'Dr\.?\s+([A-Z][a-z]+(?:\s+[A-Z][a-z]+)+)',
            r'Doctor[:\s]+([A-Z][a-z]+(?:\s+[A-Z][a-z]+)+)',
            r'Physician[:\s]+([A-Z][a-z]+(?:\s+[A-Z][a-z]+)+)',
            r'Consultant[:\s]+([A-Z][a-z]+(?:\s+[A-Z][a-z]+)+)',
        ]
        
        for pattern in patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                name = match.group(1).strip()
                if len(name.split()) >= 2:
                    return name
        
        return None
    
    def _extract_hospital_name(self, text: str) -> Optional[str]:
        """Extract hospital/clinic name from text.
        
        Args:
            text: Medical document text
            
        Returns:
            Hospital name or None
        """
        patterns = [
            r'(?:Hospital|Clinic|Medical Center|Healthcare|Health Center)[:\s]+([^\.]+)',
            r'([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*\s+(?:Hospital|Clinic|Medical Center|Healthcare))',
        ]
        
        for pattern in patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                name = match.group(0).strip() if match.lastindex == 0 else match.group(1).strip()
                if len(name) > 5 and len(name) < 100:
                    return name
        
        return None
    
    def _generate_summary(self, text: str) -> str:
        """Generate a summary of the medical document.
        
        Args:
            text: Medical document text
            
        Returns:
            Summary string
        """
        # Extract key information for summary
        patient = self._extract_patient_name(text)
        age = self._extract_age(text)
        gender = self._extract_gender(text)
        diagnosis = self._extract_diagnosis(text)
        symptoms = self._extract_symptoms(text)
        
        summary_parts = []
        
        if patient:
            summary_parts.append(f"Patient {patient}")
        if age:
            summary_parts.append(f"aged {age}")
        if gender:
            summary_parts.append(f"({gender})")
        
        if symptoms:
            summary_parts.append(f"presenting with {', '.join(symptoms[:3])}")
        
        if diagnosis:
            summary_parts.append(f"diagnosed with {diagnosis}")
        
        if not summary_parts:
            # Fallback: use first 100 characters
            return text[:100] + "..." if len(text) > 100 else text
        
        return " ".join(summary_parts) + "."