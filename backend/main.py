from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api import router
import uvicorn
import logging

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create FastAPI application
app = FastAPI(
    title="SilentVoice API",
    description="Real-time bidirectional sign language translator backend",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Configure CORS for frontend communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],  # Next.js default ports
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routes
app.include_router(router, prefix="/api/v1")

# Root endpoint
@app.get("/")
async def root():
    """
    Root endpoint with API information
    """
    return {
        "message": "Welcome to SilentVoice API",
        "description": "Real-time bidirectional sign language translator",
        "version": "1.0.0",
        "docs": "/docs",
        "websocket_endpoint": "/api/v1/ws/sign"
    }

# Startup event
@app.on_event("startup")
async def startup_event():
    logger.info("🚀 SilentVoice backend starting up...")
    logger.info("📡 WebSocket endpoint available at: ws://localhost:8000/api/v1/ws/sign")
    logger.info("📚 API documentation available at: http://localhost:8000/docs")

# Shutdown event
@app.on_event("shutdown")
async def shutdown_event():
    logger.info("🛑 SilentVoice backend shutting down...")

if __name__ == "__main__":
    # Run the application
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
