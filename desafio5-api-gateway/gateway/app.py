"""
API Gateway
Ponto único de entrada para todos os microsserviços
Orquestra chamadas e agrega dados de múltiplos serviços
"""

from flask import Flask, jsonify, request
import requests
import os
from datetime import datetime
from colorama import Fore, Style, init

init(autoreset=True)
app = Flask(__name__)

# URLs dos microsserviços internos
USERS_SERVICE_URL = os.getenv('USERS_SERVICE_URL', 'http://servico-usuarios:5001')
ORDERS_SERVICE_URL = os.getenv('ORDERS_SERVICE_URL', 'http://servico-pedidos:5002')

def log_request(method, path, service=None):
    """Log de requisições através do gateway"""
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    if service:
        print(f"{Fore.YELLOW}[GATEWAY] {timestamp} - {method} {path} -> {service}{Style.RESET_ALL}")
    else:
        print(f"{Fore.YELLOW}[GATEWAY] {timestamp} - {method} {path}{Style.RESET_ALL}")

def proxy_request(url, method='GET'):
    """Faz proxy de requisição para serviço downstream"""
    try:
        response = requests.request(method, url, timeout=10)
        return response.json(), response.status_code
    except requests.exceptions.Timeout:
        return {'error': 'Service timeout'}, 504
    except requests.exceptions.ConnectionError:
        return {'error': 'Service unavailable'}, 503
    except requests.exceptions.RequestException as e:
        return {'error': f'Service error: {str(e)}'}, 500

@app.route('/')
def home():
    """Informações do Gateway"""
    log_request('GET', '/')
    
    return jsonify({
        'service': 'API Gateway',
        'version': '1.0',
        'description': 'Ponto unico de entrada para todos os microsservicos',
        'port': 8080,
        'upstream_services': {
            'users': USERS_SERVICE_URL,
            'orders': ORDERS_SERVICE_URL
        },
        'endpoints': {
            'users': {
                'list': '/users',
                'detail': '/users/<id>',
                'with_orders': '/users/<id>/orders'
            },
            'orders': {
                'list': '/orders',
                'detail': '/orders/<id>',
                'by_user': '/orders/user/<userId>'
            },
            'health': '/health'
        }
    }), 200

# ==================== PROXY ENDPOINTS - USERS ====================

@app.route('/users')
def get_users():
    """Proxy para listar usuários"""
    log_request('GET', '/users', 'servico-usuarios')
    
    data, status = proxy_request(f'{USERS_SERVICE_URL}/users')
    return jsonify(data), status

@app.route('/users/<int:user_id>')
def get_user(user_id):
    """Proxy para buscar usuário específico"""
    log_request('GET', f'/users/{user_id}', 'servico-usuarios')
    
    data, status = proxy_request(f'{USERS_SERVICE_URL}/users/{user_id}')
    return jsonify(data), status

# ==================== PROXY ENDPOINTS - ORDERS ====================

@app.route('/orders')
def get_orders():
    """Proxy para listar pedidos"""
    log_request('GET', '/orders', 'servico-pedidos')
    
    data, status = proxy_request(f'{ORDERS_SERVICE_URL}/orders')
    return jsonify(data), status

@app.route('/orders/<int:order_id>')
def get_order(order_id):
    """Proxy para buscar pedido específico"""
    log_request('GET', f'/orders/{order_id}', 'servico-pedidos')
    
    data, status = proxy_request(f'{ORDERS_SERVICE_URL}/orders/{order_id}')
    return jsonify(data), status

@app.route('/orders/user/<int:user_id>')
def get_orders_by_user(user_id):
    """Proxy para buscar pedidos de um usuário"""
    log_request('GET', f'/orders/user/{user_id}', 'servico-pedidos')
    
    data, status = proxy_request(f'{ORDERS_SERVICE_URL}/orders/user/{user_id}')
    return jsonify(data), status

# ==================== AGGREGATED ENDPOINT ====================

