# Desafio 5 - Microsserviços com API Gateway

## Descrição

Arquitetura completa de microsserviços com API Gateway como ponto único de entrada. O Gateway orquestra chamadas para dois microsserviços independentes (Usuários e Pedidos) e oferece um endpoint agregado que combina dados de ambos.

## Arquitetura

```
┌────────────────────────────────────────────────────────────────────┐
│                    Cliente Externo                                 │
└───────────────────────────┬────────────────────────────────────────┘
                            │ HTTP (Porta 8080)
                            │ ÚNICO PONTO DE ENTRADA
                            ▼
┌────────────────────────────────────────────────────────────────────┐
│                        API GATEWAY                                 │
│                     (Porta 8080 - EXPOSTA)                         │
│                                                                     │
│  • Roteamento de requisições                                       │
│  • Agregação de dados                                              │
│  • Health check cascata                                            │
│  • Logs centralizados                                              │
│  • Tratamento de erros                                             │
└────────────┬──────────────────────────┬────────────────────────────┘
             │                          │
             │ Rede Interna             │ Rede Interna
             │ (desafio5-internal)      │ (desafio5-internal)
             ▼                          ▼
┌──────────────────────────┐  ┌──────────────────────────┐
│  Microsserviço Usuarios  │  │  Microsserviço Pedidos   │
│   (Porta 5001 INTERNA)   │  │   (Porta 5002 INTERNA)   │
│                          │  │                          │
│  • GET /users            │  │  • GET /orders           │
│  • GET /users/:id        │  │  • GET /orders/:id       │
│  • GET /health           │  │  • GET /orders/user/:id  │
│                          │  │  • GET /health           │
│  Dados: usuarios.json    │  │  Dados: pedidos.json     │
└──────────────────────────┘  └──────────────────────────┘
```

## Por que API Gateway?

### Vantagens

1. **Ponto Único de Entrada**: Clientes só precisam conhecer um endpoint
2. **Isolamento**: Microsserviços não são expostos diretamente
3. **Agregação de Dados**: Gateway pode combinar dados de múltiplos serviços
4. **Roteamento Centralizado**: Lógica de roteamento em um só lugar
5. **Cross-Cutting Concerns**: Logs, autenticação, rate limiting centralizados
6. **Flexibilidade**: Microsserviços podem mudar sem impactar clientes

### Fluxo de Requisições

```
1. Cliente → Gateway (8080)
2. Gateway → Microsserviço Interno (5001 ou 5002)
3. Microsserviço → Processa e retorna dados
4. Gateway → Retorna resposta ao cliente
```

## Estrutura do Projeto

```
desafio5-api-gateway/
├── docker-compose.yml          # Orquestração dos 3 serviços
├── README.md
├── gateway/                    # API Gateway (porta 8080)
│   ├── Dockerfile
│   ├── app.py                 # Proxy e agregação
│   └── requirements.txt
├── servico-usuarios/          # Microsserviço 1 (porta 5001)
│   ├── Dockerfile
│   ├── app.py
│   ├── requirements.txt
│   └── usuarios.json          # 5 usuários
└── servico-pedidos/           # Microsserviço 2 (porta 5002)
    ├── Dockerfile
    ├── app.py
    ├── requirements.txt
    └── pedidos.json           # 8 pedidos vinculados a usuários
```

## Tecnologias

- **API Gateway**: Flask 3.0 + requests
- **Microsserviços**: Flask 3.0
- **Container**: Docker + Docker Compose
- **Rede**: Bridge network isolada
- **Python**: 3.11-slim

## Endpoints Disponíveis

### Gateway (Porta 8080 - Acesso Externo)

| Método | Endpoint | Descrição | Tipo |
|--------|----------|-----------|------|
| GET | `/` | Informações do gateway | Info |
| GET | `/users` | Lista todos os usuários | Proxy |
| GET | `/users/:id` | Busca usuário específico | Proxy |
| GET | `/orders` | Lista todos os pedidos | Proxy |
| GET | `/orders/:id` | Busca pedido específico | Proxy |
| GET | `/orders/user/:userId` | Pedidos de um usuário | Proxy |
| GET | `/users/:id/orders` | **Usuário + seus pedidos** | **Agregado** |
| GET | `/health` | Status de todos os serviços | Health |

### Microsserviço Usuarios (Porta 5001 - Interno)

| Método | Endpoint | Descrição |
|--------|----------|-----------|
| GET | `/users` | Lista usuários |
| GET | `/users/:id` | Busca usuário |
| GET | `/health` | Health check |

