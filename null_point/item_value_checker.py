import io
import sys
from contextlib import redirect_stdout
import requests
import json
import argparse
import shlex
from datetime import datetime

def get_item_id(item_name):
    url = "https://catalog.roblox.com/v1/search/items"
    params = {"category": "All", "limit": 10, "keyword": item_name}
    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        items = response.json().get("data", [])
        if items:
            return items[0].get("id"), None
        return None, "Item not found"
    except Exception as e:
        return None, str(e)

from concurrent.futures import ThreadPoolExecutor, as_completed

def get_item_details(item_id):
    sources = {
        "roblox": f"https://economy.roblox.com/v2/assets/{item_id}/details",
        "rolimons": f"https://www.rolimons.com/itemapi/itemdetails",
        "rblx_trade": f"https://rblx.trade/api/v2/items/{item_id}"
    }
    data = {}
    errors = []
    
    def fetch(name, url):
        try:
            resp = requests.get(url, timeout=3)
            if resp.status_code == 200:
                return name, resp.json(), None
            return name, None, f"HTTP {resp.status_code}"
        except Exception as e:
            return name, None, str(e)

    with ThreadPoolExecutor(max_workers=3) as executor:
        futures = [executor.submit(fetch, name, url) for name, url in sources.items()]
        for future in as_completed(futures):
            name, result, err = future.result()
            if result:
                data[name] = result
            if err:
                errors.append(f"{name}: {err}")
    
    return data, errors if errors else None

def format_price(price):
    if not price:
        return "N/A"
    return f"R$ {price:,}"

def format_item_info(item_id, item_name, data, errors):
    output = []
    roblox_data = data.get("roblox", {})
    rolimons_data = data.get("rolimons", [])
    rblx_trade_data = data.get("rblx_trade", {})
    
    output.append("Basic Information:")
    output.append(f"    Name: {item_name}")
    output.append(f"    Item ID: {item_id}")
    output.append(f"    Asset Type: {roblox_data.get('AssetType', 'N/A')}")
    output.append(f"    Creator: {roblox_data.get('Creator', {}).get('Name', 'N/A')}")
    
    output.append("Current Values:")
    output.append(f"    Roblox Price: {format_price(roblox_data.get('Price'))}")
    output.append(f"    Roblox Resale: {format_price(roblox_data.get('Remaining', {}).get('ResalePrice'))}")
    
    if rolimons_data:
        output.append("Community Values (Rolimons):")
        output.append(f"    Value: {format_price(rolimons_data[2])}")
        output.append(f"    Demand: {rolimons_data[5]}/5")
        output.append(f"    Trend: {rolimons_data[6]}")
    
    if rblx_trade_data:
        recent_sales = rblx_trade_data.get("recentSales", [])
        if recent_sales:
            output.append("Recent Sales (RBX.Trade):")
            for sale in recent_sales[:3]:
                date = datetime.fromtimestamp(sale["timestamp"]).strftime('%Y-%m-%d')
                output.append(f"    • {date}: {format_price(sale['price'])} (Qty: {sale['quantity']})")
    
    if errors:
        output.append("Partial data with errors:")
        for error in errors:
            output.append(f"    {error}")
            
    return "\n".join(output)

def run_tool(args_str: str) -> str:
    f = io.StringIO()
    with redirect_stdout(f):
        parser = argparse.ArgumentParser(description="Check Roblox item values.", exit_on_error=False)
        parser.add_argument("item", help="Item name or ID")
        
        try:
            args = parser.parse_args(shlex.split(args_str))
            item_name = args.item
            
            if item_name.isdigit():
                item_id = item_name
                name_to_display = "Unknown"
            else:
                item_id, error = get_item_id(item_name)
                if error:
                    print(f"Error: {error}")
                    return f.getvalue()
                name_to_display = item_name
            
            data, errors = get_item_details(item_id)
            print(format_item_info(item_id, name_to_display, data, errors))
        except Exception as e:
            print(f"Error: {e}")
    return f.getvalue()

if __name__ == "__main__":
    if len(sys.argv) > 1:
        print(run_tool(sys.argv[1]))
    else:
        print("Error: No input provided.")
