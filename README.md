# 🐳 Projeto Docker e Microsserviços

[![Docker](https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white)](https://www.docker.com/)
[![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-000000?style=for-the-badge&logo=flask&logoColor=white)](https://flask.palletsprojects.com/)

## 📋 Sobre o Projeto

Projeto acadêmico completo sobre **Docker e Microsserviços**, desenvolvido através de 5 desafios progressivos que demonstram conceitos fundamentais e avançados de containerização, orquestração e arquitetura de microsserviços.

### 🎯 Objetivos do Projeto

- Dominar conceitos de containerização com Docker
- Implementar comunicação entre microsserviços
- Aplicar boas práticas de desenvolvimento e DevOps
- Criar documentação técnica de qualidade
- Desenvolver soluções escaláveis e resilientes

## 🏆 Estrutura dos Desafios

### ✅ Desafio 1: Containers em Rede (20 pontos)

**Status**: Completo

Demonstra comunicação básica entre containers Docker através de uma rede customizada.

**Tecnologias**: Docker Networks, Python, Flask, Requests

**Conceitos**:

- Redes Docker customizadas
- DNS interno do Docker
- Port mapping
- HTTP client/server

📁 [Ver Desafio 1](./desafio1-containers-rede/)

---

### 🔄 Desafio 2: Docker Compose Multi-Container (20 pontos)

**Status**: Em desenvolvimento

Aplicação multi-container com banco de dados e interface web.

**Tecnologias**: Docker Compose, PostgreSQL, React, Node.js

**Conceitos**:

- Orquestração de múltiplos containers
- Volumes persistentes
- Variáveis de ambiente
- Dependências entre serviços

---

### 🚀 Desafio 3: API RESTful com Microsserviços (20 pontos)

**Status**: Planejado

Sistema de microsserviços com API Gateway e serviços independentes.

**Tecnologias**: FastAPI, Redis, MongoDB, Nginx

**Conceitos**:

- Arquitetura de microsserviços
- API Gateway
- Cache distribuído
- Service discovery

---

### 📊 Desafio 4: Monitoramento e Logs (20 pontos)

**Status**: Planejado

Implementação de stack completa de observabilidade.

**Tecnologias**: Prometheus, Grafana, ELK Stack, Jaeger

**Conceitos**:

- Métricas e alertas
- Agregação de logs
- Distributed tracing
- Dashboards de monitoramento

---

### 🔧 Desafio 5: CI/CD e Deploy (20 pontos)

**Status**: Planejado

Pipeline completo de integração e deploy contínuo.

**Tecnologias**: GitHub Actions, Docker Hub, Kubernetes (opcional)

**Conceitos**:

- Continuous Integration
- Continuous Deployment
- Automated testing
- Container registry

---

## 📊 Critérios de Avaliação

Cada desafio é avaliado com base em:

| Critério | Peso | Descrição |
|----------|------|-----------|
| 🔧 **Funcionamento Técnico** | 40% | Código funcional, sem bugs, atende requisitos |
| 📝 **Documentação** | 30% | README claro, explicações detalhadas |
| 📁 **Organização** | 20% | Estrutura de pastas, boas práticas, código limpo |
| ✨ **Originalidade** | 10% | Funcionalidades extras, criatividade |

## 🚀 Como Começar

### Pré-requisitos

- Docker Desktop instalado ([Download](https://www.docker.com/products/docker-desktop))
- Git ([Download](https://git-scm.com/downloads))
- Editor de código (recomendado: VS Code)

### Instalação

```bash
# Clonar o repositório
git clone https://github.com/VyNas07/projeto-docker-microsservicos.git

# Entrar no diretório
cd projeto-docker-microsservicos

# Navegar para o desafio desejado
cd desafio1-containers-rede
```

### Verificar Instalação do Docker

```powershell
# Verificar versão do Docker
docker --version

# Verificar se Docker está rodando
docker ps

# Verificar Docker Compose
docker-compose --version
```

## 📚 Recursos e Referências

### Documentação Oficial

- [Docker Documentation](https://docs.docker.com/)
- [Docker Compose Documentation](https://docs.docker.com/compose/)
- [Docker Best Practices](https://docs.docker.com/develop/dev-best-practices/)

### Tutoriais Recomendados

- [Docker Getting Started](https://docs.docker.com/get-started/)
- [Docker Networking Tutorial](https://docs.docker.com/network/network-tutorial-standalone/)
- [Dockerfile Best Practices](https://docs.docker.com/develop/develop-images/dockerfile_best-practices/)

### Ferramentas Úteis

- [Docker Hub](https://hub.docker.com/) - Registry de imagens
- [Play with Docker](https://labs.play-with-docker.com/) - Ambiente de testes online
- [Docker Desktop Dashboard](https://docs.docker.com/desktop/dashboard/) - Interface gráfica

## 🛠️ Tecnologias Utilizadas

### Core

- **Docker** - Containerização
- **Docker Compose** - Orquestração
- **Python 3.11** - Linguagem principal

### Backend

- **Flask** - Framework web leve
- **FastAPI** - Framework web moderno (desafios futuros)
- **PostgreSQL** - Banco de dados relacional (desafios futuros)
- **Redis** - Cache e message broker (desafios futuros)

### DevOps

- **Git** - Controle de versão
- **GitHub Actions** - CI/CD (desafios futuros)
- **Prometheus** - Métricas (desafios futuros)
- **Grafana** - Visualização (desafios futuros)

## 📁 Estrutura do Repositório

```
projeto-docker-microsservicos/
├── README.md                          # Este arquivo
├── .gitignore                         # Arquivos ignorados pelo Git
├── desafio1-containers-rede/         # ✅ Desafio 1 completo
│   ├── README.md
│   ├── servidor/
│   ├── cliente/
│   └── scripts/
├── desafio2-docker-compose/          # 🔄 Em desenvolvimento
├── desafio3-microsservicos-api/      # 📋 Planejado
├── desafio4-monitoramento/           # 📋 Planejado
└── desafio5-cicd-deploy/             # 📋 Planejado
```

## 🤝 Como Contribuir

Este é um projeto acadêmico, mas sugestões são bem-vindas!

1. Fork o projeto
2. Crie uma branch para sua feature (`git checkout -b feature/MinhaFeature`)
3. Commit suas mudanças (`git commit -m 'Adiciona MinhaFeature'`)
4. Push para a branch (`git push origin feature/MinhaFeature`)
5. Abra um Pull Request

## 📝 Licença

Este projeto é desenvolvido para fins acadêmicos.

## 👨‍💻 Autor

**VyNas07**

- GitHub: [@VyNas07](https://github.com/VyNas07)
- Projeto: [projeto-docker-microsservicos](https://github.com/VyNas07/projeto-docker-microsservicos)

## 🙏 Agradecimentos

- Comunidade Docker pela excelente documentação
- Professores e colegas pelo suporte
- Todos os recursos open-source utilizados

---

## 📈 Progresso do Projeto

```
Desafio 1: ████████████████████ 100% ✅
Desafio 2: ░░░░░░░░░░░░░░░░░░░░   0% 🔄
Desafio 3: ░░░░░░░░░░░░░░░░░░░░   0% 📋
Desafio 4: ░░░░░░░░░░░░░░░░░░░░   0% 📋
Desafio 5: ░░░░░░░░░░░░░░░░░░░░   0% 📋
```

**Pontuação Total**: 20/100 pontos

---

<div align="center">

**🐳 Desenvolvido com Docker e ❤️**

[⬆ Voltar ao topo](#-projeto-docker-e-microsserviços)

</div>
