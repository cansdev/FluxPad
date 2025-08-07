#!/usr/bin/env python3
"""
Railway deployment startup script for FluxPad API
"""
import uvicorn
import os
import sys

# Add current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

if __name__ == "__main__":
    # Railway provides PORT environment variable
    port = int(os.getenv("PORT", 8000))
    
    print(f"Starting FluxPad API on port {port}")
    print(f"Python path: {sys.path}")
    
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=port,
        reload=False,
        workers=1,
        log_level="info"
    )