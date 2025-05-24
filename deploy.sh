#!/bin/bash

set -e

echo "Building Docker images..."
docker-compose build

echo "Starting services..."
docker-compose up -d

echo "Waiting for services to be ready..."
sleep 5

echo "Checking API health..."
curl -f http://localhost:8000/health || echo "API not ready yet"

echo ""
echo "Services started!"
echo "API: http://localhost:8000"
echo "UI: http://localhost:8501"
echo ""
echo "To view logs: docker-compose logs -f"
echo "To stop: docker-compose down"

