import requests
import time
import io
import contextlib
from typing import List, Tuple, Optional

def load_proxies(file_path: str) -> List[str]:
    """Load proxies from a file."""
    proxies = []
    try:
        with open(file_path, 'r') as f:
            for line in f:
                proxy = line.strip()
                if proxy:
                    proxies.append(proxy)
    except FileNotFoundError:
        print(f"[!] Error: File {file_path} not found.")
    except Exception as e:
        print(f"[!] Error loading file {file_path}: {e}")
    return proxies

def check_proxy(proxy: str) -> Tuple[bool, Optional[float]]:
    """Check if a proxy is working and measure its response time."""
    url = 'http://www.google.com'
    proxies = {
        'http': f'http://{proxy}',
        'https': f'http://{proxy}',
    }
    try:
        start_time = time.time()
        response = requests.get(url, proxies=proxies, timeout=5)
        response_time = time.time() - start_time
        if response.status_code == 200:
            return True, response_time
    except requests.RequestException:
        pass
    except Exception as e:
        print(f"[!] Unexpected error checking {proxy}: {e}")
    return False, None

def verify_proxies(proxy_list: List[str]) -> None:
    """Verify a list of proxies and print the results."""
    if not proxy_list:
        print("[i] No proxies to verify.")
        return

    for proxy in proxy_list:
        is_working, response_time = check_proxy(proxy)
        if is_working:
            print(f"[+] Proxy {proxy} is working. Response time: {response_time:.2f} seconds.")
        else:
            print(f"[!] Proxy {proxy} is not working.")

def run_tool(args_str: str) -> str:
    f = io.StringIO()
    with contextlib.redirect_stdout(f):
        print(f"Null Point: Proxy Verifier")
        proxies = load_proxies(args_str)
        verify_proxies(proxies)
    return f.getvalue()
