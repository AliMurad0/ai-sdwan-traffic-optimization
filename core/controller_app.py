import streamlit as st
import pandas as pd
import numpy as np
import joblib
import time
import random
import networkx as nx
import matplotlib.pyplot as plt

# --- PAGE CONFIG ---
st.set_page_config(page_title="AI SD-WAN Controller", layout="wide", page_icon="📡")

# --- CUSTOM CSS ---
st.markdown("""
    <style>
    .stApp {background-color: #0E1117;}
    div.stButton > button {width: 100%; background-color: #00FF00; color: black; font-weight: bold;}
    .report-box {background-color: #1E1E1E; padding: 20px; border-radius: 10px; border: 1px solid #444;}
    .legend-box {background-color: #262730; padding: 10px; border-radius: 5px; text-align: center; border: 1px solid #555;}
    </style>
    """, unsafe_allow_html=True)

# --- 1. LOAD AI SYSTEM ---
MODEL_PATH = 'traffic_model.pkl'
ENCODER_PATH = 'label_encoder.pkl'

@st.cache_resource
def load_ai_system():
    try:
        model = joblib.load(MODEL_PATH)
        le = joblib.load(ENCODER_PATH)
        return model, le
    except:
        return None, None

model, le = load_ai_system()

# --- 2. NETWORK TOPOLOGY SETUP ---
if 'G' not in st.session_state:
    G = nx.Graph()
    G.add_nodes_from(range(14))
    # Mesh Topology Definition
    edges = [
        (0,1), (0,2), (0,3), (1,3), (1,8), (2,5), (2,3), (3,4), (3,7),
        (4,5), (4,6), (5,12), (6,7), (7,8), (7,10), (8,11), (8,9),
        (10,9), (11,9), (12,9), (12,13)
    ]
    G.add_edges_from(edges)
    st.session_state.G = G
    
    # Node Positions
    pos = nx.spring_layout(G, seed=42) 
    pos[0] = np.array([-1.2, 0])  # USER Left
    pos[9] = np.array([1.2, 0])   # SERVER Right
    st.session_state.pos = pos

# --- 3. HELPER FUNCTIONS ---

def get_active_path(path_type):
    # Blue Path (Bottom) for High Priority
    path_video = [(0,2), (2,5), (5,12), (12,9)] 
    # Red Path (Top) for Low Priority
    path_web = [(0,1), (1,8), (8,11), (11,9)]   
    return path_video if path_type == "MPLS" else path_web

def decide_route(app_name):
    # SD-WAN Policy Logic
    if app_name in ["VoIP_Call", "Streaming", "P2P_Transfer"]:
        return "MPLS", "blue"  # Priority Lane
    else:
        return "Internet", "red" # Bulk Lane

def draw_network_map(active_edges, color_code):
    G = st.session_state.G
    pos = st.session_state.pos
    fig, ax = plt.subplots(figsize=(10, 5), facecolor='#0E1117')
    
    # 1. Passive Links (Dimmed)
    nx.draw_networkx_edges(G, pos, edge_color='#333333', width=1, ax=ax, alpha=0.5)
    
    # 2. Active Traffic Path (Bright)
    nx.draw_networkx_edges(G, pos, edgelist=active_edges, edge_color=color_code, width=5, ax=ax, alpha=1.0)
    
    # 3. Switches (Small Dots)
    switches = [n for n in G.nodes() if n not in [0, 9]]
    nx.draw_networkx_nodes(G, pos, nodelist=switches, node_color='#DDDDDD', node_size=200, ax=ax)
    
    # 4. USER (Large Square)
    nx.draw_networkx_nodes(G, pos, nodelist=[0], node_color='#00FF00', node_shape='s', node_size=1000, label="USER", ax=ax)
    
    # 5. SERVER (Large Hexagon)
    nx.draw_networkx_nodes(G, pos, nodelist=[9], node_color='#FFA500', node_shape='h', node_size=1000, label="SERVER", ax=ax)
    
    # 6. Labels
    pos_attrs = {k: (v[0], v[1]+0.15) for k, v in pos.items()}
    labels = {0: "USER", 9: "CLOUD", 1:"SW1", 2:"SW2", 5:"SW5", 8:"SW8", 12:"SW12"}
    nx.draw_networkx_labels(G, pos_attrs, labels=labels, font_size=8, font_color='white', font_weight='bold', ax=ax)

    ax.set_axis_off()
    return fig

# --- 4. MAIN LAYOUT ---
st.title("🛡️ AI SD-WAN Controller")

