FROM python:3.10

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY api/ ./api
COPY src/ ./src
COPY start.sh ./

RUN mkdir -p models data/raw data/processed && \
    chmod +x start.sh

COPY models/ ./models/

ENV PYTHONUNBUFFERED=1
ENV ENVIRONMENT=production
ENV PORT=8080

EXPOSE 8080

CMD ["sh", "-c", "echo 'Testing app import...' && python -c 'from api.app import app; print(\"App imported successfully\")' && echo 'Starting server on port' ${PORT:-8080} && exec python -m uvicorn api.app:app --host 0.0.0.0 --port ${PORT:-8080} --log-level info --timeout-keep-alive 30 --access-log"]

