import requests

def get_public_ip():
    """Get the public IP address of the current connection."""
    try:
        response = requests.get('https://api.ipify.org?format=json', timeout=10)
        response.raise_for_status()
        ip_data = response.json()
        return ip_data['ip']
    except requests.RequestException as e:
        return None

def is_vpn_active(known_non_vpn_ip):
    """Check if the VPN is active by comparing the current public IP with a known non-VPN IP."""
    current_ip = get_public_ip()
    if current_ip is None:
        return False
    return current_ip != known_non_vpn_ip

def run_tool(known_non_vpn_ip):
    """Check the VPN status and return the result as a string."""
    if not known_non_vpn_ip:
        return "Error: No known non-VPN IP address provided."
    
    if is_vpn_active(known_non_vpn_ip):
        return "VPN is active. Your connection is secure."
    else:
        return "VPN is not active. Your connection is not secure."
