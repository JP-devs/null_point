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
            robots_url = url.rstrip('/') + '/robots.txt'
            response = requests.get(robots_url, timeout=5)
            if response.status_code == 200:
                print(response.text)
            else:
                print(f"Robots.txt not found (HTTP {response.status_code})")
        except Exception as e:
            print(f"Error fetching robots.txt: {e}")
            
    return f.getvalue()

if __name__ == "__main__":
    import sys
    print(run_tool(sys.argv[1] if len(sys.argv) > 1 else ""))
