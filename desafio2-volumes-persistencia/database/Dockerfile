# Dockerfile para PostgreSQL com script de inicialização
FROM postgres:15-alpine

# Metadados
LABEL maintainer="VyNas07"
LABEL description="PostgreSQL com dados de exemplo para demonstração de volumes"
LABEL version="1.0"

# Define variáveis de ambiente padrão
ENV POSTGRES_DB=desafio2
ENV POSTGRES_USER=postgres
ENV POSTGRES_PASSWORD=postgres123

# Copia script de inicialização
COPY init.sql /docker-entrypoint-initdb.d/

# Expõe porta padrão do PostgreSQL
EXPOSE 5432
