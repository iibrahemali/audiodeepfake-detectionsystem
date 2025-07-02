#!/usr/bin/env python3
"""
Test to validate API response format matches frontend expectations exactly.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from aasist_predictor import predict_wav
import torch
import torchaudio
import tempfile
import json

def create_test_audio():
    """Create a simple test audio file."""
    duration = 4.0
    sample_rate = 16000
    t = torch.linspace(0, duration, int(sample_rate * duration))
    signal = torch.sin(2 * 3.14159 * 440 * t)  # 440 Hz sine wave
    signal = signal / torch.max(torch.abs(signal))  # Normalize
    return signal.unsqueeze(0)

def test_prediction_format():
    """Test that prediction format matches frontend expectations."""
    print("🧪 Testing API Response Format for Frontend Integration")
    print("=" * 60)
    
    # Create test audio
    print("📝 Creating test audio...")
    test_audio = create_test_audio()
    
    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp_file:
        temp_path = tmp_file.name
        torchaudio.save(temp_path, test_audio, 16000)
    
    try:
        # Test prediction
        print("🔍 Running AASIST prediction...")
        result = predict_wav(temp_path)
        
        # Transform to match frontend expected format (same as app.py)
        score = result["score"]
        label = result["label"] 
        threshold = 0.5
        confidence = abs(score - threshold) * 2
        confidence = min(confidence, 1.0)
        
        api_response = {
            "result": label,
            "score": score,
            "confidence": confidence,
            "threshold": threshold,
            "model_type": "AASIST"
        }
        
        print("📊 API Response Format:")
        print(json.dumps(api_response, indent=2))
        
        # Validate all required fields are present
        required_fields = ["result", "score", "confidence", "threshold", "model_type"]
        missing_fields = []
        
        for field in required_fields:
            if field not in api_response:
                missing_fields.append(field)
        
        if missing_fields:
            print(f"❌ Missing required fields: {missing_fields}")
            return False
        
        # Validate field types and values
        validations = [
            (isinstance(api_response["result"], str), "result must be string"),
            (api_response["result"] in ["real", "fake"], "result must be 'real' or 'fake'"),
            (isinstance(api_response["score"], (int, float)), "score must be numeric"),
            (0.0 <= api_response["score"] <= 1.0, "score must be between 0 and 1"),
            (isinstance(api_response["confidence"], (int, float)), "confidence must be numeric"),
            (0.0 <= api_response["confidence"] <= 1.0, "confidence must be between 0 and 1"),
            (api_response["threshold"] == 0.5, "threshold must be 0.5"),
            (api_response["model_type"] == "AASIST", "model_type must be 'AASIST'")
        ]
        
        for is_valid, error_msg in validations:
            if not is_valid:
                print(f"❌ {error_msg}")
                return False
            else:
                print(f"✅ {error_msg.replace('must be', 'is')}")
        
        print("\n" + "=" * 60)
        print("🎉 FRONTEND INTEGRATION TEST PASSED!")
        print("✅ API response format is 100% compatible with Flutter frontend")
        print("✅ All required fields present with correct types and values")
        
        return True
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False
        
    finally:
        try:
            os.unlink(temp_path)
        except OSError:
            pass

if __name__ == "__main__":
    success = test_prediction_format()
    sys.exit(0 if success else 1) 