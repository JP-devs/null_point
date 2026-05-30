from colorama import init, Fore, Style

# Initialize colorama
init(autoreset=True)

def print_banner(tool_name):
    print(f"{Fore.CYAN}Null Point: {tool_name}{Style.RESET_ALL}\n")

def print_success(message):
    print(f"{Fore.GREEN}[+] {message}{Style.RESET_ALL}")

def print_error(message):
    print(f"{Fore.RED}[!] {message}{Style.RESET_ALL}")

def print_input(prompt):
    return input(f"{Fore.CYAN}[?] {prompt}{Style.RESET_ALL}")

def print_info(message):
    print(f"{Fore.BLUE}[i] {message}{Style.RESET_ALL}")

import re

def strip_ansi(text):
    ansi_escape = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')
    return ansi_escape.sub('', text)
