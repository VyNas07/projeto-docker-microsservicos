"""
Microsserviço de Usuários
Fornece dados de usuários - apenas acessível internamente via Gateway
"""

from flask import Flask, jsonify
import json
from datetime import datetime
from colorama import Fore, Style, init

init(autoreset=True)
app = Flask(__name__)

def load_users():
    """Carrega usuários do arquivo JSON"""
    try:
        with open('usuarios.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print(f"{Fore.RED}[ERROR] Erro ao carregar usuarios.json: {e}{Style.RESET_ALL}")
        return []

USERS = load_users()

@app.route('/')
def home():
    """Informações do serviço"""
    print(f"{Fore.CYAN}[USUARIOS] GET /{Style.RESET_ALL}")
    
    return jsonify({
        'service': 'Servico de Usuarios',
        'version': '1.0',
        'description': 'Microsservico interno - acesso via Gateway',
        'port': 5001,
        'total_users': len(USERS)
    }), 200

@app.route('/users')
def get_users():
    """Lista todos os usuários"""
    print(f"{Fore.CYAN}[USUARIOS] GET /users - Retornando {len(USERS)} usuarios{Style.RESET_ALL}")
    
    return jsonify({
        'total': len(USERS),
        'users': USERS
    }), 200

@app.route('/users/<int:user_id>')
def get_user(user_id):
    """Retorna usuário específico"""
    print(f"{Fore.CYAN}[USUARIOS] GET /users/{user_id}{Style.RESET_ALL}")
    
    user = next((u for u in USERS if u['id'] == user_id), None)
    
    if user:
        print(f"{Fore.GREEN}[USUARIOS] Usuario {user_id} encontrado{Style.RESET_ALL}")
        return jsonify(user), 200
    else:
        print(f"{Fore.YELLOW}[USUARIOS] Usuario {user_id} nao encontrado{Style.RESET_ALL}")
        return jsonify({'error': 'User not found'}), 404

@app.route('/health')
def health():
    """Health check"""
    return jsonify({
        'status': 'healthy',
        'service': 'servico-usuarios',
        'timestamp': datetime.now().isoformat(),
        'users_loaded': len(USERS)
    }), 200

if __name__ == '__main__':
    print(f"\n{Fore.CYAN}{'='*60}")
    print(f"MICROSSERVICO DE USUARIOS")
    print(f"Porta: 5001 (INTERNA - acesso via Gateway)")
    print(f"Usuarios carregados: {len(USERS)}")
    print(f"{'='*60}{Style.RESET_ALL}\n")
    
    app.run(host='0.0.0.0', port=5001, debug=True)
