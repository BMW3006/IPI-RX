# create_link.py - Generate a new tracking link

import random
import string
from datetime import datetime

def generate_link_id():
    """Generate a unique 6-character link ID"""
    chars = string.ascii_letters + string.digits
    return ''.join(random.choice(chars) for _ in range(6))

def main():
    print("""
    ╔══════════════════════════════════════════════════╗
    ║   🔗 LINK TRACKER - GENERATE LINK              ║
    ╚══════════════════════════════════════════════════╝
    """)
    
    link_id = generate_link_id()
    
    # Get server IP (default localhost)
    server_ip = input("🔢 Server IP (Enter for localhost): ").strip()
    if not server_ip:
        server_ip = "localhost"
    
    port = input("🔢 Port (Enter for default 5000): ").strip()
    if not port:
        port = "5000"
    
    full_link = f"http://{server_ip}:{port}/track/{link_id}"
    
    print(f"\n✅ YOUR TRACKING LINK:\n")
    print(f"   📎 {full_link}\n")
    print(f"   🆔 ID: {link_id}\n")
    print(f"   💡 Send this link to someone. When they click, it will appear on your dashboard!\n")
    
    # Save link to file
    with open("links.txt", "a") as f:
        f.write(f"{datetime.now()} - {full_link} - {link_id}\n")
    
    print("   📁 Link saved to links.txt")

if __name__ == "__main__":
    main()