@app.route('/users/<int:user_id>/orders')
def get_user_with_orders(user_id):
    """
    Endpoint agregado: busca dados do usuário E seus pedidos
    Orquestra chamadas para dois microsserviços diferentes
    """
    log_request('GET', f'/users/{user_id}/orders', 'AGREGANDO: usuarios + pedidos')
    
    # Busca dados do usuário
    user_data, user_status = proxy_request(f'{USERS_SERVICE_URL}/users/{user_id}')
    
    if user_status != 200:
        return jsonify({'error': 'User not found or service unavailable'}), user_status
    
    # Busca pedidos do usuário
    orders_data, orders_status = proxy_request(f'{ORDERS_SERVICE_URL}/orders/user/{user_id}')
    
    if orders_status != 200:
        orders_data = {'total': 0, 'orders': []}
    
    # Calcula estatísticas dos pedidos
    orders_list = orders_data.get('orders', [])
    total_value = sum(o.get('price', 0) * o.get('quantity', 0) for o in orders_list)
    
    status_count = {}
    for order in orders_list:
        status = order.get('status', 'unknown')
        status_count[status] = status_count.get(status, 0) + 1
    
    # Agrega dados
    result = {
        'user': user_data,
        'orders_summary': {
            'total_orders': len(orders_list),
            'total_value': round(total_value, 2),
            'status_distribution': status_count
        },
        'orders': orders_list,
        'metadata': {
            'aggregated_at': datetime.now().isoformat(),
            'sources': ['servico-usuarios', 'servico-pedidos']
        }
    }
    
    print(f"{Fore.GREEN}[GATEWAY] Agregacao concluida: usuario {user_id} + {len(orders_list)} pedidos{Style.RESET_ALL}")
    
    return jsonify(result), 200

# ==================== HEALTH CHECK ====================

@app.route('/health')
def health():
    """
    Health check do gateway e todos os serviços downstream
    Verifica conectividade e status de cada microsserviço
    """
    log_request('GET', '/health')
    
    status = {
        'gateway': {
            'status': 'healthy',
            'timestamp': datetime.now().isoformat()
        },
        'upstream_services': {}
    }
    
    all_healthy = True
    
    # Verifica serviço de usuários
    try:
        response = requests.get(f'{USERS_SERVICE_URL}/health', timeout=5)
        if response.status_code == 200:
            status['upstream_services']['servico-usuarios'] = {
                'status': 'healthy',
                'url': USERS_SERVICE_URL
            }
            print(f"{Fore.GREEN}[GATEWAY] servico-usuarios: healthy{Style.RESET_ALL}")
        else:
            status['upstream_services']['servico-usuarios'] = {
                'status': 'unhealthy',
                'url': USERS_SERVICE_URL
            }
            all_healthy = False
            print(f"{Fore.RED}[GATEWAY] servico-usuarios: unhealthy{Style.RESET_ALL}")
    except requests.RequestException as e:
        status['upstream_services']['servico-usuarios'] = {
            'status': 'unreachable',
            'url': USERS_SERVICE_URL,
            'error': str(e)
        }
        all_healthy = False
        print(f"{Fore.RED}[GATEWAY] servico-usuarios: unreachable{Style.RESET_ALL}")
    
    # Verifica serviço de pedidos
    try:
        response = requests.get(f'{ORDERS_SERVICE_URL}/health', timeout=5)
        if response.status_code == 200:
            status['upstream_services']['servico-pedidos'] = {
                'status': 'healthy',
                'url': ORDERS_SERVICE_URL
            }
            print(f"{Fore.GREEN}[GATEWAY] servico-pedidos: healthy{Style.RESET_ALL}")
        else:
            status['upstream_services']['servico-pedidos'] = {
                'status': 'unhealthy',
                'url': ORDERS_SERVICE_URL
            }
            all_healthy = False
            print(f"{Fore.RED}[GATEWAY] servico-pedidos: unhealthy{Style.RESET_ALL}")
    except requests.RequestException as e:
        status['upstream_services']['servico-pedidos'] = {
            'status': 'unreachable',
            'url': ORDERS_SERVICE_URL,
            'error': str(e)
        }
        all_healthy = False
        print(f"{Fore.RED}[GATEWAY] servico-pedidos: unreachable{Style.RESET_ALL}")
    
    # Status geral
    status['overall_status'] = 'healthy' if all_healthy else 'degraded'
    http_status = 200 if all_healthy else 503
    
    return jsonify(status), http_status

if __name__ == '__main__':
    print(f"\n{Fore.YELLOW}{'='*60}")
    print(f"API GATEWAY")
    print(f"Porta: 8080 (UNICO PONTO DE ENTRADA EXTERNO)")
    print(f"Upstream services:")
    print(f"  - Usuarios: {USERS_SERVICE_URL}")
    print(f"  - Pedidos: {ORDERS_SERVICE_URL}")
    print(f"{'='*60}{Style.RESET_ALL}\n")
    
    app.run(host='0.0.0.0', port=8080, debug=True)
