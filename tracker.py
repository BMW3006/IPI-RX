# tracker.py - Full visitor info in Termux

import requests
import time
import os
import json

SERVER_URL = "http://localhost:5000/api/clicks"

def clear_screen():
    os.system('clear')

def get_clicks():
    try:
        response = requests.get(SERVER_URL, timeout=2)
        if response.status_code == 200:
            return response.json()
        return None
    except:
        return None

def display_clicks(data):
    clear_screen()
    print("""
    ╔══════════════════════════════════════════════════════════════════════╗
    ║              🔗 LINK TRACKER - FULL VISITOR INFO                  ║
    ╚══════════════════════════════════════════════════════════════════════╝
    """)
    
    if not data or "clicks" not in data:
        print("   ❌ No data. Make sure the server is running.")
        return
    
    clicks = data["clicks"]
    total = len(clicks)
    
    print(f"   📊 Total Clicks: {total}\n")
    
    if total == 0:
        print("   🔴 No one has clicked the link yet.")
        return
    
    recent = list(reversed(clicks))[:10]
    
    print("   📋 RECENT VISITORS:\n")
    
    for i, click in enumerate(recent, 1):
        loc = click.get('location', {})
        device = click.get('device', {})
        
        print(f"   ┌─ VISITOR #{i} ────────────────────────────────────────────────")
        print(f"   │ 🌐 IP: {click.get('ip', 'Unknown')}")
        print(f"   │ 📍 Location: {loc.get('city', '?')}, {loc.get('region', '?')}, {loc.get('country', '?')}")
        print(f"   │ 📱 Device: {device.get('device', '?')} | OS: {device.get('os', '?')}")
        print(f"   │ 🌍 Browser: {device.get('browser', '?')}")
        print(f"   │ 🕐 Time: {click.get('time', 'Unknown')}")
        print(f"   │ 🔗 Link ID: {click.get('id', 'Unknown')}")
        print(f"   └─────────────────────────────────────────────────────────\n")
    
    print(f"   🔄 Auto-refresh every 3 seconds... (Ctrl+C to exit)")

def main():
    print("   🔗 LINK TRACKER - Starting...")
    time.sleep(1)
    
    try:
        while True:
            data = get_clicks()
            display_clicks(data)
            time.sleep(3)
    except KeyboardInterrupt:
        print("\n   👋 Goodbye!")

if __name__ == "__main__":
    main()
