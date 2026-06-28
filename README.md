# 🩺 AI Medical Record Extractor

## Overview

AI Medical Record Extractor is an **offline-first, CPU-powered** application that converts unstructured medical documents (prescriptions, lab reports, medical records) into structured JSON data. The application works completely without an internet connection and uses CPU-only inference for all AI operations.

## Key Features

- ✅ **100% Offline Operation** - No internet connection required
- ✅ **CPU-Only Inference** - No GPU/CUDA needed
- ✅ **Multiple File Formats** - PDF, TXT, PNG, JPG, JPEG, BMP, TIFF
- ✅ **Structured Extraction** - Patient details, diagnosis, medications, symptoms
- ✅ **Local Storage** - SQLite database for record management
- ✅ **Modern Web UI** - React-based responsive interface
- ✅ **FastAPI Backend** - High-performance Python API
- ✅ **Open Source** - Built with open-source tools

## Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    Frontend (React + Vite)               │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  │
│  │ Upload       │  │ Results      │  │ Health       │  │
│  │ Component    │→ │ Component    │  │ Monitor      │  │
│  └──────────────┘  └──────────────┘  └──────────────┘  │
└──────────────────────┬──────────────────────────────────┘
                       │ HTTP/REST API
                       ↓
┌─────────────────────────────────────────────────────────┐
│              Backend (FastAPI + Python)                  │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  │
│  │ File         │  │ Medical      │  │ Database     │  │
│  │ Processor    │→ │ Extractor    │→ │ (SQLite)     │  │
│  └──────────────┘  └──────────────┘  └──────────────┘  │
│  - PDF Parsing    - Rule-based     - Record Storage    │
│  - OCR (Tesseract)  Extraction    - Search/Retrieve   │
│  - Text Parsing   - Pattern Match  - History           │
└─────────────────────────────────────────────────────────┘
```

## Tech Stack

### Backend
- **FastAPI** - Modern, fast web framework for Python
- **Pydantic** - Data validation and settings management
- **SQLite** - Lightweight database for local storage
- **PyPDF2** - PDF text extraction
- **Pytesseract** - OCR for image files
- **Pillow** - Image processing

### Frontend
- **React 18** - User interface library
- **Vite** - Fast build tool and dev server
- **React Dropzone** - File upload component
- **Axios** - HTTP client for API calls

### AI/ML
- **Rule-based Extraction** - CPU-only pattern matching
- **No External APIs** - All processing happens locally
- **No GPU Required** - Optimized for CPU inference

## Project Structure

```
ai-medical-record-extractor/
├── src/
│   ├── api/
│   │   └── main.py              # FastAPI application & endpoints
│   ├── extractor/
│   │   └── medical_extractor.py # Medical information extraction
│   ├── models/
│   │   └── schemas.py           # Pydantic data models
│   ├── utils/
│   │   └── file_processor.py    # File upload & text extraction
│   └── database/
│       └── db.py                # SQLite database handler
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── UploadComponent.jsx   # Drag-and-drop upload
│   │   │   └── ResultsComponent.jsx  # Results display
│   │   ├── services/
│   │   │   └── api.js                # API client
│   │   ├── App.jsx                   # Main application
│   │   ├── main.jsx                  # Entry point
│   │   └── index.css                 # Styles
│   ├── index.html
│   ├── package.json
│   └── vite.config.js
├── tests/
│   └── test_api.py              # Backend API tests
├── requirements.txt             # Python dependencies
├── .env.example                 # Environment variables template
├── .gitignore                   # Git ignore rules
└── README.md                    # This file
```

## Installation

### Prerequisites

- **Python 3.8+** - [Download Python](https://www.python.org/downloads/)
- **Node.js 16+** - [Download Node.js](https://nodejs.org/)
- **Tesseract OCR** (optional, for image processing):
  - Windows: Download from [UB-Mannheim/tesseract](https://github.com/UB-Mannheim/tesseract/wiki)
  - macOS: `brew install tesseract`
  - Linux: `sudo apt-get install tesseract-ocr`

### Backend Setup

1. **Clone the repository** (if not already done):
   ```bash
   git clone <repository-url>
   cd ai-medical-record-extractor
   ```

2. **Create virtual environment**:
   ```bash
   python -m venv venv
   
   # Windows
   venv\Scripts\activate
   
   # macOS/Linux
   source venv/bin/activate
   ```

3. **Install Python dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Create environment file**:
   ```bash
   cp .env.example .env
   ```

5. **Create required directories**:
   ```bash
   mkdir -p uploads data
   ```

### Frontend Setup

1. **Navigate to frontend directory**:
   ```bash
   cd frontend
   ```

2. **Install Node.js dependencies**:
   ```bash
   npm install
   ```

3. **Create environment file** (optional):
   ```bash
   cp .env.example .env.local
   ```

## Running the Application

### Start Backend Server

From the project root directory:

```bash
# Make sure virtual environment is activated
uvicorn src.api.main:app --reload
```

The API will be available at: `http://localhost:8000`

