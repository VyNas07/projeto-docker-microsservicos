# Script PowerShell de limpeza
# Remove todos os recursos criados

Write-Host "==========================================" -ForegroundColor Cyan
Write-Host "LIMPEZA - DESAFIO 2" -ForegroundColor Cyan
Write-Host "==========================================" -ForegroundColor Cyan
Write-Host ""

# Variáveis
$VOLUME_NAME = "desafio2-postgres-data"
$NETWORK_NAME = "desafio2-network"
$DB_CONTAINER = "desafio2-postgres"

Write-Host "[1/4] Parando containers..." -ForegroundColor Blue
docker stop $DB_CONTAINER 2>$null
Write-Host "Containers parados!" -ForegroundColor Green
Write-Host ""

Write-Host "[2/4] Removendo containers..." -ForegroundColor Blue
docker rm $DB_CONTAINER 2>$null
Write-Host "Containers removidos!" -ForegroundColor Green
Write-Host ""

Write-Host "[3/4] Removendo rede..." -ForegroundColor Blue
docker network rm $NETWORK_NAME 2>$null
Write-Host "Rede removida!" -ForegroundColor Green
Write-Host ""

Write-Host "[4/4] Removendo volume..." -ForegroundColor Red
$response = Read-Host "Deseja remover o volume? Todos os dados serao perdidos! (s/N)"
if ($response -eq 's' -or $response -eq 'S') {
    docker volume rm $VOLUME_NAME 2>$null
    Write-Host "Volume removido!" -ForegroundColor Green
} else {
    Write-Host "Volume mantido." -ForegroundColor Blue
}
Write-Host ""

Write-Host "==========================================" -ForegroundColor Cyan
Write-Host "LIMPEZA CONCLUIDA!" -ForegroundColor Green
Write-Host "==========================================" -ForegroundColor Cyan
Write-Host ""
