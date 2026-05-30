import psutil
import argparse
import shlex
import io
import contextlib

def get_interfaces():
    print("--- Network Interfaces ---")
    for interface, stats in psutil.net_if_stats().items():
        status = 'UP' if stats.isup else 'DOWN'
        print(f"{interface}: {status} | Speed: {stats.speed}Mbps | MTU: {stats.mtu}")

def get_io_counters():
    print("--- Network I/O Counters ---")
    for interface, counters in psutil.net_io_counters(pernic=True).items():
        print(f"{interface}: Sent: {counters.bytes_sent} B | Recv: {counters.bytes_recv} B")

def get_connections():
    print("--- Active Connections ---")
    for conn in psutil.net_connections():
        laddr = f"{conn.laddr.ip}:{conn.laddr.port}" if conn.laddr else "N/A"
        raddr = f"{conn.raddr.ip}:{conn.raddr.port}" if conn.raddr else "N/A"
        print(f"{conn.type}: {laddr} -> {raddr} ({conn.status})")

def run_tool(args_str: str) -> str:
    parser = argparse.ArgumentParser(description="Modern Network Traffic Analyzer", exit_on_error=False)
    parser.add_argument("-i", "--interfaces", action="store_true", help="Show interfaces")
    parser.add_argument("-c", "--counters", action="store_true", help="Show I/O counters")
    parser.add_argument("-n", "--connections", action="store_true", help="Show connections")
    
    f = io.StringIO()
    with contextlib.redirect_stdout(f):
        try:
            args = parser.parse_args(shlex.split(args_str))
            
            if not any([args.interfaces, args.counters, args.connections]):
                get_interfaces()
                print()
                get_io_counters()
                print()
                get_connections()
            else:
                if args.interfaces: 
                    get_interfaces()
                    print()
                if args.counters: 
                    get_io_counters()
                    print()
                if args.connections: 
                    get_connections()
                    print()
        except Exception as e:
            print(f"Error: {e}")
    return f.getvalue()

