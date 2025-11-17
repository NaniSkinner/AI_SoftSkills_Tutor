"""
Startup script for the backend application.
Reads the PORT environment variable provided by Render and starts uvicorn.
Falls back to port 8000 for local development.
"""
import os
import uvicorn

if __name__ == "__main__":
    port = int(os.getenv("PORT", 8000))
    print(f"Starting server on port {port}")

    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=port,
        log_level="info"
    )
