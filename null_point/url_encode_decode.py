import urllib.parse
import io
from contextlib import redirect_stdout

def run_tool(args_str: str) -> str:
    f = io.StringIO()
    with redirect_stdout(f):
        try:
            if ":" in args_str:
                mode, text = args_str.split(":", 1)
                mode = mode.strip().lower()
                text = text.strip()
                if mode == "enc":
                    print(urllib.parse.quote(text))
                elif mode == "dec":
                    print(urllib.parse.unquote(text))
                else:
                    print("Error: Use 'enc:text' or 'dec:text'")
            else:
                print("Error: Format must be 'enc:text' or 'dec:text'")
        except Exception as e:
            print(f"Error: {e}")
    return f.getvalue()

if __name__ == "__main__":
    import sys
    print(run_tool(sys.argv[1] if len(sys.argv) > 1 else ""))