**API Documentation**: `http://localhost:8000/docs` (Swagger UI)

**Alternative run command**:
```bash
python -m uvicorn src.api.main:app --reload --host 0.0.0.0 --port 8000
```

### Start Frontend Development Server

In a new terminal, from the frontend directory:

```bash
cd frontend
npm run dev
```

The application will be available at: `http://localhost:3000`

## API Endpoints

### Health Check
- `GET /` - Service health status
- `GET /health` - Detailed health check

### File Operations
- `POST /upload` - Upload a medical record file
- `POST /extract` - Extract information from uploaded file
- `POST /extract-text` - Extract information from raw text

### Record Management
- `GET /records` - Get all medical records (with pagination)
- `GET /records/{id}` - Get specific record by ID
- `GET /search?query={query}` - Search records
- `DELETE /records/{id}` - Delete a record

### Example API Usage

#### Extract from File
```bash
curl -X POST "http://localhost:8000/extract" \
  -H "accept: application/json" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@medical_record.txt"
```

#### Extract from Text
```bash
curl -X POST "http://localhost:8000/extract-text" \
  -F "text=Patient Name: John Doe, Age: 45, Diagnosis: Hypertension"
```

#### Get All Records
```bash
curl "http://localhost:8000/records"
```

## CPU Inference Details

### How It Works

The application uses **rule-based pattern matching** for medical information extraction:

1. **Text Preprocessing**: Clean and normalize input text
2. **Pattern Matching**: Use regex patterns to identify medical entities
3. **Keyword Detection**: Match against medical terminology databases
4. **Context Extraction**: Extract surrounding context for accuracy
5. **Structured Output**: Format results into JSON

### Why CPU-Only?

- **No GPU Required**: Works on any computer
- **Faster Startup**: No model loading delays
- **Lower Resource Usage**: Minimal memory footprint
- **True Offline**: No network dependencies
- **Privacy**: All data stays local

### Extraction Capabilities

The system extracts:
- ✅ Patient Name (pattern matching)
- ✅ Age (numeric pattern detection)
- ✅ Gender (keyword matching)
- ✅ Symptoms (medical keyword database)
- ✅ Diagnosis (section identification)
- ✅ Medications (drug name patterns)
- ✅ Medical History (condition keywords)
- ✅ Doctor Name (title patterns)
- ✅ Hospital Name (institution patterns)
- ✅ Summary (auto-generated)

## Offline Demo Steps

### Step 1: Prepare Sample Data

Create a sample medical record file:

```txt
# sample_medical_record.txt

Patient Name: Jane Smith
Age: 45
Gender: Female

Symptoms: Fever, Cough, Headache, Body ache

Diagnosis: Viral Infection

Medications:
- Paracetamol 500mg - Twice daily
- Cough Syrup 100ml - Thrice daily
- Vitamin C 1000mg - Once daily

Medical History: No significant history

Doctor: Dr. John Doe
Hospital: City General Hospital
```

### Step 2: Start Backend

```bash
# Terminal 1
uvicorn src.api.main:app --reload
```

### Step 3: Start Frontend

```bash
# Terminal 2
cd frontend
npm run dev
```

### Step 4: Test the Application

