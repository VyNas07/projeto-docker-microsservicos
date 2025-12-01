-- Script de inicialização do banco de dados
-- Cria tabela users e insere dados de exemplo

\c desafio3;

-- Cria tabela de usuários
CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    email VARCHAR(100) NOT NULL UNIQUE,
    full_name VARCHAR(100),
    department VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Insere usuários de exemplo
INSERT INTO
    users (
        username,
        email,
        full_name,
        department
    )
VALUES (
        'jsilva',
        'joao.silva@empresa.com',
        'João Silva',
        'Desenvolvimento'
    ),
    (
        'mcoста',
        'maria.costa@empresa.com',
        'Maria Costa',
        'Design'
    ),
    (
        'psantos',
        'pedro.santos@empresa.com',
        'Pedro Santos',
        'DevOps'
    ),
    (
        'aolive',
        'ana.oliveira@empresa.com',
        'Ana Oliveira',
        'QA'
    ),
    (
        'rlima',
        'ricardo.lima@empresa.com',
        'Ricardo Lima',
        'Desenvolvimento'
    ),
    (
        'cferr',
        'carla.ferreira@empresa.com',
        'Carla Ferreira',
        'Produto'
    ),
    (
        'lmartins',
        'lucas.martins@empresa.com',
        'Lucas Martins',
        'Segurança'
    ),
    (
        'jrodrig',
        'julia.rodrigues@empresa.com',
        'Julia Rodrigues',
        'Design'
    ),
    (
        'falves',
        'felipe.alves@empresa.com',
        'Felipe Alves',
        'DevOps'
    ),
    (
        'bcarvalho',
        'beatriz.carvalho@empresa.com',
        'Beatriz Carvalho',
        'Desenvolvimento'
    );

-- Exibe contagem
SELECT COUNT(*) as total_users FROM users;

-- Configura permissões
GRANT ALL PRIVILEGES ON DATABASE desafio3 TO postgres;

GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO postgres;

GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO postgres;