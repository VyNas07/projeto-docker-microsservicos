# Desafio 2 - Volumes e Persistência

## Descrição

Demonstração de persistência de dados usando volumes Docker. Container PostgreSQL com dados que persistem após remoção e recriação do container.

### Objetivos

- Entender volumes Docker e persistência de dados
- Diferenciar volumes de bind mounts
- Comprovar que dados sobrevivem à remoção de containers
- Gerenciar dados em ambientes containerizados

## Arquitetura

```
┌─────────────────────────────────────────────────────┐
│              Rede Docker: desafio2-network          │
│                                                      │
│  ┌──────────────────────┐      ┌─────────────────┐│
│  │ Container: PostgreSQL│      │ Container: Client││
│  │  ┌────────────────┐  │      │  ┌────────────┐ ││
│  │  │  PostgreSQL 15 │  │◄─────┤  │ Python App │ ││
│  │  │  Porta: 5432   │  │      │  │  psycopg2  │ ││
│  │  └────────────────┘  │      │  └────────────┘ ││
│  │          │            │      │                  ││
│  └──────────┼────────────┘      └─────────────────┘│
│             │                                        │
│             ▼                                        │
│  ┌─────────────────────────────┐                   │
│  │ Volume: desafio2-postgres-data                  │
│  │ /var/lib/postgresql/data                        │
│  │ (Persistido no host)                            │
│  └─────────────────────────────┘                   │
└─────────────────────────────────────────────────────┘
```

### Volumes vs Bind Mounts

**Volumes Docker:**

- Gerenciados pelo Docker
- Armazenados em área específica do host
- Melhor performance
- Backup e migração facilitados
- Usado neste projeto

**Bind Mounts:**

- Caminho específico no host
- Dependente do sistema de arquivos
- Acesso direto aos arquivos
- Útil para desenvolvimento

## Estrutura

```
desafio2-volumes-persistencia/
├── README.md
├── database/
│   ├── Dockerfile           # PostgreSQL 15
│   ├── init.sql            # Script de inicialização
│   └── .env.example        # Variáveis de ambiente
├── client/
│   ├── Dockerfile          # Cliente Python
│   ├── query.py            # Script de consulta
│   └── requirements.txt    # Dependências
└── scripts/
    ├── setup.sh / .ps1     # Setup inicial
    ├── test-persistence.sh / .ps1  # Teste de persistência
    └── cleanup.sh / .ps1   # Limpeza
```

## Tecnologias

- Docker Volumes
- PostgreSQL 15
- Python 3.11
- psycopg2 (driver PostgreSQL)

## Como Executar

### Pré-requisitos

- Docker instalado
- Porta 5432 disponível

### Setup Inicial

Windows:

```powershell
.\scripts\setup.ps1
```

Linux/Mac:

```bash
chmod +x scripts/*.sh
./scripts/setup.sh
```

Este comando:

1. Cria volume nomeado `desafio2-postgres-data`
2. Cria rede `desafio2-network`
3. Constrói imagem PostgreSQL com dados iniciais
4. Inicia container PostgreSQL
5. Constrói imagem do cliente

### Consultar Dados

```bash
docker run --rm --network desafio2-network -e POSTGRES_HOST=desafio2-postgres desafio2-client
```

### Testar Persistência

Este é o comando principal que demonstra a persistência:

Windows:

```powershell
.\scripts\test-persistence.ps1
```

Linux/Mac:

```bash
./scripts/test-persistence.sh
```

O script:

1. Consulta dados antes da remoção
2. Para e remove o container PostgreSQL
3. Recria o container usando o mesmo volume
4. Consulta dados novamente
5. Comprova que os dados persistiram

### Limpar Recursos

```powershell
# Windows
.\scripts\cleanup.ps1

# Linux/Mac
./scripts/cleanup.sh
```

## Comandos Úteis

### Gerenciamento de Volumes

```bash
# Listar volumes
docker volume ls

# Inspecionar volume
docker volume inspect desafio2-postgres-data

# Ver localização no host
docker volume inspect desafio2-postgres-data -f '{{.Mountpoint}}'

# Remover volume (quando não estiver em uso)
docker volume rm desafio2-postgres-data
```

### Consultas Diretas ao Banco

```bash
# Conectar ao PostgreSQL via psql
docker exec -it desafio2-postgres psql -U postgres -d desafio2

# Dentro do psql:
# \dt              - listar tabelas
# SELECT * FROM produtos;
# SELECT COUNT(*) FROM produtos;
# \q               - sair
```

### Logs e Debug

```bash
# Ver logs do PostgreSQL
docker logs desafio2-postgres

# Ver logs em tempo real
docker logs -f desafio2-postgres

# Verificar status do container
docker ps -a | grep desafio2
```

## Exemplo de Saída

Após executar o teste de persistência, você verá:

```
==========================================
TESTE DE PERSISTENCIA
==========================================

[1/5] Consultando dados antes da remocao...
====================================================================================================
ID    NOME                      PRECO        ESTOQUE    DATA CADASTRO       
====================================================================================================
1     Notebook Dell             R$  3499.99  15         2025-12-01 10:30:00
2     Mouse Logitech            R$   349.90  50         2025-12-01 10:30:00
...

[2/5] Parando e removendo container do banco...
Container removido!

[4/5] Recriando container com o mesmo volume...
Container recriado!

[5/5] Consultando dados apos recriacao...
====================================================================================================
ID    NOME                      PRECO        ESTOQUE    DATA CADASTRO       
====================================================================================================
1     Notebook Dell             R$  3499.99  15         2025-12-01 10:30:00
2     Mouse Logitech            R$   349.90  50         2025-12-01 10:30:00
...

Os dados foram mantidos mesmo apos remover e recriar o container!
```

## Detalhes Técnicos

### Volume Docker

O volume é montado em `/var/lib/postgresql/data` dentro do container, que é o diretório padrão onde PostgreSQL armazena seus dados.

```bash
docker run -v desafio2-postgres-data:/var/lib/postgresql/data postgres:15
```

### Script de Inicialização

O arquivo `init.sql` é executado automaticamente na primeira inicialização através do mecanismo do `docker-entrypoint-initdb.d/`.

### Persistência Garantida

Mesmo após:

- Parar o container
- Remover o container
- Recriar o container

Os dados permanecem porque estão armazenados no volume, não no container.

## Boas Práticas

- Usar volumes nomeados para produção
- Nunca armazenar dados críticos apenas no container
- Fazer backup regular dos volumes
- Usar variáveis de ambiente para credenciais
- Documentar estrutura do banco de dados

## Troubleshooting

### Porta 5432 em uso

```bash
# Windows
netstat -ano | findstr :5432
taskkill /PID <PID> /F

# Linux
sudo lsof -i :5432
sudo kill <PID>
```

### Container não inicia

```bash
# Ver logs detalhados
docker logs desafio2-postgres

# Verificar volume
docker volume inspect desafio2-postgres-data
```

### Dados não persistem

```bash
# Verificar se o volume está montado corretamente
docker inspect desafio2-postgres -f '{{json .Mounts}}'
```

## Pontuação

| Critério | Pontos |
|----------|--------|
| Uso correto de volumes | 5 |
| Persistência comprovada | 5 |
| Documentação clara | 5 |
| Organização do código | 5 |
| **TOTAL** | **20** |

## Autor

VyNas07 - [GitHub](https://github.com/VyNas07)
