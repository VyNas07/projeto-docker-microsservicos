# Desafio 4 - Microsserviços Independentes

## Descrição

Dois microsserviços independentes que se comunicam via HTTP. O Serviço A fornece dados de usuários, e o Serviço B consome esses dados para gerar relatórios e análises agregadas.

## Arquitetura

```
┌──────────────────────────────────────────────────────────┐
│              Rede Docker: desafio4-network               │
│                                                           │
│  ┌─────────────────────────┐                             │
│  │   Microsserviço A       │                             │
│  │   servico-usuarios      │                             │
│  │   Porta: 5001           │                             │
│  │                         │                             │
│  │  Endpoints:             │                             │
│  │  • GET /users           │                             │
│  │  • GET /users/:id       │◄────────┐                  │
│  │  • GET /health          │         │                  │
│  │                         │         │                  │
│  │  Dados: usuarios.json   │         │ HTTP Request     │
│  └─────────────────────────┘         │                  │
│                                      │                   │
│                                      │                   │
│  ┌─────────────────────────┐         │                  │
│  │   Microsserviço B       │         │                  │
│  │   servico-agregador     │         │                  │
│  │   Porta: 5002           │─────────┘                  │
│  │                         │                             │
│  │  Endpoints:             │                             │
│  │  • GET /report          │                             │
│  │  • GET /user/:id/details│                             │
│  │  • GET /health          │                             │
│  │                         │                             │
│  │  Processa e agrega dados│                             │
│  └─────────────────────────┘                             │
│                                                           │
└──────────────────────────────────────────────────────────┘
```

### Fluxo de Comunicação

1. Cliente faz requisição ao Serviço B
2. Serviço B requisita dados do Serviço A via HTTP
3. Serviço A retorna dados brutos (JSON)
4. Serviço B processa e enriquece os dados
5. Serviço B retorna resultado agregado ao cliente

## Estrutura

```
desafio4-microsservicos-independentes/
├── docker-compose.yml
├── README.md
├── servico-usuarios/          # Microsserviço A
│   ├── Dockerfile
│   ├── app.py
│   ├── requirements.txt
│   └── usuarios.json          # Dados mock
└── servico-agregador/         # Microsserviço B
    ├── Dockerfile
    ├── app.py
    └── requirements.txt
```

## Tecnologias

- Flask 3.0 (ambos os serviços)
- Python 3.11
- Docker Compose 3.8
- requests (comunicação HTTP)

## Endpoints

### Microsserviço A (Porta 5001)

| Método | Endpoint | Descrição |
|--------|----------|-----------|
| GET | `/` | Informações do serviço |
| GET | `/users` | Lista todos os usuários |
| GET | `/users/:id` | Busca usuário por ID |
| GET | `/health` | Health check |

### Microsserviço B (Porta 5002)

| Método | Endpoint | Descrição |
|--------|----------|-----------|
| GET | `/` | Informações do serviço |
| GET | `/report` | Relatório agregado de todos os usuários |
| GET | `/user/:id/details` | Detalhes enriquecidos de usuário |
| GET | `/health` | Health check (verifica Serviço A) |

## Como Executar

### Iniciar os Serviços

```bash
# Subir todos os microsserviços
docker compose up -d

# Ver logs
docker compose logs -f

# Ver logs de serviço específico
docker compose logs -f servico-usuarios
docker compose logs -f servico-agregador
```

### Testar Endpoints

**Microsserviço A:**

```bash
# Listar todos os usuários
curl http://localhost:5001/users

# Buscar usuário específico
curl http://localhost:5001/users/1

# Health check
curl http://localhost:5001/health
```

**Microsserviço B:**

```bash
# Gerar relatório completo
curl http://localhost:5002/report

# Detalhes enriquecidos de usuário
curl http://localhost:5002/user/1/details

# Health check (verifica ambos os serviços)
curl http://localhost:5002/health
```

### Parar Serviços

```bash
# Parar
docker compose down

# Parar e remover imagens
docker compose down --rmi all
```

## Exemplos de Resposta

### GET /users (Serviço A)

```json
{
  "total": 10,
  "users": [
    {
      "id": 1,
      "username": "jsilva",
      "full_name": "João Silva",
      "role": "Developer",
      "active": true,
      "registration_date": "2024-01-15"
    }
  ]
}
```

### GET /report (Serviço B)

```json
{
  "report_generated_at": "2025-12-01T14:30:00",
  "statistics": {
    "total_users": 10,
    "active_users": 8,
    "inactive_users": 2,
    "active_percentage": 80.0,
    "roles_distribution": {
      "Developer": 3,
      "Designer": 2,
      "DevOps": 2
    }
  },
  "users": [
    {
      "id": 1,
      "full_name": "João Silva",
      "role": "Developer",
      "dias_ativo": 320,
      "status_descricao": "Ativo ha 320 dias"
    }
  ]
}
```

### GET /user/1/details (Serviço B)

```json
{
  "basic_info": {
    "id": 1,
    "full_name": "João Silva",
    "role": "Developer"
  },
  "calculated_info": {
    "dias_ativo": 320,
    "anos_ativo": 0.9,
    "nivel_experiencia": "Senior",
    "status_descricao": "Usuario ativo ha 320 dias",
    "proxima_avaliacao": "2026-03-01"
  }
}
```

## Características dos Microsserviços

### Independência

- Cada serviço tem seu próprio Dockerfile
- Código completamente separado
- Podem ser desenvolvidos e implantados independentemente

### Comunicação HTTP

- Serviço B usa `requests` para chamar Serviço A
- URL configurada via variável de ambiente
- Tratamento de erros de comunicação

### Processamento de Dados

- Serviço A: retorna dados brutos
- Serviço B: agrega, calcula e enriquece dados
  - Calcula dias de atividade
  - Gera estatísticas
  - Determina nível de experiência
  - Adiciona metadados

## Comandos Úteis

```bash
# Status dos serviços
docker compose ps

# Rebuild de imagem específica
docker compose build servico-usuarios
docker compose build servico-agregador

# Reiniciar serviço
docker compose restart servico-agregador

# Acessar container
docker compose exec servico-usuarios sh
docker compose exec servico-agregador sh

# Testar comunicação interna
docker compose exec servico-agregador curl http://servico-usuarios:5001/users
```

## Troubleshooting

### Serviço B não consegue acessar Serviço A

```bash
# Verificar rede
docker network inspect desafio4-network

# Testar DNS
docker compose exec servico-agregador ping servico-usuarios

# Verificar variável de ambiente
docker compose exec servico-agregador env | grep USERS_SERVICE
```

### Porta em uso

```powershell
# Windows
netstat -ano | findstr :5001
netstat -ano | findstr :5002

# Linux
sudo lsof -i :5001
sudo lsof -i :5002
```

## Pontuação

| Critério | Pontos |
|----------|--------|
| Comunicação HTTP funcional | 5 |
| Dockerfiles e isolamento | 5 |
| Documentação da arquitetura | 5 |
| Clareza e originalidade | 5 |
| **TOTAL** | **20** |

## Autor

VyNas07 - [GitHub](https://github.com/VyNas07)
