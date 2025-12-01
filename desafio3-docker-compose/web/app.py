"""
API Flask para Desafio 3 - Docker Compose
Demonstra comunicação entre serviços: Web, PostgreSQL e Redis
"""

from flask import Flask, jsonify, request
import psycopg2
import redis
import os
import json
from datetime import datetime
from colorama import Fore, Style, init

# Inicializa colorama e Flask
init(autoreset=True)
app = Flask(__name__)

# Configurações
DB_CONFIG = {
    'host': os.getenv('POSTGRES_HOST', 'db'),
    'database': os.getenv('POSTGRES_DB', 'desafio3'),
    'user': os.getenv('POSTGRES_USER', 'postgres'),
    'password': os.getenv('POSTGRES_PASSWORD', 'postgres123')
}

REDIS_CONFIG = {
    'host': os.getenv('REDIS_HOST', 'cache'),
    'port': int(os.getenv('REDIS_PORT', 6379)),
    'decode_responses': True
}

# Conexões globais
db_conn = None
redis_client = None

def get_db_connection():
    """Obtém conexão com PostgreSQL"""
    global db_conn
    try:
        if db_conn is None or db_conn.closed:
            db_conn = psycopg2.connect(**DB_CONFIG)
            print(f"{Fore.GREEN}[DB] Conectado ao PostgreSQL{Style.RESET_ALL}")
        return db_conn
    except psycopg2.Error as e:
        print(f"{Fore.RED}[DB] Erro ao conectar: {e}{Style.RESET_ALL}")
        return None

def get_redis_connection():
    """Obtém conexão com Redis"""
    global redis_client
    try:
        if redis_client is None:
            redis_client = redis.Redis(**REDIS_CONFIG)
            redis_client.ping()
            print(f"{Fore.GREEN}[CACHE] Conectado ao Redis{Style.RESET_ALL}")
        return redis_client
    except redis.RedisError as e:
        print(f"{Fore.RED}[CACHE] Erro ao conectar: {e}{Style.RESET_ALL}")
        return None

@app.route('/')
def home():
    """Endpoint raiz com informações gerais"""
    print(f"{Fore.CYAN}[WEB] Requisição em /{Style.RESET_ALL}")
    
    return jsonify({
        'service': 'Desafio 3 - Docker Compose',
        'version': '1.0',
        'timestamp': datetime.now().isoformat(),
        'endpoints': {
            'info': '/',
            'users': '/users',
            'cache_set': '/cache (POST)',
            'cache_get': '/cache/<key>',
            'health': '/health'
        },
        'services': {
            'web': 'Flask API',
            'db': 'PostgreSQL 15',
            'cache': 'Redis 7'
        }
    }), 200

