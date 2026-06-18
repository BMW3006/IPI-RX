# tracker.py - Real-time click viewer for Termux

import requests
import time
import os
from datetime import datetime

# Server URL (change if running on different IP)
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
    ║              🔗 LINK TRACKER - LIVE VIEW                          ║
    ║              REAL-TIME CLICK MONITOR                              ║
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
        print("   💡 Send the link to someone and wait.")
        return
    
    # Show last 10 clicks
    recent = list(reversed(clicks))[:10]
    
    print("   📋 RECENT CLICKS:\n")
    print("   ┌─────┬─────────────────┬──────────────────────────┬──────────────┐")
    print("   │  #  │      IP         │         Time             │  Link ID     │")
    print("   ├─────┼─────────────────┼──────────────────────────┼──────────────┤")
    
    for i, click in enumerate(recent, 1):
        ip = click.get('ip', 'Unknown')
        time_str = click.get('time', 'Unknown')
        link_id = click.get('id', 'Unknown')
        print(f"   │ {i:>3} │ {ip:<15} │ {time_str:<24} │ {link_id:<12} │")
    
    print("   └─────┴─────────────────┴──────────────────────────┴──────────────┘")
    print(f"\n   🔄 Auto-refresh every 3 seconds... (Ctrl+C to exit)")

def main():
    print("   🔗 LINK TRACKER - Starting...")
    print("   💡 Make sure server is running: python server.py")
    time.sleep(2)
    
    try:
        while True:
            data = get_clicks()
            display_clicks(data)
            time.sleep(3)
    except KeyboardInterrupt:
        print("\n   👋 Goodbye!")

if __name__ == "__main__":
    main()
