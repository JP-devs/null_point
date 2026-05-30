import requests
from datetime import datetime
from collections import Counter
from typing import Tuple, Optional, Any, Dict, List
import io
import contextlib

def get_user_id(username: str) -> Tuple[Optional[str], Optional[str]]:
    url = "https://users.roblox.com/v1/usernames/users"
    payload = {"usernames": [username]}
    try:
        response = requests.post(url, json=payload, timeout=5)
        if response.status_code == 200:
            data = response.json().get("data", [])
            if data:
                return str(data[0].get("id")), None
        return None, "User not found"
    except Exception as e:
        return None, str(e)

from concurrent.futures import ThreadPoolExecutor, as_completed

def fetch_player_data(user_id: str) -> Tuple[Dict[str, Any], Optional[List[str]]]:
    endpoints = {
        "profile": f"https://users.roblox.com/v1/users/{user_id}",
        "presence": f"https://presence.roblox.com/v1/presence/users",
        "friends": f"https://friends.roblox.com/v1/users/{user_id}/friends",
        "followers": f"https://friends.roblox.com/v1/users/{user_id}/followers",
        "following": f"https://friends.roblox.com/v1/users/{user_id}/followings",
        "groups": f"https://groups.roblox.com/v1/users/{user_id}/groups/roles",
        "badges": f"https://accountinformation.roblox.com/v1/users/{user_id}/roblox-badges",
        "games": f"https://games.roblox.com/v2/users/{user_id}/games?accessFilter=2&limit=10",
        "inventory": f"https://inventory.roblox.com/v1/users/{user_id}/items/collectibles?limit=10"
    }
    
    data = {}
    errors = []
    
    def fetch_url(name, url):
        try:
            if name == "presence":
                resp = requests.post(url, json={"userIds": [user_id]}, timeout=3)
                if resp.status_code == 200:
                    return name, resp.json().get("userPresences", [{}])[0], None
            else:
                resp = requests.get(url, timeout=3)
                if resp.status_code == 200:
                    return name, resp.json(), None
                elif resp.status_code == 403:
                    return name, None, f"Access denied to {name} (private)"
        except Exception as e:
            return name, None, str(e)
        return name, None, "Unknown error"

    with ThreadPoolExecutor(max_workers=5) as executor:
        future_to_url = {executor.submit(fetch_url, name, url): name for name, url in endpoints.items()}
        for future in as_completed(future_to_url):
            name, result, err = future.result()
            if result:
                data[name] = result
            if err:
                errors.append(err)
    
    return data, errors if errors else None

def analyze_friends(friends_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    if not friends_data or not friends_data.get("data"):
        return None
    
    friends = friends_data["data"]
    creation_dates = [friend.get("created") for friend in friends if friend.get("created")]
    
    if not creation_dates:
        return None
    
    oldest_friend = min(creation_dates)
    newest_friend = max(creation_dates)
    
    try:
        avg_friend_age = (datetime.now() - datetime.strptime(oldest_friend, "%Y-%m-%dT%H:%M:%S.%fZ")).days / len(creation_dates)
    except ValueError:
        avg_friend_age = 0
        
    return {
        "count": len(friends),
        "oldest": oldest_friend,
        "newest": newest_friend,
        "avg_age_days": round(avg_friend_age, 1)
    }

def analyze_groups(groups_data: Dict[str, Any], user_id: str) -> Optional[Dict[str, Any]]:
    if not groups_data or not groups_data.get("data"):
        return None
    
    groups = groups_data["data"]
    group_roles = [group["role"]["name"] for group in groups if group.get("role")]
    role_counter = Counter(group_roles)
    
    return {
        "count": len(groups),
        "common_roles": role_counter.most_common(3),
        "premium": any(str(group.get("group", {}).get("owner", {}).get("id")) == user_id for group in groups)
    }

def format_analysis(user_id: str, data: Dict[str, Any], errors: Optional[List[str]]) -> str:
    output = io.StringIO()
    profile = data.get("profile", {})
    presence = data.get("presence", {})
    friends = data.get("friends", {})
    groups = data.get("groups", {})
    badges = data.get("badges", [])
    games = data.get("games", {}).get("data", [])
    
    output.write("Basic Profile Information:\n")
    output.write(f"    Username: {profile.get('name', 'N/A')}\n")
    output.write(f"    Display Name: {profile.get('displayName', 'N/A')}\n")
    output.write(f"    User ID: {profile.get('id', 'N/A')}\n")
    output.write(f"    Account Age: {profile.get('created', 'N/A')}\n")
    output.write(f"    Verified: {profile.get('hasVerifiedBadge', False)}\n")
    output.write(f"    Status: {presence.get('userPresenceType', 'N/A')}\n")
    output.write(f"    Last Online: {presence.get('lastOnline', 'N/A')}\n")
    
    friends_analysis = analyze_friends(friends)
    if friends_analysis:
        output.write("Friends Analysis:\n")
        output.write(f"    Friend Count: {friends_analysis['count']}\n")
        output.write(f"    Oldest Friend: {friends_analysis['oldest']}\n")
        output.write(f"    Newest Friend: {friends_analysis['newest']}\n")
        output.write(f"    Avg Friend Age: {friends_analysis['avg_age_days']} days\n")
    
    groups_analysis = analyze_groups(groups, user_id)
    if groups_analysis:
        output.write("Groups Analysis:\n")
        output.write(f"    Group Count: {groups_analysis['count']}\n")
        output.write(f"    Common Roles: {', '.join([f'{role} ({count})' for role, count in groups_analysis['common_roles']])}\n")
        output.write(f"    Owns Groups: {groups_analysis['premium']}\n")
    
    if badges:
        output.write("Badges:\n")
        for badge in badges[:5]:
            output.write(f"    • {badge.get('name', 'N/A')}\n")
        if len(badges) > 5:
            output.write(f"    • ...and {len(badges)-5} more\n")
    
    if games:
        output.write("Recently Played Games:\n")
        for game in games[:3]:
            output.write(f"    • {game.get('name', 'N/A')} (Plays: {game.get('placeVisits', 'N/A')})\n")
        if len(games) > 3:
            output.write(f"    • ...and {len(games)-3} more\n")
    
    output.write("Profile Links:\n")
    output.write(f"    • Web Profile: https://www.roblox.com/users/{user_id}/profile\n")
    
    if errors:
        output.write("Partial data with errors:\n")
        for error in errors:
            output.write(f"{error}\n")
            
    return output.getvalue()

def run_tool(identifier: str) -> str:
    if identifier.isdigit():
        user_id = identifier
    else:
        user_id, error = get_user_id(identifier)
        if error:
            return f"Error: {error}"
            
    data, errors = fetch_player_data(user_id)
    return format_analysis(user_id, data, errors)
