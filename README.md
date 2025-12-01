# Projeto Docker e Microsserviços

Projeto acadêmico completo sobre Docker, containers, volumes, orquestração e arquitetura de microsserviços.

## Descrição

Este repositório contém 5 desafios progressivos que demonstram conhecimentos práticos em:

- Redes Docker e comunicação entre containers
- Volumes e persistência de dados
- Orquestração com Docker Compose
- Arquitetura de microsserviços independentes
- API Gateway Pattern e orquestração de serviços

Cada desafio é independente e possui sua própria documentação detalhada.

## Estrutura do Projeto

```
projeto-docker-microsservicos/
├── desafio1-containers-rede/              # 20 pts - Comunicação via rede Docker
├── desafio2-volumes-persistencia/         # 20 pts - Persistência com volumes
├── desafio3-docker-compose/               # 25 pts - Orquestração multi-serviço
├── desafio4-microsservicos-independentes/ # 20 pts - Microsserviços HTTP
└── desafio5-api-gateway/                  # 25 pts - Gateway + Microsserviços
```

## Desafios

### Desafio 1 - Containers em Rede (20 pts)

**Status**: ✅ Completo

Dois containers comunicando-se via rede Docker customizada.

**Componentes:**

- Servidor web Flask (porta 8080)
- Cliente HTTP com requisições periódicas
- Rede customizada com DNS interno
- Scripts de automação (PowerShell e Bash)

**Conceitos:**

- Docker Networks (bridge)
- Comunicação entre containers
- DNS interno do Docker
- Logs de comunicação

[📁 Ver Desafio 1](./desafio1-containers-rede/)

---

### Desafio 2 - Volumes e Persistência (20 pts)

**Status**: ✅ Completo

Demonstração de persistência de dados usando volumes Docker.

**Componentes:**

- PostgreSQL 15 com volume nomeado
- Cliente Python para consultas
- Script de teste de persistência
- Dados sobrevivem à remoção do container

**Conceitos:**

- Volumes Docker nomeados
- Persistência de dados
- Diferença entre volumes e bind mounts
- Backup e recuperação

[📁 Ver Desafio 2](./desafio2-volumes-persistencia/)

---

### Desafio 3 - Docker Compose Orquestrando Serviços (25 pts)

**Status**: ✅ Completo

Orquestração de múltiplos serviços interdependentes com Docker Compose.

**Componentes:**

- API Flask (web)
- PostgreSQL 15 (database)
- Redis 7 (cache)
- Comunicação entre os 3 serviços

**Conceitos:**

- Docker Compose (version 3.8)
- Depends_on e health checks
- Variáveis de ambiente
- Volumes para persistência
- Rede interna automática

[📁 Ver Desafio 3](./desafio3-docker-compose/)

---

### Desafio 4 - Microsserviços Independentes (20 pts)

**Status**: ✅ Completo

Dois microsserviços independentes comunicando-se via HTTP.

**Componentes:**

- Microsserviço A: API de Usuários (porta 5001)
- Microsserviço B: Agregador de Dados (porta 5002)
- Dockerfiles separados para cada serviço
- Comunicação HTTP entre serviços

**Conceitos:**

- Arquitetura de microsserviços
- Comunicação via HTTP/REST
- Agregação de dados
- Isolamento de serviços

[📁 Ver Desafio 4](./desafio4-microsservicos-independentes/)

---

### Desafio 5 - Microsserviços com API Gateway (25 pts)

**Status**: ✅ Completo

Arquitetura completa com API Gateway como ponto único de entrada.

**Componentes:**

- API Gateway (porta 8080 - única exposta)
- Microsserviço de Usuários (porta 5001 - interna)
- Microsserviço de Pedidos (porta 5002 - interna)
- Endpoint agregado (orquestração)

**Conceitos:**

- API Gateway Pattern
- Isolamento de rede
- Proxy reverso
- Agregação de dados de múltiplos serviços
- Health check cascata
- Service mesh

[📁 Ver Desafio 5](./desafio5-api-gateway/)

## Tecnologias Utilizadas

**Containerização:**

- Docker 20.10+
- Docker Compose 2.0+

**Backend:**

- Python 3.11
- Flask 3.0
- psycopg2 (PostgreSQL driver)
- redis (Redis client)
- requests (HTTP client)

**Databases:**

- PostgreSQL 15 Alpine
- Redis 7 Alpine

**Ferramentas:**

