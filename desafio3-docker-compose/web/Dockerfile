# Dockerfile para API Flask
FROM python:3.11-slim

# Metadados
LABEL maintainer="VyNas07"
LABEL description="API Flask para orquestração de serviços"
LABEL version="1.0"

# Define diretório de trabalho
WORKDIR /app

# Copia dependências
COPY requirements.txt .

# Instala dependências
RUN pip install --no-cache-dir -r requirements.txt

# Copia código
COPY app.py .

# Expõe porta
EXPOSE 5000

# Define variáveis de ambiente
ENV PYTHONUNBUFFERED=1
ENV FLASK_APP=app.py

# Comando de inicialização
CMD ["python", "app.py"]
