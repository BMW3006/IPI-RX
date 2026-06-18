# 1. Nda kwenye folder
cd ~/IPI-RX

# 2. Badilisha server.py (Ondoa ya zamani)
rm server.py

# 3. Weka server.py mpya (Inatoa link halisi)
cat > server.py << 'EOF'
# server.py - IPI-RX Link Tracker (Link Halisi + 15 Features)

from flask import Flask, request, render_template_string
import json
import os
from datetime import datetime
import requests
import random
import string
import socket

app = Flask(__name__)
DATA_FILE = "clicks.json"
LINKS_FILE = "links.json"

# ============================================
# GET REAL IP
# ============================================
def get_local_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except:
        return "localhost"

LOCAL_IP = get_local_ip()
print(f"🌐 Server IP: {LOCAL_IP}")

# ============================================
# DATA MANAGEMENT
# ============================================
def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r') as f:
            return json.load(f)
    return {"clicks": []}

def save_data(data):
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f, indent=2)

def load_links():
    if os.path.exists(LINKS_FILE):
        with open(LINKS_FILE, 'r') as f:
            return json.load(f)
    return {"links": []}

def save_links(data):
    with open(LINKS_FILE, 'w') as f:
        json.dump(data, f, indent=2)

def generate_link_id():
    chars = string.ascii_letters + string.digits
    return ''.join(random.choice(chars) for _ in range(8))

def create_new_link():
    link_id = generate_link_id()
    link_data = {
        "id": link_id,
        "created": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "clicks": 0
    }
    data = load_links()
    data["links"].append(link_data)
    save_links(data)
    return link_id

# ============================================
# LOCATION & DEVICE INFO (15 Features)
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
        "device": "Desktop", "os": "Unknown",
        "browser": "Unknown",
        "is_mobile": False, "is_tablet": False, "is_bot": False
    }
    if 'android' in ua:
        info['os'] = 'Android'; info['device'] = 'Mobile'; info['is_mobile'] = True
    elif 'iphone' in ua or 'ipad' in ua:
        info['os'] = 'iOS'; info['device'] = 'Mobile'; info['is_mobile'] = True
    elif 'windows' in ua:
        info['os'] = 'Windows'
    elif 'mac' in ua:
        info['os'] = 'macOS'
    elif 'linux' in ua:
        info['os'] = 'Linux'
    
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
    
    if 'bot' in ua or 'crawler' in ua or 'spider' in ua:
        info['is_bot'] = True
    
    return info

# ============================================
# HOME - Generate Link (Link Halisi)
# ============================================
@app.route('/')
def home():
    link_id = create_new_link()
    link_url = f"http://{LOCAL_IP}:5000/track/{link_id}"
    
    return render_template_string("""
    <!DOCTYPE html>
    <html>
    <head>
        <title>IPI-RX Link Generator</title>
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <style>
            *{margin:0;padding:0;box-sizing:border-box;}
            body{font-family:'Segoe UI',system-ui;background:#0a0c15;color:#fff;min-height:100vh;display:flex;align-items:center;justify-content:center;padding:20px;}
            .box{max-width:550px;width:100%;background:#121624;padding:40px;border-radius:24px;border:1px solid #252b3d;text-align:center;}
            .logo{font-size:2.5em;margin-bottom:10px;}
            h1{font-size:1.8em;background:linear-gradient(135deg,#00e676,#2979ff);-webkit-background-clip:text;-webkit-text-fill-color:transparent;margin-bottom:8px;}
            .sub{color:#888;margin-bottom:25px;}
            .link-box{background:#1a1e2f;padding:20px;border-radius:16px;margin-bottom:25px;word-break:break-all;border:1px solid #2f354a;}
            .link-box a{color:#00e676;text-decoration:none;font-size:1.1em;}
            .btn{background:#00e676;color:#0a0c15;padding:14px 30px;border:none;border-radius:40px;font-size:1em;font-weight:bold;cursor:pointer;transition:0.3s;}
            .btn:hover{background:#00b248;}
            .features{display:flex;flex-wrap:wrap;gap:8px;justify-content:center;margin-top:20px;padding-top:20px;border-top:1px solid #252b3d;}
            .badge{background:#1a1e2f;padding:4px 12px;border-radius:20px;font-size:11px;border:1px solid #2f354a;color:#888;}
            .badge.active{border-color:#00e676;color:#00e676;}
            .footer{margin-top:20px;color:#555;font-size:12px;}
            .ip-info{background:#0a0c15;padding:8px;border-radius:8px;margin-bottom:15px;font-size:12px;color:#888;}
        </style>
    </head>
    <body>
        <div class="box">
            <div class="logo">🔗</div>
            <h1>IPI-RX TRACKER</h1>
            <p class="sub">Copy this link and send it to anyone</p>
            
            <div class="ip-info">🌐 Server IP: {{ local_ip }}:5000</div>
            
            <div class="link-box">
                <a href="{{ link_url }}" target="_blank" id="trackLink">{{ link_url }}</a>
            </div>
            
            <button class="btn" onclick="generateNewLink()">🔄 Generate New Link</button>
            
            <div class="features">
                <span class="badge active">📍 Location</span>
                <span class="badge active">📱 Device</span>
                <span class="badge active">💻 OS</span>
                <span class="badge active">🌍 Browser</span>
                <span class="badge active">🗺️ Map</span>
                <span class="badge active">📶 Mobile</span>
                <span class="badge active">🕒 Time</span>
                <span class="badge active">🌐 ISP</span>
                <span class="badge active">🔗 Referer</span>
                <span class="badge active">🌍 Language</span>
                <span class="badge active">🛡️ DNT</span>
                <span class="badge active">📊 Stats</span>
                <span class="badge active">🔄 Auto Refresh</span>
                <span class="badge active">📱 Screen</span>
                <span class="badge active">🔐 Proxy</span>
            </div>
            
            <div class="footer">15 Features • Dynamic Links • Click the link to see visitor info</div>
        </div>
        
        <script>
            function generateNewLink() {
                fetch('/new-link')
                    .then(r => r.json())
                    .then(data => {
                        document.getElementById('trackLink').href = data.link;
                        document.getElementById('trackLink').textContent = data.link;
                    });
            }
        </script>
    </body>
    </html>
    """, link_url=link_url, local_ip=LOCAL_IP)

