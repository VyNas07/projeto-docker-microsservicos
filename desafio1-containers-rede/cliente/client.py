"""
Cliente Python para Desafio 1 - Containers em Rede
Faz requisições periódicas ao servidor Flask
"""

import requests
import time
from datetime import datetime
from colorama import Fore, Back, Style, init
import signal
import sys

# Inicializa colorama
init(autoreset=True)

# Configurações
SERVER_URL = "http://servidor:8080"
REQUEST_INTERVAL = 5  # segundos

# Flag para controle de shutdown gracioso
running = True

# ASCII Art para startup
STARTUP_ART = f"""
{Fore.YELLOW}
╔══════════════════════════════════════════╗
║      CLIENTE HTTP - DESAFIO 1          ║
║     Requisicoes Periodicas ao Servidor  ║
╚══════════════════════════════════════════╝
{Style.RESET_ALL}
"""

def signal_handler(sig, frame):
    """Handler para shutdown gracioso com Ctrl+C"""
    global running
    print(f"\n{Fore.RED}Recebido sinal de interrupcao. Encerrando cliente...{Style.RESET_ALL}")
    running = False

def make_request():
    """Faz uma requisição HTTP ao servidor e exibe a resposta"""
    try:
        # Faz requisição GET ao servidor
        response = requests.get(SERVER_URL, timeout=3)
        
        if response.status_code == 200:
            data = response.json()
            
            # Log colorido da resposta bem-sucedida
            print(f"{Fore.GREEN}{'='*60}")
            print(f"{Fore.GREEN}RESPOSTA RECEBIDA - [{datetime.now().strftime('%H:%M:%S')}]")
            print(f"{Fore.CYAN}   Hostname do Servidor: {Fore.WHITE}{data.get('hostname')}")
            print(f"{Fore.CYAN}   IP do Servidor: {Fore.WHITE}{data.get('container_ip')}")
            print(f"{Fore.CYAN}   Timestamp: {Fore.WHITE}{data.get('timestamp')}")
            print(f"{Fore.CYAN}   Numero da Requisicao: {Fore.WHITE}{data.get('request_number')}")
            print(f"{Fore.CYAN}   Uptime do Servidor: {Fore.WHITE}{data.get('uptime')}")
            print(f"{Fore.CYAN}   Mensagem: {Fore.WHITE}{data.get('message')}")
            print(f"{Fore.GREEN}{'='*60}{Style.RESET_ALL}\n")
            
            return True
        else:
            print(f"{Fore.RED}ERRO: Status code {response.status_code}{Style.RESET_ALL}")
            return False
            
    except requests.exceptions.ConnectionError:
        print(f"{Fore.RED}[{datetime.now().strftime('%H:%M:%S')}] "
              f"Erro de conexao - Servidor nao esta acessivel{Style.RESET_ALL}")
        return False
        
    except requests.exceptions.Timeout:
        print(f"{Fore.RED}[{datetime.now().strftime('%H:%M:%S')}] "
              f"Timeout - Servidor nao respondeu a tempo{Style.RESET_ALL}")
        return False
        
    except requests.exceptions.RequestException as e:
        print(f"{Fore.RED}[{datetime.now().strftime('%H:%M:%S')}] "
              f"Erro na requisicao: {str(e)}{Style.RESET_ALL}")
        return False

def main():
    """Função principal do cliente"""
    global running
    
    # Registra handler para Ctrl+C
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    print(STARTUP_ART)
    print(f"{Fore.MAGENTA}Cliente iniciado em {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"URL do servidor: {SERVER_URL}")
    print(f"Intervalo de requisicoes: {REQUEST_INTERVAL} segundos")
    print(f"{Fore.YELLOW}Pressione Ctrl+C para encerrar{Style.RESET_ALL}\n")
    
    request_count = 0
    success_count = 0
    failure_count = 0
    
    # Loop principal
    while running:
        request_count += 1
        print(f"{Fore.BLUE}Enviando requisicao #{request_count}...{Style.RESET_ALL}")
        
        success = make_request()
        
        if success:
            success_count += 1
        else:
            failure_count += 1
        
        # Aguarda antes da próxima requisição
        if running:
            print(f"{Fore.YELLOW}Aguardando {REQUEST_INTERVAL} segundos para proxima requisicao...\n{Style.RESET_ALL}")
            time.sleep(REQUEST_INTERVAL)
    
    # Estatísticas finais
    print(f"\n{Fore.CYAN}{'='*60}")
    print(f"{Fore.CYAN}ESTATISTICAS FINAIS")
    print(f"{Fore.CYAN}   Total de requisicoes: {request_count}")
    print(f"{Fore.GREEN}   Sucessos: {success_count}")
    print(f"{Fore.RED}   Falhas: {failure_count}")
    print(f"{Fore.CYAN}{'='*60}{Style.RESET_ALL}")
    print(f"{Fore.GREEN}Cliente encerrado com sucesso!{Style.RESET_ALL}")

if __name__ == "__main__":
    main()
