#!/usr/bin/env python3
"""
Railway deployment startup script for FluxPad API
"""
import uvicorn
import os

if __name__ == "__main__":
    # Railway provides PORT environment variable
    port = int(os.getenv("PORT", 8000))
    
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=port,
        reload=False,
        workers=1
    )