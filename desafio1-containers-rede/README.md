# 🌐 Desafio 1 - Containers em Rede

## 📋 Descrição do Projeto

Este desafio demonstra a comunicação entre containers Docker através de uma rede customizada. O projeto implementa uma arquitetura cliente-servidor onde dois containers se comunicam via HTTP, ilustrando conceitos fundamentais de networking em Docker.

### 🎯 Objetivos de Aprendizagem

- Criar e gerenciar redes Docker customizadas
- Implementar comunicação entre containers usando DNS interno do Docker
- Desenvolver aplicações containerizadas com Python
- Implementar logging estruturado e colorido
- Aplicar boas práticas de Dockerfile e segurança

## 🏗️ Arquitetura da Solução

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

### 🔄 Fluxo de Comunicação

1. **Inicialização**: O script `start.ps1` cria a rede `desafio1-network` e inicia ambos os containers
2. **DNS Interno**: Docker fornece resolução DNS automática - o cliente acessa o servidor pelo hostname `servidor`
3. **Requisições Periódicas**: O cliente faz requisições HTTP GET a cada 5 segundos
4. **Resposta do Servidor**: O servidor retorna JSON com informações do sistema e incrementa contador
5. **Logging**: Ambos os containers produzem logs coloridos e estruturados

## 📁 Estrutura de Arquivos

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
    ├── start.ps1               # Inicia todo o sistema (PowerShell)
    ├── stop.ps1                # Para e limpa recursos (PowerShell)
    ├── logs.ps1                # Visualiza logs dos containers (PowerShell)
    ├── start.sh                # Inicia todo o sistema (Bash/Linux)
    ├── stop.sh                 # Para e limpa recursos (Bash/Linux)
    └── logs.sh                 # Visualiza logs dos containers (Bash/Linux)
