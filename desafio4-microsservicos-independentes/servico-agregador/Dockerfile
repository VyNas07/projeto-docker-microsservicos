# Dockerfile para Microsserviço B - Serviço Agregador
FROM python:3.11-slim

# Metadados
LABEL maintainer="VyNas07"
LABEL description="Microsservico B - Agregador de dados"
LABEL version="1.0"

# Instala curl para health check
RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*

# Define diretório de trabalho
WORKDIR /app

# Copia dependências
COPY requirements.txt .

# Instala dependências Python
RUN pip install --no-cache-dir -r requirements.txt

# Copia código
COPY app.py .

# Expõe porta
EXPOSE 5002

# Define variáveis de ambiente
ENV PYTHONUNBUFFERED=1
ENV FLASK_APP=app.py

# Comando de inicialização
CMD ["python", "app.py"]
