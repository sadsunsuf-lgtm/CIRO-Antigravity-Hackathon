import json
import os
import datetime
from .agents import (
    SocialSignalAgent, WeatherAgent, TrafficAgent, CrisisDetectionAgent,
    ReasoningAgent, SeverityAnalysisAgent, ActionPlanningAgent,
    NotificationAgent, SimulationAgent, OutcomeEvaluationAgent,
    DroneVerificationAgent, ResourceInventoryAgent, DispatchAgent,
    TrafficGridAgent, SafetyManualAgent
)

def run_ciro_system(scenario="STANDARD"):
    print(f"\n=== CIRO ORCHESTRATION: {scenario} MODE ===")
    
    # Initialize all agents
    agents = {
        "social": SocialSignalAgent(),
        "weather": WeatherAgent(),
        "traffic": TrafficAgent(),
        "grid": TrafficGridAgent(),
        "safety": SafetyManualAgent(),
        "drone": DroneVerificationAgent(),
        "resource": ResourceInventoryAgent(),
        "detection": CrisisDetectionAgent(),
        "reasoning": ReasoningAgent(),
        "severity": SeverityAnalysisAgent(),
        "planning": ActionPlanningAgent(),
        "dispatch": DispatchAgent(),
        "notify": NotificationAgent(),
        "simulation": SimulationAgent(),
        "outcome": OutcomeEvaluationAgent()
    }
    
    # Step 1: Signal Ingestion
    twitter_path = 'mock_signals/twitter_feed.json'
    if os.path.exists(twitter_path):
        with open(twitter_path, 'r') as f:
            twitter_raw = json.load(f).get('data', [])
        social_signals = agents["social"].process_signals(twitter_raw)
    
    # Step 2: Traffic Arterial Monitoring
    traffic_jams = agents["grid"].get_jams()

    # Step 3: Crisis Detection
    detected_crisis = agents["detection"].detect([])
    
    # Step 4: Safety Protocols
    safety_checklist = agents["safety"].get_checklist(detected_crisis["type"])

    # Step 5: Drone Dispatch Logic
    agents["drone"].verify(24.8607, 67.0011)

    # Step 6: Severity & Impact
    impact_score = agents["severity"].calculate_impact(85, 1200, 480)
    efficiency_stats = agents["severity"].calculate_resource_savings(45)

    # Step 7: Dispatch & Ticker
    agents["resource"].dispatch("ambulances", 3)
    ticker_logs = []
    ticker_logs.append(agents["dispatch"].generate_ticker_log("Drone", "Drone scanning Surjani sectors..."))
    ticker_logs.append(agents["dispatch"].generate_ticker_log("Traffic", "Shahrah-e-Faisal BLOCKED due to water."))
    ticker_logs.append(agents["dispatch"].generate_ticker_log("SOS", "Alerting Edhi (115) and Chhipa (1020)..."))

    # Step 8: Conflict Handling
    crises = [{"type": "Flood", "loc": "Surjani"}, {"type": "Heatwave", "loc": "Lyari"}]
    priority_matrix = agents["planning"].generate_priority_matrix(crises)

    # Step 9: Save Final Trace for Karachi Emergency App
    full_trace = {
        "timestamp": datetime.datetime.now().isoformat(),
        "crisis_type": detected_crisis["type"],
        "impact_score": impact_score,
        "resources_remaining": agents["resource"].get_status(),
        "traffic_jams": traffic_jams,
        "safety_checklist": safety_checklist,
        "optimization_metrics": {
            "efficiency": efficiency_stats,
            "priority_logic": priority_matrix,
            "ticker_logs": ticker_logs
        },
        "status": agents["outcome"].evaluate()
    }
    
    with open('agent_trace.json', 'w') as f:
        json.dump(full_trace, f, indent=4)

    print("\n=== KARACHI EMERGENCY APP REFACTOR COMPLETE ===")
    print(f"Alert: {detected_crisis['type']} | Efficiency: {efficiency_stats['efficiency']}%")

if __name__ == "__main__":
    run_ciro_system("KARACHI_APP_V2")