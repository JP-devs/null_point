import subprocess
import io
from contextlib import redirect_stdout

def run_tool(args_str: str) -> str:
    f = io.StringIO()
    with redirect_stdout(f):
        try:
            # Check Windows Firewall status using netsh
            result = subprocess.run(['netsh', 'advfirewall', 'show', 'allprofiles'], capture_output=True, text=True, timeout=10)
            if result.returncode == 0:
                print(result.stdout)
            else:
                print(f"Error executing netsh: {result.stderr}")
        except Exception as e:
            print(f"Unexpected error: {e}")
    return f.getvalue()

if __name__ == "__main__":
    import sys
    print(run_tool(sys.argv[1] if len(sys.argv) > 1 else ""))
