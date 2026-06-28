# How to Run the AI Medical Record Extractor

## Prerequisites
- Python 3.8+ installed
- Node.js 16+ installed
- Backend dependencies installed: `pip install -r requirements.txt`
- Frontend dependencies installed: `cd frontend && npm install`

## Running the Application

### Step 1: Start the Backend Server

Open a terminal in the project root directory and run:

```bash
python run_backend.py
```

The backend will start on http://localhost:8000

**Note:** There is NO `backend` folder. The backend code is in the `src/` directory. Use `python run_backend.py` from the project root.

### Step 2: Start the Frontend Server

Open a **new** terminal window and run:

```bash
cd frontend
npm run dev
```

The frontend will start on http://localhost:3000

## Access the Application

- **Frontend UI**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs

## Stopping the Servers

- Press `Ctrl+C` in each terminal to stop the servers

## Troubleshooting

### Backend won't start?
- Ensure you're in the project root directory
- Run: `python run_backend.py` (not `cd backend`)
- Check that all Python dependencies are installed

### Frontend can't connect to backend?
- Ensure backend is running on port 8000
- Check that `VITE_API_URL` is set correctly in `frontend/.env`
- Default API URL: `http://localhost:8000/api`

### Port already in use?
- Backend: Set `BACKEND_PORT` environment variable
- Frontend: Vite will automatically use the next available port

## Quick Reference

| Command | Description |
|---------|-------------|
| `python run_backend.py` | Start backend server (from project root) |
| `cd frontend && npm run dev` | Start frontend dev server |
| `cd frontend && npm run build` | Build frontend for production |
| `cd frontend && npm run preview` | Preview production build |