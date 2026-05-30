import requests
import json
import io
import contextlib
import os
from datetime import datetime
from prettytable import PrettyTable

class SteamOSINT:
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = "https://api.steampowered.com"
        
    def search_user(self, username):
        """Search for a Steam user by name"""
        url = f"{self.base_url}/ISteamUser/ResolveVanityURL/v1/"
        params = {
            'key': self.api_key,
            'vanityurl': username
        }
        
        try:
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            if data.get('response', {}).get('success') == 1:
                steam_id = data['response']['steamid']
                return self.get_user_details(steam_id)
            else:
                return {"error": "User not found"}
                
        except requests.exceptions.RequestException as e:
            return {"error": f"API request failed: {str(e)}"}
    
    def get_user_details(self, steam_id):
        """Get detailed information about a Steam user"""
        url = f"{self.base_url}/ISteamUser/GetPlayerSummaries/v2/"
        params = {
            'key': self.api_key,
            'steamids': steam_id
        }
        
        try:
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            if data.get('response', {}).get('players'):
                return data['response']['players'][0]
            else:
                return {"error": "No user details found"}
                
        except requests.exceptions.RequestException as e:
            return {"error": f"API request failed: {str(e)}"}
    
    def display_results(self, user_data):
        """Display the user information in a formatted table"""
        if 'error' in user_data:
            print(f"[!] Error: {user_data['error']}")
            return
            
        print("[+] Steam Account Information Found:")
        table = PrettyTable()
        table.field_names = ["Field", "Value"]
        table.align["Field"] = "l"
        table.align["Value"] = "l"
        
        # Add basic information
        table.add_row(["SteamID", user_data.get('steamid', 'N/A')])
        table.add_row(["Username", user_data.get('personaname', 'N/A')])
        table.add_row(["Profile URL", user_data.get('profileurl', 'N/A')])
        table.add_row(["Account Created", self.format_timestamp(user_data.get('timecreated', 0))])
        table.add_row(["Last Logoff", self.format_timestamp(user_data.get('lastlogoff', 0))])
        table.add_row(["Country", user_data.get('loccountrycode', 'N/A')])
        table.add_row(["State/Province", user_data.get('locstatecode', 'N/A')])
        table.add_row(["City", user_data.get('loccityid', 'N/A')])
        table.add_row(["Profile Visibility", "Public" if user_data.get('communityvisibilitystate', 1) == 3 else "Private"])
        
        print(table)
        
        # Add avatar URLs if available
        print("[+] Avatar URLs:")
        print(f"Small: {user_data.get('avatar', 'N/A')}")
        print(f"Medium: {user_data.get('avatarmedium', 'N/A')}")
        print(f"Large: {user_data.get('avatarfull', 'N/A')}")
        
    def format_timestamp(self, timestamp):
        """Convert Unix timestamp to readable date"""
        if timestamp == 0:
            return "N/A"
        return datetime.utcfromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S UTC')

def run_tool(args_str: str) -> str:
    # Expecting args_str to be "api_key,username"
    try:
        api_key, username = args_str.split(',')
    except ValueError:
        return "[!] Error: Invalid arguments. Expected 'api_key,username'"

    f = io.StringIO()
    with contextlib.redirect_stdout(f):
        print(f"Null Point: Steam OSINT Tool")
        
        tool = SteamOSINT(api_key)
        
        print(f"[i] Searching for Steam user: {username}")
        user_data = tool.search_user(username)
        tool.display_results(user_data)
    return f.getvalue()

