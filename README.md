# 🩺 AI Medical Record Extractor

## Overview

AI Medical Record Extractor is an offline-first, CPU-powered application that converts unstructured medical documents such as prescriptions, lab reports, and medical records into structured JSON data. The application works without an internet connection and optionally syncs records online when connectivity is available.

## Problem Statement

Medical records are often stored as images or PDF documents, making them difficult to search and organize. This project automatically extracts important information and converts it into structured data for easy access and management.

## Features

- Upload medical prescriptions, lab reports, and medical documents
- Extract patient details automatically
- Identify medicines and dosage
- Extract diagnosis and test results
- Detect follow-up dates
- Generate structured JSON output
- Store records locally
- Search and view previous records
- Works completely offline using CPU
- Optional online synchronization and backup

## Input

- Prescription Images
- Medical Reports
- PDF Documents
- Scanned Records

## Output

The application extracts:

- Patient Name
- Age
- Gender
- Doctor Name
- Hospital Name
- Diagnosis
- Medicines
- Dosage
- Test Results
- Follow-up Date

## Tech Stack

### Frontend
- React.js

### Backend
- FastAPI

### OCR
- Tesseract OCR

### Local AI
- Ollama (Llama 3.2)

### Database
- SQLite

## Workflow

Upload Document
→ OCR extracts text
→ Local AI structures the information
→ JSON is generated
→ Save to SQLite
→ Search and View Records

## Project Structure

```
AI-Medical-Record-Extractor/
│── frontend/
│── backend/
│── docs/
│── sample-data/
│── outputs/
│── models/
│── README.md
│── LICENSE
│── CONTRIBUTING.md
│── CHANGELOG.md
│── .gitlab-ci.yml
```

## Future Enhancements

- Multi-language support
- Voice input
- Medical history timeline
- Disease prediction
- Cloud synchronization

## License

This project is licensed under the GNU General Public License v3.0 (GPL-3.0).

## Contributors

- Shirisha Kowkuntla
- Vamshidhar Chary