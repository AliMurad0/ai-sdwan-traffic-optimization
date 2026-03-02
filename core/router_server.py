import socket
import joblib
import json
import numpy as np

# --- CONFIG ---
ROUTER_IP = '127.0.0.1'
ROUTER_PORT = 9999 # New Port

# --- LOAD MODEL ---
print("⚙️ Loading New 4-Feature Model...")
model = joblib.load('traffic_model.pkl')
le = joblib.load('label_encoder.pkl')
print(f"✅ Loaded. Expecting classes: {le.classes_}")

# --- SOCKET ---
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((ROUTER_IP, ROUTER_PORT))
print(f"👂 Listening on {ROUTER_PORT}...")

while True:
    try:
        data, addr = sock.recvfrom(1024)
        packet = json.loads(data.decode('utf-8'))
        features = np.array(packet['features']).reshape(1, -1)
        
        # DEBUG: Print what the router received
        # print(f"Received Inputs: {features}")

        # PREDICT
        pred_idx = model.predict(features)[0]
        app_name = le.inverse_transform([pred_idx])[0]
        prob = max(model.predict_proba(features)[0]) * 100
        
        # ROUTE
        route = "MPLS (Blue)" if app_name in ["Streaming", "VoIP_Call"] else "Internet (Red)"
        
        print(f"\n📦 Packet from {addr}")
        print(f"   🧠 AI Analysis: {app_name} ({prob:.1f}%)")
        print(f"   🔀 Route: {route}")

    except KeyboardInterrupt:
        break
    except Exception as e:
        print(e)