#!/bin/bash
set -e

PORT=${PORT:-8080}

echo "Starting API server on port $PORT"

python -m uvicorn api.app:app --host 0.0.0.0 --port $PORT --workers 1

