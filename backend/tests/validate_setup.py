#!/usr/bin/env python3
"""
Comprehensive validation script for AASIST backend setup.
"""

import os
import sys
import json
from pathlib import Path

def main():
    """Main validation function."""
    print("🚀 AASIST Backend Validation")
    print("=" * 50)
    
    # Check files
    print("🔍 Checking required files...")
    required_files = [
        "aasist/config/AASIST.conf",
        "aasist/models/weights/AASIST.pth", 
        "aasist/models/AASIST.py",
        "aasist_predictor.py",
        "app.py"
    ]
    
    all_good = True
    for file_path in required_files:
        if Path(file_path).exists():
            print(f"  ✅ {file_path}")
        else:
            print(f"  ❌ {file_path}")
            all_good = False
    
    # Test imports
    print("\n🧠 Testing imports...")
    try:
        from aasist_predictor import _model
        print("  ✅ AASIST model imported")
    except Exception as e:
        print(f"  ❌ AASIST import failed: {e}")
        all_good = False
    
    try:
        from app import app
        print("  ✅ FastAPI app imported")
    except Exception as e:
        print(f"  ❌ FastAPI import failed: {e}")
        all_good = False
    
    print("\n" + "=" * 50)
    if all_good:
        print("🎉 ALL CHECKS PASSED! Backend is ready.")
        print("\nTo start the server: python start_production.py")
    else:
        print("💥 Some checks failed. Please fix the issues.")
    
    return 0 if all_good else 1

if __name__ == "__main__":
    sys.exit(main()) 