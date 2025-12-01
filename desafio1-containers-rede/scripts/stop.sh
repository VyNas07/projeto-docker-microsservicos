#!/bin/bash

# Script para parar o Desafio 1 - Containers em Rede
# Para e remove containers e rede

set -e  # Para execução em caso de erro

echo "=========================================="
echo "PARANDO DESAFIO 1 - CONTAINERS EM REDE"
echo "=========================================="
echo ""

# Cores para output
RED='\033[0;31m'
BLUE='\033[0;34m'
GREEN='\033[0;32m'
NC='\033[0m' # No Color

# Nome da rede
NETWORK_NAME="desafio1-network"

# Nomes dos containers
SERVER_CONTAINER="desafio1-servidor"
CLIENT_CONTAINER="desafio1-cliente"

echo -e "${BLUE}[1/3]${NC} Parando containers..."

if docker ps -q -f name=$CLIENT_CONTAINER | grep -q .; then
    echo -e "${BLUE}Parando cliente...${NC}"
    docker stop $CLIENT_CONTAINER
    echo -e "${GREEN}Cliente parado!${NC}"
else
    echo -e "${BLUE}Cliente nao esta em execucao.${NC}"
fi

if docker ps -q -f name=$SERVER_CONTAINER | grep -q .; then
    echo -e "${BLUE}Parando servidor...${NC}"
    docker stop $SERVER_CONTAINER
    echo -e "${GREEN}Servidor parado!${NC}"
else
    echo -e "${BLUE}Servidor nao esta em execucao.${NC}"
fi
echo ""

echo -e "${BLUE}[2/3]${NC} Removendo containers..."
docker rm $CLIENT_CONTAINER 2>/dev/null || echo -e "${BLUE}Container cliente nao existe.${NC}"
docker rm $SERVER_CONTAINER 2>/dev/null || echo -e "${BLUE}Container servidor nao existe.${NC}"
echo -e "${GREEN}Containers removidos!${NC}"
echo ""

echo -e "${BLUE}[3/3]${NC} Removendo rede Docker..."
if docker network inspect $NETWORK_NAME >/dev/null 2>&1; then
    docker network rm $NETWORK_NAME
    echo -e "${GREEN}Rede $NETWORK_NAME removida!${NC}"
else
    echo -e "${BLUE}Rede $NETWORK_NAME nao existe.${NC}"
fi
echo ""

echo "=========================================="
echo -e "${GREEN}SISTEMA ENCERRADO COM SUCESSO!${NC}"
echo "=========================================="
echo ""
echo "Para reiniciar, execute: ./scripts/start.sh"
echo ""
