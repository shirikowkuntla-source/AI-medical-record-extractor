from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime


class MedicalRecord(BaseModel):
    """Medical record data model."""
    patient_name: Optional[str] = None
    age: Optional[int] = None
    gender: Optional[str] = None
    symptoms: List[str] = []
    diagnosis: Optional[str] = None
    medicines: List[str] = []
    medical_history: List[str] = []
    doctor_name: Optional[str] = None
    hospital_name: Optional[str] = None
    summary: Optional[str] = None
    extracted_at: datetime = Field(default_factory=datetime.now)


class ExtractionRequest(BaseModel):
    """Request model for extraction."""
    document_text: str


class ExtractionResponse(BaseModel):
    """Response model for extraction."""
    patient_name: Optional[str] = None
    age: Optional[int] = None
    gender: Optional[str] = None
    symptoms: List[str] = []
    diagnosis: Optional[str] = None
    medications: List[str] = []
    medical_history: List[str] = []
    doctor_name: Optional[str] = None
    hospital_name: Optional[str] = None
    summary: str


class UploadResponse(BaseModel):
    """Response model for file upload."""
    filename: str
    content_type: str
    size: int
    message: str


class ErrorResponse(BaseModel):
    """Error response model."""
    detail: str
    error_type: str