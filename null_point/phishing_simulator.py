import argparse
import threading
from flask import Flask, render_template
import io
import contextlib

app = Flask(__name__)

@app.route('/')
def dashboard():
    campaigns = ["Campaign 1", "Campaign 2", "Campaign 3"]
    return render_template('dashboard.html', campaigns=campaigns)

def run_tool(args_str: str) -> str:
    f = io.StringIO()
    with contextlib.redirect_stdout(f):
        print("Null Point: Phishing Simulator")
        
        # Simplified parsing
        parts = args_str.split(':')
        host = parts[0] if len(parts) > 0 else '127.0.0.1'
        port = int(parts[1]) if len(parts) > 1 else 5000
        
        print(f"[+] Starting phishing simulator on http://{host}:{port}")
        try:
            threading.Thread(target=app.run, kwargs={"host": host, "port": port, "debug": False, "use_reloader": False}).start()
        except Exception as e:
            print(f"[!] Error starting server: {e}")
    return f.getvalue()
