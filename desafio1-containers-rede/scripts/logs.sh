#!/bin/bash

# Script para visualizar logs do Desafio 1 - Containers em Rede
# Exibe logs de ambos os containers em tempo real

echo "=========================================="
echo "LOGS - DESAFIO 1"
echo "=========================================="
echo ""

# Cores para output
BLUE='\033[0;34m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Nomes dos containers
SERVER_CONTAINER="desafio1-servidor"
CLIENT_CONTAINER="desafio1-cliente"

# Verifica se os containers estão rodando
if ! docker ps -q -f name=$SERVER_CONTAINER | grep -q .; then
    echo -e "${YELLOW}Container servidor nao esta em execucao!${NC}"
    echo ""
fi

if ! docker ps -q -f name=$CLIENT_CONTAINER | grep -q .; then
    echo -e "${YELLOW}Container cliente nao esta em execucao!${NC}"
    echo ""
fi

echo -e "${BLUE}Escolha uma opção:${NC}"
echo "  1) Logs do Servidor"
echo "  2) Logs do Cliente"
echo "  3) Logs de Ambos (intercalados)"
echo "  4) Logs do Servidor (últimas 50 linhas)"
echo "  5) Logs do Cliente (últimas 50 linhas)"
echo ""
read -p "Digite o número da opção [1-5]: " option

case $option in
    1)
        echo -e "${GREEN}Exibindo logs do SERVIDOR (Ctrl+C para sair)...${NC}"
        echo ""
        docker logs -f $SERVER_CONTAINER
        ;;
    2)
        echo -e "${GREEN}Exibindo logs do CLIENTE (Ctrl+C para sair)...${NC}"
        echo ""
        docker logs -f $CLIENT_CONTAINER
        ;;
    3)
        echo -e "${GREEN}Exibindo logs de AMBOS os containers (Ctrl+C para sair)...${NC}"
        echo -e "${YELLOW}Os logs serao intercalados. Para logs separados, use opcoes 1 ou 2.${NC}"
        echo ""
        # Usa docker-compose logs se disponível, senão mostra um de cada vez
        if command -v docker-compose &> /dev/null; then
            docker-compose logs -f
        else
            # Alternativa: mostra logs em paralelo (requer instalação de 'multitail' ou similar)
            echo -e "${BLUE}=== LOGS DO SERVIDOR ===${NC}"
            docker logs --tail 20 $SERVER_CONTAINER
            echo ""
            echo -e "${BLUE}=== LOGS DO CLIENTE ===${NC}"
            docker logs --tail 20 $CLIENT_CONTAINER
            echo ""
            echo -e "${YELLOW}Dica: Use as opcoes 1 ou 2 para ver logs em tempo real de cada container.${NC}"
        fi
        ;;
    4)
        echo -e "${GREEN}Ultimas 50 linhas do SERVIDOR:${NC}"
        echo ""
        docker logs --tail 50 $SERVER_CONTAINER
        ;;
    5)
        echo -e "${GREEN}Ultimas 50 linhas do CLIENTE:${NC}"
        echo ""
        docker logs --tail 50 $CLIENT_CONTAINER
        ;;
    *)
        echo -e "${YELLOW}Opcao invalida!${NC}"
        exit 1
        ;;
esac