# --- LEGEND BAR ---
st.markdown("""
<div class="legend-box">
    <b>TRAFFIC LEGEND:</b> &nbsp;&nbsp;&nbsp; 
    🔵 <span style='color:#3498db; font-weight:bold'>BLUE PATH: MPLS (VoIP/Video)</span> 
    &nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;&nbsp; 
    🔴 <span style='color:#e74c3c; font-weight:bold'>RED PATH: Internet (Web/Email)</span>
</div>
<br>
""", unsafe_allow_html=True)

# Split Layout: Map vs Stats
col_left, col_right = st.columns([2.5, 1])

with col_left:
    st.subheader("🌐 Live Network Mesh")
    graph_place = st.empty()

with col_right:
    st.subheader("📡 Live Analysis")
    metric_container = st.empty()
    st.divider()
    st.subheader("📜 Recent Logs")
    log_place = st.empty()

# --- GRAPHS SECTION (NEW!) ---
st.divider()
col_g1, col_g2 = st.columns(2)

with col_g1:
    st.subheader("📉 Network Latency (Jitter)")
    # Placeholder for Jitter Graph
    jitter_chart_place = st.empty()

with col_g2:
    st.subheader("📊 Application Distribution")
    # Placeholder for Bar Chart
    bar_chart_place = st.empty()

# --- 5. SIMULATION LOGIC ---
if st.button("▶️ START DIVERSE TRAFFIC SIMULATION"):
    
    # A. Init Data Lists for Graphs
    jitter_data = []
    app_counts = {"Web": 0, "VoIP": 0, "Video": 0, "Other": 0}
    
    # B. Traffic Playlist (To ensure variety)
    traffic_playlist = [
        "Web_Browsing", "Web_Browsing", 
        "VoIP_Call", "VoIP_Call", 
        "Streaming", "Streaming", 
        "Email", "P2P_Transfer", 
        "VoIP_Call", "Web_Browsing",
        "Streaming", "VoIP_Call",
        "Web_Browsing", "Email"
    ]
    
    session_history = []
    
    # Run loop
    for i in range(len(traffic_playlist)):
        app_name = traffic_playlist[i] 
        
        # 1. Routing Decision
        route_type, color_code = decide_route(app_name)
        active_edges = get_active_path(route_type)
        
        # 2. Simulate Jitter (Graph Data)
        # MPLS (Blue) = Stable (Low Jitter 2-10ms)
        # Internet (Red) = Unstable (High Jitter 20-80ms)
        if route_type == "MPLS":
            current_jitter = random.randint(2, 10)
        else:
            current_jitter = random.randint(20, 80)
            
        jitter_data.append(current_jitter)
        
        # 3. Update Counts (Graph Data)
        if "Web" in app_name: app_counts["Web"] += 1
        elif "VoIP" in app_name: app_counts["VoIP"] += 1
        elif "Streaming" in app_name: app_counts["Video"] += 1
        else: app_counts["Other"] += 1

        # 4. Record History
        timestamp = time.strftime("%H:%M:%S")
        session_history.append({"ID": i+1, "Time": timestamp, "App": app_name, "Route": route_type})
        
        # 5. UPDATE VISUALS
        
        # A. Network Map
        fig = draw_network_map(active_edges, color_code)
        graph_place.pyplot(fig)
        plt.close(fig)
        
        # B. Metrics
        with metric_container.container():
            st.metric("Detected App", app_name)
            if route_type == "MPLS":
                st.success(f"Route: {route_type}")
            else:
                st.error(f"Route: {route_type}")
        
        # C. Logs (Side Panel)
        with log_place.container():
            recent_df = pd.DataFrame(session_history[-3:])
            st.dataframe(recent_df[["Time", "App", "Route"]], hide_index=True)

        # D. LIVE GRAPHS (Here is the update!)
        with jitter_chart_place.container():
            # Create simple line chart
            st.line_chart(jitter_data, height=200)
            
        with bar_chart_place.container():
            # Create bar chart
            st.bar_chart(app_counts, height=200)

        time.sleep(1.0) # Speed of simulation

    # --- 6. END OF SESSION SUMMARY BOX ---
    st.divider()
    st.markdown("<div class='report-box'>", unsafe_allow_html=True)
    st.subheader("✅ Simulation Complete: Session Report")
    
    df_final = pd.DataFrame(session_history)
    count_mpls = len(df_final[df_final['Route']=="MPLS"])
    count_net = len(df_final[df_final['Route']=="Internet"])
    
    col_sum1, col_sum2, col_sum3 = st.columns(3)
    col_sum1.metric("Total Packets", len(df_final))
    col_sum2.metric("Routed via MPLS (Blue)", count_mpls)
    col_sum3.metric("Routed via Internet (Red)", count_net)
    
    st.write("Full History Log:")
    st.dataframe(df_final, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)