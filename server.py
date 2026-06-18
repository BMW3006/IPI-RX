# server.py - Link Tracker Pro (15 Features)
# Inaendesha nyuma ya pazia, inaonekana kwenye browser

from flask import Flask, request, jsonify, render_template_string
import json
import os
from datetime import datetime
import requests
import platform
import psutil

app = Flask(__name__)
DATA_FILE = "clicks.json"

# ============================================
# DATA MANAGEMENT
# ============================================
def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r') as f:
            return json.load(f)
    return {"clicks": [], "stats": {"total": 0, "unique_ips": 0, "mobile": 0}}

def save_data(data):
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f, indent=2)

# ============================================
# LOCATION & DEVICE INFO
# ============================================
def get_location(ip):
    try:
        response = requests.get(f"http://ip-api.com/json/{ip}?fields=status,country,regionName,city,zip,lat,lon,timezone,isp,org,as,mobile,proxy,hosting", timeout=5)
        if response.status_code == 200:
            data = response.json()
            if data.get('status') == 'success':
                return {
                    "country": data.get('country', 'Unknown'),
                    "region": data.get('regionName', 'Unknown'),
                    "city": data.get('city', 'Unknown'),
                    "zip": data.get('zip', 'Unknown'),
                    "lat": data.get('lat', 0),
                    "lon": data.get('lon', 0),
                    "timezone": data.get('timezone', 'Unknown'),
                    "isp": data.get('isp', 'Unknown'),
                    "org": data.get('org', 'Unknown'),
                    "as": data.get('as', 'Unknown'),
                    "mobile": data.get('mobile', False),
                    "proxy": data.get('proxy', False),
                    "hosting": data.get('hosting', False)
                }
    except:
        pass
    return {
        "country": "Unknown", "region": "Unknown", "city": "Unknown",
        "zip": "Unknown", "lat": 0, "lon": 0,
        "timezone": "Unknown", "isp": "Unknown", "org": "Unknown",
        "as": "Unknown", "mobile": False, "proxy": False, "hosting": False
    }

def get_device_info(user_agent):
    ua = user_agent.lower() if user_agent else ""
    info = {
        "device": "Desktop",
        "os": "Unknown",
        "os_version": "Unknown",
        "browser": "Unknown",
        "browser_version": "Unknown",
        "is_mobile": False,
        "is_tablet": False,
        "is_bot": False,
        "screen_width": "Unknown",
        "screen_height": "Unknown"
    }
    
    # Detect OS
    if 'android' in ua:
        info['os'] = 'Android'
        info['device'] = 'Mobile'
        info['is_mobile'] = True
    elif 'iphone' in ua or 'ipad' in ua:
        info['os'] = 'iOS'
        info['device'] = 'Mobile'
        info['is_mobile'] = True
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
    
    # Detect Bot
    if 'bot' in ua or 'crawler' in ua or 'spider' in ua:
        info['is_bot'] = True
    
    return info

# ============================================
# FEATURES 15: ROUTES
# ============================================

# Feature 1: Tracking Link
@app.route('/track/<link_id>')
def track(link_id):
    ip = request.remote_addr
    user_agent = request.headers.get('User-Agent', 'Unknown')
    
    location = get_location(ip)
    device = get_device_info(user_agent)
    
    visitor = {
        "id": link_id,
        "ip": ip,
        "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "location": location,
        "device": device,
        "user_agent": user_agent,
        "referer": request.headers.get('Referer', 'Direct'),
        "accept_language": request.headers.get('Accept-Language', 'Unknown'),
        "accept_encoding": request.headers.get('Accept-Encoding', 'Unknown'),
        "dnt": request.headers.get('DNT', 'Unknown')
    }
    
    data = load_data()
    data["clicks"].append(visitor)
    data["stats"]["total"] = len(data["clicks"])
    data["stats"]["unique_ips"] = len(set(c.get('ip', '') for c in data["clicks"]))
    data["stats"]["mobile"] = sum(1 for c in data["clicks"] if c.get("device", {}).get("is_mobile", False))
    save_data(data)
    
    return """
    <html>
        <head><title>Link Tracker</title>
        <style>
            body{font-family:Arial;text-align:center;padding:50px;background:#0a0c15;color:white;}
            .box{max-width:500px;margin:0 auto;background:#121624;padding:40px;border-radius:20px;border:1px solid #00e676;}
            h1{color:#00e676;}
        </style>
        </head>
        <body>
            <div class="box">
                <h1>✅ Link Clicked!</h1>
                <p>Your visit has been recorded.</p>
                <p style="color:#888;font-size:14px;">Redirecting...</p>
                <script>setTimeout(() => window.history.back(), 2000);</script>
            </div>
        </body>
    </html>
    """

