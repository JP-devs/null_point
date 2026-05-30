import os
import io
from collections import defaultdict
from contextlib import redirect_stdout

def run_tool(folder_path: str) -> str:
    f = io.StringIO()
    with redirect_stdout(f):
        if not folder_path:
            print("Error: Folder path is required.")
            return f.getvalue()
        
        if not os.path.isdir(folder_path):
            print(f"Error: {folder_path} is not a valid directory.")
            return f.getvalue()
        
        try:
            hashes = defaultdict(list)
            for root, _, files in os.walk(folder_path):
                for name in files:
                    path = os.path.join(root, name)
                    try:
                        with open(path, "rb") as rb:
                            # Use first 1MB for speed, then full if needed (simplified here)
                            content = rb.read(1024*1024)
                            hashes[hash(content)].append(path)
                    except:
                        continue
            
            duplicates = [paths for paths in hashes.values() if len(paths) > 1]
            if not duplicates:
                print("No duplicate files found.")
            else:
                for group in duplicates:
                    print(f"Duplicate Group: {group}")
        except Exception as e:
            print(f"Error finding duplicates: {e}")
            
    return f.getvalue()

if __name__ == "__main__":
    import sys
    print(run_tool(sys.argv[1] if len(sys.argv) > 1 else ""))
