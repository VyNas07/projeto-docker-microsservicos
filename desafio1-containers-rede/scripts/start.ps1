# Script PowerShell para iniciar o Desafio 1 - Containers em Rede
# Cria rede Docker, builda as imagens e inicia os containers

Write-Host "=========================================" -ForegroundColor Cyan
Write-Host "DESAFIO 1 - CONTAINERS EM REDE" -ForegroundColor Cyan
Write-Host "=========================================" -ForegroundColor Cyan
Write-Host ""

# Nome da rede
$NETWORK_NAME = "desafio1-network"

# Nomes dos containers
$SERVER_CONTAINER = "desafio1-servidor"
$CLIENT_CONTAINER = "desafio1-cliente"

Write-Host "[1/5] Verificando se a rede já existe..." -ForegroundColor Blue
$networkExists = docker network inspect $NETWORK_NAME 2>$null
if ($networkExists) {
    Write-Host "Rede $NETWORK_NAME ja existe. Usando a existente." -ForegroundColor Yellow
}
else {
    Write-Host "Criando rede Docker: $NETWORK_NAME" -ForegroundColor Blue
    docker network create $NETWORK_NAME
    Write-Host "Rede criada com sucesso!" -ForegroundColor Green
}
Write-Host ""

Write-Host "[2/5] Parando containers existentes (se houver)..." -ForegroundColor Blue
docker stop $SERVER_CONTAINER 2>$null
docker stop $CLIENT_CONTAINER 2>$null
docker rm $SERVER_CONTAINER 2>$null
docker rm $CLIENT_CONTAINER 2>$null
Write-Host "Limpeza concluida!" -ForegroundColor Green
Write-Host ""

Write-Host "[3/5] Construindo imagem do servidor..." -ForegroundColor Blue
docker build -t desafio1-servidor:latest ./servidor
Write-Host "Imagem do servidor construida!" -ForegroundColor Green
Write-Host ""

Write-Host "[4/5] Construindo imagem do cliente..." -ForegroundColor Blue
docker build -t desafio1-cliente:latest ./cliente
Write-Host "Imagem do cliente construida!" -ForegroundColor Green
Write-Host ""

Write-Host "[5/5] Iniciando containers..." -ForegroundColor Blue
Write-Host "Iniciando servidor na porta 8080..." -ForegroundColor Blue
docker run -d `
    --name $SERVER_CONTAINER `
    --network $NETWORK_NAME `
    -p 8080:8080 `
    desafio1-servidor:latest

# Aguarda o servidor iniciar
Write-Host "Aguardando servidor inicializar..." -ForegroundColor Yellow
Start-Sleep -Seconds 3

Write-Host "Iniciando cliente..." -ForegroundColor Blue
docker run -d `
    --name $CLIENT_CONTAINER `
    --network $NETWORK_NAME `
    desafio1-cliente:latest

Write-Host "Containers iniciados com sucesso!" -ForegroundColor Green
Write-Host ""

Write-Host "=========================================" -ForegroundColor Cyan
Write-Host "SISTEMA INICIADO COM SUCESSO!" -ForegroundColor Green
Write-Host "=========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Informacoes:"
Write-Host "   - Rede: $NETWORK_NAME"
Write-Host "   - Servidor: $SERVER_CONTAINER (porta 8080)"
Write-Host "   - Cliente: $CLIENT_CONTAINER"
Write-Host ""
Write-Host "Comandos uteis:"
Write-Host "   - Ver logs do servidor: docker logs -f $SERVER_CONTAINER"
Write-Host "   - Ver logs do cliente:  docker logs -f $CLIENT_CONTAINER"
Write-Host "   - Ver ambos os logs:    .\scripts\logs.ps1"
Write-Host "   - Parar o sistema:      .\scripts\stop.ps1"
Write-Host "   - Testar servidor:      curl http://localhost:8080"
Write-Host ""
Write-Host "O cliente fara requisicoes a cada 5 segundos."
Write-Host ""
