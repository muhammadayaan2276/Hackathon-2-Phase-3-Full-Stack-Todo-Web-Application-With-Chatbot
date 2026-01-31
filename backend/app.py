"""
Hugging Face Spaces Entry Point
This file imports and runs the FastAPI app from main.py
"""
from main import app
import uvicorn

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=7860)
