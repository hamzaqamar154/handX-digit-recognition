"""
Script to start both API and UI services.
"""
import subprocess
import sys
import time
import os
from threading import Thread

def start_api():
    """Start FastAPI server."""
    print("Starting FastAPI server...")
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    subprocess.run([sys.executable, "-m", "uvicorn", "api.app:app", "--reload", "--host", "0.0.0.0", "--port", "8000"])

def start_ui():
    """Start Streamlit UI."""
    print("Starting Streamlit UI...")
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    subprocess.run([sys.executable, "-m", "streamlit", "run", "ui/app.py", "--server.port", "8501"])

if __name__ == "__main__":
    print("=" * 60)
    print("Starting Handwriting Recognition Services")
    print("=" * 60)
    
    # Start API in background thread
    api_thread = Thread(target=start_api, daemon=True)
    api_thread.start()
    
    # Wait a bit for API to start
    time.sleep(2)
    
    # Start UI (this will block)
    start_ui()

