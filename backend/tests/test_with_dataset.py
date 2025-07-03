#!/usr/bin/env python3
"""
Test AASIST backend with real dataset files.
Place your ASVspoof WAV/FLAC files in ./test_dataset/ folder.
"""

import os
import sys
import json
from pathlib import Path

# Add parent directory to path for imports
sys.path.append(str(Path(__file__).parent.parent))
from aasist_predictor import predict_wav

def main():
    """Test AASIST on files in test_dataset folder."""
    test_dir = Path("test_dataset")
    
    if not test_dir.exists():
        print("❌ test_dataset folder not found!")
        print("Please create it and add some audio files.")
        return 1
    
    # Find all audio files (WAV and FLAC)
    audio_files = list(test_dir.glob("*.wav")) + list(test_dir.glob("*.flac"))
    if not audio_files:
        print("❌ No audio files found in test_dataset/")
        print("Please add some ASVspoof WAV or FLAC files to test.")
        return 1
    
    print(f"🧪 Testing AASIST on {len(audio_files)} files from test_dataset/")
    print("=" * 60)
    
    results = []
    for audio_file in sorted(audio_files):
        try:
            print(f"📁 Processing: {audio_file.name}")
            result = predict_wav(str(audio_file))
            results.append({
                "file": audio_file.name,
                "result": result["label"],
                "score": result["score"]
            })
            
            # Format output nicely
            label = result["label"].upper()
            score = result["score"]
            confidence = "HIGH" if abs(score - 0.5) > 0.3 else "MEDIUM" if abs(score - 0.5) > 0.1 else "LOW"
            
            print(f"   Result: {label} (score: {score:.4f}, confidence: {confidence})")
            print()
            
        except Exception as e:
            print(f"   ❌ Error: {e}")
            print()
    
    # Summary
    if results:
        fake_count = sum(1 for r in results if r["result"] == "fake")
        real_count = len(results) - fake_count
        
        print("=" * 60)
        print("📊 SUMMARY:")
        print(f"   Total files: {len(results)}")
        print(f"   Detected as REAL: {real_count}")
        print(f"   Detected as FAKE: {fake_count}")
        print()
        
        # Show all results in a table
        print("📋 DETAILED RESULTS:")
        for r in results:
            print(f"   {r['file']:<30} → {r['result'].upper():<4} (score: {r['score']:.4f})")
    
    return 0

if __name__ == "__main__":
    sys.exit(main()) 