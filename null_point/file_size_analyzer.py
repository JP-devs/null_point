import os
import io
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
            files = []
            for root, _, filenames in os.walk(folder_path):
                for name in filenames:
                    path = os.path.join(root, name)
                    try:
                        files.append((path, os.path.getsize(path)))
                    except:
                        continue
            
            files.sort(key=lambda x: x[1], reverse=True)
            print("Top 10 Largest Files:")
            for path, size in files[:10]:
                print(f"{size / 1024:.2f} KB - {path}")
        except Exception as e:
            print(f"Error analyzing sizes: {e}")
            
    return f.getvalue()

if __name__ == "__main__":
    import sys
    print(run_tool(sys.argv[1] if len(sys.argv) > 1 else ""))
