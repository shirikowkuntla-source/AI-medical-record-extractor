import os
import io
import logging
from typing import Optional, Tuple
from pathlib import Path

logger = logging.getLogger(__name__)


class FileProcessor:
    """Handle file upload and text extraction from various formats."""
    
    ALLOWED_EXTENSIONS = {'.pdf', '.txt', '.png', '.jpg', '.jpeg', '.bmp', '.tiff'}
    MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB
    
    @classmethod
    def validate_file(cls, filename: str, file_size: int) -> Tuple[bool, str]:
        """Validate uploaded file.
        
        Args:
            filename: Name of the uploaded file
            file_size: Size of the file in bytes
            
        Returns:
            Tuple of (is_valid, error_message)
        """
        if not filename:
            return False, "No filename provided"
        
        file_ext = Path(filename).suffix.lower()
        if file_ext not in cls.ALLOWED_EXTENSIONS:
            return False, f"File type not allowed. Allowed types: {', '.join(cls.ALLOWED_EXTENSIONS)}"
        
        if file_size > cls.MAX_FILE_SIZE:
            return False, f"File size too large. Maximum size: {cls.MAX_FILE_SIZE / 1024 / 1024}MB"
        
        return True, ""
    
    @classmethod
    def extract_text(cls, file_path: str, content_type: str) -> str:
        """Extract text from uploaded file.
        
        Args:
            file_path: Path to the uploaded file
            content_type: MIME type of the file
            
        Returns:
            Extracted text content
            
        Raises:
            ValueError: If file format is not supported
            Exception: If text extraction fails
        """
        file_ext = Path(file_path).suffix.lower()
        
        try:
            if file_ext == '.txt':
                return cls._extract_from_txt(file_path)
            elif file_ext == '.pdf':
                return cls._extract_from_pdf(file_path)
            elif file_ext in {'.png', '.jpg', '.jpeg', '.bmp', '.tiff'}:
                return cls._extract_from_image(file_path)
            else:
                raise ValueError(f"Unsupported file format: {file_ext}")
        except Exception as e:
            logger.error(f"Error extracting text from {file_path}: {str(e)}")
            raise
    
    @staticmethod
    def _extract_from_txt(file_path: str) -> str:
        """Extract text from plain text file.
        
        Args:
            file_path: Path to text file
            
        Returns:
            Text content
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return f.read()
        except UnicodeDecodeError:
            # Try with different encoding
            with open(file_path, 'r', encoding='latin-1') as f:
                return f.read()
    
    @staticmethod
    def _extract_from_pdf(file_path: str) -> str:
        """Extract text from PDF file.
        
        Args:
            file_path: Path to PDF file
            
        Returns:
            Extracted text content
        """
        try:
            import PyPDF2
            with open(file_path, 'rb') as f:
                pdf_reader = PyPDF2.PdfReader(f)
                text = ""
                for page in pdf_reader.pages:
                    text += page.extract_text() or ""
                return text.strip()
        except ImportError:
            raise ImportError("PyPDF2 is required for PDF processing. Install with: pip install PyPDF2")
    
    @staticmethod
    def _extract_from_image(file_path: str) -> str:
        """Extract text from image using OCR.
        
        Args:
            file_path: Path to image file
            
        Returns:
            Extracted text content
        """
        try:
            import pytesseract
            from PIL import Image
            
            image = Image.open(file_path)
            text = pytesseract.image_to_string(image)
            return text.strip()
        except ImportError:
            raise ImportError("pytesseract and PIL are required for image processing. Install with: pip install pytesseract Pillow")
    
    @staticmethod
    def get_file_info(file_path: str) -> dict:
        """Get file information.
        
        Args:
            file_path: Path to the file
            
        Returns:
            Dictionary with file information
        """
        path = Path(file_path)
        stat = path.stat()
        
        return {
            "filename": path.name,
            "extension": path.suffix.lower(),
            "size": stat.st_size,
            "created_at": stat.st_ctime
        }