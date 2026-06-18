# tracker.py - Full Feature Viewer for Termux

import requests
import time
import os
import json

SERVER_URL = "http://localhost:5000/api/clicks"

def clear():
    os.system('clear')

def get_clicks():
    try:
        r = requests.get(SERVER_URL, timeout=2)
        if r.status_code == 200:
            return r.json()
    except:
        pass
    return None

def display_visitor(click, index):
    loc = click.get('location', {})
    dev = click.get('device', {})
    
    print(f"   ┌─ VISITOR #{index} ──────────────────────────────────────────────────")
    print(f"   │ 🌐 IP: {click.get('ip', 'Unknown')}")
    print(f"   │ 📍 Location: {loc.get('city', '?')}, {loc.get('region', '?')}, {loc.get('country', '?')}")
    print(f"   │ 📱 Device: {dev.get('device', '?')} | Brand: {dev.get('brand', '?')} {dev.get('model', '?')}")
    print(f"   │ 💻 OS: {dev.get('os', '?')} {dev.get('os_version', '?')}")
    print(f"   │ 🌍 Browser: {dev.get('browser', '?')} {dev.get('browser_version', '?')}")
    print(f"   │ 📶 Mobile: {'✅ Yes' if dev.get('is_mobile') else '❌ No'}")
    print(f"   │ 🕐 Time: {click.get('time', 'Unknown')}")
    print(f"   │ 🔗 Link ID: {click.get('id', 'Unknown')}")
    if click.get('map_link'):
        print(f"   │ 🗺️ Map: {click.get('map_link')}")
    print(f"   └───────────────────────────────────────────────────────────────────\n")

def main():
    print("🔗 Starting Tracker...")
    while True:
        clear()
        print("   ╔═══════════════════════════════════════════════════════════════════╗")
        print("   ║              📊 LINK TRACKER - FULL VISITOR INFO                ║")
        print("   ╚═══════════════════════════════════════════════════════════════════╝\n")
        
        data = get_clicks()
        if not data:
            print("   ❌ No data. Make sure server is running.")
        else:
            clicks = data.get("clicks", [])
            print(f"   📊 Total Clicks: {len(clicks)}\n")
            if clicks:
                for i, c in enumerate(reversed(clicks[-5:]), 1):
                    display_visitor(c, i)
            else:
                print("   🔴 No one has clicked the link yet.")
        
        print("   🔄 Auto-refresh in 3s... (Ctrl+C to exit)")
        time.sleep(3)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n   👋 Goodbye!")
