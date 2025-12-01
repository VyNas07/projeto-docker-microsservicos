# Dockerfile - Microsserviço de Pedidos
FROM python:3.11-slim

LABEL maintainer="VyNas07"
LABEL description="Microsservico de Pedidos - acesso interno via Gateway"

# Instala curl para health check
RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app.py .
COPY pedidos.json .

EXPOSE 5002

ENV PYTHONUNBUFFERED=1

CMD ["python", "app.py"]
