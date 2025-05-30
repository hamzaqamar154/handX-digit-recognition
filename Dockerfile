FROM python:3.10-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN mkdir -p models data/raw data/processed

ENV PYTHONUNBUFFERED=1
ENV ENVIRONMENT=production
ENV PORT=8080

EXPOSE 8080

CMD sh -c "uvicorn api.app:app --host 0.0.0.0 --port ${PORT:-8080} --workers 1"

