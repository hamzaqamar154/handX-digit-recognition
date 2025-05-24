from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from PIL import Image
import io
import sys
import os
import logging

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.predict import HandwritingPredictor
from src.config import MODEL_PATH, CORS_ORIGINS, ENVIRONMENT

logging.basicConfig(
    level=logging.INFO if ENVIRONMENT == "production" else logging.DEBUG,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

app = FastAPI(title="Handwriting Recognition API", version="1.0.0")

if CORS_ORIGINS == ["*"]:
    allow_origins = ["*"]
else:
    allow_origins = [origin.strip() for origin in CORS_ORIGINS]

app.add_middleware(
    CORSMiddleware,
    allow_origins=allow_origins,
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)

predictor = None

@app.on_event("startup")
async def startup_event():
    global predictor
    if os.path.exists(MODEL_PATH):
        logger.info(f"Loading model from {MODEL_PATH}")
        predictor = HandwritingPredictor()
        logger.info("Model loaded successfully")
    else:
        logger.warning(f"Model not found at {MODEL_PATH}")

@app.get("/")
async def root():
    return {
        "message": "Handwriting Recognition API",
        "endpoints": {
            "/predict": "POST - Upload image for prediction",
            "/health": "GET - Health check"
        }
    }

@app.get("/health")
async def health():
    return {
        "status": "healthy",
        "model_loaded": predictor is not None
    }

@app.post("/predict")
async def predict(file: UploadFile = File(...)):
    if predictor is None:
        logger.error("Prediction attempted but model not loaded")
        raise HTTPException(status_code=503, detail="Model not loaded. Please train the model first.")
    
    try:
        if file.size > 10 * 1024 * 1024:
            raise HTTPException(status_code=400, detail="File too large. Maximum size is 10MB.")
        
        contents = await file.read()
        image = Image.open(io.BytesIO(contents))
        
        if image.format not in ["PNG", "JPEG", "JPG", "GIF", "BMP"]:
            raise HTTPException(status_code=400, detail="Unsupported image format")
        
        result = predictor.predict(image)
        logger.info(f"Prediction: {result['predicted_digit']} (confidence: {result['confidence']:.2f})")
        
        return {
            "success": True,
            "predicted_digit": result["predicted_digit"],
            "confidence": result["confidence"],
            "top_3": result["top_3"]
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error processing image: {str(e)}")
        raise HTTPException(status_code=400, detail=f"Error processing image: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    from src.config import API_HOST, API_PORT, API_RELOAD, API_WORKERS, ENVIRONMENT
    
    if ENVIRONMENT == "production":
        uvicorn.run(
            app,
            host=API_HOST,
            port=API_PORT,
            workers=API_WORKERS,
            log_level="info"
        )
    else:
        uvicorn.run(
            app,
            host=API_HOST,
            port=API_PORT,
            reload=API_RELOAD
        )
