# Desafio 3 - Docker Compose Orquestrando Serviços

## Descrição

Orquestração de múltiplos serviços usando Docker Compose. Aplicação com 3 serviços interdependentes: API Flask (web), PostgreSQL (db) e Redis (cache).

## Arquitetura

```
┌─────────────────────────────────────────────────────────┐
│           Rede Docker: desafio3-network                 │
│                                                          │
│  ┌──────────────┐      ┌──────────────┐                │
│  │   PostgreSQL │◄─────┤   Flask API  │                │
│  │   (db:5432)  │      │  (web:5000)  │                │
│  │              │      │              │                │
│  │  Volume:     │      └──────┬───────┘                │
│  │  postgres_data│             │                        │
│  └──────────────┘             │                         │
│                                ▼                         │
│                       ┌──────────────┐                  │
│                       │    Redis     │                  │
│                       │ (cache:6379) │                  │
│                       │              │                  │
│                       │  Volume:     │                  │
│                       │  redis_data  │                  │
│                       └──────────────┘                  │
└─────────────────────────────────────────────────────────┘
```

### Fluxo de Dependências

1. `db` e `cache` iniciam primeiro (sem dependências)
2. `web` aguarda health checks de `db` e `cache`
3. API Flask conecta aos dois serviços

## Estrutura

```
desafio3-docker-compose/
├── docker-compose.yml      # Orquestração
├── .env.example           # Variáveis de ambiente
├── README.md
├── web/
│   ├── Dockerfile
│   ├── app.py            # API Flask
│   └── requirements.txt
└── db/
    └── init.sql          # Dados iniciais
```

## Tecnologias

- Docker Compose 3.8
- Flask 3.0 (API REST)
- PostgreSQL 15 Alpine
- Redis 7 Alpine
- Python 3.11

## Endpoints da API

| Método | Endpoint | Descrição |
|--------|----------|-----------|
| GET | `/` | Informações gerais |
| GET | `/users` | Lista usuários (PostgreSQL) |
| POST | `/cache` | Salva no Redis |
| GET | `/cache/<key>` | Busca no Redis |
| GET | `/health` | Status dos serviços |

## Como Executar

### Pré-requisitos

- Docker e Docker Compose
- Porta 5000 disponível

### Iniciar Serviços

```bash
# Subir todos os serviços
docker compose up -d

# Ver logs
docker compose logs -f

# Ver logs de um serviço específico
docker compose logs -f web
```

### Testar Endpoints

```bash
# Informações gerais
curl http://localhost:5000/

# Listar usuários
curl http://localhost:5000/users

# Salvar no cache
curl -X POST http://localhost:5000/cache \
  -H "Content-Type: application/json" \
  -d '{"key": "user:1", "value": {"name": "João"}, "ttl": 300}'

# Buscar do cache
curl http://localhost:5000/cache/user:1

# Health check
curl http://localhost:5000/health
```

### Parar e Limpar

```bash
# Parar serviços
docker compose down

# Parar e remover volumes
docker compose down -v
```

## Comandos Úteis

```bash
# Status dos serviços
docker compose ps

# Reconstruir imagens
docker compose build

# Reiniciar serviço específico
docker compose restart web

# Acessar container
docker compose exec web sh
docker compose exec db psql -U postgres -d desafio3

# Ver uso de recursos
docker stats desafio3-web desafio3-postgres desafio3-redis
```

## Recursos do Docker Compose

### Health Checks

- **db**: `pg_isready` verifica PostgreSQL
- **cache**: `redis-cli ping` verifica Redis
- **web**: depende dos health checks anteriores

### Volumes

- `postgres_data`: Persiste banco de dados
- `redis_data`: Persiste cache Redis

### Rede

- Bridge network isolada
- Resolução DNS automática entre serviços
- Comunicação interna por nomes de serviço

### Restart Policies

- `unless-stopped`: Reinicia automaticamente exceto se parado manualmente

## Exemplo de Uso Completo

```bash
# 1. Iniciar
docker compose up -d

# 2. Aguardar serviços
sleep 10

# 3. Verificar saúde
curl http://localhost:5000/health

# 4. Listar usuários
curl http://localhost:5000/users

# 5. Cachear dados
curl -X POST http://localhost:5000/cache \
  -H "Content-Type: application/json" \
  -d '{"key": "test", "value": {"msg": "Hello"}, "ttl": 60}'

# 6. Recuperar cache
curl http://localhost:5000/cache/test

# 7. Parar
docker compose down
```

## Troubleshooting

### Serviços não iniciam

```bash
# Ver logs detalhados
docker compose logs

# Verificar ordem de inicialização
docker compose ps
```

### Erro de conexão

```bash
# Verificar rede
docker network inspect desafio3-network

# Testar conectividade
docker compose exec web ping db
docker compose exec web ping cache
```

### Porta em uso

```powershell
# Windows
netstat -ano | findstr :5000
taskkill /PID <PID> /F

# Linux
sudo lsof -i :5000
sudo kill <PID>
```

## Pontuação

| Critério | Pontos |
|----------|--------|
| Compose funcional | 10 |
| Comunicação entre serviços | 5 |
| Documentação | 5 |
| Boas práticas | 5 |
| **TOTAL** | **25** |

## Autor

VyNas07 - [GitHub](https://github.com/VyNas07)
