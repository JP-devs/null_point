import requests
import io
from contextlib import redirect_stdout

def run_tool(url: str) -> str:
    f = io.StringIO()
    with redirect_stdout(f):
        if not url:
            print("Error: URL is required.")
            return f.getvalue()
        
        if not url.startswith("http"):
            url = "http://" + url
            
        try:
            response = requests.get(url, timeout=5)
            headers = response.headers
            for key, value in headers.items():
                print(f"{key}: {value}")
        except Exception as e:
            print(f"Error fetching headers: {e}")
            
    return f.getvalue()

if __name__ == "__main__":
    import sys
    print(run_tool(sys.argv[1] if len(sys.argv) > 1 else ""))
