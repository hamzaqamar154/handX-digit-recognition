from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from PIL import Image
import io
import sys
import os
import logging

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

try:
    from src.predict import HandwritingPredictor
    from src.config import MODEL_PATH, CORS_ORIGINS, ENVIRONMENT
except Exception as e:
    logger.error(f"Failed to import modules: {e}", exc_info=True)
    MODEL_PATH = None
    CORS_ORIGINS = ["*"]
    ENVIRONMENT = os.getenv("ENVIRONMENT", "production")
    HandwritingPredictor = None

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
model_loading = False

import threading

def load_model_background():
    global predictor, model_loading
    if HandwritingPredictor is None:
        logger.warning("HandwritingPredictor not available - model loading skipped")
        return
    try:
        if MODEL_PATH and os.path.exists(MODEL_PATH):
            logger.info(f"Background: Loading model from {MODEL_PATH}")
            model_loading = True
            predictor = HandwritingPredictor()
            model_loading = False
            logger.info("Background: Model loaded successfully")
        else:
            logger.warning(f"Background: Model not found at {MODEL_PATH}")
    except Exception as e:
        model_loading = False
        logger.error(f"Background: Error loading model: {str(e)}", exc_info=True)

def ensure_model_loaded():
    global predictor, model_loading
    if predictor is None and not model_loading:
        thread = threading.Thread(target=load_model_background, daemon=True)
        thread.start()

@app.get("/")
async def root():
    ensure_model_loaded()
    return {
        "message": "Handwriting Recognition API",
        "status": "running",
        "endpoints": {
            "/predict": "POST - Upload image for prediction",
            "/health": "GET - Health check"
        }
    }

@app.get("/health")
async def health():
    ensure_model_loaded()
    return {
        "status": "healthy",
        "model_loaded": predictor is not None,
        "model_loading": model_loading
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
