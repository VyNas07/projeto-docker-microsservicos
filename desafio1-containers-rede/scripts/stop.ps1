# Script PowerShell para parar o Desafio 1 - Containers em Rede
# Para e remove containers e rede

Write-Host "=========================================" -ForegroundColor Cyan
Write-Host "PARANDO DESAFIO 1 - CONTAINERS EM REDE" -ForegroundColor Cyan
Write-Host "=========================================" -ForegroundColor Cyan
Write-Host ""

# Nome da rede
$NETWORK_NAME = "desafio1-network"

# Nomes dos containers
$SERVER_CONTAINER = "desafio1-servidor"
$CLIENT_CONTAINER = "desafio1-cliente"

Write-Host "[1/3] Parando containers..." -ForegroundColor Blue

$clientRunning = docker ps -q -f name=$CLIENT_CONTAINER
if ($clientRunning) {
    Write-Host "Parando cliente..." -ForegroundColor Blue
    docker stop $CLIENT_CONTAINER
    Write-Host "Cliente parado!" -ForegroundColor Green
}
else {
    Write-Host "Cliente nao esta em execucao." -ForegroundColor Blue
}

$serverRunning = docker ps -q -f name=$SERVER_CONTAINER
if ($serverRunning) {
    Write-Host "Parando servidor..." -ForegroundColor Blue
    docker stop $SERVER_CONTAINER
    Write-Host "Servidor parado!" -ForegroundColor Green
}
else {
    Write-Host "Servidor nao esta em execucao." -ForegroundColor Blue
}
Write-Host ""

Write-Host "[2/3] Removendo containers..." -ForegroundColor Blue
docker rm $CLIENT_CONTAINER 2>$null
docker rm $SERVER_CONTAINER 2>$null
Write-Host "Containers removidos!" -ForegroundColor Green
Write-Host ""

Write-Host "[3/3] Removendo rede Docker..." -ForegroundColor Blue
$networkExists = docker network inspect $NETWORK_NAME 2>$null
if ($networkExists) {
    docker network rm $NETWORK_NAME
    Write-Host "Rede $NETWORK_NAME removida!" -ForegroundColor Green
}
else {
    Write-Host "Rede $NETWORK_NAME nao existe." -ForegroundColor Blue
}
Write-Host ""

Write-Host "=========================================" -ForegroundColor Cyan
Write-Host "SISTEMA ENCERRADO COM SUCESSO!" -ForegroundColor Green
Write-Host "=========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Para reiniciar, execute: .\scripts\start.ps1"
Write-Host ""