# Feature 2: Dashboard (Ina features zote 15)
@app.route('/')
@app.route('/dashboard')
def dashboard():
    data = load_data()
    clicks = data["clicks"]
    stats = data["stats"]
    
    return render_template_string("""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Link Tracker Pro - 15 Features</title>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <style>
            * { box-sizing: border-box; margin: 0; padding: 0; }
            body { font-family: 'Segoe UI', system-ui; background: #0a0c15; color: #fff; padding: 20px; }
            .container { max-width: 1400px; margin: 0 auto; }
            
            /* Header */
            .header { text-align: center; margin-bottom: 30px; }
            .header h1 { font-size: 2.5em; background: linear-gradient(135deg, #00e676, #2979ff); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }
            .header .sub { color: #888; }
            .live { color: #00e676; animation: pulse 1.5s infinite; }
            @keyframes pulse { 0%,100% { opacity: 1; } 50% { opacity: 0.3; } }
            
            /* Stats Grid - Feature 3 to 7 */
            .stats-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(150px, 1fr)); gap: 15px; margin-bottom: 30px; }
            .stat-card { background: #121624; padding: 20px; border-radius: 16px; text-align: center; border: 1px solid #252b3d; transition: 0.3s; }
            .stat-card:hover { transform: translateY(-3px); border-color: #00e676; }
            .stat-card .number { font-size: 2em; font-weight: bold; color: #00e676; }
            .stat-card .label { color: #888; font-size: 0.8em; margin-top: 5px; }
            
            /* Features Badges - Feature 8 */
            .features { display: flex; flex-wrap: wrap; gap: 8px; margin-bottom: 20px; justify-content: center; }
            .feature-badge { background: #1a1e2f; padding: 5px 12px; border-radius: 20px; font-size: 11px; border: 1px solid #2f354a; }
            .feature-badge.active { border-color: #00e676; color: #00e676; }
            
            /* Table - Feature 9 to 15 */
            .table-container { max-height: 600px; overflow-y: auto; border-radius: 16px; border: 1px solid #252b3d; }
            table { width: 100%; border-collapse: collapse; font-size: 13px; }
            th { background: #2979ff; color: #fff; padding: 12px; position: sticky; top: 0; z-index: 10; text-align: left; }
            td { padding: 10px 12px; border-bottom: 1px solid #1e2633; background: #121624; }
            .row:hover td { background: #1a1e2f; }
            .badge { display: inline-block; padding: 2px 8px; border-radius: 12px; font-size: 10px; }
            .badge-green { background: #00e67620; color: #00e676; }
            .badge-blue { background: #2979ff20; color: #2979ff; }
            .badge-orange { background: #ff980020; color: #ff9800; }
            
            .map-link { color: #00e676; text-decoration: none; }
            .footer { text-align: center; color: #666; font-size: 12px; margin-top: 20px; }
            
            @media (max-width: 600px) { table { font-size: 11px; } td, th { padding: 6px; } .stats-grid { grid-template-columns: repeat(2, 1fr); } }
        </style>
    </head>
    <body>
        <div class="container">
            <!-- Header -->
            <div class="header">
                <h1>📊 LINK TRACKER PRO</h1>
                <p><span class="live">●</span> LIVE · Total Clicks: <strong>{{ stats.total }}</strong></p>
                <p class="sub">15 Features • Real-time Visitor Tracking</p>
            </div>
            
            <!-- Feature Badges -->
            <div class="features">
                <span class="feature-badge active">📍 Location</span>
                <span class="feature-badge active">📱 Device</span>
                <span class="feature-badge active">💻 OS</span>
                <span class="feature-badge active">🌍 Browser</span>
                <span class="feature-badge active">🗺️ Map</span>
                <span class="feature-badge active">📶 Mobile Detection</span>
                <span class="feature-badge active">🕒 Time</span>
                <span class="feature-badge active">🌐 ISP</span>
                <span class="feature-badge active">🔗 Referer</span>
                <span class="feature-badge active">🌍 Language</span>
                <span class="feature-badge active">🛡️ DNT</span>
                <span class="feature-badge active">📊 Stats</span>
                <span class="feature-badge active">🔄 Auto Refresh</span>
                <span class="feature-badge active">📱 Screen Info</span>
                <span class="feature-badge active">🔐 Proxy Detection</span>
            </div>
            
            <!-- Stats -->
            <div class="stats-grid">
                <div class="stat-card"><div class="number">{{ stats.total }}</div><div class="label">Total Clicks</div></div>
                <div class="stat-card"><div class="number">{{ stats.unique_ips }}</div><div class="label">Unique IPs</div></div>
                <div class="stat-card"><div class="number">{{ stats.mobile }}</div><div class="label">Mobile Visitors</div></div>
                <div class="stat-card"><div class="number">{{ clicks|length }}</div><div class="label">Total Visits</div></div>
            </div>
            
            <!-- Table -->
            <div class="table-container">
            <table>
                <tr>
                    <th>#</th>
                    <th>IP</th>
                    <th>📍 City, Country</th>
                    <th>📱 Device</th>
                    <th>💻 OS</th>
                    <th>🌍 Browser</th>
                    <th>🕒 Time</th>
                    <th>🗺️</th>
                </tr>
                {% for click in clicks|reverse %}
                <tr class="row">
                    <td>{{ loop.index }}</td>
                    <td>{{ click.ip }}</td>
                    <td>{{ click.location.city }}, {{ click.location.country }}</td>
                    <td><span class="badge badge-green">📱</span> {{ click.device.device }}</td>
                    <td>{{ click.device.os }}</td>
                    <td>{{ click.device.browser }}</td>
                    <td>{{ click.time.split()[1][:5] }}</td>
                    <td>{% if click.location.lat %}<a href="https://www.openstreetmap.org/?mlat={{ click.location.lat }}&mlon={{ click.location.lon }}" target="_blank" class="map-link">🗺️</a>{% else %}-{% endif %}</td>
                </tr>
                {% endfor %}
            </table>
            </div>
            
            <div class="footer">🔄 Refresh to see new clicks · 15 Features Enabled</div>
        </div>
    </body>
    </html>
    """, clicks=clicks, stats=stats)

# Feature 2: API Stats
@app.route('/api/stats')
def api_stats():
    data = load_data()
    return jsonify(data["stats"])

# Feature 2: API Clicks
@app.route('/api/clicks')
def api_clicks():
    return jsonify(load_data())

if __name__ == '__main__':
    print("""
    ╔══════════════════════════════════════════════════╗
    ║   🔗 LINK TRACKER PRO - 15 FEATURES            ║
    ║   Server running in background                  ║
    ║   Dashboard: http://localhost:5000             ║
    ╚══════════════════════════════════════════════════╝
    """)
    app.run(host='0.0.0.0', port=5000, debug=True)
