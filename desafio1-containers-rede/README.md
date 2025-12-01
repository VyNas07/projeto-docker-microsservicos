# Desafio 1 - Containers em Rede

## Descrição

Demonstração de comunicação entre containers Docker através de rede customizada. Arquitetura cliente-servidor com dois containers comunicando via HTTP.

### Objetivos

- Criar e gerenciar redes Docker customizadas
- Implementar comunicação entre containers usando DNS interno
- Desenvolver aplicações containerizadas com Python
- Aplicar boas práticas de Dockerfile

## Arquitetura

```
┌─────────────────────────────────────────────────────────┐
│              Rede Docker: desafio1-network              │
│                     (Bridge Network)                     │
│                                                          │
│  ┌──────────────────────┐      ┌───────────────────┐   │
│  │  Container: Servidor │      │ Container: Cliente│   │
│  │  ┌────────────────┐  │      │  ┌──────────────┐ │   │
│  │  │  Flask App     │  │◄─────┤  │ HTTP Client  │ │   │
│  │  │  (Python)      │  │ HTTP │  │  (Python)    │ │   │
│  │  │  Porta: 8080   │  │      │  │  Req/5s      │ │   │
│  │  └────────────────┘  │      │  └──────────────┘ │   │
│  │  hostname: servidor  │      │  hostname: cliente│   │
│  └──────────────────────┘      └───────────────────┘   │
│           │                                              │
│           │                                              │
└───────────┼──────────────────────────────────────────────┘
            │
            │ Port Mapping
            ▼
     Host: localhost:8080
```

### Fluxo de Comunicação

1. Script cria a rede `desafio1-network` e inicia containers
2. Docker fornece DNS automático - cliente acessa servidor por hostname
3. Cliente faz requisições HTTP GET a cada 5 segundos
4. Servidor retorna JSON com informações do sistema
5. Logs coloridos são produzidos por ambos os containers

## Estrutura de Arquivos

```
desafio1-containers-rede/
├── README.md                    # Este arquivo
├── servidor/
│   ├── Dockerfile              # Imagem Docker do servidor Flask
│   ├── app.py                  # Aplicação Flask com endpoints REST
│   └── requirements.txt        # Dependências Python (Flask, colorama)
├── cliente/
│   ├── Dockerfile              # Imagem Docker do cliente HTTP
│   ├── client.py               # Cliente que faz requisições periódicas
│   └── requirements.txt        # Dependências Python (requests, colorama)
└── scripts/
    ├── start.ps1 / start.sh    # Inicia o sistema
    ├── stop.ps1 / stop.sh      # Para e limpa recursos
    └── logs.ps1 / logs.sh      # Visualiza logs
```

## Tecnologias

- Docker
- Python 3.11
- Flask 3.0.0
- Requests 2.31.0
- Colorama 0.4.6

## Como Executar

### Pré-requisitos

- Docker Desktop instalado
- PowerShell (Windows) ou Bash (Linux/Mac)
- Porta 8080 disponível

### Iniciar

Windows:

```powershell
.\scripts\start.ps1
```

Linux/Mac:

```bash
chmod +x scripts/*.sh
./scripts/start.sh
```

### Visualizar Logs

```powershell
# Windows
.\scripts\logs.ps1

# Linux/Mac  
./scripts/logs.sh
```

Ou diretamente:

```bash
docker logs -f desafio1-servidor
docker logs -f desafio1-cliente
```

### Testar

```bash
curl http://localhost:8080
curl http://localhost:8080/health
```

### Parar

```powershell
# Windows
.\scripts\stop.ps1

# Linux/Mac
./scripts/stop.sh
```

## Exemplo de Saída

Resposta JSON do servidor:

```json
{
  "hostname": "a1b2c3d4e5f6",
  "timestamp": "2025-12-01T14:30:15.123456",
  "request_number": 1,
  "uptime": "0:00:15",
  "message": "Comunicacao bem-sucedida entre containers!",
  "container_ip": "172.18.0.2"
}
```

## Detalhes Técnicos

### Rede Docker

Tipo: Bridge network (`desafio1-network`)

- Isolamento entre containers
- DNS interno automático
- Tráfego isolado do host

### Endpoints

| Endpoint | Método | Descrição |
|----------|--------|-----------|
| `/` | GET | Informações do sistema |
| `/health` | GET | Health check |

### Boas Práticas

- Imagem base slim (menor tamanho)
- Cache de layers otimizado
- Health check configurado
- Output unbuffered para logs
- Tratamento de erros robusto

## Troubleshooting

### Problema: Porta 8080 já está em uso

**Solução**: Pare o processo que está usando a porta ou mude a porta no script:

```powershell
# Descobrir o processo
netstat -ano | findstr :8080

# Parar o processo (substitua PID)
taskkill /PID <PID> /F
```

### Problema: Cliente não consegue conectar ao servidor

**Verificações**:

```powershell
# 1. Verificar se ambos estão na mesma rede
docker inspect desafio1-servidor -f '{{.NetworkSettings.Networks}}'
docker inspect desafio1-cliente -f '{{.NetworkSettings.Networks}}'

# 2. Testar conectividade
docker exec desafio1-cliente ping servidor

# 3. Verificar se servidor está escutando
docker exec desafio1-servidor netstat -tlnp | grep 8080
```

### Imagens não constroem

Limpe o cache:

```bash
docker builder prune -a
```

## Pontuação

| Critério | Pontos |
|----------|--------|
| Configuração da rede | 5 |
| Comunicação entre containers | 5 |
| Documentação | 5 |
| Organização e scripts | 5 |
| **TOTAL** | **20** |

## Autor

VyNas07 - [GitHub](https://github.com/VyNas07)
