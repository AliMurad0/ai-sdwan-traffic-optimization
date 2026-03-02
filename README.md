# 🌐 AI-Driven SD-WAN: Intelligent Traffic Classification

This project implements a Real-Time SD-WAN simulation using **XGBoost** to classify network traffic and optimize routing paths dynamically.

## 🚀 The Real-Time Pipeline
The system consists of three active components communicating via **Socket Programming**:
1. **Sender (`sender_client.py`)**: Simulates traffic for apps like VoIP (Skype), Video (YouTube), and Web (HTTP).
2. **Router (`router_server.py`)**: Acts as the gateway, intercepting traffic flow statistics.
3. **Controller (`controller_app.py`)**: The AI Brain. It predicts the application type and chooses the **MPLS Path** for critical data or the **Broadband Path** for bulk data.

## 📊 Performance Statistics
- **Model Accuracy**: 94.1% (XGBoost) vs 74.0% (Random Forest).
- **VoIP Detection**: 96% success rate.
- **Routing Decision**: < 15ms latency.

## 🛠️ How to Run the Simulation
1. Start the Network Gateway: `python router_server.py`
2. Start the AI Controller UI: `streamlit run controller_app.py`
3. Generate Live Traffic: `python sender_client.py`