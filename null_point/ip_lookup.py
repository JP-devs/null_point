import requests
import json
import argparse
import io
import contextlib
from null_point_theme import print_banner, print_success, print_error, print_input, print_info

def get_ip_data(ip_address: str):
    apis = [
        ("ip-api.com", f"http://ip-api.com/json/{ip_address}"),
        ("ipinfo.io", f"https://ipinfo.io/{ip_address}/json"),
        ("ipapi.co", f"https://ipapi.co/{ip_address}/json/"),
        ("ipwhois.io", f"https://ipwhois.io/{ip_address}"),
        ("geoip.nekudo.com", f"https://geoip.nekudo.com/api/{ip_address}"),
    ]
    results = {}
    for name, url in apis:
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            results[name] = response.json()
        except Exception as e:
            results[name] = f"Error: {e}"
    return results

def ip_lookup_extreme(ip_address: str):
    """
    Performs an extreme IP lookup and retrieves data from various APIs.
    """
    print_info(f"Lookup for IP Address: {ip_address}")

    apis = [
        ("ip-api.com", f"http://ip-api.com/json/{ip_address}"),
        ("ipinfo.io", f"https://ipinfo.io/{ip_address}/json"),
        ("ipapi.co", f"https://ipapi.co/{ip_address}/json/"),
        ("ipwhois.io", f"https://ipwhois.io/{ip_address}"),
        ("geoip.nekudo.com", f"https://geoip.nekudo.com/api/{ip_address}"),
    ]

    for name, url in apis:
        print_info(f"--- Abfrage von {name} ---")
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            data = response.json()
            print(json.dumps(data, indent=4))
        except requests.exceptions.RequestException as e:
            print_error(f"Error querying {name}: {e}")
        except json.JSONDecodeError:
            print_error(f"Error decoding the JSON response from {name}.")

def run_tool(ip_address: str):
    buffer = io.StringIO()
    with contextlib.redirect_stdout(buffer):
        ip_lookup_extreme(ip_address)
    return buffer.getvalue()

if __name__ == "__main__":
    print_banner("IP Lookup Tool")
    
    parser = argparse.ArgumentParser(description="Perform an extreme IP lookup.")
    parser.add_argument("ip", nargs="?", help="The IP address to investigate")
    args = parser.parse_args()

    ip_to_lookup = args.ip
    if not ip_to_lookup:
        ip_to_lookup = print_input("Enter the IP address you want to investigate: ").strip()

    if ip_to_lookup:
        print(run_tool(ip_to_lookup))
    else:
        print_error("No IP address provided. Exiting.")

