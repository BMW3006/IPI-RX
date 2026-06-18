# server.py - Full Featured Link Tracker
# Features: Location, Device, Browser, OS, Screen, Language, Timezone, ISP, Referer, GPS, Map Link

from flask import Flask, request, jsonify, render_template_string
import json
import os
from datetime import datetime
import requests
import user_agents

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
    """Get location, ISP, timezone from IP"""
    try:
        response = requests.get(f"http://ip-api.com/json/{ip}?fields=status,message,country,regionName,city,zip,lat,lon,timezone,isp,org,as,reverse,mobile,proxy,hosting,query", timeout=5)
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
    return {"country": "Unknown", "region": "Unknown", "city": "Unknown", "lat": 0, "lon": 0}

def get_device_info(user_agent_str):
    """Parse full device info using user_agents library"""
    try:
        ua = user_agents.parse(user_agent_str)
        return {
            "device": ua.device.family if ua.device.family else "Unknown",
            "brand": ua.device.brand if ua.device.brand else "Unknown",
            "model": ua.device.model if ua.device.model else "Unknown",
            "os": ua.os.family if ua.os.family else "Unknown",
            "os_version": ua.os.version_string if ua.os.version_string else "Unknown",
            "browser": ua.browser.family if ua.browser.family else "Unknown",
            "browser_version": ua.browser.version_string if ua.browser.version_string else "Unknown",
            "is_mobile": ua.is_mobile,
            "is_tablet": ua.is_tablet,
            "is_pc": ua.is_pc,
            "is_bot": ua.is_bot
        }
    except:
        return {
            "device": "Unknown", "brand": "Unknown", "model": "Unknown",
            "os": "Unknown", "os_version": "Unknown",
            "browser": "Unknown", "browser_version": "Unknown",
            "is_mobile": False, "is_tablet": False, "is_pc": False, "is_bot": False
        }

def get_screen_info(ua_str):
    """Extract screen info from user agent"""
    info = {"width": "Unknown", "height": "Unknown", "density": "Unknown"}
    try:
        # Common screen sizes patterns
        if "Android" in ua_str:
            if "Mobile" in ua_str:
                info = {"width": "360-428", "height": "640-926", "density": "~2.0-3.0"}
            else:
                info = {"width": "800-1280", "height": "1280-1920", "density": "~1.5-2.5"}
        elif "iPhone" in ua_str:
            info = {"width": "390-430", "height": "844-932", "density": "~3.0"}
        elif "Windows" in ua_str or "Macintosh" in ua_str:
            info = {"width": "1366-1920", "height": "768-1080", "density": "~1.0-1.5"}
    except:
        pass
    return info

