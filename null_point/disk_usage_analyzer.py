import shutil
import io
from contextlib import redirect_stdout

def run_tool(drive: str) -> str:
    f = io.StringIO()
    with redirect_stdout(f):
        try:
            # Defaults to C: if not provided
            path = drive if drive else "C:/"
            total, used, free = shutil.disk_usage(path)
            print(f"Drive: {path}")
            print(f"Total: {total // (2**30)} GB")
            print(f"Used: {used // (2**30)} GB")
            print(f"Free: {free // (2**30)} GB")
            print(f"Usage: {100 * used / total:.2f}%")
        except Exception as e:
            print(f"Error: {e}")
    return f.getvalue()

if __name__ == "__main__":
    import sys
    print(run_tool(sys.argv[1] if len(sys.argv) > 1 else ""))
