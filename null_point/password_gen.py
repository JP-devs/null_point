import argparse
import io
import random
import string
from contextlib import redirect_stdout
from null_point_theme import print_banner, print_success, print_info

def generate_password(length: int = 16) -> str:
    chars = string.ascii_letters + string.digits + string.punctuation
    return ''.join(random.choice(chars) for _ in range(length))

def run_tool(args_str: str) -> str:
    f = io.StringIO()
    with redirect_stdout(f):
        print_banner("Password Generator")
        try:
            length = int(args_str) if args_str.isdigit() else 16
        except:
            length = 16
        password = generate_password(length)
        print_success(f"Generated Password ({length} chars): {password}")
    return f.getvalue()

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("length", nargs='?', default="16")
    args = parser.parse_args()
    print(run_tool(args.length))
