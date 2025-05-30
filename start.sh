#!/bin/bash
set -e

PORT=${PORT:-8080}

echo "=========================================="
echo "Starting HandX API Server"
echo "Port: $PORT"
echo "Working directory: $(pwd)"
echo "Python: $(python --version)"
echo "=========================================="

echo "Checking Python imports..."
python -c "import fastapi; import uvicorn; print('Imports OK')" || {
    echo "ERROR: Failed to import required modules"
    exit 1
}

echo "Testing app import..."
python -c "import sys; sys.path.insert(0, '.'); from api.app import app; print('App import OK')" || {
    echo "ERROR: Failed to import app"
    exit 1
}

echo "Checking model file..."
if [ -f "models/handwriting_model.h5" ]; then
    echo "Model file found: models/handwriting_model.h5"
    ls -lh models/handwriting_model.h5
else
    echo "WARNING: Model file not found at models/handwriting_model.h5"
    echo "Listing models directory:"
    ls -la models/ || echo "Models directory does not exist"
    echo "Server will start but predictions will fail until model is available"
fi

echo "Starting uvicorn server on port $PORT..."
echo "Command: python -m uvicorn api.app:app --host 0.0.0.0 --port $PORT --log-level info"

exec python -m uvicorn api.app:app --host 0.0.0.0 --port $PORT --log-level info --timeout-keep-alive 30 --access-log

