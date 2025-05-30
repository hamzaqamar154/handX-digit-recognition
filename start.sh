#!/bin/bash

PORT=${PORT:-8080}

echo "Starting API server on port $PORT"
echo "Working directory: $(pwd)"
echo "Model path: ${MODEL_PATH:-models/handwriting_model.h5}"
echo "Checking if model exists..."
ls -la models/ || echo "Models directory check failed"

echo "Starting uvicorn..."
exec python -m uvicorn api.app:app --host 0.0.0.0 --port $PORT --workers 1

