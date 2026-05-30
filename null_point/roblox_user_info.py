import requests

def get_user_data(identifier):
    # Determine if input is ID or Username
    try:
        if identifier.isdigit():
            user_id = identifier
        else:
            resp = requests.post("https://users.roblox.com/v1/usernames/users", 
                                 json={"usernames": [identifier]}, timeout=5).json()
            user_id = resp["data"][0]["id"]
        
        user_info = requests.get(f"https://users.roblox.com/v1/users/{user_id}", timeout=5).json()
        presence = requests.post("https://presence.roblox.com/v1/presence/users", 
                                 json={"userIds": [int(user_id)]}, timeout=5).json()
        
        presence_data = presence.get("userPresences", [{}])[0]
        
        return {
            "name": user_info.get("name"),
            "display": user_info.get("displayName"),
            "created": user_info.get("created"),
            "presence": presence_data.get("userPresenceType"),
            "banned": user_info.get("isBanned")
        }
    except Exception as e:
        return None

def run_tool(identifier: str) -> str:
    """Callable function for the screen tool"""
    data = get_user_data(identifier)
    if data:
        result = "--- User Profile ---\n"
        for key, value in data.items():
            result += f"{key.capitalize()}: {value}\n"
        return result
    else:
        return "Could not retrieve data."

