# server.py - Link Tracker Backend
# Captures and stores click data from users

from flask import Flask, request, jsonify
import json
import os
from datetime import datetime

app = Flask(__name__)

# Data storage file
DATA_FILE = "clicks.json"

# Load existing data
def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r') as f:
            return json.load(f)
    return {"clicks": []}

# Save data
def save_data(data):
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f, indent=2)

# Tracking endpoint (the link you send to others)
@app.route('/track/<link_id>')
def track(link_id):
    # Get visitor information
    visitor = {
        "id": link_id,
        "ip": request.remote_addr,
        "user_agent": request.headers.get('User-Agent'),
        "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "referer": request.headers.get('Referer', 'Direct')
    }
    
    # Save data
    data = load_data()
    data["clicks"].append(visitor)
    save_data(data)
    
    # Show confirmation page
    return """
    <html>
        <head><title>Link Tracker</title></head>
        <body style="font-family: Arial; text-align: center; padding: 50px; background: #0a0c15; color: white;">
            <h1>✅ Link Clicked!</h1>
            <p>Your visit has been recorded.</p>
            <p style="color: #888; font-size: 14px;">Redirecting...</p>
            <script>
                setTimeout(() => window.history.back(), 2000);
            </script>
        </body>
    </html>
    """

# Dashboard to view all clicks
@app.route('/dashboard')
def dashboard():
    data = load_data()
    clicks = data["clicks"]
    
    html = """
    <html>
        <head>
            <title>Link Tracker Dashboard</title>
            <style>
                body { font-family: monospace; background: #0a0c15; color: #fff; padding: 20px; }
                table { width: 100%; border-collapse: collapse; }
                th, td { padding: 10px; border-bottom: 1px solid #333; text-align: left; }
                th { background: #2979ff; color: #fff; }
                td { background: #121624; }
                .live { color: #00e676; }
                .header { text-align: center; margin-bottom: 30px; }
                .count { font-size: 24px; color: #00e676; }
            </style>
        </head>
        <body>
            <div class="header">
                <h1>📊 LINK TRACKER DASHBOARD</h1>
                <p><span class="live">🔴 LIVE</span> Total Clicks: <span class="count">""" + str(len(clicks)) + """</span></p>
            </div>
            <table>
                <tr>
                    <th>#</th>
                    <th>IP Address</th>
                    <th>Time</th>
                    <th>Device / Browser</th>
                    <th>Link ID</th>
                </tr>
    """
    
    for i, click in enumerate(reversed(clicks), 1):
        device = click.get('user_agent', 'Unknown')[:50] + '...' if len(click.get('user_agent', '')) > 50 else click.get('user_agent', 'Unknown')
        html += f"""
            <tr>
                <td>{i}</td>
                <td>{click.get('ip', 'Unknown')}</td>
                <td>{click.get('time', 'Unknown')}</td>
                <td>{device}</td>
                <td>{click.get('id', 'Unknown')}</td>
            </tr>
        """
    
    html += """
            </table>
            <p style="margin-top: 20px; color: #888;">💡 Refresh to see new clicks</p>
        </body>
    </html>
    """
    return html

# API endpoint to get data as JSON (for tracker.py)
@app.route('/api/clicks')
def api_clicks():
    data = load_data()
    return jsonify(data)

if __name__ == '__main__':
    print("""
    ╔══════════════════════════════════════════════════╗
    ║   🔗 LINK TRACKER - STARTED!                    ║
    ╠══════════════════════════════════════════════════╣
    ║   Send this link to someone:                    ║
    ║   http://localhost:5000/track/your_link_id      ║
    ║                                                  ║
    ║   Dashboard:                                    ║
    ║   http://localhost:5000/dashboard               ║
    ╚══════════════════════════════════════════════════╝
    """)
    app.run(host='0.0.0.0', port=5000, debug=True)
