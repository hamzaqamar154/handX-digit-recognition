import os

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_RAW_DIR = os.path.join(BASE_DIR, "data", "raw")
DATA_PROCESSED_DIR = os.path.join(BASE_DIR, "data", "processed")
MODELS_DIR = os.path.join(BASE_DIR, "models")

IMG_SIZE = int(os.getenv("IMG_SIZE", 28))
NUM_CLASSES = int(os.getenv("NUM_CLASSES", 10))
BATCH_SIZE = int(os.getenv("BATCH_SIZE", 32))
EPOCHS = int(os.getenv("EPOCHS", 15))
LEARNING_RATE = float(os.getenv("LEARNING_RATE", 0.001))

MODEL_PATH = os.getenv("MODEL_PATH", os.path.join(MODELS_DIR, "handwriting_model.h5"))

API_HOST = os.getenv("API_HOST", "0.0.0.0")
API_PORT = int(os.getenv("PORT", os.getenv("API_PORT", 8000)))
API_RELOAD = os.getenv("API_RELOAD", "false").lower() == "true"
API_WORKERS = int(os.getenv("API_WORKERS", 1))

STREAMLIT_PORT = int(os.getenv("STREAMLIT_PORT", 8501))
STREAMLIT_HOST = os.getenv("STREAMLIT_HOST", "0.0.0.0")

CORS_ORIGINS = os.getenv("CORS_ORIGINS", "*").split(",")
ENVIRONMENT = os.getenv("ENVIRONMENT", "development")
