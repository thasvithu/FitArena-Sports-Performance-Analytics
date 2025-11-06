"""
FitArena Backend Server Runner
Run this script to start the FastAPI backend server
"""
import sys
from pathlib import Path
import uvicorn

# Add the backend directory to Python path
backend_dir = Path(__file__).parent
sys.path.insert(0, str(backend_dir))

if __name__ == "__main__":
    print("🚀 Starting FitArena Backend Server...")
    print("📍 API will be available at: http://localhost:8000")
    print("📚 API Docs available at: http://localhost:8000/api/docs")
    print("\nPress CTRL+C to stop the server\n")
    
    # Run with import string for reload to work
    uvicorn.run(
        "src.api.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
