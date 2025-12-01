"""
Servidor Flask para Desafio 1 - Containers em Rede
Demonstra comunicação entre containers Docker
"""

from flask import Flask, jsonify
from datetime import datetime
import socket
import os
from colorama import Fore, Style, init

# Inicializa colorama para logs coloridos
init(autoreset=True)

app = Flask(__name__)

# Contador global de requisições
request_counter = 0
start_time = datetime.now()

# ASCII Art para startup
STARTUP_ART = f"""
{Fore.CYAN}
╔══════════════════════════════════════════╗
║      SERVIDOR FLASK - DESAFIO 1        ║
║     Comunicação entre Containers        ║
╚══════════════════════════════════════════╝
{Style.RESET_ALL}
"""

@app.route('/', methods=['GET'])
def home():
    """Endpoint principal que retorna informações do sistema"""
    global request_counter
    request_counter += 1
    
    # Calcula uptime
    uptime = datetime.now() - start_time
    uptime_str = str(uptime).split('.')[0]  # Remove microsegundos
    
    response_data = {
        'hostname': socket.gethostname(),
        'timestamp': datetime.now().isoformat(),
        'request_number': request_counter,
        'uptime': uptime_str,
        'message': 'Comunicacao bem-sucedida entre containers!',
        'container_ip': socket.gethostbyname(socket.gethostname())
    }
    
    # Log colorido da requisição
    print(f"{Fore.GREEN}[{datetime.now().strftime('%H:%M:%S')}] "
          f"Requisicao #{request_counter} recebida{Style.RESET_ALL}")
    
    return jsonify(response_data), 200

@app.route('/health', methods=['GET'])
def health():
    """Endpoint de health check"""
    print(f"{Fore.YELLOW}[{datetime.now().strftime('%H:%M:%S')}] "
          f"Health check realizado{Style.RESET_ALL}")
    
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'uptime': str(datetime.now() - start_time).split('.')[0]
    }), 200

@app.before_request
def log_request():
    """Log de cada requisição recebida"""
    from flask import request
    print(f"{Fore.CYAN}[{datetime.now().strftime('%H:%M:%S')}] "
          f"{request.method} {request.path} - {request.remote_addr}{Style.RESET_ALL}")

if __name__ == '__main__':
    print(STARTUP_ART)
    print(f"{Fore.MAGENTA}Servidor iniciado em {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Hostname: {socket.gethostname()}")
    print(f"IP: {socket.gethostbyname(socket.gethostname())}")
    print(f"Porta: 8080{Style.RESET_ALL}\n")
    
    # Inicia o servidor Flask
    app.run(host='0.0.0.0', port=8080, debug=False)
