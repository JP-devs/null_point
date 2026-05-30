import requests
import io
import contextlib

def get_user_data(user_id):
    try:
        user_info = requests.get(f"https://users.roblox.com/v1/users/{user_id}", timeout=5).json()
        presence = requests.post("https://presence.roblox.com/v1/presence/users", json={"userIds": [int(user_id)]}, timeout=5).json()
        
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

def run_tool(user_id: str) -> str:
    f = io.StringIO()
    with contextlib.redirect_stdout(f):
        print(f"Null Point: Roblox User ID Info Tool")
        if not user_id.isdigit():
            print("[!] Invalid ID.")
            return f.getvalue()

        print(f"[i] Fetching info for {user_id}...")
        data = get_user_data(user_id)
        
        if data:
            print("[+] --- User Profile ---")
            for key, value in data.items():
                print(f"{key.capitalize()}: {value}")
        else:
            print("[!] Could not retrieve data.")
    return f.getvalue()

