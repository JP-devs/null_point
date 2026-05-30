import subprocess
import io
from contextlib import redirect_stdout

def run_tool(args_str: str) -> str:
    f = io.StringIO()
    with redirect_stdout(f):
        try:
            # Use 'docker ps' to list containers
            result = subprocess.run(['docker', 'ps', '-a'], capture_output=True, text=True, timeout=5)
            if result.returncode == 0:
                print("Docker Containers:\n")
                print(result.stdout)
            else:
                print(f"Error executing docker ps: {result.stderr}")
        except FileNotFoundError:
            print("Error: Docker is not installed or not in PATH.")
        except Exception as e:
            print(f"Unexpected error: {e}")
    return f.getvalue()

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        print(run_tool(sys.argv[1]))
    else:
        print(run_tool(""))
