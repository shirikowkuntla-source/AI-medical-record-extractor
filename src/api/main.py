import os
import logging
import uuid
from typing import Optional
from fastapi import FastAPI, File, UploadFile, HTTPException, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from models.schemas import (
    ExtractionResponse,
    UploadResponse,
    ErrorResponse
)
from extractor.medical_extractor import MedicalExtractor
from utils.file_processor import FileProcessor
from database.db import Database

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="AI Medical Record Extractor",
    description="Extract structured medical information from unstructured documents using CPU-only inference",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify exact origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize components
extractor = MedicalExtractor()
file_processor = FileProcessor()
db = Database()

# Create upload directory
UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)


@app.get("/")
async def root():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "service": "AI Medical Record Extractor",
        "version": "1.0.0"
    }


@app.get("/health")
async def health_check():
    """Detailed health check."""
    return {
        "status": "healthy",
        "database": "connected",
        "extractor": "ready"
    }


@app.post("/upload", response_model=UploadResponse)
async def upload_file(file: UploadFile = File(...)):
    """Upload a medical record file.
    
    Accepts:
    - PDF files (.pdf)
    - Text files (.txt)
    - Image files (.png, .jpg, .jpeg, .bmp, .tiff)
    
    Args:
        file: Uploaded file
        
    Returns:
        Upload response with file information
        
    Raises:
        HTTPException: If file validation fails
    """
    try:
        logger.info(f"Upload request received: {file.filename}")
        
        # Validate file
        is_valid, error_msg = file_processor.validate_file(file.filename, file.size)
        if not is_valid:
            logger.warning(f"File validation failed: {error_msg}")
            raise HTTPException(status_code=400, detail=error_msg)
        
        # Generate unique filename
        file_ext = os.path.splitext(file.filename)[1]
        unique_filename = f"{uuid.uuid4()}{file_ext}"
        file_path = os.path.join(UPLOAD_DIR, unique_filename)
        
        # Save file
        with open(file_path, "wb") as buffer:
            content = await file.read()
            buffer.write(content)
        
        logger.info(f"File uploaded successfully: {unique_filename}")
        
        return UploadResponse(
            filename=file.filename,
            content_type=file.content_type,
            size=file.size,
            message="File uploaded successfully"
        )
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error uploading file: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error uploading file: {str(e)}")


@app.post("/extract", response_model=ExtractionResponse)
async def extract_information(file: UploadFile = File(...)):
    """Extract structured medical information from uploaded file.
    
    Args:
        file: Uploaded medical record file
        
    Returns:
        Extracted medical information in structured format
        
    Raises:
        HTTPException: If extraction fails
    """
    try:
        logger.info(f"Extraction request received: {file.filename}")
        
        # Validate file
        is_valid, error_msg = file_processor.validate_file(file.filename, file.size)
        if not is_valid:
            logger.warning(f"File validation failed: {error_msg}")
            raise HTTPException(status_code=400, detail=error_msg)
        
        # Save file temporarily
        file_ext = os.path.splitext(file.filename)[1]
        unique_filename = f"{uuid.uuid4()}{file_ext}"
        file_path = os.path.join(UPLOAD_DIR, unique_filename)
        
        with open(file_path, "wb") as buffer:
            content = await file.read()
            buffer.write(content)
        
        try:
            # Extract text from file
            logger.info(f"Extracting text from {file.filename}")
            text = file_processor.extract_text(file_path, file.content_type)
            
            if not text or len(text.strip()) < 10:
                raise HTTPException(
                    status_code=400,
                    detail="Could not extract sufficient text from file. Please ensure the file contains readable text."
                )
            
            # Extract medical information
            logger.info("Extracting medical information")
            extracted_data = extractor.extract(text)
            
            # Save to database
            logger.info("Saving to database")
            record_id = db.save_record(extracted_data)
            logger.info(f"Record saved with ID: {record_id}")
            
            # Return response
            return ExtractionResponse(**extracted_data)
        
        finally:
            # Clean up temporary file
            if os.path.exists(file_path):
                os.remove(file_path)
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error during extraction: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Extraction failed: {str(e)}")


@app.post("/extract-text", response_model=ExtractionResponse)
async def extract_from_text(text: str = Form(...)):
    """Extract medical information from raw text.
    
    Args:
        text: Raw medical document text
        
    Returns:
        Extracted medical information
    """
    try:
        logger.info("Text extraction request received")
        
        if not text or len(text.strip()) < 10:
            raise HTTPException(
                status_code=400,
                detail="Text is too short for extraction. Please provide more content."
            )
        
        # Extract medical information
        extracted_data = extractor.extract(text)
        
        # Save to database
        record_id = db.save_record(extracted_data)
        logger.info(f"Record saved with ID: {record_id}")
        
        return ExtractionResponse(**extracted_data)
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error during text extraction: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Extraction failed: {str(e)}")


@app.get("/records")
async def get_records(limit: int = 100, offset: int = 0):
    """Get all medical records.
    
    Args:
        limit: Maximum number of records to return
        offset: Offset for pagination
        
    Returns:
        List of medical records
    """
    try:
        records = db.get_all_records(limit=limit, offset=offset)
        return {
            "records": records,
            "limit": limit,
            "offset": offset,
            "count": len(records)
        }
    except Exception as e:
        logger.error(f"Error fetching records: {str(e)}")
        raise HTTPException(status_code=500, detail="Error fetching records")


@app.get("/records/{record_id}")
async def get_record(record_id: int):
    """Get a specific medical record by ID.
    
    Args:
        record_id: Record ID
        
    Returns:
        Medical record details
    """
    try:
        record = db.get_record(record_id)
        if not record:
            raise HTTPException(status_code=404, detail="Record not found")
        return record
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error fetching record: {str(e)}")
        raise HTTPException(status_code=500, detail="Error fetching record")


@app.get("/search")
async def search_records(query: str):
    """Search medical records.
    
    Args:
        query: Search query (patient name or diagnosis)
        
    Returns:
        List of matching records
    """
    try:
        if not query or len(query.strip()) < 2:
            raise HTTPException(
                status_code=400,
                detail="Search query must be at least 2 characters long"
            )
        
        records = db.search_records(query)
        return {
            "query": query,
            "results": records,
            "count": len(records)
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error searching records: {str(e)}")
        raise HTTPException(status_code=500, detail="Error searching records")


@app.delete("/records/{record_id}")
async def delete_record(record_id: int):
    """Delete a medical record.
    
    Args:
        record_id: Record ID
        
    Returns:
        Success message
    """
    try:
        deleted = db.delete_record(record_id)
        if not deleted:
            raise HTTPException(status_code=404, detail="Record not found")
        
        return {"message": "Record deleted successfully", "id": record_id}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error deleting record: {str(e)}")
        raise HTTPException(status_code=500, detail="Error deleting record")


@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    """Global exception handler."""
    logger.error(f"Unhandled exception: {str(exc)}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content=ErrorResponse(
            detail="An unexpected error occurred",
            error_type="internal_error"
        ).dict()
    )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)