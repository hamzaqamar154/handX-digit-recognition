#!/bin/bash
set -e

PORT=${PORT:-8080}

echo "=========================================="
echo "Starting HandX API Server"
echo "Port: $PORT"
echo "Working directory: $(pwd)"
echo "Python: $(python --version)"
echo "=========================================="

echo "Checking model file..."
if [ -f "models/handwriting_model.h5" ]; then
    echo "Model file found: models/handwriting_model.h5"
    ls -lh models/handwriting_model.h5
else
    echo "WARNING: Model file not found at models/handwriting_model.h5"
    echo "Listing models directory:"
    ls -la models/ || echo "Models directory does not exist"
fi

echo "Starting uvicorn server..."
exec python -m uvicorn api.app:app --host 0.0.0.0 --port $PORT --workers 1 --log-level info

