import requests
from bs4 import BeautifulSoup
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
            soup = BeautifulSoup(response.text, 'xml')
            urls = [loc.text for loc in soup.find_all('loc')]
            if urls:
                for u in urls:
                    print(u)
            else:
                print("No URLs found in sitemap.")
        except Exception as e:
            print(f"Error parsing sitemap: {e}")
            
    return f.getvalue()

if __name__ == "__main__":
    import sys
    print(run_tool(sys.argv[1] if len(sys.argv) > 1 else ""))
