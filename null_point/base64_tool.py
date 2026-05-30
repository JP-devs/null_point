import argparse
import base64
import io
from contextlib import redirect_stdout
from null_point_theme import print_banner, print_success, print_error

def encode_base64(data: str) -> str:
    return base64.b64encode(data.encode()).decode()

def decode_base64(data: str) -> str:
    try:
        return base64.b64decode(data.encode()).decode()
    except Exception as e:
        return f"Error: {e}"

def run_tool(args_str: str) -> str:
    f = io.StringIO()
    with redirect_stdout(f):
        print_banner("Base64 Tool")
        # Logic: expect "encode|data" or "decode|data"
        if "|" in args_str:
            mode, data = args_str.split("|", 1)
            if mode == "encode":
                print_success(f"Encoded: {encode_base64(data)}")
            elif mode == "decode":
                print_success(f"Decoded: {decode_base64(data)}")
            else:
                print_error("Invalid mode. Use 'encode|data' or 'decode|data'")
        else:
            print_error("Invalid format. Use 'encode|data' or 'decode|data'")
    return f.getvalue()

if __name__ == "__main__":
    # For CLI
    print(run_tool("encode|hello world"))
