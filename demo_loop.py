import time
import json
import random
import datetime
import os
from ciro_orchestrator import run_ciro_system

# Randomized Karachi Hotspots
KARACHI_HOTSPOTS = [
    {"name": "Surjani Town", "coords": [25.02, 67.04], "type": "Flood"},
    {"name": "I.I. Chundrigar Road", "coords": [24.85, 67.01], "type": "Traffic Blockage"},
    {"name": "Lyari", "coords": [24.87, 66.99], "type": "Fire"},
    {"name": "Gulshan-e-Iqbal", "coords": [24.92, 67.09], "type": "Heatwave"},
    {"name": "Clifton", "coords": [24.81, 67.03], "type": "Storm Surge"}
]

def initialize_skeleton():
    """Initialize JSONs so frontend isn't blank on first load."""
    if not os.path.exists("live_stream.json"):
        with open("live_stream.json", "w") as f:
            json.dump([{"time": "00:00:00", "agent": "System", "msg": "CIRO Karachi Online. Waiting for signals..."}], f)
    
    if not os.path.exists("agent_trace.json"):
        skeleton_trace = {
            "timestamp": datetime.datetime.now().isoformat(),
            "impact_score": 0,
            "resources_remaining": {"ambulances": 15, "fire_trucks": 8, "boats": 5},
            "final_traffic_index": 50,
            "optimization_metrics": {
                "efficiency": {"efficiency": 0},
                "priority_logic": {"decision": "Monitoring Karachi sectors..."},
                "ticker_logs": ["[SYSTEM] Link Established."]
            },
            "status": "Stable"
        }
        with open("agent_trace.json", "w") as f:
            json.dump(skeleton_trace, f)

def demo_mode():
    print("=== CIRO KARACHI DEMO LOOP STARTED ===")
    print("Refreshing every 10 seconds with randomized crisis data...")
    initialize_skeleton()
    
    while True:
        hotspot = random.choice(KARACHI_HOTSPOTS)
        print(f"\n[DEMO] Simulating {hotspot['type']} at {hotspot['name']}...")
        
        # Trigger the orchestrator
        # We pass a scenario name to simulate different Karachi regions
        try:
            run_ciro_system(f"DEMO_{hotspot['name'].replace(' ', '_')}")
        except Exception as e:
            print(f"Orchestrator Error: {e}")
            
        time.sleep(10)

if __name__ == "__main__":
    demo_mode()
