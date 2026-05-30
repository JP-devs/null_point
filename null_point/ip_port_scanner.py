import socket
import argparse
import sys
import io
import contextlib
from concurrent.futures import ThreadPoolExecutor
from colorama import init, Fore, Style

init(autoreset=True)

def run_tool(args_str: str) -> str:
    parts = args_str.strip().split()
    if not parts:
        return "Please provide IP and optional ports."
    
    ip = parts[0]
    start_port = int(parts[1]) if len(parts) > 1 else 1
    end_port = int(parts[2]) if len(parts) > 2 else 1024
    
    f = io.StringIO()
    with contextlib.redirect_stdout(f):
        print(create_banner())
        open_ports = scan_ports(ip, start_port, end_port)
        print(f"\nScan completed.")
        print(f"Open ports: {open_ports}")
    return f.getvalue()

def create_banner():
    banner = r"""
  ___ ___   ___  ___  ___ _____ ___ 
 | _ \ _ \ | _ \/ _ \| _ \_   _| _ \
 |  _/  _/ |  _/ (_) |   / | | |  _/
 |_| |_|   |_|  \___/|_|_\ |_| |_|  
                                     
    IP Port Scanner Tool
    """
    return Fore.RED + banner + Style.RESET_ALL

def scan_port(ip, port, timeout=1):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.settimeout(timeout)
        if s.connect_ex((ip, port)) == 0:
            print(f"{Fore.GREEN}[+] Port {port} is OPEN{Style.RESET_ALL}")
            return port
    return None

def scan_ports(ip, start_port, end_port, threads=50):
    print(f"{Fore.CYAN}Scanning {ip} from port {start_port} to {end_port} with {threads} threads...{Style.RESET_ALL}")
    open_ports = []
    
    with ThreadPoolExecutor(max_workers=threads) as executor:
        results = [executor.submit(scan_port, ip, port) for port in range(start_port, end_port + 1)]
        for result in results:
            port = result.result()
            if port:
                open_ports.append(port)
                
    return open_ports

def main():
    parser = argparse.ArgumentParser(description="Modern IP Port Scanner Tool")
    parser.add_argument("ip", nargs='?', help="IP address to scan")
    parser.add_argument("-s", "--start", type=int, default=1, help="Start port (default: 1)")
    parser.add_argument("-e", "--end", type=int, default=1024, help="End port (default: 1024)")
    args = parser.parse_args()

    print(create_banner())

    if not args.ip:
        ip = input(f"{Fore.WHITE}Enter IP address to scan: ").strip()
        if not ip:
            print(f"{Fore.RED}IP address is required.{Style.RESET_ALL}")
            return
    else:
        ip = args.ip

    open_ports = scan_ports(ip, args.start, args.end)
    
    print(f"\n{Fore.CYAN}Scan completed.{Style.RESET_ALL}")
    print(f"{Fore.GREEN}Open ports: {open_ports}{Style.RESET_ALL}")

if __name__ == "__main__":
    try:
        arg = ' '.join(sys.argv[1:]) if len(sys.argv) > 1 else ''
        if arg:
            print(run_tool(arg))
        else:
            main()
    except KeyboardInterrupt:
        print(f"\n{Fore.RED}Scan cancelled.{Style.RESET_ALL}")
        sys.exit(0)
    except Exception as e:
        print(f"\n{Fore.RED}Error: {e}{Style.RESET_ALL}")
        sys.exit(1)
