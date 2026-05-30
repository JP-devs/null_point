import subprocess
import requests
import argparse
import platform
import sys
import io
from contextlib import redirect_stdout
from null_point_theme import print_banner, print_success, print_error, print_input, print_info

def ping_ip(ip: str) -> bool:
    print_info(f"Pinging {ip} to check if alive...")
    param = '-n' if platform.system().lower() == 'windows' else '-c'
    command = ['ping', param, '2', ip]
    
    try:
        subprocess.check_output(command, stderr=subprocess.STDOUT)
        print_success(f"IP {ip} is UP.")
        return True
    except subprocess.CalledProcessError:
        print_error(f"IP {ip} is DOWN.")
        return False

def get_ip_info(ip: str):
    print_info(f"Fetching information for {ip}...")
    try:
        response = requests.get(f"https://ipinfo.io/{ip}/json", timeout=5)
        response.raise_for_status()
        data = response.json()
        print_success("IP Information:")
        for key, value in data.items():
            print(f"{key.capitalize()}: {value}")
    except requests.exceptions.RequestException as e:
        print_error(f"Error fetching IP info: {e}")

def run_tool(ip: str) -> str:
    """Captures and returns the tool's output."""
    f = io.StringIO()
    with redirect_stdout(f):
        print_banner("IP Scanner Tool")
        if ping_ip(ip):
            get_ip_info(ip)
    return f.getvalue()

def main():
    parser = argparse.ArgumentParser(description="Modern IP Scanner Tool")
    parser.add_argument("ip", nargs='?', help="IP address to scan")
    args = parser.parse_args()

    if not args.ip:
        ip = print_input("Enter IP address to scan: ").strip()
    else:
        ip = args.ip

    if ip:
        print(run_tool(ip))

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print_error("Operation cancelled.")
        sys.exit(0)
    except Exception as e:
        print_error(f"An error occurred: {e}")
        sys.exit(1)
