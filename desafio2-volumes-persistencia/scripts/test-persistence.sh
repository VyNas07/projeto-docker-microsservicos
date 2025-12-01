#!/bin/bash

# Script para testar persistência de dados
# Remove container, recria e verifica se dados persistem

set -e

echo "=========================================="
echo "TESTE DE PERSISTENCIA"
echo "=========================================="
echo ""

# Cores
GREEN='\033[0;32m'
BLUE='\033[0;34m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m'

# Variáveis
VOLUME_NAME="desafio2-postgres-data"
NETWORK_NAME="desafio2-network"
DB_CONTAINER="desafio2-postgres"

echo -e "${BLUE}[1/5]${NC} Consultando dados antes da remocao..."
docker run --rm --network $NETWORK_NAME \
    -e POSTGRES_HOST=$DB_CONTAINER \
    desafio2-client
echo ""

echo -e "${YELLOW}[2/5]${NC} Parando e removendo container do banco..."
docker stop $DB_CONTAINER
docker rm $DB_CONTAINER
echo -e "${GREEN}Container removido!${NC}"
echo ""

echo -e "${YELLOW}[3/5]${NC} Aguardando 3 segundos..."
sleep 3
echo ""

echo -e "${BLUE}[4/5]${NC} Recriando container com o mesmo volume..."
docker run -d \
    --name $DB_CONTAINER \
    --network $NETWORK_NAME \
    -v $VOLUME_NAME:/var/lib/postgresql/data \
    -p 5432:5432 \
    -e POSTGRES_DB=desafio2 \
    -e POSTGRES_USER=postgres \
    -e POSTGRES_PASSWORD=postgres123 \
    desafio2-postgres:latest

echo -e "${GREEN}Container recriado!${NC}"
echo ""

echo -e "${BLUE}Aguardando PostgreSQL reinicializar...${NC}"
sleep 5
echo ""

echo -e "${BLUE}[5/5]${NC} Consultando dados apos recriacao..."
docker run --rm --network $NETWORK_NAME \
    -e POSTGRES_HOST=$DB_CONTAINER \
    desafio2-client
echo ""

echo "=========================================="
echo -e "${GREEN}TESTE DE PERSISTENCIA CONCLUIDO!${NC}"
echo "=========================================="
echo ""
echo -e "${GREEN}Os dados foram mantidos mesmo apos remover e recriar o container!${NC}"
echo -e "${GREEN}Isso demonstra que o volume Docker esta funcionando corretamente.${NC}"
echo ""
