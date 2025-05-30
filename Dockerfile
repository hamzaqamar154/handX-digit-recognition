FROM python:3.10-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY src/ ./src/
COPY api/ ./api/
COPY models/ ./models/
COPY start.sh ./

RUN mkdir -p data/raw data/processed && \
    chmod +x start.sh

ENV PYTHONUNBUFFERED=1
ENV ENVIRONMENT=production
ENV PORT=8080

EXPOSE 8080

CMD ./start.sh

