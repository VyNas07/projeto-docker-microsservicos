"""
Microsserviço B - Agregador de Dados
Consome o serviço de usuários e processa informações
"""

from flask import Flask, jsonify
import requests
import os
from datetime import datetime, timedelta
from colorama import Fore, Style, init

# Inicializa colorama e Flask
init(autoreset=True)
app = Flask(__name__)

# URL do serviço de usuários
USERS_SERVICE_URL = os.getenv('USERS_SERVICE_URL', 'http://servico-usuarios:5001')

def calcular_dias_ativo(registration_date):
    """Calcula quantos dias o usuário está ativo"""
    try:
        data_registro = datetime.strptime(registration_date, '%Y-%m-%d')
        dias = (datetime.now() - data_registro).days
        return dias
    except:
        return 0

def obter_usuarios():
    """Busca usuários do microsserviço A"""
    try:
        response = requests.get(f'{USERS_SERVICE_URL}/users', timeout=5)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"{Fore.RED}[ERROR] Erro ao buscar usuarios: {e}{Style.RESET_ALL}")
        return None

def obter_usuario(user_id):
    """Busca usuário específico do microsserviço A"""
    try:
        response = requests.get(f'{USERS_SERVICE_URL}/users/{user_id}', timeout=5)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"{Fore.RED}[ERROR] Erro ao buscar usuario {user_id}: {e}{Style.RESET_ALL}")
        return None

@app.route('/')
def home():
    """Endpoint raiz com informações do serviço"""
    print(f"{Fore.MAGENTA}[INFO] GET /{Style.RESET_ALL}")
    
    return jsonify({
        'service': 'Servico Agregador',
        'version': '1.0',
        'description': 'Microsservico B - agrega e processa dados de usuarios',
        'endpoints': {
            'report': '/report',
            'user_details': '/user/<id>/details',
            'health': '/health'
        },
        'upstream_service': USERS_SERVICE_URL
    }), 200

@app.route('/report')
def generate_report():
    """Gera relatório agregado de todos os usuários"""
    print(f"{Fore.MAGENTA}[INFO] GET /report - Gerando relatorio{Style.RESET_ALL}")
    
    data = obter_usuarios()
    if not data:
        return jsonify({'error': 'Failed to fetch users'}), 503
    
    users = data.get('users', [])
    
    # Estatísticas agregadas
    total = len(users)
    ativos = sum(1 for u in users if u.get('active', False))
    inativos = total - ativos
    
    # Contagem por role
    roles = {}
    for user in users:
        role = user.get('role', 'Unknown')
        roles[role] = roles.get(role, 0) + 1
    
    # Usuário mais antigo
    usuarios_ordenados = sorted(
        users,
        key=lambda u: u.get('registration_date', '9999-12-31')
    )
    mais_antigo = usuarios_ordenados[0] if usuarios_ordenados else None
    
    # Lista processada com dias de atividade
    usuarios_processados = []
    for user in users:
        dias_ativo = calcular_dias_ativo(user.get('registration_date', ''))
        usuarios_processados.append({
            'id': user.get('id'),
            'full_name': user.get('full_name'),
            'role': user.get('role'),
            'active': user.get('active'),
            'dias_ativo': dias_ativo,
            'status_descricao': f"Ativo ha {dias_ativo} dias" if user.get('active') else "Inativo"
        })
    
    print(f"{Fore.GREEN}[SUCCESS] Relatorio gerado: {total} usuarios{Style.RESET_ALL}")
    
    return jsonify({
        'report_generated_at': datetime.now().isoformat(),
        'statistics': {
            'total_users': total,
            'active_users': ativos,
            'inactive_users': inativos,
            'active_percentage': round((ativos / total * 100), 2) if total > 0 else 0,
            'roles_distribution': roles
        },
        'oldest_user': {
            'name': mais_antigo.get('full_name') if mais_antigo else None,
            'registration_date': mais_antigo.get('registration_date') if mais_antigo else None
        } if mais_antigo else None,
        'users': usuarios_processados
    }), 200

@app.route('/user/<int:user_id>/details')
def get_user_details(user_id):
    """Retorna detalhes enriquecidos de um usuário específico"""
    print(f"{Fore.MAGENTA}[INFO] GET /user/{user_id}/details{Style.RESET_ALL}")
    
    user = obter_usuario(user_id)
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    # Adiciona informações calculadas
    dias_ativo = calcular_dias_ativo(user.get('registration_date', ''))
    
    # Determina nível baseado em dias ativos
    if dias_ativo < 100:
        nivel = 'Junior'
    elif dias_ativo < 300:
        nivel = 'Pleno'
    else:
        nivel = 'Senior'
    
    user_details = {
        'basic_info': {
            'id': user.get('id'),
            'username': user.get('username'),
            'full_name': user.get('full_name'),
            'email': user.get('email'),
            'role': user.get('role'),
            'active': user.get('active')
        },
        'calculated_info': {
            'registration_date': user.get('registration_date'),
            'dias_ativo': dias_ativo,
            'anos_ativo': round(dias_ativo / 365, 1),
            'nivel_experiencia': nivel,
            'status_descricao': f"Usuario ativo ha {dias_ativo} dias" if user.get('active') else f"Usuario inativo (foi ativo por {dias_ativo} dias)",
            'proxima_avaliacao': (datetime.now() + timedelta(days=90)).strftime('%Y-%m-%d')
        },
        'metadata': {
            'consulted_at': datetime.now().isoformat(),
            'data_source': 'servico-usuarios'
        }
    }
    
    print(f"{Fore.GREEN}[SUCCESS] Detalhes do usuario {user_id} gerados{Style.RESET_ALL}")
    
    return jsonify(user_details), 200

@app.route('/health')
def health():
    """Health check com verificação do serviço upstream"""
    status = {
        'status': 'healthy',
        'service': 'servico-agregador',
        'timestamp': datetime.now().isoformat(),
        'upstream_service': {
            'url': USERS_SERVICE_URL,
            'status': 'unknown'
        }
    }
    
    # Testa conectividade com serviço de usuários
    try:
        response = requests.get(f'{USERS_SERVICE_URL}/health', timeout=3)
        if response.status_code == 200:
            status['upstream_service']['status'] = 'healthy'
            return jsonify(status), 200
        else:
            status['upstream_service']['status'] = 'unhealthy'
            status['status'] = 'degraded'
            return jsonify(status), 503
    except requests.RequestException:
        status['upstream_service']['status'] = 'unreachable'
        status['status'] = 'degraded'
        return jsonify(status), 503

if __name__ == '__main__':
    print(f"\n{Fore.MAGENTA}{'='*60}")
    print(f"MICROSSERVICO B - SERVICO AGREGADOR")
    print(f"URL upstream: {USERS_SERVICE_URL}")
    print(f"Porta: 5002")
    print(f"{'='*60}{Style.RESET_ALL}\n")
    
    app.run(host='0.0.0.0', port=5002, debug=True)
