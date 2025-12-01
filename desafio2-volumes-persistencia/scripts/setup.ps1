# Script PowerShell de setup do Desafio 2
# Cria volume, rede, containers e popula banco

Write-Host "==========================================" -ForegroundColor Cyan
Write-Host "DESAFIO 2 - VOLUMES E PERSISTENCIA" -ForegroundColor Cyan
Write-Host "Setup Inicial" -ForegroundColor Cyan
Write-Host "==========================================" -ForegroundColor Cyan
Write-Host ""

# Variáveis
$VOLUME_NAME = "desafio2-postgres-data"
$NETWORK_NAME = "desafio2-network"
$DB_CONTAINER = "desafio2-postgres"
$CLIENT_CONTAINER = "desafio2-client"

Write-Host "[1/6] Criando volume Docker..." -ForegroundColor Blue
$volumeExists = docker volume inspect $VOLUME_NAME 2>$null
if ($volumeExists) {
    Write-Host "Volume $VOLUME_NAME ja existe." -ForegroundColor Yellow
} else {
    docker volume create $VOLUME_NAME
    Write-Host "Volume criado com sucesso!" -ForegroundColor Green
}
Write-Host ""

Write-Host "[2/6] Criando rede Docker..." -ForegroundColor Blue
$networkExists = docker network inspect $NETWORK_NAME 2>$null
if ($networkExists) {
    Write-Host "Rede $NETWORK_NAME ja existe." -ForegroundColor Yellow
} else {
    docker network create $NETWORK_NAME
    Write-Host "Rede criada com sucesso!" -ForegroundColor Green
}
Write-Host ""

Write-Host "[3/6] Construindo imagem do PostgreSQL..." -ForegroundColor Blue
docker build -t desafio2-postgres:latest ./database
Write-Host "Imagem construida!" -ForegroundColor Green
Write-Host ""

Write-Host "[4/6] Iniciando container PostgreSQL..." -ForegroundColor Blue
docker run -d `
    --name $DB_CONTAINER `
    --network $NETWORK_NAME `
    -v ${VOLUME_NAME}:/var/lib/postgresql/data `
    -p 5432:5432 `
    -e POSTGRES_DB=desafio2 `
    -e POSTGRES_USER=postgres `
    -e POSTGRES_PASSWORD=postgres123 `
    desafio2-postgres:latest

Write-Host "Container iniciado!" -ForegroundColor Green
Write-Host ""

Write-Host "[5/6] Aguardando PostgreSQL inicializar..." -ForegroundColor Blue
Start-Sleep -Seconds 5
Write-Host "PostgreSQL pronto!" -ForegroundColor Green
Write-Host ""

Write-Host "[6/6] Construindo imagem do cliente..." -ForegroundColor Blue
docker build -t desafio2-client:latest ./client
Write-Host "Imagem do cliente construida!" -ForegroundColor Green
Write-Host ""

Write-Host "==========================================" -ForegroundColor Cyan
Write-Host "SETUP CONCLUIDO COM SUCESSO!" -ForegroundColor Green
Write-Host "==========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Informacoes:"
Write-Host "  Volume: $VOLUME_NAME"
Write-Host "  Rede: $NETWORK_NAME"
Write-Host "  Container DB: $DB_CONTAINER (porta 5432)"
Write-Host ""
Write-Host "Comandos uteis:"
Write-Host "  Consultar dados:     docker run --rm --network $NETWORK_NAME -e POSTGRES_HOST=$DB_CONTAINER desafio2-client"
Write-Host "  Inspecionar volume:  docker volume inspect $VOLUME_NAME"
Write-Host "  Ver logs do banco:   docker logs $DB_CONTAINER"
Write-Host "  Testar persistencia: .\scripts\test-persistence.ps1"
Write-Host "  Limpar tudo:         .\scripts\cleanup.ps1"
Write-Host ""
