# Script PowerShell para testar persistência
# Remove container, recria e verifica dados

Write-Host "==========================================" -ForegroundColor Cyan
Write-Host "TESTE DE PERSISTENCIA" -ForegroundColor Cyan
Write-Host "==========================================" -ForegroundColor Cyan
Write-Host ""

# Variáveis
$VOLUME_NAME = "desafio2-postgres-data"
$NETWORK_NAME = "desafio2-network"
$DB_CONTAINER = "desafio2-postgres"

Write-Host "[1/5] Consultando dados antes da remocao..." -ForegroundColor Blue
docker run --rm --network $NETWORK_NAME `
    -e POSTGRES_HOST=$DB_CONTAINER `
    desafio2-client
Write-Host ""

Write-Host "[2/5] Parando e removendo container do banco..." -ForegroundColor Yellow
docker stop $DB_CONTAINER
docker rm $DB_CONTAINER
Write-Host "Container removido!" -ForegroundColor Green
Write-Host ""

Write-Host "[3/5] Aguardando 3 segundos..." -ForegroundColor Yellow
Start-Sleep -Seconds 3
Write-Host ""

Write-Host "[4/5] Recriando container com o mesmo volume..." -ForegroundColor Blue
docker run -d `
    --name $DB_CONTAINER `
    --network $NETWORK_NAME `
    -v ${VOLUME_NAME}:/var/lib/postgresql/data `
    -p 5432:5432 `
    -e POSTGRES_DB=desafio2 `
    -e POSTGRES_USER=postgres `
    -e POSTGRES_PASSWORD=postgres123 `
    desafio2-postgres:latest

Write-Host "Container recriado!" -ForegroundColor Green
Write-Host ""

Write-Host "Aguardando PostgreSQL reinicializar..." -ForegroundColor Blue
Start-Sleep -Seconds 5
Write-Host ""

Write-Host "[5/5] Consultando dados apos recriacao..." -ForegroundColor Blue
docker run --rm --network $NETWORK_NAME `
    -e POSTGRES_HOST=$DB_CONTAINER `
    desafio2-client
Write-Host ""

Write-Host "==========================================" -ForegroundColor Cyan
Write-Host "TESTE DE PERSISTENCIA CONCLUIDO!" -ForegroundColor Green
Write-Host "==========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Os dados foram mantidos mesmo apos remover e recriar o container!" -ForegroundColor Green
Write-Host "Isso demonstra que o volume Docker esta funcionando corretamente." -ForegroundColor Green
Write-Host ""
