# Dockerfile para o Cliente HTTP
# Desafio 1 - Containers em Rede

FROM python:3.11-slim

# Metadados da imagem
LABEL maintainer="VyNas07"
LABEL description="Cliente HTTP para comunicação entre containers"
LABEL version="1.0"

# Define diretório de trabalho
WORKDIR /app

# Copia arquivo de dependências primeiro (cache layer)
COPY requirements.txt .

# Instala dependências Python
RUN pip install --no-cache-dir -r requirements.txt

# Copia código da aplicação
COPY client.py .

# Define variável de ambiente
ENV PYTHONUNBUFFERED=1

# Comando para executar a aplicação
CMD ["python", "client.py"]
