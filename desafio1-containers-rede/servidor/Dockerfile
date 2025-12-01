# Dockerfile para o Servidor Flask
# Desafio 1 - Containers em Rede

FROM python:3.11-slim

# Metadados da imagem
LABEL maintainer="VyNas07"
LABEL description="Servidor Flask para comunicação entre containers"
LABEL version="1.0"

# Define diretório de trabalho
WORKDIR /app

# Copia arquivo de dependências primeiro (cache layer)
COPY requirements.txt .

# Instala dependências Python
RUN pip install --no-cache-dir -r requirements.txt

# Copia código da aplicação
COPY app.py .

# Expõe porta 8080
EXPOSE 8080

# Define variável de ambiente
ENV FLASK_APP=app.py
ENV PYTHONUNBUFFERED=1

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
    CMD python -c "import requests; requests.get('http://localhost:8080/health')" || exit 1

# Comando para executar a aplicação
CMD ["python", "app.py"]