### Microsserviço Pedidos (Porta 5002 - Interno)

| Método | Endpoint | Descrição |
|--------|----------|-----------|
| GET | `/orders` | Lista pedidos |
| GET | `/orders/:id` | Busca pedido |
| GET | `/orders/user/:userId` | Pedidos de usuário |
| GET | `/health` | Health check |

## Como Executar

### Iniciar a Arquitetura

```bash
# Subir todos os serviços
docker compose up -d

# Ver logs de todos os serviços
docker compose logs -f

# Ver logs do gateway
docker compose logs -f gateway

# Ver logs separados
docker compose logs -f servico-usuarios
docker compose logs -f servico-pedidos
```

### Verificar Status

```bash
# Status dos containers
docker compose ps

# Health check completo
curl http://localhost:8080/health
```

## Exemplos de Uso

### 1. Informações do Gateway

```bash
curl http://localhost:8080/
```

**Resposta:**
```json
{
  "service": "API Gateway",
  "version": "1.0",
  "upstream_services": {
    "users": "http://servico-usuarios:5001",
    "orders": "http://servico-pedidos:5002"
  },
  "endpoints": {
    "users": {
      "list": "/users",
      "detail": "/users/<id>",
      "with_orders": "/users/<id>/orders"
    }
  }
}
```

### 2. Listar Usuários (Proxy)

```bash
curl http://localhost:8080/users
```

**Resposta:**
```json
{
  "total": 5,
  "users": [
    {
      "id": 1,
      "username": "jsilva",
      "full_name": "João Silva",
      "department": "TI",
      "status": "active"
    }
  ]
}
```

### 3. Buscar Usuário Específico

```bash
curl http://localhost:8080/users/1
```

**Resposta:**
```json
{
  "id": 1,
  "username": "jsilva",
  "email": "joao.silva@empresa.com",
  "full_name": "João Silva",
  "department": "TI",
  "status": "active"
}
```

### 4. Listar Pedidos (Proxy)

```bash
curl http://localhost:8080/orders
```

**Resposta:**
```json
{
  "total": 8,
  "orders": [
    {
      "id": 1,
      "user_id": 1,
      "order_number": "ORD-2024-001",
      "product": "Notebook Dell Inspiron",
      "quantity": 1,
      "price": 3499.99,
      "status": "delivered"
    }
  ]
}
```

### 5. Buscar Pedido Específico

```bash
curl http://localhost:8080/orders/1
```

### 6. Pedidos de um Usuário

```bash
curl http://localhost:8080/orders/user/1
```

**Resposta:**
```json
{
  "user_id": 1,
  "total": 2,
  "orders": [
    {
      "id": 1,
      "user_id": 1,
      "order_number": "ORD-2024-001",
      "product": "Notebook Dell Inspiron",
      "price": 3499.99
    },
    {
      "id": 2,
      "user_id": 1,
      "order_number": "ORD-2024-002",
      "product": "Mouse Logitech MX Master",
      "price": 349.90
    }
  ]
}
```

### 7. Endpoint Agregado (Usuário + Pedidos)

**Este é o endpoint mais importante - demonstra a orquestração do Gateway**

```bash
curl http://localhost:8080/users/1/orders
```

**Resposta:**
```json
{
  "user": {
    "id": 1,
    "username": "jsilva",
    "full_name": "João Silva",
    "department": "TI",
    "status": "active"
  },
  "orders_summary": {
    "total_orders": 2,
    "total_value": 3849.89,
    "status_distribution": {
      "delivered": 2
    }
  },
  "orders": [
    {
      "id": 1,
      "order_number": "ORD-2024-001",
      "product": "Notebook Dell Inspiron",
      "quantity": 1,
      "price": 3499.99,
      "status": "delivered"
    },
    {
      "id": 2,
      "order_number": "ORD-2024-002",
      "product": "Mouse Logitech MX Master",
      "quantity": 2,
      "price": 349.90,
      "status": "delivered"
    }
  ],
  "metadata": {
    "aggregated_at": "2025-12-01T15:30:00",
    "sources": ["servico-usuarios", "servico-pedidos"]
  }
}
```

**O que acontece internamente:**
1. Gateway recebe requisição em `/users/1/orders`
2. Gateway faz requisição para `servico-usuarios:5001/users/1`
3. Gateway faz requisição para `servico-pedidos:5002/orders/user/1`
4. Gateway combina os dados, calcula estatísticas
5. Gateway retorna resposta agregada ao cliente

### 8. Health Check Completo

```bash
curl http://localhost:8080/health
```

