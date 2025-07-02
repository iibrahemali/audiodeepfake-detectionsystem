#!/usr/bin/env python3
"""
Production startup script for AASIST Deepfake Audio Detection API.
"""

import os
import sys
import uvicorn
import logging
from pathlib import Path

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/production.log'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

def check_prerequisites():
    """Check if all required files and directories exist."""
    required_files = [
        "aasist/config/AASIST.conf",
        "aasist/models/weights/AASIST.pth",
        "aasist/models/AASIST.py"
    ]
    
    missing_files = []
    for file_path in required_files:
        if not Path(file_path).exists():
            missing_files.append(file_path)
    
    if missing_files:
        logger.error("Missing required files:")
        for file_path in missing_files:
            logger.error(f"  - {file_path}")
        return False
    
    return True

def main():
    """Main function to start the production server."""
    logger.info("🚀 Starting AASIST Deepfake Audio Detection API...")
    
    # Create logs directory if it doesn't exist
    os.makedirs("logs", exist_ok=True)
    
    # Check prerequisites
    if not check_prerequisites():
        logger.error("❌ Prerequisites not met. Exiting.")
        sys.exit(1)
    
    # Test model loading
    try:
        logger.info("🧠 Testing AASIST model loading...")
        from aasist_predictor import _model
        if _model is None:
            raise RuntimeError("Model failed to load")
        logger.info("✅ AASIST model loaded successfully")
    except Exception as e:
        logger.error(f"❌ Failed to load AASIST model: {e}")
        sys.exit(1)
    
    # Start the server
    try:
        logger.info("🌐 Starting FastAPI server...")
        logger.info("📍 Server will be available at: http://0.0.0.0:8000")
        logger.info("📍 API documentation at: http://0.0.0.0:8000/docs")
        logger.info("🏥 Health check at: http://0.0.0.0:8000/health")
        
        uvicorn.run(
            "app:app",
            host="0.0.0.0",
            port=8000,
            log_level="info",
            access_log=True,
            workers=1  # AASIST model doesn't support multi-processing
        )
    except KeyboardInterrupt:
        logger.info("🛑 Server stopped by user")
    except Exception as e:
        logger.error(f"❌ Server failed to start: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 