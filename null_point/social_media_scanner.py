import argparse
import requests
import threading
import time
from queue import Queue
from null_point_theme import print_banner, print_success, print_error, print_input, print_info
from typing import List, Tuple, Dict

# Thread-safe Data structures
found_accounts: List[Tuple[str, str]] = []
lock = threading.Lock()
queue = Queue()

def check_url(platform: str, url: str, username: str) -> None:
    full_url = url.format(username)
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
        }
        
        # Timeout reduced to 5 seconds (from 10)
        response = requests.get(full_url, headers=headers, timeout=5)
        
        if response.status_code == 200:
            with lock:
                found_accounts.append((platform, full_url))
        # Some platforms return different status codes for existing profiles
        elif response.status_code in [301, 302, 403]:
            with lock:
                found_accounts.append((platform, full_url))
    
    except requests.exceptions.RequestException:
        pass
    except Exception as e:
        print_error(f"Error checking {platform}: {e}")

def worker() -> None:
    while True:
        item = queue.get()
        if item is None:
            break
        platform, url, username = item
        check_url(platform, url, username)
        queue.task_done()

def check_username(username: str, thread_count: int = 20) -> List[Tuple[str, str]]:
    print_info(f"Checking username '{username}' across {len(PLATFORMS)} platforms...\n")
    
    # Thread-Pool create
    threads = []
    for _ in range(thread_count):
        t = threading.Thread(target=worker)
        t.start()
        threads.append(t)
    
    # Put jobs into the queue
    for platform, url in PLATFORMS.items():
        queue.put((platform, url, username))
    
    # Wait for completion
    queue.join()
    
    # Stop worker threads
    for _ in range(thread_count):
        queue.put(None)
    for t in threads:
        t.join()
    
    return found_accounts

def print_results(found_accounts: List[Tuple[str, str]]) -> None:
    if found_accounts:
        print_success("Found accounts:")
        for platform, url in sorted(found_accounts, key=lambda x: x[0]):
            print(f"  • {platform}: {url}")
    else:
        print_error("No accounts found with this username.")

def run_tool(username: str) -> str:
    """Callable function for the screen tool"""
    global found_accounts
    found_accounts = []
    found = check_username(username)
    
    if found:
        result = "Found accounts:\n"
        for platform, url in sorted(found, key=lambda x: x[0]):
            result += f"  • {platform}: {url}\n"
        return result
    else:
        return "No accounts found with this username."

