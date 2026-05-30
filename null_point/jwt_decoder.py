import base64
import json
import io
from contextlib import redirect_stdout

def run_tool(jwt_token: str) -> str:
    f = io.StringIO()
    with redirect_stdout(f):
        try:
            parts = jwt_token.split('.')
            if len(parts) != 3:
                print("Error: Invalid JWT token format (must have 3 parts).")
                return f.getvalue()
            
            payload_b64 = parts[1]
            # Add padding if needed
            missing_padding = len(payload_b64) % 4
            if missing_padding:
                payload_b64 += '=' * (4 - missing_padding)
            
            decoded = base64.b64decode(payload_b64).decode('utf-8')
            print("JWT Payload:")
            try:
                print(json.dumps(json.loads(decoded), indent=4))
            except:
                print(decoded)
        except Exception as e:
            print(f"Error decoding JWT: {e}")
    return f.getvalue()

if __name__ == "__main__":
    import sys
    print(run_tool(sys.argv[1] if len(sys.argv) > 1 else ""))
