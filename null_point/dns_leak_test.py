import socket
import io
from contextlib import redirect_stdout

def run_tool(args_str: str) -> str:
    f = io.StringIO()
    with redirect_stdout(f):
        try:
            # Use Google's DNS to check for leak
            hostname = "google.com"
            ip = socket.gethostbyname(hostname)
            print(f"DNS Resolve for {hostname}: {ip}")
            print("Check if this IP matches your ISP's DNS servers.")
        except Exception as e:
            print(f"Error: {e}")
    return f.getvalue()

if __name__ == "__main__":
    import sys
    print(run_tool(sys.argv[1] if len(sys.argv) > 1 else ""))
