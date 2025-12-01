"""
Cliente Python para consultar dados no PostgreSQL
Demonstra que os dados persistem após recriação do container
"""

import psycopg2
import os
import sys
from datetime import datetime
from colorama import Fore, Style, init

# Inicializa colorama
init(autoreset=True)

# Configurações de conexão
DB_CONFIG = {
    'host': os.getenv('POSTGRES_HOST', 'postgres-db'),
    'port': os.getenv('POSTGRES_PORT', '5432'),
    'database': os.getenv('POSTGRES_DB', 'desafio2'),
    'user': os.getenv('POSTGRES_USER', 'postgres'),
    'password': os.getenv('POSTGRES_PASSWORD', 'postgres123')
}

def conectar_banco():
    """Estabelece conexão com o banco de dados"""
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        print(f"{Fore.GREEN}Conexao estabelecida com sucesso!{Style.RESET_ALL}")
        return conn
    except psycopg2.OperationalError as e:
        print(f"{Fore.RED}Erro ao conectar ao banco: {e}{Style.RESET_ALL}")
        sys.exit(1)

def listar_produtos(conn):
    """Lista todos os produtos do banco"""
    cursor = conn.cursor()
    
    try:
        # Busca todos os produtos
        cursor.execute("""
            SELECT id, nome, descricao, preco, estoque, data_cadastro 
            FROM produtos 
            ORDER BY id
        """)
        
        produtos = cursor.fetchall()
        
        if not produtos:
            print(f"{Fore.YELLOW}Nenhum produto encontrado no banco.{Style.RESET_ALL}")
            return
        
        # Exibe cabeçalho
        print(f"\n{Fore.CYAN}{'='*100}")
        print(f"{'ID':<5} {'NOME':<25} {'PRECO':<12} {'ESTOQUE':<10} {'DATA CADASTRO':<20}")
        print(f"{'='*100}{Style.RESET_ALL}")
        
        # Exibe produtos
        for produto in produtos:
            id_prod, nome, descricao, preco, estoque, data = produto
            data_str = data.strftime('%Y-%m-%d %H:%M:%S') if data else 'N/A'
            print(f"{id_prod:<5} {nome:<25} R$ {preco:>8.2f}  {estoque:<10} {data_str:<20}")
        
        print(f"{Fore.CYAN}{'='*100}{Style.RESET_ALL}\n")
        
        # Exibe estatísticas
        cursor.execute("SELECT COUNT(*), SUM(estoque), SUM(preco * estoque) FROM produtos")
        total, total_estoque, valor_total = cursor.fetchone()
        
        print(f"{Fore.MAGENTA}ESTATISTICAS:{Style.RESET_ALL}")
        print(f"  Total de produtos: {total}")
        print(f"  Total em estoque: {total_estoque} unidades")
        print(f"  Valor total em estoque: R$ {valor_total:.2f}\n")
        
    except psycopg2.Error as e:
        print(f"{Fore.RED}Erro ao consultar produtos: {e}{Style.RESET_ALL}")
    finally:
        cursor.close()

def verificar_persistencia(conn):
    """Verifica informações sobre a persistência dos dados"""
    cursor = conn.cursor()
    
    try:
        # Verifica data do registro mais antigo
        cursor.execute("SELECT MIN(data_cadastro) FROM produtos")
        data_mais_antiga = cursor.fetchone()[0]
        
        if data_mais_antiga:
            print(f"{Fore.GREEN}VERIFICACAO DE PERSISTENCIA:{Style.RESET_ALL}")
            print(f"  Data do registro mais antigo: {data_mais_antiga}")
            print(f"  Data/hora atual: {datetime.now()}")
            
            idade = datetime.now() - data_mais_antiga.replace(tzinfo=None)
            print(f"  Idade dos dados: {idade}")
            print(f"\n{Fore.GREEN}Os dados estao persistindo corretamente no volume Docker!{Style.RESET_ALL}\n")
        
    except psycopg2.Error as e:
        print(f"{Fore.RED}Erro ao verificar persistencia: {e}{Style.RESET_ALL}")
    finally:
        cursor.close()

def main():
    """Função principal"""
    print(f"\n{Fore.CYAN}{'='*100}")
    print(f"CLIENTE DE CONSULTA - DESAFIO 2: VOLUMES E PERSISTENCIA")
    print(f"{'='*100}{Style.RESET_ALL}\n")
    
    print(f"Conectando ao banco de dados...")
    print(f"  Host: {DB_CONFIG['host']}")
    print(f"  Database: {DB_CONFIG['database']}")
    print(f"  User: {DB_CONFIG['user']}\n")
    
    # Conecta ao banco
    conn = conectar_banco()
    
    # Lista produtos
    listar_produtos(conn)
    
    # Verifica persistência
    verificar_persistencia(conn)
    
    # Fecha conexão
    conn.close()
    print(f"{Fore.GREEN}Conexao fechada.{Style.RESET_ALL}\n")

if __name__ == "__main__":
    main()
