import argparse
import io
from contextlib import redirect_stdout
from null_point_theme import print_banner, print_success, print_error

def run_tool(args_str: str) -> str:
    f = io.StringIO()
    with redirect_stdout(f):
        print_banner("Image Metadata Tool")
        # Placeholder for actual library logic (e.g., using PIL)
        print_success(f"Scanning image at: {args_str}")
        print("Metadata: [Width: 1920, Height: 1080, Format: PNG]")
    return f.getvalue()

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("path", nargs='?', help="Image path")
    args = parser.parse_args()
    print(run_tool(args.path or ""))
