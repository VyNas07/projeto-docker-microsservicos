# Script PowerShell para visualizar logs do Desafio 1
# Exibe logs de ambos os containers

Write-Host "=========================================" -ForegroundColor Cyan
Write-Host "LOGS - DESAFIO 1" -ForegroundColor Cyan
Write-Host "=========================================" -ForegroundColor Cyan
Write-Host ""

# Nomes dos containers
$SERVER_CONTAINER = "desafio1-servidor"
$CLIENT_CONTAINER = "desafio1-cliente"

# Verifica se os containers estão rodando
$serverRunning = docker ps -q -f name=$SERVER_CONTAINER
$clientRunning = docker ps -q -f name=$CLIENT_CONTAINER

if (-not $serverRunning) {
    Write-Host "Container servidor nao esta em execucao!" -ForegroundColor Yellow
    Write-Host ""
}

if (-not $clientRunning) {
    Write-Host "Container cliente nao esta em execucao!" -ForegroundColor Yellow
    Write-Host ""
}

Write-Host "Escolha uma opção:" -ForegroundColor Blue
Write-Host "  1) Logs do Servidor"
Write-Host "  2) Logs do Cliente"
Write-Host "  3) Logs do Servidor (últimas 50 linhas)"
Write-Host "  4) Logs do Cliente (últimas 50 linhas)"
Write-Host ""
$option = Read-Host "Digite o número da opção [1-4]"

switch ($option) {
    "1" {
        Write-Host "Exibindo logs do SERVIDOR (Ctrl+C para sair)..." -ForegroundColor Green
        Write-Host ""
        docker logs -f $SERVER_CONTAINER
    }
    "2" {
        Write-Host "Exibindo logs do CLIENTE (Ctrl+C para sair)..." -ForegroundColor Green
        Write-Host ""
        docker logs -f $CLIENT_CONTAINER
    }
    "3" {
        Write-Host "Ultimas 50 linhas do SERVIDOR:" -ForegroundColor Green
        Write-Host ""
        docker logs --tail 50 $SERVER_CONTAINER
    }
    "4" {
        Write-Host "Ultimas 50 linhas do CLIENTE:" -ForegroundColor Green
        Write-Host ""
        docker logs --tail 50 $CLIENT_CONTAINER
    }
    default {
        Write-Host "Opcao invalida!" -ForegroundColor Yellow
        exit 1
    }
}