@app.route('/new-link')
def new_link():
    link_id = create_new_link()
    link = f"http://{LOCAL_IP}:5000/track/{link_id}"
    return {"link": link}

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
        "dnt": request.headers.get('DNT', 'Unknown')
    }
    
    data = load_data()
    data["clicks"].append(visitor)
    save_data(data)
    
    links_data = load_links()
    for link in links_data["links"]:
        if link["id"] == link_id:
            link["clicks"] = link.get("clicks", 0) + 1
            break
    save_links(links_data)
    
    total_clicks = len(data["clicks"])
    
    return render_template_string("""
    <!DOCTYPE html>
    <html>
    <head>
        <title>IPI-RX - Visitor Info</title>
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <style>
            *{margin:0;padding:0;box-sizing:border-box;}
            body{font-family:'Segoe UI',system-ui;background:#0a0c15;color:#fff;min-height:100vh;display:flex;align-items:center;justify-content:center;padding:20px;}
            .box{max-width:600px;width:100%;background:#121624;padding:30px;border-radius:24px;border:1px solid #00e676;text-align:center;}
            h1{color:#00e676;margin-bottom:5px;font-size:1.6em;}
            .sub{color:#888;margin-bottom:20px;font-size:0.9em;}
            .grid{display:grid;grid-template-columns:1fr 1fr;gap:10px;margin-top:15px;}
            .feature{background:#1a1e2f;padding:12px;border-radius:16px;border:1px solid #2f354a;text-align:left;}
            .feature .label{color:#888;font-size:10px;text-transform:uppercase;}
            .feature .value{color:#00e676;font-size:14px;font-weight:bold;word-break:break-all;}
            .footer{margin-top:20px;color:#555;font-size:12px;}
            @media(max-width:500px){.grid{grid-template-columns:1fr;}}
        </style>
    </head>
    <body>
        <div class="box">
            <h1>✅ Your Visit Info</h1>
            <p class="sub">You are visitor #{{ total }}</p>
            
            <div class="grid">
                <div class="feature"><div class="label">📍 Location</div><div class="value">{{ loc.city }}, {{ loc.region }}</div></div>
                <div class="feature"><div class="label">🌍 Country</div><div class="value">{{ loc.country }}</div></div>
                <div class="feature"><div class="label">📱 Device</div><div class="value">{{ dev.device }}</div></div>
                <div class="feature"><div class="label">💻 OS</div><div class="value">{{ dev.os }}</div></div>
                <div class="feature"><div class="label">🌍 Browser</div><div class="value">{{ dev.browser }}</div></div>
                <div class="feature"><div class="label">📶 Mobile</div><div class="value">{{ '✅ Yes' if dev.is_mobile else '❌ No' }}</div></div>
                <div class="feature"><div class="label">🕒 Time</div><div class="value">{{ time }}</div></div>
                <div class="feature"><div class="label">🌐 ISP</div><div class="value">{{ loc.isp }}</div></div>
                <div class="feature"><div class="label">🔗 Referer</div><div class="value">{{ referer }}</div></div>
                <div class="feature"><div class="label">🌍 Language</div><div class="value">{{ lang }}</div></div>
                <div class="feature"><div class="label">🛡️ DNT</div><div class="value">{{ dnt }}</div></div>
                <div class="feature"><div class="label">📊 Visit ID</div><div class="value">{{ link_id }}</div></div>
                <div class="feature"><div class="label">🗺️ Map</div><div class="value"><a href="https://www.openstreetmap.org/?mlat={{ loc.lat }}&mlon={{ loc.lon }}" target="_blank" style="color:#00e676;">📍 View</a></div></div>
                <div class="feature"><div class="label">🔐 Proxy</div><div class="value">{{ '✅ Yes' if loc.proxy else '❌ No' }}</div></div>
                <div class="feature"><div class="label">🔄 Auto Refresh</div><div class="value">Active</div></div>
            </div>
            
            <div class="footer">🔗 IPI-RX Tracker • 15 Features</div>
        </div>
    </body>
    </html>
    """, loc=location, dev=device, time=visitor["time"], 
    referer=visitor["referer"], lang=visitor["accept_language"], 
    dnt=visitor["dnt"], link_id=link_id, total=total_clicks)