**Resposta:**
```json
{
  "gateway": {
    "status": "healthy",
    "timestamp": "2025-12-01T15:30:00"
  },
  "upstream_services": {
    "servico-usuarios": {
      "status": "healthy",
      "url": "http://servico-usuarios:5001"
    },
    "servico-pedidos": {
      "status": "healthy",
      "url": "http://servico-pedidos:5002"
    }
  },
  "overall_status": "healthy"
}
```

## Testando o Isolamento da Rede

Os microsserviços NÃO são acessíveis externamente:

```bash
# Isto NÃO funciona (porta não exposta)
curl http://localhost:5001/users  # Connection refused
curl http://localhost:5002/orders # Connection refused

# Apenas o Gateway é acessível
curl http://localhost:8080/users  # OK
```

## Comandos Úteis

### Gerenciamento de Serviços

```bash
# Rebuild de imagens
docker compose build

# Rebuild e restart
docker compose up -d --build

# Parar tudo
docker compose down

# Parar e remover volumes/redes
docker compose down -v

# Reiniciar gateway
docker compose restart gateway

# Escalar serviços (exemplo conceitual)
docker compose up -d --scale servico-usuarios=2
```

### Debug e Monitoramento

```bash
# Acessar container do gateway
docker compose exec gateway sh

# Testar comunicação interna
docker compose exec gateway curl http://servico-usuarios:5001/health
docker compose exec gateway curl http://servico-pedidos:5002/health

# Ver variáveis de ambiente
docker compose exec gateway env

# Inspecionar rede
docker network inspect desafio5-internal

# Recursos usados
docker stats desafio5-gateway desafio5-usuarios desafio5-pedidos
```

### Testes Completos

```bash
# Script de teste completo (PowerShell)
$base = "http://localhost:8080"

Write-Host "1. Gateway info"
curl $base/

Write-Host "2. Lista usuarios"
curl $base/users

Write-Host "3. Usuario especifico"
curl $base/users/1

Write-Host "4. Lista pedidos"
curl $base/orders

Write-Host "5. Pedidos de usuario"
curl $base/orders/user/1

Write-Host "6. AGREGADO: Usuario + Pedidos"
curl $base/users/1/orders

Write-Host "7. Health check"
curl $base/health
```

## Detalhes Técnicos

### Configuração de Rede

- **Rede Interna**: `desafio5-internal` (bridge)
- **Resolução DNS**: Containers se comunicam por nome de serviço
- **Isolamento**: Apenas gateway expõe porta externamente

### Health Checks

- Gateway verifica status de todos os microsserviços
- Cascata de health checks garante disponibilidade
- Status HTTP 503 quando serviços downstream falham

### Tratamento de Erros

Gateway trata:
- Timeout de serviços (504)
- Serviços indisponíveis (503)
- Erros genéricos (500)
- Recursos não encontrados (404)

### Logs Centralizados

Gateway registra:
- Timestamp de cada requisição
- Método e path
- Serviço downstream alvo
- Status da operação

## Troubleshooting

### Gateway não consegue acessar microsserviços

```bash
# Verificar rede
docker network inspect desafio5-internal

# Testar DNS
docker compose exec gateway ping servico-usuarios
docker compose exec gateway ping servico-pedidos

# Verificar variáveis de ambiente
docker compose exec gateway env | grep SERVICE_URL
```

### Porta 8080 em uso

```powershell
# Windows
netstat -ano | findstr :8080
taskkill /PID <PID> /F

# Linux
sudo lsof -i :8080
sudo kill <PID>
```

### Serviços não iniciam na ordem correta

```bash
# Ver ordem de inicialização
docker compose ps

# Verificar depends_on e health checks no docker-compose.yml
docker compose config
```

## Conceitos Demonstrados

1. **API Gateway Pattern**: Ponto único de entrada
2. **Service Mesh**: Comunicação entre microsserviços
3. **Data Aggregation**: Combinação de dados de múltiplas fontes
4. **Service Discovery**: DNS interno do Docker
5. **Network Isolation**: Microsserviços isolados na rede interna
6. **Health Check Cascade**: Verificação em cascata de dependências
7. **Proxy Pattern**: Gateway como proxy reverso
8. **Circuit Breaker**: Tratamento de falhas de serviços downstream

## Pontuação

| Critério | Pontos |
|----------|--------|
| Gateway como ponto único | 10 |
| Integração entre serviços | 5 |
| Documentação detalhada | 5 |
| Clareza e organização | 5 |
| **TOTAL** | **25** |

## Autor

VyNas07 - [GitHub](https://github.com/VyNas07)
