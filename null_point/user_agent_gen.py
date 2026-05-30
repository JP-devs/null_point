import io
import random
from contextlib import redirect_stdout
from null_point_theme import print_banner, print_success, print_info

def generate_ua() -> str:
    uas = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
    ]
    return random.choice(uas)

def run_tool(args: str) -> str:
    f = io.StringIO()
    with redirect_stdout(f):
        print_banner("UA Generator")
        print_success(f"Generated UA: {generate_ua()}")
    return f.getvalue()

if __name__ == "__main__":
    print(run_tool(""))
