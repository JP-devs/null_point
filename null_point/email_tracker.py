import requests
import argparse
import sys
import random
import io
import contextlib
from null_point_theme import print_banner, print_success, print_error, print_input, print_info

def run_tool(args_str: str) -> str:
    f = io.StringIO()
    with contextlib.redirect_stdout(f):
        # Run tracking
        email = args_str.strip()
        if not email:
            print_error("Email required.")
            return f.getvalue()
        print_info(f"Tracking {email}...\n")
        sites = [
            ("GitHub", check_github),
        ]
        found_sites = []
        for name, func in sites:
            if check_site(name, func, email):
                found_sites.append(name)
        print_success(f"Found on: {', '.join(found_sites) if found_sites else 'None'}")
    return f.getvalue()

USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"
]

def check_site(name, check_func, email):
    try:
        result = check_func(email)
        if result:
            print_success(f"{name}: Found")
        else:
            print_error(f"{name}: Not Found")
        return result
    except Exception as e:
        print_info(f"{name}: Error - {e}")
        return False

def check_github(email):
    # Publicly available GitHub join check is often rate-limited or blocked
    # This is a basic example
    session = requests.Session()
    headers = {'User-Agent': random.choice(USER_AGENTS)}
    response = session.get("https://github.com/join", params={"user[email]": email}, headers=headers, timeout=5)
    return "already in use" in response.text

def main():
    parser = argparse.ArgumentParser(description="Modern Email Tracker Tool")
    parser.add_argument("email", nargs='?', help="Email address to track")
    args = parser.parse_args()

    print_banner('Email Tracker')

    if not args.email:
        email = print_input("Enter email to check: ").strip()
        if not email:
            print_error("Email required.")
            return
    else:
        email = args.email

    print_info(f"Tracking {email}...\n")
    
    # Due to API changes in many services (especially Twitter/Facebook), 
    # many of these checks are now unreliable or blocked by CAPTCHA/bot protection.
    sites = [
        ("GitHub", check_github),
        # Add more reliable checks here as they are discovered
    ]
    
    found_sites = []
    for name, func in sites:
        if check_site(name, func, email):
            found_sites.append(name)
            
    print_success(f"Found on: {', '.join(found_sites) if found_sites else 'None'}")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        sys.exit(0)
    except Exception as e:
        print_error(f"Error: {e}")
        sys.exit(1)

