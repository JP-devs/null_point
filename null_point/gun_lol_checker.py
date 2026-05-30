import argparse
import shlex

def check_username(username):
    # [Demo]
    return f"[Demo] Checking username: {username}\nExample result: Username '{username}' is available!"

def check_item(item_id):
    # [Demo]
    if not item_id.isdigit():
        return "Error: Item ID must be a number!"
    return f"[Demo] Checking item ID: {item_id}\nExample result: Item #{item_id} costs $10.99 (5 in stock)"

def run_tool(args_str):
    parser = argparse.ArgumentParser(description='Guns.lol Checker Demo', exit_on_error=False)
    subparsers = parser.add_subparsers(dest='command', help='Commands')

    # Username command
    user_parser = subparsers.add_parser('username', help='Check a username')
    user_parser.add_argument('username', help='Username to check')

    # Item command
    item_parser = subparsers.add_parser('item', help='Check an item')
    item_parser.add_argument('item_id', help='Item ID to check')

    try:
        args = parser.parse_args(shlex.split(args_str))
        if args.command == 'username':
            return check_username(args.username)
        elif args.command == 'item':
            return check_item(args.item_id)
        else:
            return "Invalid command. Usage: username <name> | item <id>"
    except Exception as e:
        return f"Error: {e}"
