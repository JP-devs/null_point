import subprocess
import io
from contextlib import redirect_stdout

def run_tool(args_str: str) -> str:
    f = io.StringIO()
    with redirect_stdout(f):
        try:
            # Use 'systeminfo' on Windows
            result = subprocess.run(['systeminfo'], capture_output=True, text=True, timeout=10)
            if result.returncode == 0:
                print(result.stdout)
            else:
                print(f"Error executing systeminfo: {result.stderr}")
        except FileNotFoundError:
            print("Error: systeminfo command not found.")
        except Exception as e:
            print(f"Unexpected error: {e}")
    return f.getvalue()

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        print(run_tool(sys.argv[1]))
    else:
        print(run_tool(""))
