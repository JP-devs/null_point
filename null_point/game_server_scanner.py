import requests
import argparse
import shlex
import concurrent.futures

def get_game_info(universe_id):
    url = f"https://games.roblox.com/v1/games?universeIds={universe_id}"
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json().get("data", [])
        return data[0] if data else None, None
    except Exception as e:
        return None, f"Error fetching game info: {e}"

def get_servers(universe_id, limit=100, cursor=""):
    url = f"https://games.roblox.com/v1/games/{universe_id}/servers/Public"
    params = {"limit": limit, "cursor": cursor}
    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        return response.json(), None
    except Exception as e:
        return None, f"Error fetching servers: {e}"

def scan_server(server):
    try:
        ping_url = f"http://{server['ip']}:{server['port']}/ping"
        response = requests.get(ping_url, timeout=2)
        return response.status_code == 200, server
    except:
        return False, server

def format_server_info(game_info, active_servers, total_servers):
    output = []
    output.append("Game Information:")
    output.append(f"    Name: {game_info.get('name', 'N/A')}")
    output.append(f"    Players: {game_info.get('playing', 0)}/{game_info.get('maxPlayers', 0)}")
    output.append(f"    Active Servers: {len(active_servers)}/{total_servers}")
    
    output.append("Server List:")
    for idx, server in enumerate(active_servers[:10], 1):
        output.append(f"    {idx}. {server['id']}")
        output.append(f"       IP: {server['ip']}:{server['port']}")
        output.append(f"       Players: {server['playing']}/{server['maxPlayers']}")
        output.append(f"       FPS: {server.get('fps', 'N/A')}")
        output.append(f"       Ping: {server.get('ping', 'N/A')}ms")
    
    if len(active_servers) > 10:
        output.append(f"\n    ...and {len(active_servers)-10} more servers")
    return "\n".join(output)

def run_tool(args_str):
    parser = argparse.ArgumentParser(description='Roblox Game Server Scanner', exit_on_error=False)
    parser.add_argument('universe', help='Roblox Universe ID')
    
    try:
        args = parser.parse_args(shlex.split(args_str))
        universe_id = args.universe
        if not universe_id.isdigit():
            return "Error: Invalid Universe ID."
            
        game_info, error = get_game_info(universe_id)
        if error:
            return error
        if not game_info:
            return "Error: Game not found."
            
        servers_data, error = get_servers(universe_id)
        if error:
            return error
        if not servers_data or not servers_data.get("data"):
            return "Error: No servers found."
            
        servers = servers_data["data"]
        active_servers = []
        
        with concurrent.futures.ThreadPoolExecutor(max_workers=20) as executor:
            futures = [executor.submit(scan_server, server) for server in servers]
            for future in concurrent.futures.as_completed(futures):
                is_active, server = future.result()
                if is_active:
                    active_servers.append(server)
        
        return format_server_info(game_info, active_servers, len(servers))
    except Exception as e:
        return f"Error: {e}"

