<div align="center">

# 🌐 AI-Driven SD-WAN Controller
### Intelligent Network Traffic Classification & Dynamic Path Optimization

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue?logo=python&logoColor=white)](https://python.org)
[![XGBoost](https://img.shields.io/badge/XGBoost-ML%20Model-orange?logo=data:image/png;base64,)](https://xgboost.readthedocs.io)
[![Streamlit](https://img.shields.io/badge/Streamlit-Dashboard-red?logo=streamlit)](https://streamlit.io)
[![Accuracy](https://img.shields.io/badge/Accuracy-94.07%25-brightgreen)](#model-performance)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)


> **A real-time, AI-powered Software-Defined WAN controller that classifies network traffic using machine learning and automatically routes packets to optimize Quality of Service (QoS) — without Deep Packet Inspection.**

[Features](#-key-features) • [Architecture](#-system-architecture) • [Quick Start](#-quick-start) • [Model Performance](#-model-performance) • [Demo](#-demo) • [Team](#-team)



## 📖 Overview

Traditional enterprise WANs use static routing protocols (OSPF, BGP) that treat all traffic equally — routing critical **VoIP calls** the same way as **background file downloads**. This causes severe performance bottlenecks and poor user experience.

This project solves that problem with an **Intelligent SD-WAN Controller** that:

- **Classifies** network traffic in real-time using an XGBoost machine learning model
- **Routes** high-priority traffic (VoIP, Streaming) via dedicated **MPLS paths**
- **Offloads** bulk traffic (Web, Email) via cost-effective **Internet paths**
- **Visualizes** the entire network topology and traffic flow on a live **Streamlit dashboard**

> This approach achieves **94.07% classification accuracy** at **< 1ms inference time** without ever inspecting encrypted packet payloads (no DPI required).

---

## ✨ Key Features

| Feature | Description |
|---|---|
| **AI Traffic Classification** | XGBoost model classifies flows into VoIP, Streaming, or Web Browsing |
| **Dynamic Path Selection** | Automatically routes critical traffic to MPLS and bulk traffic to Internet |
| **Real-Time Dashboard** | Live Streamlit UI with interactive mesh topology, jitter graphs, and routing logs |
| **No Deep Packet Inspection** | Works entirely on statistical flow metadata — privacy-preserving and fast |
| **14-Node Network Mesh** | Simulated mesh topology with NetworkX including full path visualization |
| **Session Reports** | End-of-simulation summary with full packet routing history |

---

## 🏗️ System Architecture

The system is built on a **Decoupled Control Plane Architecture**, mirroring real-world SDN principles:

## 🧠 System Architecture

<p align="center">
  <img src="docs/architecture.png" width="800">
</p>

### The 4-Feature Pipeline

Each packet is classified using only **4 statistical features** (no payload inspection):

| Feature | VoIP Profile | Streaming Profile | Web Profile |
|---|---|---|---|
| **Protocol** | UDP (17) | TCP (6) | TCP (6) |
| **Flow Duration** | Long (60–90M µs) | Long (60–90M µs) | Short (< 500K µs) |
| **Total Bytes** | Small (10K–100K) | Large (5M–50M) | Small (1K–50K) |
| **Destination Port** | 5060 | 443 | 80 |

---

## 📁 Project Structure

```
ai-sdwan-controller/
│
├── controller_app.py        # Streamlit dashboard — main UI
├── router_server.py         # AI controller — receives + classifies packets
├── sender_client.py         # Traffic generator — sends synthetic flows
├── SDWAN_Controller.py      # Core controller module
├── train_perfect_model.py   # Model training script
│
├── traffic_model.pkl        # Trained XGBoost classifier
├── label_encoder.pkl        # Scikit-learn LabelEncoder
│
├── architecture.png         # System architecture diagram
└── README.md
```

---

## 🚀 Quick Start

### Prerequisites

```bash
Python 3.8+
```

### 1. Clone the Repository

```bash
git clone https://github.com/YOUR_USERNAME/ai-sdwan-controller.git
cd ai-sdwan-controller
```

### 2. Install Dependencies

```bash
pip install streamlit pandas numpy scikit-learn xgboost joblib networkx matplotlib
```

### 3. (Optional) Retrain the Model

```bash
python train_perfect_model.py
```

### 4. Launch the Dashboard

```bash
streamlit run controller_app.py
```

### 5. (Optional) Run the Live Router + Sender

Open two separate terminals:

```bash
# Terminal 1 — Start the AI Router
python router_server.py

# Terminal 2 — Start the Traffic Sender
python sender_client.py
```

---

## 📊 Model Performance

The XGBoost classifier was trained on a balanced synthetic dataset derived from the **Unicauca Network Traffic Dataset** (~250,000 flow records) and evaluated on a 20% held-out test set.

| Metric | Score |
|---|---|
| **Overall Accuracy** | **94.07%** |
| Precision (Web Browsing) | 0.94 |
| Recall (VoIP Call) | 0.92 |
| F1-Score (Streaming) | 0.42* |
| Inference Time | **< 1ms per packet** |

> *F1 for Streaming is lower due to class imbalance in the raw dataset. The simulation prototype uses a perfectly balanced set, achieving near-perfect routing outcomes.

### Why XGBoost?

- Handles tabular/structured flow data natively
- Microsecond-level inference — critical for real-time networking
- Resistant to overfitting with the right depth/estimator tuning
- Outperforms simple Random Forest and SVM on this feature set

---

## 🖥️ Demo

### Live Dashboard

The Streamlit dashboard provides:
- **Live Network Mesh** — 14-node topology with animated active path (Blue = MPLS, Red = Internet)
- **Jitter Graph** — Real-time latency visualization (MPLS: 2–10ms vs Internet: 20–80ms)
- **Application Distribution** — Live bar chart of classified traffic types
- **Session Report** — Full routing log at simulation end

### Routing Logic

```python
# SD-WAN Policy:
# High-priority apps → MPLS (low jitter, guaranteed QoS)
# Bulk apps         → Internet (cost-effective)

if app in ["VoIP_Call", "Streaming", "P2P_Transfer"]:
    route → MPLS   # Blue Path
else:
    route → Internet  # Red Path
```

---

## 🔬 Technical Deep Dive

### Statistical Flow Analysis vs. DPI

| Approach | Speed | Privacy | Encrypted Traffic | Cost |
|---|---|---|---|---|
| Deep Packet Inspection (DPI) | Slow | ❌ Invasive | ❌ Fails on TLS 1.3 | High |
| **Statistical Flow Analysis (This Project)** | **< 1ms** | **✅ Preserving** | **✅ Works** | **Low** |
| Static ACLs | Fast | ✅ | ✅ | Low |

### Dataset

- **Source:** [Unicauca Network Traffic Dataset](https://www.kaggle.com/datasets/jsrojas/ip-network-traffic-flows-labeled-with-87-apps) — 87 labeled applications
- **Feature Reduction:** 87 original features → **4 key features** (using correlation heatmap analysis)
- **Class Balancing:** Synthetic data generation for equal class representation
- **Train/Test Split:** 80% / 20%

---

## 🔮 Future Work

- [ ] **Raspberry Pi Deployment** — Run as a physical gateway between two computers
- [ ] **Deep Learning (CNN)** — Improve detection of obfuscated TLS 1.3 traffic
- [ ] **Reinforcement Learning** — RL agent that learns optimal paths from real-time jitter/loss feedback
- [ ] **Multi-Protocol Support** — Extend beyond VoIP/Streaming/Web to QUIC, WebRTC, RTSP
- [ ] **Live PCAP Integration** — Connect to a real network interface via `scapy` or `pyshark`

---

## 🛠️ Tech Stack

| Layer | Technologies |
|---|---|
| **AI / ML** | XGBoost, Scikit-learn, NumPy, Pandas |
| **Networking** | Python Sockets (UDP), NetworkX |
| **Dashboard** | Streamlit, Matplotlib |
| **Model Persistence** | Joblib (.pkl) |
| **Training Environment** | Google Colab + VS Code |



## 📄 License

This project is licensed under the MIT License. See [LICENSE](LICENSE) for details.



<div align="center">

**If this project helped you, please give it a ⭐ — it helps others find it!**

*Built with Python, XGBoost, and Streamlit at NUST *

</div>
