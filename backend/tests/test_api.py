#!/usr/bin/env python3
"""
Test script for the Deepfake Audio Detection API
"""
import requests
import numpy as np
import soundfile as sf
import tempfile
import os
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def create_test_audio(duration=4, sample_rate=16000, frequency=440):
    """Create a test audio file"""
    t = np.linspace(0, duration, int(duration * sample_rate))
    audio = 0.5 * np.sin(2 * np.pi * frequency * t)
    return audio

def test_api(base_url="http://localhost:8000"):
    """Test the API endpoints"""
    
    # Test health endpoint
    logger.info("Testing health endpoint...")
    try:
        response = requests.get(f"{base_url}/health")
        print(f"Health check: {response.status_code} - {response.json()}")
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        return False
    
    # Create test audio file
    logger.info("Creating test audio file...")
    test_audio = create_test_audio()
    
    with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as temp_file:
        sf.write(temp_file.name, test_audio, 16000)
        temp_file_path = temp_file.name
    
    try:
        # Test prediction endpoint
        logger.info("Testing prediction endpoint...")
        with open(temp_file_path, 'rb') as audio_file:
            files = {'file': ('test.wav', audio_file, 'audio/wav')}
            response = requests.post(f"{base_url}/predict/", files=files)
            
        print(f"Prediction: {response.status_code}")
        if response.status_code == 200:
            result = response.json()
            print(f"Result: {result}")
            return True
        else:
            print(f"Error: {response.text}")
            return False
            
    except Exception as e:
        logger.error(f"Prediction test failed: {e}")
        return False
    
    finally:
        # Clean up
        try:
            os.unlink(temp_file_path)
        except:
            pass

if __name__ == "__main__":
    import sys
    
    base_url = sys.argv[1] if len(sys.argv) > 1 else "http://localhost:8000"
    logger.info(f"Testing API at {base_url}")
    
    success = test_api(base_url)
    if success:
        logger.info("✅ All tests passed!")
    else:
        logger.error("❌ Tests failed!")
        sys.exit(1) 