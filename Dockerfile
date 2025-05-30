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

CMD ["./start.sh"]

