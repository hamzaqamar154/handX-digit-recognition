Write-Host "Building Docker images..." -ForegroundColor Green
docker-compose build

Write-Host "Starting services..." -ForegroundColor Green
docker-compose up -d

Write-Host "Waiting for services to be ready..." -ForegroundColor Yellow
Start-Sleep -Seconds 5

Write-Host "Checking API health..." -ForegroundColor Yellow
try {
    Invoke-WebRequest -Uri "http://localhost:8000/health" -UseBasicParsing | Out-Null
    Write-Host "API is healthy!" -ForegroundColor Green
} catch {
    Write-Host "API not ready yet" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "Services started!" -ForegroundColor Green
Write-Host "API: http://localhost:8000"
Write-Host "UI: http://localhost:8501"
Write-Host ""
Write-Host "To view logs: docker-compose logs -f"
Write-Host "To stop: docker-compose down"

