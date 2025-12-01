# Dockerfile para cliente de consulta
FROM python:3.11-slim

# Metadados
LABEL maintainer="VyNas07"
LABEL description="Cliente Python para consultar PostgreSQL"
LABEL version="1.0"

# Define diretório de trabalho
WORKDIR /app

# Copia dependências
COPY requirements.txt .

# Instala dependências
RUN pip install --no-cache-dir -r requirements.txt

# Copia código
COPY query.py .

# Define variável de ambiente
ENV PYTHONUNBUFFERED=1

# Comando padrão
CMD ["python", "query.py"]
