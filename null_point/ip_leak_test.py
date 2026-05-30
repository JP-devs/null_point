import requests
import io
from contextlib import redirect_stdout

def run_tool(args_str: str) -> str:
    f = io.StringIO()
    with redirect_stdout(f):
        try:
            ip = requests.get("https://api.ipify.org", timeout=5).text
            print(f"Your Public IP: {ip}")
            
            # Check if it's a known VPN/Proxy (Simple check via a free API)
            proxy_check = requests.get(f"https://ipapi.co/{ip}/json/", timeout=5).json()
            org = proxy_check.get("org", "Unknown")
            print(f"ISP/Organization: {org}")
            
            if "VPN" in org or "Hosting" in org or "Cloud" in org:
                print("\n[!] Potential Proxy/VPN detected.")
            else:
                print("\n[+] No obvious proxy detected.")
        except Exception as e:
            print(f"Error: {e}")
    return f.getvalue()

if __name__ == "__main__":
    import sys
    print(run_tool(sys.argv[1] if len(sys.argv) > 1 else ""))