- Bash (Linux/Mac)
- PowerShell (Windows)
- curl (testes de API)

## Requisitos

Para executar os desafios, você precisa ter instalado:

- **Docker** 20.10 ou superior
- **Docker Compose** 2.0 ou superior
- **Sistema Operacional**: Linux, macOS ou Windows com WSL2
- **Git** (para clonar o repositório)

### Verificar Instalação

```bash
docker --version
docker compose version
```

## Como Executar

Cada desafio possui seu próprio README com instruções detalhadas de execução.

### Execução Geral

1. Clone o repositório:

```bash
git clone https://github.com/VyNas07/projeto-docker-microsservicos.git
cd projeto-docker-microsservicos
```

2. Navegue até o desafio desejado:

```bash
cd desafio1-containers-rede
```

3. Siga as instruções do README específico do desafio.

### Execução Rápida por Desafio

**Desafio 1:**

```bash
cd desafio1-containers-rede
# Windows: .\scripts\start.ps1
# Linux/Mac: ./scripts/start.sh
```

**Desafio 2:**

```bash
cd desafio2-volumes-persistencia
# Windows: .\scripts\setup.ps1
# Linux/Mac: ./scripts/setup.sh
```

**Desafio 3:**

```bash
cd desafio3-docker-compose
docker compose up -d
curl http://localhost:5000/health
```

**Desafio 4:**

```bash
cd desafio4-microsservicos-independentes
docker compose up -d
curl http://localhost:5002/report
```

**Desafio 5:**

```bash
cd desafio5-api-gateway
docker compose up -d
curl http://localhost:8080/users/1/orders
```

## Conceitos Aprendidos

Ao longo dos 5 desafios, os seguintes conceitos foram explorados:

**Docker Fundamentals:**

- Containers e imagens
- Dockerfiles e multi-stage builds
- Redes Docker (bridge, custom networks)
- Volumes (named volumes, bind mounts)
- Port mapping e exposição de serviços

**Orquestração:**

- Docker Compose (version 3.8)
- Service dependencies (depends_on)
- Health checks
- Environment variables
- Restart policies

**Arquitetura de Microsserviços:**

- Separação de responsabilidades
- Comunicação via HTTP/REST
- API Gateway Pattern
- Service mesh
- Data aggregation
- Isolamento de serviços

**Boas Práticas:**

- Imagens otimizadas (Alpine Linux)
- Logs estruturados
- Tratamento de erros
- Health checks em cascata
- Scripts de automação
- Documentação clara

## Comandos Úteis

### Docker Basics

```bash
# Listar containers
docker ps -a

# Listar imagens
docker images

# Listar volumes
docker volume ls

# Listar redes
docker network ls

# Ver logs
docker logs <container-name>

# Inspecionar container
docker inspect <container-name>
```

### Docker Compose

```bash
# Iniciar serviços
docker compose up -d

# Ver logs
docker compose logs -f

# Parar serviços
docker compose down

# Rebuild e restart
docker compose up -d --build

# Ver status
docker compose ps
```

### Limpeza

```bash
# Remover containers parados
docker container prune

# Remover imagens não usadas
docker image prune

# Remover volumes não usados
docker volume prune

# Limpeza completa
docker system prune -a
```

## Troubleshooting

### Porta em uso

```powershell
# Windows
netstat -ano | findstr :<PORT>
taskkill /PID <PID> /F

# Linux
sudo lsof -i :<PORT>
sudo kill <PID>
```

### Container não inicia

```bash
# Ver logs detalhados
docker logs <container-name>

# Inspecionar container
docker inspect <container-name>
```

### Problemas de rede

```bash
# Verificar rede
docker network inspect <network-name>

# Testar conectividade
docker exec <container> ping <outro-container>
```

## Recursos Adicionais

- [Documentação Oficial Docker](https://docs.docker.com/)
- [Docker Compose Reference](https://docs.docker.com/compose/compose-file/)
- [Best Practices for Dockerfiles](https://docs.docker.com/develop/dev-best-practices/)
- [Microservices Architecture](https://microservices.io/)

## Licença

Este projeto é de uso acadêmico.

## Autor

**Vyktor Nascimento** - [GitHub](https://github.com/VyNas07)

---

**Repositório:** [projeto-docker-microsservicos](https://github.com/VyNas07/projeto-docker-microsservicos)

**Data de Conclusão:** Dezembro 2025
