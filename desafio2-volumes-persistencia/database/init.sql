-- Script de inicialização do banco de dados
-- Cria tabela de produtos e insere dados de exemplo

-- Conecta ao banco de dados desafio2
\c desafio2;

-- Cria tabela de produtos
CREATE TABLE IF NOT EXISTS produtos (
    id SERIAL PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    descricao TEXT,
    preco DECIMAL(10, 2) NOT NULL,
    estoque INTEGER DEFAULT 0,
    data_cadastro TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Insere dados de exemplo
INSERT INTO produtos (nome, descricao, preco, estoque) VALUES
    ('Notebook Dell', 'Notebook Dell Inspiron 15, Intel Core i5, 8GB RAM, 256GB SSD', 3499.99, 15),
    ('Mouse Logitech', 'Mouse sem fio Logitech MX Master 3', 349.90, 50),
    ('Teclado Mecânico', 'Teclado mecânico RGB, switches blue', 299.00, 30),
    ('Monitor LG 24"', 'Monitor LG 24 polegadas Full HD IPS', 899.00, 20),
    ('Webcam Logitech', 'Webcam Logitech C920 Full HD 1080p', 449.90, 25),
    ('Headset Gamer', 'Headset gamer com microfone, RGB, som surround', 249.90, 40),
    ('SSD Kingston 480GB', 'SSD SATA III 480GB Kingston A400', 279.00, 60),
    ('Memória RAM 16GB', 'Memória RAM DDR4 16GB 3200MHz', 389.90, 35),
    ('HD Externo 1TB', 'HD Externo portátil 1TB USB 3.0', 349.00, 45),
    ('Cadeira Gamer', 'Cadeira gamer ergonômica com apoio lombar', 899.00, 12);

-- Exibe contagem de registros inseridos
SELECT COUNT(*) as total_produtos FROM produtos;

-- Exibe alguns produtos
SELECT id, nome, preco FROM produtos LIMIT 5;

GRANT ALL PRIVILEGES ON DATABASE desafio2 TO postgres;
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO postgres;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO postgres;
