#!/usr/bin/env python3
"""
Test script to verify Railway configuration
"""
import os
import sys

def test_railway_config():
    print("🔍 Railway Configuration Test")
    print("=" * 40)
    
    # Check environment variables
    port = os.getenv("PORT", "Not set")
    railway_env = os.getenv("RAILWAY_ENVIRONMENT", "Not set")
    
    print(f"📍 PORT: {port}")
    print(f"🚄 RAILWAY_ENVIRONMENT: {railway_env}")
    print(f"🐍 Python version: {sys.version}")
    print(f"📁 Current directory: {os.getcwd()}")
    
    # Check if main.py can be imported
    try:
        import main
        print("✅ main.py imported successfully")
        print(f"📦 FastAPI app: {main.app}")
        print(f"🔗 App title: {main.app.title}")
    except Exception as e:
        print(f"❌ Failed to import main.py: {e}")
        return False
    
    # Check uvicorn availability
    try:
        import uvicorn
        print(f"✅ uvicorn available: {uvicorn.__version__}")
    except Exception as e:
        print(f"❌ uvicorn not available: {e}")
        return False
    
    print("=" * 40)
    print("🎉 All checks passed!")
    return True

if __name__ == "__main__":
    test_railway_config()
