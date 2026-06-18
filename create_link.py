# create_link.py - Generate new tracking link

import random
import string
from datetime import datetime

def generate_link_id():
    chars = string.ascii_letters + string.digits
    return ''.join(random.choice(chars) for _ in range(6))

def main():
    print("""
    ╔══════════════════════════════════════════════════╗
    ║   🔗 LINK TRACKER - GENERATE LINK              ║
    ╚══════════════════════════════════════════════════╝
    """)
    
    link_id = generate_link_id()
    server_ip = input("🔢 Server IP (Enter for localhost): ").strip() or "localhost"
    port = input("🔢 Port (Enter for 5000): ").strip() or "5000"
    
    full_link = f"http://{server_ip}:{port}/track/{link_id}"
    
    print(f"\n✅ YOUR TRACKING LINK:\n")
    print(f"   📎 {full_link}\n")
    print(f"   🆔 ID: {link_id}\n")
    print(f"   💡 Send this link. Full visitor info will be captured!\n")
    
    with open("links.txt", "a") as f:
        f.write(f"{datetime.now()} - {full_link} - {link_id}\n")

if __name__ == "__main__":
    main()
