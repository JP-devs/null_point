import os
import platform
import subprocess
import time
from datetime import datetime
import argparse
import socket
import io
from contextlib import redirect_stdout
from null_point_theme import print_banner, print_success, print_error, print_input, print_info

class IPPinger:
    def __init__(self):
        self.results = []

    def clear_screen(self):
        os.system('cls' if platform.system() == 'Windows' else 'clear')

    def display_banner(self):
        print_banner("IP Pinger")
        print("="*60)
        print(f"Tool started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("="*60)
        print()

    def ping_host(self, host: str, count: int = 4, timeout: int = 2) -> tuple[bool, float]:
        try:
            ip = socket.gethostbyname(host)
            if platform.system().lower() == "windows":
                cmd = ['ping', '-n', str(count), '-w', str(timeout*1000), ip]
            else:
                cmd = ['ping', '-c', str(count), '-W', str(timeout), ip]
            output = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, check=False)
            if output.returncode == 0:
                if platform.system().lower() == "windows":
                    lines = output.stdout.split('\n')
                    for line in lines:
                        if 'Average' in line:
                            latency = line.split('=')[-1].strip().replace('ms', '')
                            return (True, float(latency))
                else:
                    lines = output.stdout.split('\n')
                    for line in lines:
                        if 'min/avg/max' in line:
                            latency = line.split('=')[1].split('/')[1]
                            return (True, float(latency))
                return (True, 0.0)
            return (False, 0.0)
        except Exception as e:
            print_error(f"Error pinging host: {e}")
            return (False, 0.0)

    def continuous_ping(self, host: str, interval: float = 1.0, max_pings: int = None):
        print_info(f"Starting continuous ping to {host}")
        print_info("Press Ctrl+C to stop\n")
        count = 0
        try:
            while True:
                if max_pings and count >= max_pings: break
                timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                success, latency = self.ping_host(host, count=1)
                status = "UP" if success else "DOWN"
                latency_str = f"{latency:.2f}" if success else "N/A"
                print(f"{timestamp} | {host} | {status} | {latency_str} ms")
                self.results.append({'timestamp': timestamp, 'host': host, 'status': status, 'latency': latency_str})
                count += 1
                time.sleep(interval)
        except KeyboardInterrupt:
            print_info("Ping stopped by user")

def run_tool(args_str: str) -> str:
    """Callable function for the screen tool"""
    f = io.StringIO()
    with redirect_stdout(f):
        pinger = IPPinger()
        success, latency = pinger.ping_host(args_str)
        if success:
            print_success(f"Host {args_str} is reachable (latency: {latency:.2f} ms)")
        else:
            print_error(f"Host {args_str} is unreachable")
    return f.getvalue()

def main():
    parser = argparse.ArgumentParser(description="IP Pinger Tool")
    parser.add_argument("host", nargs='?', help="Host to ping")
    args = parser.parse_args()

    if not args.host:
        args.host = print_input("Host/IP: ").strip()
    
    if args.host:
        print(run_tool(args.host))

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        sys.exit(0)
    except Exception as e:
        print_error(f"An error occurred: {str(e)}")
