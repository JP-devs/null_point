import requests
import io
from contextlib import redirect_stdout

def run_tool(domain: str) -> str:
    f = io.StringIO()
    with redirect_stdout(f):
        if not domain:
            print("Error: Domain is required.")
            return f.getvalue()
        
        try:
            url = f"https://crt.sh/?q={domain}&output=json"
            response = requests.get(url, timeout=10)
            if response.status_code == 200:
                import json
                data = response.json()
                for entry in data:
                    print(f"Common Name: {entry['common_name']} | Name Value: {entry['name_value']}")
            else:
                print(f"CRT.sh error: HTTP {response.status_code}")
        except Exception as e:
            print(f"Error: {e}")
            
    return f.getvalue()

if __name__ == "__main__":
    import sys
    print(run_tool(sys.argv[1] if len(sys.argv) > 1 else ""))
