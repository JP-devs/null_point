import requests
import io
from contextlib import redirect_stdout

def run_tool(url: str) -> str:
    f = io.StringIO()
    with redirect_stdout(f):
        if not url:
            print("Error: URL is required.")
            return f.getvalue()
        
        try:
            response = requests.get(url, allow_redirects=True, timeout=5)
            print(f"Final URL: {response.url}")
            print(f"Status Code: {response.status_code}")
        except Exception as e:
            print(f"Error expanding URL: {e}")
            
    return f.getvalue()

if __name__ == "__main__":
    import sys
    print(run_tool(sys.argv[1] if len(sys.argv) > 1 else ""))
