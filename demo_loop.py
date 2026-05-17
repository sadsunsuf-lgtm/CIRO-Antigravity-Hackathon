import time
import json
import random
import datetime
import os
from ciro_orchestrator import run_ciro_system

# Randomized Pakistan-Wide Hotspots
PAKISTAN_HOTSPOTS = [
    {"name": "Surjani Town", "city": "Karachi", "coords": [25.02, 67.04], "type": "Flood"},
    {"name": "I.I. Chundrigar Road", "city": "Karachi", "coords": [24.85, 67.01], "type": "Traffic Blockage"},
    {"name": "Ravi River", "city": "Lahore", "coords": [31.59, 74.32], "type": "Flood"},
    {"name": "Mall Road", "city": "Lahore", "coords": [31.55, 74.32], "type": "Traffic Blockage"},
    {"name": "G-10", "city": "Islamabad", "coords": [33.68, 73.04], "type": "Flood"},
    {"name": "Qissa Khwani", "city": "Peshawar", "coords": [34.01, 71.58], "type": "Heatwave"},
    {"name": "Circular Road", "city": "Multan", "coords": [30.19, 71.48], "type": "Heatwave"},
    {"name": "City Center", "city": "Quetta", "coords": [30.18, 66.98], "type": "Cold Wave"},
    {"name": "Indus Area", "city": "Hyderabad", "coords": [25.36, 68.37], "type": "Flood"}
]

def initialize_skeleton():
    """Initialize JSONs so frontend isn't blank on first load."""
    if not os.path.exists("live_stream.json"):
        with open("live_stream.json", "w") as f:
            json.dump([{"time": "00:00:00", "agent": "System", "msg": "CIRO Pakistan Online. Waiting for signals..."}], f)
    
    if not os.path.exists("agent_trace.json"):
        skeleton_trace = {
            "timestamp": datetime.datetime.now().isoformat(),
            "impact_score": 0,
            "resources_remaining": {"ambulances": 15, "fire_trucks": 8, "boats": 5},
            "final_traffic_index": 50,
            "optimization_metrics": {
                "efficiency": {"efficiency": 0},
                "priority_logic": {"decision": "Monitoring national sectors..."},
                "ticker_logs": ["[SYSTEM] Link Established."]
            },
            "status": "Stable"
        }
        with open("agent_trace.json", "w") as f:
            json.dump(skeleton_trace, f)

def demo_mode():
    print("=== CIRO PAKISTAN DEMO LOOP STARTED ===")
    print("Refreshing every 10 seconds with randomized national crisis data...")
    initialize_skeleton()
    
    while True:
        hotspot = random.choice(PAKISTAN_HOTSPOTS)
        print(f"\n[DEMO] Simulating {hotspot['type']} at {hotspot['name']}, {hotspot['city']}...")
        
        # Trigger the orchestrator
        # We pass a scenario name to simulate different regions
        try:
            run_ciro_system(f"DEMO_{hotspot['city'].upper()}_{hotspot['name'].replace(' ', '_')}")
        except Exception as e:
            print(f"Orchestrator Error: {e}")
            
        time.sleep(10)

if __name__ == "__main__":
    demo_mode()
