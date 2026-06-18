# server.py - Link Tracker with Full Visitor Info

from flask import Flask, request, jsonify
import json
import os
from datetime import datetime
import requests

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

def get_location(ip):
    """Get location from IP using free API"""
    try:
        response = requests.get(f"http://ip-api.com/json/{ip}", timeout=3)
        if response.status_code == 200:
            data = response.json()
            if data.get('status') == 'success':
                return {
                    "city": data.get('city', 'Unknown'),
                    "region": data.get('regionName', 'Unknown'),
                    "country": data.get('country', 'Unknown'),
                    "lat": data.get('lat', 0),
                    "lon": data.get('lon', 0),
                    "isp": data.get('isp', 'Unknown')
                }
    except:
        pass
    return {"city": "Unknown", "region": "Unknown", "country": "Unknown", "lat": 0, "lon": 0, "isp": "Unknown"}

def get_device_info(user_agent):
    """Extract device and browser info from user agent"""
    info = {"device": "Unknown", "os": "Unknown", "browser": "Unknown"}
    
    if not user_agent:
        return info
    
    ua = user_agent.lower()
    
    # Detect OS
    if 'android' in ua:
        info['os'] = 'Android'
    elif 'iphone' in ua or 'ipad' in ua:
        info['os'] = 'iOS'
    elif 'windows' in ua:
        info['os'] = 'Windows'
    elif 'mac' in ua:
        info['os'] = 'macOS'
    elif 'linux' in ua:
        info['os'] = 'Linux'
    
    # Detect Browser
    if 'chrome' in ua and 'edg' not in ua:
        info['browser'] = 'Chrome'
    elif 'firefox' in ua:
        info['browser'] = 'Firefox'
    elif 'safari' in ua and 'chrome' not in ua:
        info['browser'] = 'Safari'
    elif 'edg' in ua:
        info['browser'] = 'Edge'
    elif 'opera' in ua:
        info['browser'] = 'Opera'
    
    # Detect Device Type
    if 'mobile' in ua or 'android' in ua or 'iphone' in ua:
        info['device'] = 'Mobile'
    elif 'tablet' in ua or 'ipad' in ua:
        info['device'] = 'Tablet'
    else:
        info['device'] = 'Desktop'
    
    return info

@app.route('/track/<link_id>')
def track(link_id):
    ip = request.remote_addr
    user_agent = request.headers.get('User-Agent', 'Unknown')
    
    # Get location from IP
    location = get_location(ip)
    
    # Get device info
    device_info = get_device_info(user_agent)
    
    visitor = {
        "id": link_id,
        "ip": ip,
        "user_agent": user_agent,
        "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "referer": request.headers.get('Referer', 'Direct'),
        "location": location,
        "device": device_info,
        "screen": request.headers.get('X-Screen-Info', 'Unknown')
    }
    
    data = load_data()
    data["clicks"].append(visitor)
    save_data(data)
    
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
                table { width: 100%; border-collapse: collapse; font-size: 14px; }
                th, td { padding: 8px; border-bottom: 1px solid #333; text-align: left; }
                th { background: #2979ff; color: #fff; position: sticky; top: 0; }
                td { background: #121624; }
                .live { color: #00e676; }
                .header { text-align: center; margin-bottom: 30px; }
                .count { font-size: 24px; color: #00e676; }
                .container { max-height: 500px; overflow-y: auto; }
                .location { color: #ffb74d; font-size: 12px; }
            </style>
        </head>
        <body>
            <div class="header">
                <h1>📊 LINK TRACKER DASHBOARD</h1>
                <p><span class="live">🔴 LIVE</span> Total Clicks: <span class="count">""" + str(len(clicks)) + """</span></p>
            </div>
            <div class="container">
            <table>
                <tr>
                    <th>#</th>
                    <th>IP</th>
                    <th>Location</th>
                    <th>Device</th>
                    <th>OS</th>
                    <th>Browser</th>
                    <th>Time</th>
                </tr>
    """
    
    for i, click in enumerate(reversed(clicks), 1):
        loc = click.get('location', {})
        device = click.get('device', {})
        location_str = f"{loc.get('city', '?')}, {loc.get('country', '?')}"
        html += f"""
            <tr>
                <td>{i}</td>
                <td>{click.get('ip', 'Unknown')}</td>
                <td class="location">{location_str}</td>
                <td>{device.get('device', '?')}</td>
                <td>{device.get('os', '?')}</td>
                <td>{device.get('browser', '?')}</td>
                <td>{click.get('time', 'Unknown')}</td>
            </tr>
        """
    
    html += """
            </table>
            </div>
            <p style="margin-top: 20px; color: #888;">💡 Refresh to see new clicks</p>
        </body>
    </html>
    """
    return html

@app.route('/api/clicks')
def api_clicks():
    data = load_data()
    return jsonify(data)

if __name__ == '__main__':
    print("""
    ╔══════════════════════════════════════════════════╗
    ║   🔗 LINK TRACKER - STARTED!                    ║
    ║   FULL VISITOR INFO ENABLED                     ║
    ╚══════════════════════════════════════════════════╝
    """)
    app.run(host='0.0.0.0', port=5000, debug=True)
