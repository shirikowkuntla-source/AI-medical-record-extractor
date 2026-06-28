#!/usr/bin/env python3
"""
Quick start script for the AI Medical Record Extractor backend.
This script starts the FastAPI server with proper configuration.
"""

import uvicorn
import os
import sys
from pathlib import Path

def main():
    """Start the backend server."""
    # Ensure required directories exist
    os.makedirs("uploads", exist_ok=True)
    os.makedirs("data", exist_ok=True)
    
    # Add src directory to Python path
    src_path = Path(__file__).parent / "src"
    sys.path.insert(0, str(src_path))
    
    # Get configuration from environment or use defaults
    host = os.getenv("BACKEND_HOST", "0.0.0.0")
    port = int(os.getenv("BACKEND_PORT", "8000"))
    reload = os.getenv("BACKEND_RELOAD", "true").lower() == "true"
    
    print(f"🏥 Starting AI Medical Record Extractor Backend")
    print(f"   Server: http://{host}:{port}")
    print(f"   API Docs: http://{host}:{port}/docs")
    print(f"   Reload: {reload}")
    print(f"   Press Ctrl+C to stop\n")
    
    # Start the server
    uvicorn.run(
        "src.api.main:app",
        host=host,
        port=port,
        reload=reload,
        log_level="info"
    )

if __name__ == "__main__":
    main()