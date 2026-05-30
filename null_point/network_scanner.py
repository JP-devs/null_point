import socket
import subprocess
import argparse
import shlex
import io
import contextlib

def ping_ip(ip):
    try:
        param = '-n' if subprocess.os.name == 'nt' else '-c'
        command = ['ping', param, '2', ip]
        output = subprocess.check_output(command, stderr=subprocess.STDOUT, universal_newlines=True)
        print(output)
    except subprocess.CalledProcessError as e:
        print(f"Ping failed: {e.output.strip()}")

def scan_ports(ip, ports):
    print(f"Scanning ports on {ip}...")
    for port in ports:
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.settimeout(1)
                result = s.connect_ex((ip, port))
                if result == 0:
                    print(f"Port {port}: open")
                else:
                    print(f"Port {port}: closed")
        except Exception as e:
            print(f"Error scanning port {port}: {e}")

def run_tool(args_str: str) -> str:
    f = io.StringIO()
    with contextlib.redirect_stdout(f):
        parser = argparse.ArgumentParser(description="Basic Network Scanner", exit_on_error=False)
        parser.add_argument("ip", help="Target IP address")
        
        try:
            args = parser.parse_args(shlex.split(args_str))
            ping_ip(args.ip)
            ports = [22, 80, 443, 8080]
            scan_ports(args.ip, ports)
        except Exception as e:
            print(f"Error: {e}")
    return f.getvalue()
