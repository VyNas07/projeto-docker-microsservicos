# Dockerfile - API Gateway
FROM python:3.11-slim

LABEL maintainer="VyNas07"
LABEL description="API Gateway - Ponto unico de entrada"

# Instala curl para health check
RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app.py .

EXPOSE 8080

ENV PYTHONUNBUFFERED=1

CMD ["python", "app.py"]
