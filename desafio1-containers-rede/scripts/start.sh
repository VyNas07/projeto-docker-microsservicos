#!/bin/bash

# Script para iniciar o Desafio 1 - Containers em Rede
# Cria rede Docker, builda as imagens e inicia os containers

set -e  # Para execução em caso de erro

echo "=========================================="
echo "DESAFIO 1 - CONTAINERS EM REDE"
echo "=========================================="
echo ""

# Cores para output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Nome da rede
NETWORK_NAME="desafio1-network"

# Nomes dos containers
SERVER_CONTAINER="desafio1-servidor"
CLIENT_CONTAINER="desafio1-cliente"

echo -e "${BLUE}[1/5]${NC} Verificando se a rede ja existe..."
if docker network inspect $NETWORK_NAME >/dev/null 2>&1; then
    echo -e "${YELLOW}Rede $NETWORK_NAME ja existe. Usando a existente.${NC}"
else
    echo -e "${BLUE}Criando rede Docker: $NETWORK_NAME${NC}"
    docker network create $NETWORK_NAME
    echo -e "${GREEN}Rede criada com sucesso!${NC}"
fi
echo ""

echo -e "${BLUE}[2/5]${NC} Parando containers existentes (se houver)..."
docker stop $SERVER_CONTAINER 2>/dev/null || true
docker stop $CLIENT_CONTAINER 2>/dev/null || true
docker rm $SERVER_CONTAINER 2>/dev/null || true
docker rm $CLIENT_CONTAINER 2>/dev/null || true
echo -e "${GREEN}Limpeza concluida!${NC}"
echo ""

echo -e "${BLUE}[3/5]${NC} Construindo imagem do servidor..."
docker build -t desafio1-servidor:latest ./servidor
echo -e "${GREEN}Imagem do servidor construida!${NC}"
echo ""

echo -e "${BLUE}[4/5]${NC} Construindo imagem do cliente..."
docker build -t desafio1-cliente:latest ./cliente
echo -e "${GREEN}Imagem do cliente construida!${NC}"
echo ""

echo -e "${BLUE}[5/5]${NC} Iniciando containers..."
echo -e "${BLUE}Iniciando servidor na porta 8080...${NC}"
docker run -d \
    --name $SERVER_CONTAINER \
    --network $NETWORK_NAME \
    -p 8080:8080 \
    desafio1-servidor:latest

# Aguarda o servidor iniciar
echo -e "${YELLOW}Aguardando servidor inicializar...${NC}"
sleep 3

echo -e "${BLUE}Iniciando cliente...${NC}"
docker run -d \
    --name $CLIENT_CONTAINER \
    --network $NETWORK_NAME \
    desafio1-cliente:latest

echo -e "${GREEN}Containers iniciados com sucesso!${NC}"
echo ""

echo "=========================================="
echo -e "${GREEN}SISTEMA INICIADO COM SUCESSO!${NC}"
echo "=========================================="
echo ""
echo "Informacoes:"
echo "   - Rede: $NETWORK_NAME"
echo "   - Servidor: $SERVER_CONTAINER (porta 8080)"
echo "   - Cliente: $CLIENT_CONTAINER"
echo ""
echo "Comandos uteis:"
echo "   - Ver logs do servidor: docker logs -f $SERVER_CONTAINER"
echo "   - Ver logs do cliente:  docker logs -f $CLIENT_CONTAINER"
echo "   - Ver ambos os logs:    ./scripts/logs.sh"
echo "   - Parar o sistema:      ./scripts/stop.sh"
echo "   - Testar servidor:      curl http://localhost:8080"
echo ""
echo "O cliente fara requisicoes a cada 5 segundos."
echo ""