@app.route('/users')
def get_users():
    """Lista todos os usuários do PostgreSQL"""
    print(f"{Fore.CYAN}[WEB] Requisição em /users{Style.RESET_ALL}")
    
    conn = get_db_connection()
    if not conn:
        return jsonify({'error': 'Database connection failed'}), 503
    
    try:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT id, username, email, full_name, department, created_at 
            FROM users 
            ORDER BY id
        """)
        
        users = []
        for row in cursor.fetchall():
            users.append({
                'id': row[0],
                'username': row[1],
                'email': row[2],
                'full_name': row[3],
                'department': row[4],
                'created_at': row[5].isoformat() if row[5] else None
            })
        
        cursor.close()
        print(f"{Fore.GREEN}[DB] {len(users)} usuarios retornados{Style.RESET_ALL}")
        
        return jsonify({
            'total': len(users),
            'users': users
        }), 200
        
    except psycopg2.Error as e:
        print(f"{Fore.RED}[DB] Erro na consulta: {e}{Style.RESET_ALL}")
        return jsonify({'error': str(e)}), 500

@app.route('/cache', methods=['POST'])
def set_cache():
    """Salva dados no Redis"""
    print(f"{Fore.CYAN}[WEB] Requisição POST em /cache{Style.RESET_ALL}")
    
    data = request.get_json()
    if not data or 'key' not in data or 'value' not in data:
        return jsonify({'error': 'key and value required'}), 400
    
    cache = get_redis_connection()
    if not cache:
        return jsonify({'error': 'Redis connection failed'}), 503
    
    try:
        key = data['key']
        value = json.dumps(data['value'])
        ttl = data.get('ttl', 3600)  # TTL padrão: 1 hora
        
        cache.setex(key, ttl, value)
        print(f"{Fore.GREEN}[CACHE] Chave '{key}' salva (TTL: {ttl}s){Style.RESET_ALL}")
        
        return jsonify({
            'message': 'Data cached successfully',
            'key': key,
            'ttl': ttl
        }), 201
        
    except redis.RedisError as e:
        print(f"{Fore.RED}[CACHE] Erro ao salvar: {e}{Style.RESET_ALL}")
        return jsonify({'error': str(e)}), 500

@app.route('/cache/<key>')
def get_cache(key):
    """Busca dados do Redis"""
    print(f"{Fore.CYAN}[WEB] Requisição GET em /cache/{key}{Style.RESET_ALL}")
    
    cache = get_redis_connection()
    if not cache:
        return jsonify({'error': 'Redis connection failed'}), 503
    
    try:
        value = cache.get(key)
        
        if value is None:
            print(f"{Fore.YELLOW}[CACHE] Chave '{key}' nao encontrada{Style.RESET_ALL}")
            return jsonify({'error': 'Key not found'}), 404
        
        ttl = cache.ttl(key)
        print(f"{Fore.GREEN}[CACHE] Chave '{key}' recuperada (TTL: {ttl}s){Style.RESET_ALL}")
        
        return jsonify({
            'key': key,
            'value': json.loads(value),
            'ttl': ttl
        }), 200
        
    except redis.RedisError as e:
        print(f"{Fore.RED}[CACHE] Erro ao buscar: {e}{Style.RESET_ALL}")
        return jsonify({'error': str(e)}), 500

@app.route('/health')
def health():
    """Verifica status de todos os serviços"""
    print(f"{Fore.CYAN}[WEB] Requisição em /health{Style.RESET_ALL}")
    
    status = {
        'web': {'status': 'ok', 'service': 'Flask API'},
        'db': {'status': 'unknown', 'service': 'PostgreSQL'},
        'cache': {'status': 'unknown', 'service': 'Redis'}
    }
    
    # Testa PostgreSQL
    try:
        conn = get_db_connection()
        if conn:
            cursor = conn.cursor()
            cursor.execute('SELECT 1')
            cursor.close()
            status['db']['status'] = 'ok'
            print(f"{Fore.GREEN}[DB] Health check OK{Style.RESET_ALL}")
    except Exception as e:
        status['db']['status'] = 'error'
        status['db']['error'] = str(e)
        print(f"{Fore.RED}[DB] Health check FAILED{Style.RESET_ALL}")
    
    # Testa Redis
    try:
        cache = get_redis_connection()
        if cache and cache.ping():
            status['cache']['status'] = 'ok'
            print(f"{Fore.GREEN}[CACHE] Health check OK{Style.RESET_ALL}")
    except Exception as e:
        status['cache']['status'] = 'error'
        status['cache']['error'] = str(e)
        print(f"{Fore.RED}[CACHE] Health check FAILED{Style.RESET_ALL}")
    
    # Define status geral
    all_ok = all(s['status'] == 'ok' for s in status.values())
    http_status = 200 if all_ok else 503
    
    return jsonify({
        'status': 'healthy' if all_ok else 'degraded',
        'timestamp': datetime.now().isoformat(),
        'services': status
    }), http_status

if __name__ == '__main__':
    print(f"\n{Fore.CYAN}{'='*60}")
    print(f"DESAFIO 3 - DOCKER COMPOSE")
    print(f"API Flask iniciando...")
    print(f"{'='*60}{Style.RESET_ALL}\n")
    
    app.run(host='0.0.0.0', port=5000, debug=True)
