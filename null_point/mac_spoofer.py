import subprocess
import re
import io
import contextlib

def change_mac(interface, new_mac):
    print(f"[i] Changing MAC address for {interface} to {new_mac}")
    
    try:
        # Disable/Enable to apply changes
        subprocess.run(["netsh", "interface", "set", "interface", interface, "admin=disable"], check=True, capture_output=True)
        subprocess.run(["netsh", "interface", "set", "interface", interface, "admin=enable"], check=True, capture_output=True)
        
        # Registry modification
        reg_path = r"HKLM\SYSTEM\CurrentControlSet\Control\Class\{4d36e972-e325-11ce-bfc1-08002be10318}\000X"
        subprocess.run(["reg", "add", reg_path, "/v", "NetworkAddress", "/d", new_mac, "/f"], check=True, capture_output=True)
        
        # Apply change
        subprocess.run(["netsh", "interface", "set", "interface", interface, "admin=disable"], check=True, capture_output=True)
        subprocess.run(["netsh", "interface", "set", "interface", interface, "admin=enable"], check=True, capture_output=True)
        print("[+] MAC address modification commands executed.")
    except subprocess.CalledProcessError as e:
        print(f"[!] Error executing command: {e}")

def get_current_mac(interface):
    try:
        result = subprocess.check_output(["getmac", "/v", "/fo", "LIST"], stderr=subprocess.STDOUT)
        mac_address_search_result = re.search(rf"{interface}.*\n\s*Physical Address:\s*([\w-]+)", result.decode(), re.IGNORECASE)
        if mac_address_search_result:
            return mac_address_search_result.group(1).replace("-", "")
        else:
            print("[!] Could not read MAC address.")
            return None
    except Exception as e:
        print(f"[!] Error reading MAC: {e}")
        return None

def run_tool(args_str: str) -> str:
    f = io.StringIO()
    with contextlib.redirect_stdout(f):
        print(f"Null Point: MAC Spoofer\n")
        
        parts = args_str.split(':')
        interface = parts[0] if len(parts) > 0 else ""
        new_mac = parts[1] if len(parts) > 1 else ""
        
        if not interface or not new_mac:
            print("[!] Invalid input format. Expected: interface:mac")
        else:
            current_mac = get_current_mac(interface)
            print(f"[i] Current MAC = {current_mac}")
            
            change_mac(interface, new_mac)
            
            new_mac_check = get_current_mac(interface)
            if new_mac_check == new_mac:
                print(f"[+] MAC address was successfully changed to {new_mac_check}")
            else:
                print("[!] MAC address did not get changed.")
    return f.getvalue()
