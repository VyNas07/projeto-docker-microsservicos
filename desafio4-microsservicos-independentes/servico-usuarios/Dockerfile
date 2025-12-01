# Dockerfile para Microsserviço A - Serviço de Usuários
FROM python:3.11-slim

# Metadados
LABEL maintainer="VyNas07"
LABEL description="Microsservico A - API de usuarios"
LABEL version="1.0"

# Instala curl para health check
RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*

# Define diretório de trabalho
WORKDIR /app

# Copia dependências
COPY requirements.txt .

# Instala dependências Python
RUN pip install --no-cache-dir -r requirements.txt

# Copia código e dados
COPY app.py .
COPY usuarios.json .

# Expõe porta
EXPOSE 5001

# Define variáveis de ambiente
ENV PYTHONUNBUFFERED=1
ENV FLASK_APP=app.py

# Comando de inicialização
CMD ["python", "app.py"]
