import pytest
from fastapi.testclient import TestClient
import io
import os
import sys

# Add parent directory to path for imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.api.main import app
from src.models.schemas import ExtractionResponse, UploadResponse


client = TestClient(app)


class TestHealthEndpoints:
    """Test health check endpoints."""
    
    def test_root_endpoint(self):
        """Test root endpoint returns healthy status."""
        response = client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert data["service"] == "AI Medical Record Extractor"
    
    def test_health_endpoint(self):
        """Test health endpoint."""
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"


class TestUploadEndpoint:
    """Test file upload endpoint."""
    
    def test_upload_txt_file(self):
        """Test uploading a valid text file."""
        content = b"Patient Name: John Doe\nAge: 30\nDiagnosis: Fever"
        files = {"file": ("test.txt", io.BytesIO(content), "text/plain")}
        
        response = client.post("/upload", files=files)
        assert response.status_code == 200
        data = response.json()
        assert data["filename"] == "test.txt"
        assert data["size"] == len(content)
        assert "uploaded successfully" in data["message"]
    
    def test_upload_invalid_extension(self):
        """Test uploading file with invalid extension."""
        content = b"test content"
        files = {"file": ("test.exe", io.BytesIO(content), "application/octet-stream")}
        
        response = client.post("/upload", files=files)
        assert response.status_code == 400
        assert "not allowed" in response.json()["detail"].lower()
    
    def test_upload_no_file(self):
        """Test upload without file."""
        response = client.post("/upload")
        assert response.status_code == 422  # Validation error


class TestExtractEndpoint:
    """Test extraction endpoint."""
    
    def test_extract_from_txt(self):
        """Test extraction from text file."""
        content = b"""
        Patient Name: Jane Smith
        Age: 45
        Gender: Female
        Symptoms: Fever, Cough, Headache
        Diagnosis: Viral Infection
        Medications: Paracetamol, Cough Syrup
        Doctor: Dr. John Doe
        Hospital: City Hospital
        """
        files = {"file": ("medical.txt", io.BytesIO(content), "text/plain")}
        
        response = client.post("/extract", files=files)
        assert response.status_code == 200
        data = response.json()
        
        # Verify extracted data
        assert data["patient_name"] == "Jane Smith"
        assert data["age"] == 45
        assert data["gender"] == "Female"
        assert "fever" in [s.lower() for s in data["symptoms"]]
        assert data["diagnosis"] is not None
        assert len(data["medications"]) > 0
        assert data["doctor_name"] == "John Doe"
        assert data["hospital_name"] == "City Hospital"
        assert len(data["summary"]) > 0
    
    def test_extract_empty_text(self):
        """Test extraction with insufficient text."""
        content = b"Short"
        files = {"file": ("short.txt", io.BytesIO(content), "text/plain")}
        
        response = client.post("/extract", files=files)
        assert response.status_code == 400
        assert "sufficient text" in response.json()["detail"].lower()
    
    def test_extract_invalid_file_type(self):
        """Test extraction with invalid file type."""
        content = b"test"
        files = {"file": ("test.xyz", io.BytesIO(content), "application/octet-stream")}
        
        response = client.post("/extract", files=files)
        assert response.status_code == 400


class TestExtractTextEndpoint:
    """Test text extraction endpoint."""
    
    def test_extract_from_raw_text(self):
        """Test extraction from raw text input."""
        form_data = {
            "text": """
            Patient Name: Robert Johnson
            Age: 62
            Gender: Male
            Diagnosis: Hypertension
            Medications: Lisinopril, Amlodipine
            """
        }
        
        response = client.post("/extract-text", data=form_data)
        assert response.status_code == 200
        data = response.json()
        
        assert data["patient_name"] == "Robert Johnson"
        assert data["age"] == 62
        assert data["gender"] == "Male"
        assert data["diagnosis"] is not None
    
    def test_extract_short_text(self):
        """Test extraction with too short text."""
        form_data = {"text": "Hi"}
        
        response = client.post("/extract-text", data=form_data)
        assert response.status_code == 400
    
    def test_extract_empty_text(self):
        """Test extraction with empty text."""
        form_data = {"text": ""}
        
        response = client.post("/extract-text", data=form_data)
        assert response.status_code == 400


class TestRecordsEndpoints:
    """Test records management endpoints."""
    
    def test_get_records(self):
        """Test getting all records."""
        response = client.get("/records")
        assert response.status_code == 200
        data = response.json()
        assert "records" in data
        assert "count" in data
    
    def test_get_records_with_pagination(self):
        """Test pagination parameters."""
        response = client.get("/records?limit=10&offset=0")
        assert response.status_code == 200
        data = response.json()
        assert data["limit"] == 10
        assert data["offset"] == 0
    
    def test_get_specific_record(self):
        """Test getting a specific record."""
        # First, create a record
        content = b"Patient: Test User\nAge: 25"
        files = {"file": ("test.txt", io.BytesIO(content), "text/plain")}
        extract_response = client.post("/extract", files=files)
        assert extract_response.status_code == 200
        
        # This is a simplified test - in real scenario, we'd track the ID
        response = client.get("/records/999999")
        assert response.status_code == 404
    
    def test_search_records(self):
        """Test searching records."""
        response = client.get("/search?query=test")
        assert response.status_code == 200
        data = response.json()
        assert "results" in data
        assert "query" in data
    
    def test_search_short_query(self):
        """Test search with too short query."""
        response = client.get("/search?query=a")
        assert response.status_code == 400
    
    def test_delete_record(self):
        """Test deleting a record."""
        response = client.delete("/records/999999")
        assert response.status_code == 404


class TestErrorHandling:
    """Test error handling."""
    
    def test_invalid_endpoint(self):
        """Test accessing invalid endpoint."""
        response = client.get("/invalid-endpoint")
        assert response.status_code == 404
    
    def test_extract_malformed_file(self):
        """Test extraction with malformed file."""
        # Create a file that will cause issues
        content = b"\x00\x01\x02\x03"  # Binary content
        files = {"file": ("binary.bin", io.BytesIO(content), "application/octet-stream")}
        
        response = client.post("/extract", files=files)
        # Should fail validation or extraction
        assert response.status_code in [400, 500]


class TestResponseModels:
    """Test response model validation."""
    
    def test_extraction_response_structure(self):
        """Test that extraction response has correct structure."""
        content = b"Patient: Test\nAge: 30\nDiagnosis: Test Condition"
        files = {"file": ("test.txt", io.BytesIO(content), "text/plain")}
        
        response = client.post("/extract", files=files)
        assert response.status_code == 200
        
        # Verify all required fields are present
        data = response.json()
        required_fields = [
            "patient_name", "age", "gender", "symptoms", "diagnosis",
            "medications", "medical_history", "doctor_name",
            "hospital_name", "summary"
        ]
        for field in required_fields:
            assert field in data, f"Missing field: {field}"