# 🚀 Quick Start Guide

Get the AI Medical Record Extractor running in 5 minutes!

## Prerequisites

- Python 3.8 or higher
- Node.js 16 or higher
- Git (optional)

## Installation & Setup

### 1. Backend Setup (2 minutes)

```bash
# Navigate to project directory
cd ai-medical-record-extractor

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Create required directories
mkdir -p uploads data
```

### 2. Frontend Setup (2 minutes)

```bash
# Navigate to frontend directory
cd frontend

# Install dependencies
npm install

# Go back to project root
cd ..
```

### 3. Start the Application (1 minute)

**Terminal 1 - Start Backend:**
```bash
# Make sure you're in the project root and venv is activated
uvicorn src.api.main:app --reload
```

You should see:
```
INFO:     Uvicorn running on http://0.0.0.0:8000
INFO:     Application startup complete.
```

**Terminal 2 - Start Frontend:**
```bash
cd frontend
npm run dev
```

You should see:
```
VITE v5.0.8  ready in 1234 ms

➜  Local:   http://localhost:3000/
➜  Network: use --host to expose
```

### 4. Use the Application

1. Open your browser to **http://localhost:3000**
2. You'll see the AI Medical Record Extractor homepage
3. Drag and drop a medical record file (or click to browse)
4. Wait for processing (usually < 2 seconds)
5. View the extracted structured data

## Test with Sample Data

We've included a sample medical record for testing:

```bash
# The file is located at:
sample_medical_record.txt
```

Try uploading this file to see the extraction in action!

## Verify It's Working

### Check Backend Health
```bash
curl http://localhost:8000/health
```

Expected response:
```json
{
  "status": "healthy",
  "database": "connected",
  "extractor": "ready"
}
```

### Check Frontend
- Open http://localhost:3000
- You should see "Backend Connected" in green in the top right
- The upload zone should be visible

## Common Issues & Solutions

### Issue: "ModuleNotFoundError"
```bash
# Solution: Make sure virtual environment is activated
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Then reinstall:
pip install -r requirements.txt
```

### Issue: "Port already in use"
```bash
# Backend on different port:
uvicorn src.api.main:app --reload --port 8001

# Frontend on different port:
npm run dev -- --port 3001
```

### Issue: "CORS error"
```bash
# Make sure backend is running first, then start frontend
# The vite.config.js has proxy setup to avoid CORS
```

### Issue: "Tesseract not found" (for image processing)
```bash
# Windows: Download from https://github.com/UB-Mannheim/tesseract/wiki
# macOS: brew install tesseract
# Linux: sudo apt-get install tesseract-ocr

# Or skip OCR - text and PDF files work without Tesseract
```

## Quick Test

### Test Backend API
```bash
# Extract from text
curl -X POST "http://localhost:8000/extract-text" \
  -F "text=Patient Name: John Doe, Age: 30, Diagnosis: Fever"

# Get all records
curl "http://localhost:8000/records"
```

### Test Frontend
1. Open http://localhost:3000
2. Upload `sample_medical_record.txt`
3. Verify you see extracted data:
   - Patient Name: Jane Smith
   - Age: 45
   - Gender: Female
   - Symptoms: Fever, Cough, etc.
   - Diagnosis: Viral Infection
   - Medications: Paracetamol, etc.

## Run Tests

```bash
# Install test dependencies (if not already installed)
pip install pytest pytest-asyncio httpx

# Run tests
pytest tests/ -v

# Expected: All tests pass ✅
```

## Project Structure Overview

```
ai-medical-record-extractor/
├── src/                    # Backend code
│   ├── api/main.py        # FastAPI endpoints
│   ├── extractor/         # Medical extraction logic
│   ├── models/            # Pydantic models
│   ├── utils/             # File processing
│   └── database/          # SQLite handler
├── frontend/              # React frontend
│   └── src/
│       ├── components/    # UI components
│       ├── services/      # API client
│       └── App.jsx        # Main app
├── tests/                 # Test suite
├── requirements.txt       # Python dependencies
├── sample_medical_record.txt  # Test data
└── README.md             # Full documentation
```

## What's Next?

1. **Try different files**: Upload PDFs, images, or text files
2. **Explore the API**: Visit http://localhost:8000/docs for interactive API docs
3. **Check the database**: Records are saved in `data/medical_records.db`
4. **Read the docs**: See README.md for detailed information

## Need Help?

- **Full Documentation**: See [README.md](README.md)
- **API Documentation**: http://localhost:8000/docs (when backend is running)
- **Project Summary**: See [PROJECT_SUMMARY.md](PROJECT_SUMMARY.md)
- **Issues**: Check [ISSUES.md](ISSUES.md)

## Success Checklist

- ✅ Backend running on http://localhost:8000
- ✅ Frontend running on http://localhost:3000
- ✅ Health check shows "Backend Connected"
- ✅ Can upload files successfully
- ✅ Extraction returns structured data
- ✅ Tests pass

---

**You're all set! Start extracting medical information in minutes!** 🏥