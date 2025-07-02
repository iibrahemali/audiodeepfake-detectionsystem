import os
import tempfile
import uvicorn
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import logging
# Use the thin wrapper around the official AASIST implementation
from aasist_predictor import predict_wav

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="Deepfake Audio Detection API",
    description="API for detecting deepfake audio using AASIST model",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# No explicit startup needed; model is loaded lazily inside `aasist_predictor`.

@app.get("/")
async def root():
    """Health check endpoint"""
    return {"message": "Deepfake Audio Detection API is running"}

@app.get("/health")
async def health_check():
    """Return basic service & model availability information."""
    try:
        # Attempt a trivial model attribute access to ensure import succeeded
        from aasist_predictor import _model  # type: ignore
        model_status = "loaded" if _model is not None else "not loaded"
    except Exception:
        model_status = "error"
    return {
        "status": "healthy",
        "model_status": model_status,
        "version": "1.0.0"
    }

@app.post("/predict/")
async def predict_audio(file: UploadFile = File(...)):
    """
    Predict if the uploaded audio is real or fake using AASIST model
    
    Args:
        file: WAV audio file
        
    Returns:
        JSON with prediction result and confidence score
    """
    # Validate file type
    if not file.filename.lower().endswith((".wav", ".flac")):
        raise HTTPException(status_code=400, detail="Only WAV/FLAC files supported")

    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp:
        data = await file.read()
        tmp.write(data)
        temp_path = tmp.name

    try:
        logger.info(f"Processing audio file: {file.filename}")
        result = predict_wav(temp_path)
        
        # Transform to match frontend expected format
        score = result["score"]  # Raw probability of fake (0-1)
        label = result["label"]  # "real" or "fake"
        threshold = 0.5         # Fixed threshold used by AASIST
        
        # Calculate confidence based on how far the score is from the threshold
        confidence = abs(score - threshold) * 2  # Scale to 0-1 range
        confidence = min(confidence, 1.0)        # Cap at 1.0
        
        response = {
            "result": label,
            "score": score,
            "confidence": confidence,
            "threshold": threshold,
            "model_type": "AASIST"
        }
        
        logger.info(f"Prediction result: {response}")
        return JSONResponse(content=response)
    except Exception as e:
        logger.exception("Prediction failed")
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        try:
            os.unlink(temp_path)
        except OSError:
            pass

if __name__ == "__main__":
    uvicorn.run(
        "app:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    ) 