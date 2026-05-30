import requests
import io
import time
from contextlib import redirect_stdout
from null_point_theme import print_banner, print_success, print_error, print_info

# Using Mail.gw API - requires two-step process: account creation + inbox check
BASE_URL = "https://api.mail.gw"

def create_account():
    try:
        # 1. Create a domain
        domains = requests.get(f"{BASE_URL}/domains", timeout=5).json()['hydra:member']
        domain = domains[0]['domain']
        
        # 2. Generate a random username
        username = f"test_{int(time.time())}"
        address = f"{username}@{domain}"
        
        # 3. Create account
        response = requests.post(f"{BASE_URL}/accounts", json={"address": address, "password": "password"}, timeout=5)
        response.raise_for_status()
        
        return address, "password"
    except Exception as e:
        print_error(f"Error creating account: {e}")
        return None, None

def check_inbox(address, password):
    try:
        # Get token
        token = requests.post(f"{BASE_URL}/token", json={"address": address, "password": "password"}, timeout=5).json()['token']
        headers = {"Authorization": f"Bearer {token}"}
        
        # Get messages
        messages = requests.get(f"{BASE_URL}/messages", headers=headers, timeout=5).json()
        return messages['hydra:member']
    except Exception as e:
        print_error(f"Error checking inbox: {e}")
        return []

def run_tool(args: str) -> str:
    f = io.StringIO()
    with redirect_stdout(f):
        print_banner("Temp Mail Generator (Mail.gw)")
        email, password = create_account()
        if email:
            print_success(f"Generated Email: {email}")
            print_info("Checking for messages in 5 seconds...")
            time.sleep(5)
            messages = check_inbox(email, password)
            if messages:
                print_info(f"Inbox: {messages}")
            else:
                print_info("Inbox is empty.")
        else:
            print_error("Failed to generate email.")
    return f.getvalue()

if __name__ == "__main__":
    print(run_tool(""))
