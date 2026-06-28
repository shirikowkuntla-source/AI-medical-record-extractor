import fastapi
import uvicorn
import pydantic
import PyPDF2
from PIL import Image
import pytesseract

print("SUCCESS: All core dependencies installed!")
print(f"FastAPI: {fastapi.__version__}")
print(f"Pydantic: {pydantic.__version__}")
print(f"PyPDF2: {PyPDF2.__version__}")
print(f"Pillow: {Image.__version__ if hasattr(Image, '__version__') else 'installed'}")
print(f"pytesseract: {pytesseract.__version__}")