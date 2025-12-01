#!/bin/bash

# Script de limpeza - Remove todos os recursos criados

set -e

echo "=========================================="
echo "LIMPEZA - DESAFIO 2"
echo "=========================================="
echo ""

# Cores
RED='\033[0;31m'
BLUE='\033[0;34m'
GREEN='\033[0;32m'
NC='\033[0m'

# Variáveis
VOLUME_NAME="desafio2-postgres-data"
NETWORK_NAME="desafio2-network"
DB_CONTAINER="desafio2-postgres"

echo -e "${BLUE}[1/4]${NC} Parando containers..."
docker stop $DB_CONTAINER 2>/dev/null || echo "Container ja estava parado"
echo -e "${GREEN}Containers parados!${NC}"
echo ""

echo -e "${BLUE}[2/4]${NC} Removendo containers..."
docker rm $DB_CONTAINER 2>/dev/null || echo "Container ja foi removido"
echo -e "${GREEN}Containers removidos!${NC}"
echo ""

echo -e "${BLUE}[3/4]${NC} Removendo rede..."
docker network rm $NETWORK_NAME 2>/dev/null || echo "Rede ja foi removida"
echo -e "${GREEN}Rede removida!${NC}"
echo ""

echo -e "${RED}[4/4]${NC} Removendo volume..."
read -p "Deseja remover o volume? Todos os dados serao perdidos! (s/N): " -n 1 -r
echo
if [[ $REPLY =~ ^[SsYy]$ ]]; then
    docker volume rm $VOLUME_NAME 2>/dev/null || echo "Volume ja foi removido"
    echo -e "${GREEN}Volume removido!${NC}"
else
    echo -e "${BLUE}Volume mantido.${NC}"
fi
echo ""

echo "=========================================="
echo -e "${GREEN}LIMPEZA CONCLUIDA!${NC}"
echo "=========================================="
echo ""
