import socket
import json
import time
import random

ROUTER_IP = '127.0.0.1'
ROUTER_PORT =  9999
 # MUST MATCH DASHBOARD

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# 4 Features: [Protocol, Duration, Total_Bytes, Dest_Port]
def get_netflix(): return [6, 80000000, 50000000, 443]
def get_voip(): return [17, 80000000, 50000, 5060]
def get_web(): return [6, 500, 1000, 80]

print(f"🎯 SENDER STARTED. Sending to Port {ROUTER_PORT}...")

while True:
    choice = random.choice(["Netflix", "VoIP", "Web"])
    if choice == "Netflix": data = get_netflix(); icon="🎬"
    elif choice == "VoIP": data = get_voip(); icon="📞"
    else: data = get_web(); icon="🌐"

    msg = json.dumps({"features": data}).encode('utf-8')
    sock.sendto(msg, (ROUTER_IP, ROUTER_PORT))
    
    print(f"Sent {icon} {choice}")
    time.sleep(1.5)