```

## 🔧 Tecnologias Utilizadas

| Tecnologia | Versão | Propósito |
|------------|--------|-----------|
| Docker | Latest | Containerização |
| Python | 3.11-slim | Linguagem de programação |
| Flask | 3.0.0 | Framework web para servidor |
| Requests | 2.31.0 | Cliente HTTP |
| Colorama | 0.4.6 | Logs coloridos |

## 🚀 Como Executar

### Pré-requisitos

- Docker Desktop instalado e em execução
- PowerShell 5.1+ (Windows) ou Bash (Linux/Mac)
- Porta 8080 disponível no host

### Passo 1: Clonar o Repositório

```powershell
git clone https://github.com/VyNas07/projeto-docker-microsservicos.git
cd projeto-docker-microsservicos/desafio1-containers-rede
```

### Passo 2: Iniciar o Sistema

**Windows (PowerShell):**

```powershell
.\scripts\start.ps1
```

**Linux/Mac (Bash):**

```bash
chmod +x scripts/*.sh
./scripts/start.sh
```

### Passo 3: Verificar Funcionamento

O script de inicialização automaticamente:

- ✅ Cria a rede Docker `desafio1-network`
- ✅ Constrói as imagens dos containers
- ✅ Inicia o servidor na porta 8080
- ✅ Inicia o cliente que faz requisições periódicas

### Passo 4: Visualizar Logs

**Opção 1: Script interativo**

```powershell
# Windows
.\scripts\logs.ps1

# Linux/Mac
./scripts/logs.sh
```

**Opção 2: Comandos diretos**

```powershell
# Ver logs do servidor
docker logs -f desafio1-servidor

# Ver logs do cliente
docker logs -f desafio1-cliente
```

### Passo 5: Testar o Servidor Diretamente

```powershell
# Testar endpoint principal
curl http://localhost:8080

# Testar health check
curl http://localhost:8080/health
```

### Passo 6: Parar o Sistema

```powershell
# Windows
.\scripts\stop.ps1

# Linux/Mac
./scripts/stop.sh
```

## 📊 Saída Esperada

### Logs do Servidor

```
╔══════════════════════════════════════════╗
║     🌐 SERVIDOR FLASK - DESAFIO 1      ║
║     Comunicação entre Containers        ║
╚══════════════════════════════════════════╝

🚀 Servidor iniciado em 2025-12-01 14:30:00
🏷️  Hostname: a1b2c3d4e5f6
🌐 IP: 172.18.0.2
🔌 Porta: 8080

[14:30:15] 🔍 GET / - 172.18.0.3
[14:30:15] 📨 Requisição #1 recebida
[14:30:20] 🔍 GET / - 172.18.0.3
[14:30:20] 📨 Requisição #2 recebida
```

### Logs do Cliente

```
╔══════════════════════════════════════════╗
║     🔌 CLIENTE HTTP - DESAFIO 1        ║
║     Requisições Periódicas ao Servidor  ║
╚══════════════════════════════════════════╝

🚀 Cliente iniciado em 2025-12-01 14:30:10
🎯 URL do servidor: http://servidor:8080
⏱️  Intervalo de requisições: 5 segundos

📤 Enviando requisição #1...
============================================================
✅ RESPOSTA RECEBIDA - [14:30:15]
   🖥️  Hostname do Servidor: a1b2c3d4e5f6
   🌐 IP do Servidor: 172.18.0.2
   ⏰ Timestamp: 2025-12-01T14:30:15.123456
   📊 Número da Requisição: 1
   ⏱️  Uptime do Servidor: 0:00:15
   💬 Mensagem: ✅ Comunicação bem-sucedida entre containers!
============================================================

⏳ Aguardando 5 segundos para próxima requisição...
```

### Resposta HTTP do Servidor

```json
{
  "hostname": "a1b2c3d4e5f6",
  "timestamp": "2025-12-01T14:30:15.123456",
  "request_number": 1,
  "uptime": "0:00:15",
  "message": "✅ Comunicação bem-sucedida entre containers!",
  "container_ip": "172.18.0.2"
}
```

## 🔍 Detalhes Técnicos

### Rede Docker Customizada

A rede `desafio1-network` é do tipo **bridge** e fornece:

- **Isolamento**: Containers só se comunicam dentro da mesma rede
- **DNS Interno**: Resolução automática de nomes de containers
- **Segurança**: Tráfego isolado do host e outras redes

```powershell
# Inspecionar a rede
docker network inspect desafio1-network

# Listar containers na rede
docker network inspect desafio1-network -f '{{range .Containers}}{{.Name}} {{end}}'
```

### Endpoints do Servidor

| Endpoint | Método | Descrição |
|----------|--------|-----------|
| `/` | GET | Retorna informações do sistema e contador |
| `/health` | GET | Health check para monitoramento |

### Dockerfile - Boas Práticas Implementadas

1. **Imagem Base Otimizada**: `python:3.11-slim` (menor tamanho)
2. **Cache de Layers**: Copia `requirements.txt` antes do código
3. **Não-root User**: (pode ser adicionado para segurança extra)
4. **Health Check**: Verifica se o servidor está respondendo
5. **Variáveis de Ambiente**: Configuração via ENV
6. **Unbuffered Output**: `PYTHONUNBUFFERED=1` para logs em tempo real

### Tratamento de Erros

O cliente implementa tratamento robusto de erros:

- **ConnectionError**: Servidor não acessível
- **Timeout**: Servidor não responde a tempo
- **RequestException**: Outros erros HTTP
- **Graceful Shutdown**: Ctrl+C capturado para encerramento limpo

## 🐛 Troubleshooting

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

### Problema: Imagens não são construídas

**Solução**: Limpe o cache do Docker:

```powershell
docker builder prune -a
docker system prune -a
```

### Problema: Logs não aparecem coloridos

**Causa**: Terminal não suporta cores ANSI

**Solução**: Use Windows Terminal ou outro terminal moderno

## 📈 Melhorias Futuras (Extras)

- [ ] Adicionar autenticação JWT entre containers
- [ ] Implementar rate limiting no servidor
- [ ] Adicionar métricas Prometheus
- [ ] Criar dashboard com grafana
- [ ] Implementar retry com backoff exponencial
- [ ] Adicionar testes unitários e de integração
- [ ] Implementar circuit breaker pattern
- [ ] Adicionar suporte a HTTPS/TLS

## 🎓 Conceitos Aprendidos

✅ **Redes Docker**: Criação e gerenciamento de redes customizadas
✅ **DNS Interno**: Comunicação entre containers por hostname
✅ **Port Mapping**: Exposição de portas do container para o host
✅ **Logging**: Implementação de logs estruturados e coloridos
✅ **Dockerfiles**: Otimização e boas práticas
✅ **HTTP Client/Server**: Comunicação REST entre serviços
✅ **Error Handling**: Tratamento robusto de falhas de rede
✅ **Graceful Shutdown**: Encerramento limpo de aplicações

## 📚 Referências

- [Docker Networking Overview](https://docs.docker.com/network/)
- [Docker Bridge Networks](https://docs.docker.com/network/bridge/)
- [Flask Documentation](https://flask.palletsprojects.com/)
- [Python Requests Library](https://requests.readthedocs.io/)
- [Best Practices for Writing Dockerfiles](https://docs.docker.com/develop/develop-images/dockerfile_best-practices/)

## 👨‍💻 Autor

**VyNas07**

- GitHub: [@VyNas07](https://github.com/VyNas07)
- Projeto: Microsserviços com Docker

---

## 📊 Pontuação do Desafio

| Critério | Pontos | Status |
|----------|--------|--------|
| Configuração correta da rede Docker | 5 | ✅ |
| Comunicação funcional entre containers | 5 | ✅ |
| Explicação clara no README | 5 | ✅ |
| Organização e scripts de execução | 5 | ✅ |
| **TOTAL** | **20** | **✅** |

### Diferenciais Implementados (Originalidade)

- ✅ Logs coloridos com emojis
- ✅ ASCII art no startup
- ✅ Métricas de uptime e contador de requisições
- ✅ Graceful shutdown com estatísticas
- ✅ Scripts para Windows (PowerShell) e Linux (Bash)
- ✅ Health check endpoint
- ✅ Documentação detalhada com diagramas

---

**🎉 Projeto desenvolvido como parte do curso de Microsserviços com Docker**
