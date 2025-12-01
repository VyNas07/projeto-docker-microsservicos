"""
Microsserviço de Pedidos
Fornece dados de pedidos - apenas acessível internamente via Gateway
"""

from flask import Flask, jsonify
import json
from datetime import datetime
from colorama import Fore, Style, init

init(autoreset=True)
app = Flask(__name__)

def load_orders():
    """Carrega pedidos do arquivo JSON"""
    try:
        with open('pedidos.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print(f"{Fore.RED}[ERROR] Erro ao carregar pedidos.json: {e}{Style.RESET_ALL}")
        return []

ORDERS = load_orders()

@app.route('/')
def home():
    """Informações do serviço"""
    print(f"{Fore.MAGENTA}[PEDIDOS] GET /{Style.RESET_ALL}")
    
    return jsonify({
        'service': 'Servico de Pedidos',
        'version': '1.0',
        'description': 'Microsservico interno - acesso via Gateway',
        'port': 5002,
        'total_orders': len(ORDERS)
    }), 200

@app.route('/orders')
def get_orders():
    """Lista todos os pedidos"""
    print(f"{Fore.MAGENTA}[PEDIDOS] GET /orders - Retornando {len(ORDERS)} pedidos{Style.RESET_ALL}")
    
    return jsonify({
        'total': len(ORDERS),
        'orders': ORDERS
    }), 200

@app.route('/orders/<int:order_id>')
def get_order(order_id):
    """Retorna pedido específico"""
    print(f"{Fore.MAGENTA}[PEDIDOS] GET /orders/{order_id}{Style.RESET_ALL}")
    
    order = next((o for o in ORDERS if o['id'] == order_id), None)
    
    if order:
        print(f"{Fore.GREEN}[PEDIDOS] Pedido {order_id} encontrado{Style.RESET_ALL}")
        return jsonify(order), 200
    else:
        print(f"{Fore.YELLOW}[PEDIDOS] Pedido {order_id} nao encontrado{Style.RESET_ALL}")
        return jsonify({'error': 'Order not found'}), 404

@app.route('/orders/user/<int:user_id>')
def get_orders_by_user(user_id):
    """Retorna pedidos de um usuário específico"""
    print(f"{Fore.MAGENTA}[PEDIDOS] GET /orders/user/{user_id}{Style.RESET_ALL}")
    
    user_orders = [o for o in ORDERS if o['user_id'] == user_id]
    
    print(f"{Fore.GREEN}[PEDIDOS] {len(user_orders)} pedidos encontrados para usuario {user_id}{Style.RESET_ALL}")
    
    return jsonify({
        'user_id': user_id,
        'total': len(user_orders),
        'orders': user_orders
    }), 200

@app.route('/health')
def health():
    """Health check"""
    return jsonify({
        'status': 'healthy',
        'service': 'servico-pedidos',
        'timestamp': datetime.now().isoformat(),
        'orders_loaded': len(ORDERS)
    }), 200

if __name__ == '__main__':
    print(f"\n{Fore.MAGENTA}{'='*60}")
    print(f"MICROSSERVICO DE PEDIDOS")
    print(f"Porta: 5002 (INTERNA - acesso via Gateway)")
    print(f"Pedidos carregados: {len(ORDERS)}")
    print(f"{'='*60}{Style.RESET_ALL}\n")
    
    app.run(host='0.0.0.0', port=5002, debug=True)