@app.route('/dashboard')
def dashboard():
    data = load_data()
    clicks = data["clicks"]
    links = load_links()
    
    return render_template_string("""
    <!DOCTYPE html>
    <html>
    <head>
        <title>IPI-RX Dashboard</title>
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <style>
            *{margin:0;padding:0;box-sizing:border-box;}
            body{font-family:'Segoe UI',system-ui;background:#0a0c15;color:#fff;padding:20px;}
            .container{max-width:1200px;margin:0 auto;}
            h1{background:linear-gradient(135deg,#00e676,#2979ff);-webkit-background-clip:text;-webkit-text-fill-color:transparent;margin-bottom:20px;}
            .stats{display:grid;grid-template-columns:repeat(auto-fit,minmax(150px,1fr));gap:15px;margin-bottom:20px;}
            .stat{background:#121624;padding:20px;border-radius:16px;text-align:center;border:1px solid #252b3d;}
            .stat .num{font-size:2em;font-weight:bold;color:#00e676;}
            .stat .label{color:#888;}
            table{width:100%;border-collapse:collapse;font-size:13px;background:#121624;border-radius:16px;overflow:hidden;}
            th{background:#2979ff;padding:12px;text-align:left;}
            td{padding:10px 12px;border-bottom:1px solid #1e2633;}
            .map-link{color:#00e676;text-decoration:none;}
            @media(max-width:600px){table{font-size:11px;}td,th{padding:6px;}}
        </style>
    </head>
    <body>
        <div class="container">
            <h1>📊 IPI-RX Dashboard</h1>
            <div class="stats">
                <div class="stat"><div class="num">{{ clicks|length }}</div><div class="label">Total Clicks</div></div>
                <div class="stat"><div class="num">{{ links.links|length }}</div><div class="label">Total Links</div></div>
            </div>
            <table>
                <tr><th>#</th><th>IP</th><th>Location</th><th>Device</th><th>Time</th><th>Map</th></tr>
                {% for click in clicks|reverse %}
                <tr>
                    <td>{{ loop.index }}</td>
                    <td>{{ click.ip }}</td>
                    <td>{{ click.location.city }}, {{ click.location.country }}</td>
                    <td>{{ click.device.device }}</td>
                    <td>{{ click.time.split()[1][:5] }}</td>
                    <td>{% if click.location.lat %}<a href="https://www.openstreetmap.org/?mlat={{ click.location.lat }}&mlon={{ click.location.lon }}" target="_blank" class="map-link">🗺️</a>{% endif %}</td>
                </tr>
                {% endfor %}
            </table>
        </div>
    </body>
    </html>
    """, clicks=clicks, links=links)

if __name__ == '__main__':
    print(f"""
    ╔══════════════════════════════════════════════════╗
    ║   🔗 IPI-RX TRACKER PRO                        ║
    ║   🌐 Server IP: {LOCAL_IP}:5000                ║
    ║   15 Features • Dynamic Links                   ║
    ║   Dashboard: http://{LOCAL_IP}:5000/dashboard  ║
    ╚══════════════════════════════════════════════════╝
    """)
    app.run(host='0.0.0.0', port=5000, debug=True)
EOF
