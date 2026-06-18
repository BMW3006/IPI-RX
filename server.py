# server.py - Link Tracker (Simple & Working)

from flask import Flask, request, jsonify
import json
import os
from datetime import datetime

app = Flask(__name__)
DATA_FILE = "clicks.json"

def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r') as f:
            return json.load(f)
    return {"clicks": []}

def save_data(data):
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f, indent=2)

@app.route('/track/<link_id>')
def track(link_id):
    visitor = {
        "id": link_id,
        "ip": request.remote_addr,
        "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "user_agent": request.headers.get('User-Agent', 'Unknown')
    }
    
    data = load_data()
    data["clicks"].append(visitor)
    save_data(data)
    
    return """
    <html>
        <body style="background:#0a0c15;color:white;text-align:center;padding:50px;">
            <h1>✅ Click Recorded!</h1>
            <p>Your visit has been recorded.</p>
        </body>
    </html>
    """

@app.route('/dashboard')
def dashboard():
    data = load_data()
    clicks = data["clicks"]
    
    html = "<html><head><title>Dashboard</title></head><body style='background:#0a0c15;color:white;padding:20px;'>"
    html += f"<h1>📊 Total Clicks: {len(clicks)}</h1><table border='1' style='width:100%;'>"
    html += "<tr><th>#</th><th>IP</th><th>Time</th><th>User Agent</th></tr>"
    
    for i, click in enumerate(reversed(clicks), 1):
        html += f"<tr><td>{i}</td><td>{click.get('ip', '?')}</td><td>{click.get('time', '?')}</td><td>{click.get('user_agent', '?')[:50]}</td></tr>"
    
    html += "</table></body></html>"
    return html

@app.route('/api/clicks')
def api_clicks():
    return jsonify(load_data())

if __name__ == '__main__':
    print("✅ Server Running on http://0.0.0.0:5000")
    app.run(host='0.0.0.0', port=5000, debug=True)
