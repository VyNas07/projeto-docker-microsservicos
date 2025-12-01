#!/bin/bash

# Script de setup do Desafio 2 - Volumes e Persistência
# Cria volume, rede, containers e popula banco de dados

set -e

echo "=========================================="
echo "DESAFIO 2 - VOLUMES E PERSISTENCIA"
echo "Setup Inicial"
echo "=========================================="
echo ""

# Cores
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m'

# Variáveis
VOLUME_NAME="desafio2-postgres-data"
NETWORK_NAME="desafio2-network"
DB_CONTAINER="desafio2-postgres"
CLIENT_CONTAINER="desafio2-client"

echo -e "${BLUE}[1/6]${NC} Criando volume Docker..."
if docker volume inspect $VOLUME_NAME >/dev/null 2>&1; then
    echo -e "${YELLOW}Volume $VOLUME_NAME ja existe.${NC}"
else
    docker volume create $VOLUME_NAME
    echo -e "${GREEN}Volume criado com sucesso!${NC}"
fi
echo ""

echo -e "${BLUE}[2/6]${NC} Criando rede Docker..."
if docker network inspect $NETWORK_NAME >/dev/null 2>&1; then
    echo -e "${YELLOW}Rede $NETWORK_NAME ja existe.${NC}"
else
    docker network create $NETWORK_NAME
    echo -e "${GREEN}Rede criada com sucesso!${NC}"
fi
echo ""

echo -e "${BLUE}[3/6]${NC} Construindo imagem do PostgreSQL..."
docker build -t desafio2-postgres:latest ./database
echo -e "${GREEN}Imagem construida!${NC}"
echo ""

echo -e "${BLUE}[4/6]${NC} Iniciando container PostgreSQL..."
docker run -d \
    --name $DB_CONTAINER \
    --network $NETWORK_NAME \
    -v $VOLUME_NAME:/var/lib/postgresql/data \
    -p 5432:5432 \
    -e POSTGRES_DB=desafio2 \
    -e POSTGRES_USER=postgres \
    -e POSTGRES_PASSWORD=postgres123 \
    desafio2-postgres:latest

echo -e "${GREEN}Container iniciado!${NC}"
echo ""

echo -e "${BLUE}[5/6]${NC} Aguardando PostgreSQL inicializar..."
sleep 5
echo -e "${GREEN}PostgreSQL pronto!${NC}"
echo ""

echo -e "${BLUE}[6/6]${NC} Construindo imagem do cliente..."
docker build -t desafio2-client:latest ./client
echo -e "${GREEN}Imagem do cliente construida!${NC}"
echo ""

echo "=========================================="
echo -e "${GREEN}SETUP CONCLUIDO COM SUCESSO!${NC}"
echo "=========================================="
echo ""
echo "Informacoes:"
echo "  Volume: $VOLUME_NAME"
echo "  Rede: $NETWORK_NAME"
echo "  Container DB: $DB_CONTAINER (porta 5432)"
echo ""
echo "Comandos uteis:"
echo "  Consultar dados:     docker run --rm --network $NETWORK_NAME -e POSTGRES_HOST=$DB_CONTAINER desafio2-client"
echo "  Inspecionar volume:  docker volume inspect $VOLUME_NAME"
echo "  Ver logs do banco:   docker logs $DB_CONTAINER"
echo "  Testar persistencia: ./scripts/test-persistence.sh"
echo "  Limpar tudo:         ./scripts/cleanup.sh"
echo ""