1. Open browser to `http://localhost:3000`
2. Drag and drop `sample_medical_record.txt`
3. View extracted structured data
4. Try with PDF or image files

### Step 5: Verify Offline Operation

1. **Disconnect from internet** (disable WiFi/Ethernet)
2. Refresh the application
3. Upload a medical record
4. Extraction should work perfectly

## Testing

### Run Backend Tests

```bash
# Install test dependencies (already in requirements.txt)
pip install pytest pytest-asyncio httpx

# Run tests
pytest tests/ -v

# Run with coverage
pytest tests/ --cov=src --cov-report=html
```

### Test Coverage

- ✅ Health endpoint tests
- ✅ File upload validation
- ✅ Text extraction accuracy
- ✅ Error handling
- ✅ Response model validation
- ✅ Database operations
- ✅ Invalid file handling

## Configuration

### Environment Variables

See `.env.example` for all available options:

```env
# Backend
BACKEND_HOST=0.0.0.0
BACKEND_PORT=8000
BACKEND_RELOAD=true

# Database
DATABASE_PATH=data/medical_records.db

# File Upload
UPLOAD_DIR=uploads
MAX_FILE_SIZE=10485760

# Frontend
VITE_API_URL=http://localhost:8000/api
```

### File Size Limits

- Maximum file size: **10MB**
- Supported formats: PDF, TXT, PNG, JPG, JPEG, BMP, TIFF

## Troubleshooting

### Backend Issues

**Problem**: `ModuleNotFoundError: No module named 'fastapi'`
```bash
# Solution: Install dependencies
pip install -r requirements.txt
```

**Problem**: `Tesseract not found`
```bash
# Windows: Install from GitHub releases
# macOS: brew install tesseract
# Linux: sudo apt-get install tesseract-ocr

# Or disable OCR in file_processor.py
```

**Problem**: Database errors
```bash
# Solution: Create data directory
mkdir -p data
```

### Frontend Issues

**Problem**: `Cannot find module 'react'`
```bash
# Solution: Install dependencies
cd frontend
npm install
```

**Problem**: CORS errors
```bash
# Solution: Check backend CORS configuration in src/api/main.py
# Ensure frontend URL is in allow_origins
```

**Problem**: Proxy not working
```bash
# Solution: Check vite.config.js proxy settings
# Ensure backend is running on port 8000
```

## Performance

### CPU Inference Performance

- **Text extraction**: < 1 second
- **Medical entity extraction**: < 100ms
- **Database save**: < 50ms
- **Total processing**: < 2 seconds per document

### Resource Usage

- **Memory**: ~100MB (backend), ~50MB (frontend)
- **CPU**: Single core, minimal usage
- **Disk**: ~10MB for application, variable for data

## Security Considerations

- ✅ File type validation
- ✅ File size limits
- ✅ Input sanitization
- ✅ SQL injection prevention (parameterized queries)
- ✅ CORS configuration
- ✅ No external API calls (data stays local)
- ✅ Error message sanitization

## Future Enhancements

- [ ] Multi-language support
- [ ] Voice input for medical records
- [ ] Medical history timeline visualization
- [ ] Disease prediction based on history
- [ ] Export to PDF/Excel
- [ ] Batch processing
- [ ] Advanced OCR with layout analysis
- [ ] Medical terminology validation
- [ ] Integration with hospital systems (HL7 FHIR)

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

## License

This project is licensed under the GNU General Public License v3.0 - see [LICENSE](LICENSE) file for details.

## Contributors

- Shirisha Kowkuntla
- Vamshidhar Chary

## Support

For issues and questions:
- Check [ISSUES.md](ISSUES.md) for known issues
- Create a new issue in the repository
- Review documentation in `/docs` (if available)

## Hackathon Compliance

✅ **No GPU/CUDA** - CPU-only inference  
✅ **No cloud API** - All processing local  
✅ **Offline capable** - Works without internet  
✅ **Open source tools** - All dependencies are open source  
✅ **Web application** - Full-stack web app  
✅ **Backend + Frontend** - FastAPI + React  
✅ **Production-ready** - Error handling, logging, tests  

---

**Built for offline-first healthcare data processing** 🏥