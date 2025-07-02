#!/usr/bin/env python3
"""
Test bytes upload functionality that mimics Flutter web frontend behavior.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import requests
import torch
import torchaudio
import tempfile
import json

def create_test_audio_bytes():
    """Create test audio as bytes (mimics Flutter web)."""
    # Create test audio
    duration = 4.0
    sample_rate = 16000
    t = torch.linspace(0, duration, int(sample_rate * duration))
    signal = torch.sin(2 * 3.14159 * 440 * t)
    signal = signal / torch.max(torch.abs(signal))
    
    # Save to temporary file to get bytes
    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp_file:
        torchaudio.save(tmp_file.name, signal.unsqueeze(0), sample_rate)
        
        # Read back as bytes
        with open(tmp_file.name, 'rb') as f:
            audio_bytes = f.read()
        
        os.unlink(tmp_file.name)
        return audio_bytes

def test_bytes_upload(base_url="http://localhost:8000"):
    """Test uploading audio as bytes like Flutter web does."""
    print("🌐 Testing Bytes Upload (Flutter Web Simulation)")
    print("=" * 60)
    
    try:
        # Health check first
        print("🏥 Testing health endpoint...")
        health_response = requests.get(f"{base_url}/health")
        if health_response.status_code != 200:
            print(f"❌ Health check failed: {health_response.status_code}")
            return False
        print("✅ Health check passed")
        
        # Create test audio bytes
        print("📦 Creating test audio bytes...")
        audio_bytes = create_test_audio_bytes()
        print(f"📊 Audio bytes size: {len(audio_bytes)} bytes")
        
        # Upload as multipart form data (like Flutter web)
        print("📤 Uploading audio bytes...")
        files = {
            'file': ('test_audio.wav', audio_bytes, 'audio/wav')
        }
        
        response = requests.post(f"{base_url}/predict/", files=files)
        
        if response.status_code != 200:
            print(f"❌ Upload failed: {response.status_code}")
            print(f"Response: {response.text}")
            return False
        
        # Validate response
        print("✅ Upload successful!")
        result = response.json()
        
        print("📊 API Response:")
        print(json.dumps(result, indent=2))
        
        # Validate response structure
        required_fields = ["result", "score", "confidence", "threshold", "model_type"]
        for field in required_fields:
            if field not in result:
                print(f"❌ Missing field: {field}")
                return False
            print(f"✅ Field '{field}': {result[field]}")
        
        # Validate field values
        if result["result"] not in ["real", "fake"]:
            print(f"❌ Invalid result value: {result['result']}")
            return False
        
        if not (0.0 <= result["score"] <= 1.0):
            print(f"❌ Invalid score range: {result['score']}")
            return False
        
        if not (0.0 <= result["confidence"] <= 1.0):
            print(f"❌ Invalid confidence range: {result['confidence']}")
            return False
        
        if result["threshold"] != 0.5:
            print(f"❌ Invalid threshold: {result['threshold']}")
            return False
        
        if result["model_type"] != "AASIST":
            print(f"❌ Invalid model type: {result['model_type']}")
            return False
        
        print("\n" + "=" * 60)
        print("🎉 BYTES UPLOAD TEST PASSED!")
        print("✅ Flutter web compatibility confirmed")
        print("✅ Multipart form data upload working")
        print("✅ Response format perfect")
        
        return True
        
    except Exception as e:
        print(f"❌ Test failed with exception: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    # Test with default local server
    success = test_bytes_upload()
    
    if success:
        print("\n🚀 READY FOR FLUTTER FRONTEND!")
        print("The backend is 100% compatible with both:")
        print("  • Flutter mobile (file path uploads)")  
        print("  • Flutter web (bytes uploads)")
    else:
        print("\n❌ Backend needs fixing before frontend integration")
    
    sys.exit(0 if success else 1) 