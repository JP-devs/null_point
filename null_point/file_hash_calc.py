import hashlib
import os
import io
from contextlib import redirect_stdout

def run_tool(file_path: str) -> str:
    f = io.StringIO()
    with redirect_stdout(f):
        if not file_path:
            print("Error: File path is required.")
            return f.getvalue()
        
        if not os.path.exists(file_path):
            print(f"Error: File {file_path} not found.")
            return f.getvalue()
        
        try:
            hashes = {
                "MD5": hashlib.md5(),
                "SHA1": hashlib.sha1(),
                "SHA256": hashlib.sha256()
            }
            
            for name, h in hashes.items():
                with open(file_path, "rb") as rb:
                    while chunk := rb.read(8192):
                        h.update(chunk)
                print(f"{name}: {h.hexdigest()}")
        except Exception as e:
            print(f"Error calculating hashes: {e}")
            
    return f.getvalue()

if __name__ == "__main__":
    import sys
    print(run_tool(sys.argv[1] if len(sys.argv) > 1 else ""))
