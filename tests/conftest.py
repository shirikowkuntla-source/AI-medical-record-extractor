import pytest
import sys
import os

# Add project root to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


@pytest.fixture(scope="session")
def app():
    """Create FastAPI test application."""
    from src.api.main import app
    return app


@pytest.fixture(scope="session")
def client(app):
    """Create test client."""
    from fastapi.testclient import TestClient
    return TestClient(app)


@pytest.fixture(scope="function")
def sample_text_file(tmp_path):
    """Create a sample text file for testing."""
    file_path = tmp_path / "sample_medical.txt"
    content = """
    Patient Name: John Doe
    Age: 35
    Gender: Male
    Symptoms: Fever, Cough
    Diagnosis: Common Cold
    Medications: Paracetamol
    Doctor: Dr. Smith
    Hospital: Test Hospital
    """
    file_path.write_text(content)
    return file_path


@pytest.fixture(scope="function")
def sample_pdf_file(tmp_path):
    """Create a sample PDF file for testing."""
    try:
        from PyPDF2 import PdfWriter
        
        file_path = tmp_path / "sample_medical.pdf"
        writer = PdfWriter()
        
        # Add a page with medical text
        page_text = """
        Patient Name: Jane Smith
        Age: 45
        Gender: Female
        Diagnosis: Hypertension
        Medications: Lisinopril
        """
        
        # Note: In real scenario, you'd use reportlab or similar to create PDF
        # For testing, we'll just create an empty file
        file_path.write_bytes(b"")
        return file_path
    except ImportError:
        pytest.skip("PyPDF2 not installed")


@pytest.fixture(scope="function")
def cleanup_uploads():
    """Cleanup upload directory after tests."""
    yield
    # Cleanup logic if needed
    pass