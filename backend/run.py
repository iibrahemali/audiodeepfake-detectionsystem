#!/usr/bin/env python3
"""
Simple run script for the AASIST Deepfake Audio Detection Backend.
This script ensures everything is properly set up before starting the server.
"""

import sys
import os
from pathlib import Path

def check_requirements():
    """Check if all requirements are met."""
    print("🔍 Checking requirements...")
    
    # Check if we're in the right directory
    if not Path("app.py").exists():
        print("❌ Error: app.py not found. Please run this script from the backend directory.")
        return False
    
    # Check if AASIST model exists
    model_path = Path("aasist/models/weights/AASIST.pth")
    if not model_path.exists():
        print("❌ Error: AASIST model weights not found!")
        print(f"Expected location: {model_path}")
        print("Please ensure the AASIST model is properly installed.")
        return False
    
    # Check if config exists
    config_path = Path("aasist/config/AASIST.conf")
    if not config_path.exists():
        print("❌ Error: AASIST config not found!")
        print(f"Expected location: {config_path}")
        return False
    
    # Try importing required modules
    try:
        import torch
        import torchaudio
        import fastapi
        import uvicorn
        from aasist_predictor import predict_wav
        print("✅ All Python dependencies available")
    except ImportError as e:
        print(f"❌ Error: Missing Python dependency: {e}")
        print("Please install requirements: pip install -r requirements.txt")
        return False
    
    print("✅ All requirements satisfied")
    return True

def main():
    """Main function to start the server."""
    print("🚀 AASIST Deepfake Audio Detection Backend")
    print("=" * 50)
    
    if not check_requirements():
        print("\n❌ Setup validation failed. Please fix the issues above.")
        sys.exit(1)
    
    print("\n🏁 Starting production server...")
    print("📍 Server will be available at: http://localhost:8000")
    print("📚 API documentation: http://localhost:8000/docs")
    print("🏥 Health check: http://localhost:8000/health")
    print("\nPress Ctrl+C to stop the server")
    print("=" * 50)
    
    # Import and run the production server
    try:
        import start_production
        start_production.main()
    except KeyboardInterrupt:
        print("\n\n👋 Server stopped by user")
    except Exception as e:
        print(f"\n❌ Server error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 