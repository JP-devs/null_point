import os

screens_dir = r'D:\My-tools\Null-Point-Main\null_point\screens'
for filename in os.listdir(screens_dir):
    if filename.endswith('_screen.py'):
        path = os.path.join(screens_dir, filename)
        with open(path, 'r') as f:
            content = f.read()
        
        # Replace the problematic path with "../theme.css"
        new_content = content.replace('CSS_PATH = os.path.join(os.path.dirname(__file__), "..", "theme.css")', 'CSS_PATH = "../theme.css"')
        
        # Also catch just in case it was a raw string
        new_content = new_content.replace("CSS_PATH = os.path.join(os.path.dirname(__file__), '..', 'theme.css')", 'CSS_PATH = "../theme.css"')
        
        # Remove unused imports if they exist
        if 'import os' in new_content and 'os.path' not in new_content:
            new_content = new_content.replace('import os', '')
            
        with open(path, 'w') as f:
            f.write(new_content)
print("Files updated successfully.")