@app.route('/track/<link_id>')
def track(link_id):
    ip = request.remote_addr
    user_agent = request.headers.get('User-Agent', 'Unknown')
    accept_language = request.headers.get('Accept-Language', 'Unknown')
    accept_encoding = request.headers.get('Accept-Encoding', 'Unknown')
    dnt = request.headers.get('DNT', 'Unknown')
    
    # Get location
    location = get_location(ip)
    
    # Get device info
    device_info = get_device_info(user_agent)
    
    # Get screen info
    screen_info = get_screen_info(user_agent)
    
    # Get map link
    map_link = f"https://www.openstreetmap.org/?mlat={location.get('lat', 0)}&mlon={location.get('lon', 0)}" if location.get('lat') else None
    
    visitor = {
        "id": link_id,
        "ip": ip,
        "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "timestamp": datetime.now().timestamp(),
        "user_agent": user_agent,
        "accept_language": accept_language,
        "accept_encoding": accept_encoding,
        "dnt": dnt,
        "location": location,
        "device": device_info,
        "screen": screen_info,
        "map_link": map_link,
        "referer": request.headers.get('Referer', 'Direct')
    }
    
    data = load_data()
    data["clicks"].append(visitor)
    save_data(data)
    
    return """
    <html>
        <head><title>Link Tracker</title>
        <style>
            body { font-family: Arial; text-align: center; padding: 50px; background: #0a0c15; color: white; }
            .container { max-width: 500px; margin: 0 auto; background: #121624; padding: 40px; border-radius: 20px; }
            h1 { color: #00e676; }
            .icon { font-size: 50px; }
        </style>
        </head>
        <body>
            <div class="container">
                <div class="icon">✅</div>
                <h1>Link Clicked!</h1>
                <p>Your visit has been recorded.</p>
                <p style="color: #888; font-size: 14px;">Redirecting...</p>
                <script>setTimeout(() => window.history.back(), 2000);</script>
            </div>
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
                * { box-sizing: border-box; }
                body { font-family: 'Segoe UI', system-ui; background: #0a0c15; color: #fff; padding: 20px; margin: 0; }
                .header { text-align: center; margin-bottom: 30px; }
                .header h1 { font-size: 2em; background: linear-gradient(135deg, #00e676, #2979ff); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }
                .stats { display: grid; grid-template-columns: repeat(auto-fit, minmax(150px, 1fr)); gap: 15px; margin-bottom: 30px; }
                .stat-card { background: #121624; padding: 20px; border-radius: 16px; text-align: center; border: 1px solid #252b3d; }
                .stat-card .number { font-size: 2em; font-weight: bold; color: #00e676; }
                .stat-card .label { color: #888; font-size: 0.8em; }
                .container { max-height: 600px; overflow-y: auto; border-radius: 16px; border: 1px solid #252b3d; }
                table { width: 100%; border-collapse: collapse; font-size: 13px; }
                th { background: #2979ff; color: #fff; padding: 12px; position: sticky; top: 0; z-index: 10; text-align: left; }
                td { padding: 10px 12px; border-bottom: 1px solid #1e2633; background: #121624; }
                .row:hover td { background: #1a1e2f; }
                .badge { display: inline-block; padding: 2px 8px; border-radius: 12px; font-size: 11px; }
                .badge-green { background: #00e67620; color: #00e676; }
                .badge-blue { background: #2979ff20; color: #2979ff; }
                .badge-orange { background: #ff980020; color: #ff9800; }
                .badge-red { background: #ff444420; color: #ff4444; }
                .map-link { color: #00e676; text-decoration: none; }
                .live { color: #00e676; animation: pulse 1.5s infinite; }
                @keyframes pulse { 0%, 100% { opacity: 1; } 50% { opacity: 0.3; } }
                .footer { text-align: center; color: #666; font-size: 12px; margin-top: 20px; }
                .grid-3 { display: grid; grid-template-columns: repeat(3, 1fr); gap: 5px; font-size: 12px; }
                .grid-3 div { background: #1a1e2f; padding: 4px 8px; border-radius: 4px; }
                @media (max-width: 600px) { table { font-size: 11px; } td, th { padding: 6px; } .stats { grid-template-columns: repeat(2, 1fr); } }
            </style>
        </head>
        <body>
            <div class="header">
                <h1>📊 LINK TRACKER DASHBOARD</h1>
                <p><span class="live">●</span> LIVE · Total Clicks: <strong>""" + str(len(clicks)) + """</strong></p>
            </div>
            
            <div class="stats">
                <div class="stat-card"><div class="number">""" + str(len(clicks)) + """</div><div class="label">Total Clicks</div></div>
                <div class="stat-card"><div class="number">""" + str(len(set(c.get('ip', '') for c in clicks))) + """</div><div class="label">Unique IPs</div></div>
                <div class="stat-card"><div class="number">""" + str(sum(1 for c in clicks if c.get('location', {}).get('city', '') != 'Unknown')) + """</div><div class="label">Locations Found</div></div>
                <div class="stat-card"><div class="number">""" + str(sum(1 for c in clicks if c.get('device', {}).get('is_mobile', False))) + """</div><div class="label">Mobile Visitors</div></div>
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
                    <th>Map</th>
                </tr>
    """
    
    for i, click in enumerate(reversed(clicks), 1):
        loc = click.get('location', {})
        dev = click.get('device', {})
        is_mobile = dev.get('is_mobile', False)
        mobile_badge = '<span class="badge badge-green">📱</span>' if is_mobile else '<span class="badge badge-blue">💻</span>'
        
        location_str = f"{loc.get('city', '?')}, {loc.get('country', '?')}"
        map_link = click.get('map_link', '')
        map_html = f'<a href="{map_link}" target="_blank" class="map-link">🗺️</a>' if map_link else '-'
        
        html += f"""
            <tr class="row">
                <td>{i}</td>
                <td>{click.get('ip', '?')}</td>
                <td>{location_str}</td>
                <td>{mobile_badge} {dev.get('device', '?')}</td>
                <td>{dev.get('os', '?')}</td>
                <td>{dev.get('browser', '?')}</td>
                <td>{click.get('time', '?').split()[1][:5]}</td>
                <td>{map_html}</td>
            </tr>
        """
    
    html += """
            </table>
            </div>
            <div class="footer">🔄 Refresh to see new clicks · IPI-RX Tracker</div>
        </body>
    </html>
    """
    return html

@app.route('/api/clicks')
def api_clicks():
    return jsonify(load_data())

@app.route('/api/stats')
def api_stats():
    data = load_data()
    clicks = data["clicks"]
    return jsonify({
        "total": len(clicks),
        "unique_ips": len(set(c.get('ip', '') for c in clicks)),
        "mobile": sum(1 for c in clicks if c.get('device', {}).get('is_mobile', False)),
        "cities": list(set(c.get('location', {}).get('city', '') for c in clicks if c.get('location', {}).get('city', '')))
    })

if __name__ == '__main__':
    print("""
    ╔══════════════════════════════════════════════════════════════════╗
    ║   🔗 LINK TRACKER - FULL FEATURES ENABLED                      ║
    ║   📍 Location | 📱 Device | 🌍 Browser | 🗺️ Map Link          ║
    ╚══════════════════════════════════════════════════════════════════╝
    """)
    app.run(host='0.0.0.0', port=5000, debug=True)
