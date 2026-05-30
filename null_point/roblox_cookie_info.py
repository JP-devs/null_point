import requests

def get_roblox_user_info(cookie):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
        "Cookie": f".ROBLOSECURITY={cookie}"
    }
    
    try:
        response = requests.get("https://www.roblox.com/mobileapi/userinfo", headers=headers, timeout=5)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        return None

def run_tool(cookie):
    if not cookie:
        return "Error: Cookie required."
    
    info = get_roblox_user_info(cookie)
    
    if info:
        return (
            "--- User Profile ---\n"
            f"Username: {info.get('UserName')}\n"
            f"User ID: {info.get('UserID')}\n"
            f"Robux: {info.get('RobuxBalance')}\n"
            f"Premium: {'Yes' if info.get('IsPremium') else 'No'}"
        )
    else:
        return "Error: Invalid cookie or connection error."
