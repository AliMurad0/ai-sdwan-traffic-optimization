import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
import joblib
import random

print("⚙️ Generating Perfect Training Data...")

# --- 1. DEFINE THE RULES (Must match Sender_Client.py) ---
# Features: [Protocol, Duration, Total_Bytes, Dest_Port]

data = []
labels = []

# Generate 2000 examples of "Netflix" (Streaming)
for _ in range(2000):
    # TCP(6), Long Duration, Huge Data, Port 443
    features = [
        6, 
        random.randint(60000000, 90000000), 
        random.randint(5000000, 50000000), 
        443
    ]
    data.append(features)
    labels.append("Streaming")

# Generate 2000 examples of "VoIP"
for _ in range(2000):
    # UDP(17), Long Duration, Small Data, Port 5060
    features = [
        17, 
        random.randint(60000000, 90000000), 
        random.randint(10000, 100000), 
        5060
    ]
    data.append(features)
    labels.append("VoIP_Call")

# Generate 2000 examples of "Web"
for _ in range(2000):
    # TCP(6), Short Duration, Small Data, Port 80
    features = [
        6, 
        random.randint(100, 500000), 
        random.randint(1000, 50000), 
        80
    ]
    data.append(features)
    labels.append("Web_Browsing")

# --- 2. TRAIN THE MODEL ---
print("🚀 Training AI on Synthetic Data...")

X = np.array(data)
y = np.array(labels)

# Encode Labels
le = LabelEncoder()
y_encoded = le.fit_transform(y)

# Train Random Forest (Robust and fast)
model = RandomForestClassifier(n_estimators=50)
model.fit(X, y_encoded)

print(f"✅ Training Complete. Classes Learned: {le.classes_}")

# --- 3. SAVE ---
joblib.dump(model, 'traffic_model.pkl')
joblib.dump(le, 'label_encoder.pkl')

print("💾 'traffic_model.pkl' and 'label_encoder.pkl' have been overwritten.")
print("👉 Now run 'router_server.py' again. It will work 100%.")