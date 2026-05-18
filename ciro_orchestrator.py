"""
CIRO — Crisis Intelligence & Response Orchestrator
Google Antigravity Hackathon 2026

This orchestrator uses Google Gemini (Antigravity) to generate
natural-language reasoning summaries at the crisis detection stage.
All 15 agents run autonomously; Gemini enhances the reasoning layer.
"""
import json
import os
import datetime

# ─── Google Gemini / Antigravity Integration ─────────────────────────────────
try:
    import google.generativeai as genai
    _key = os.environ.get("GEMINI_API_KEY", "")
    if _key:
        genai.configure(api_key=_key)
        ANTIGRAVITY_MODEL = genai.GenerativeModel(
            model_name="gemini-2.0-flash",
            system_instruction=(
                "You are the reasoning core of CIRO, Pakistan's Crisis Intelligence System. "
                "Given a crisis situation, produce a 3-sentence strategic reasoning summary: "
                "(1) what you detected, (2) why it is high priority, (3) what the key action is."
            )
        )
        HAS_ANTIGRAVITY = True
    else:
        HAS_ANTIGRAVITY = False
except ImportError:
    HAS_ANTIGRAVITY = False

def antigravity_reasoning(crisis_type: str, location: str, confidence: float, severity: int) -> str:
    """Call Gemini to generate a natural-language reasoning summary for the detected crisis."""
    if not HAS_ANTIGRAVITY:
        return (
            f"[Local Reasoning] Detected {crisis_type} at {location}. "
            f"Confidence: {confidence} | Severity: {severity}/150. "
            f"Dispatching emergency response units."
        )
    try:
        prompt = (
            f"Crisis detected: {crisis_type} at {location}, Pakistan. "
            f"Confidence score: {confidence}. Severity index: {severity}/150. "
            f"Generate a 3-sentence strategic reasoning summary."
        )
        response = ANTIGRAVITY_MODEL.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        return f"[Antigravity reasoning unavailable: {e}]"

# ─────────────────────────────────────────────────────────────────────────────
from agents import (
    SocialSignalAgent, WeatherAgent, TrafficAgent, CrisisDetectionAgent,
    ReasoningAgent, SeverityAnalysisAgent, ActionPlanningAgent,
    NotificationAgent, SimulationAgent, OutcomeEvaluationAgent,
    DroneVerificationAgent, ResourceInventoryAgent, DispatchAgent,
    TrafficGridAgent, SafetyManualAgent
)


def load_json(path):
    if not os.path.exists(path):
        return None
    with open(path, 'r', encoding='utf-8') as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return None


def fallback_signal_data(source):
    if source == 'weather':
        return {
            'data': {
                'city': 'Unknown',
                'region': 'Unknown',
                'warning_level': 'Yellow',
                'current_rain_mm': 15,
                'temperature_c': 35,
                'humidity_percent': 70,
                'flood_risk': 'Moderate',
                'heatwave_risk': 'Medium',
                'wind_speed_kmh': 22,
                'forecast_next_3h': 'Moderate showers possible',
                'source': 'Cached PMD fallback',
                'credibility_score': 0.65
            }
        }
    if source == 'traffic':
        return {
            'data': {
                'city': 'Unknown',
                'location': 'Unknown Corridor',
                'status': 'Slow',
                'cause': 'Stale traffic data',
                'delay_minutes': 20,
                'congestion_level': 'Medium',
                'affected_roads': [],
                'alternate_routes': [],
                'vehicles_stranded': 0,
                'last_updated': datetime.datetime.now().isoformat(),
                'source': 'Cached NHA fallback',
                'credibility_score': 0.60
            }
        }
    return None


def infer_crisis_type(weather_data, traffic_data, social_signals):
    types = []
    if weather_data:
        warning = weather_data.get('warning_level', '').lower()
        flood_risk = weather_data.get('flood_risk', '').lower()
        heat_risk = weather_data.get('heatwave_risk', '').lower()
        if 'red' in warning or 'critical' in flood_risk:
            types.append('Urban Flooding')
        if 'high' in heat_risk or 'heat' in warning:
            types.append('Heatwave')

    if traffic_data:
        cause = traffic_data.get('cause', '').lower()
        if 'flood' in cause or 'waterlogging' in cause:
            types.append('Urban Flooding')
        if 'accident' in cause or 'blocked' in traffic_data.get('status', '').lower():
            types.append('Road Blockage')

    if social_signals:
        for signal in social_signals:
            text = signal.get('text', '').lower()
            if 'heatwave' in text or 'heat' in text or 'temperature' in text:
                types.append('Heatwave')
            if 'fire' in text or 'smoke' in text:
                types.append('Industrial Fire')
            if 'flood' in text or 'pani' in text or 'water' in text:
                types.append('Urban Flooding')
            if 'blocked' in text or 'stuck' in text or 'accident' in text:
                types.append('Road Blockage')

    if not types:
        return 'Unknown Incident'
    if 'Urban Flooding' in types:
        return 'Urban Flooding'
    if 'Heatwave' in types:
        return 'Heatwave'
    if 'Industrial Fire' in types:
        return 'Industrial Fire'
    return types[0]


def fuse_signals(weather_data, traffic_data, social_signals, degraded_mode=False):
    credibility = {
        'weather': weather_data.get('data', {}).get('credibility_score', 0.0) if weather_data else 0.0,
        'traffic': traffic_data.get('data', {}).get('credibility_score', 0.0) if traffic_data else 0.0,
        'social_avg': 0.0
    }
    social_scores = []
    suspicious_sources = []
    contradictory_signal = False
    mention_velocity = 0

    if social_signals:
        for post in social_signals:
            user = post.get('user', '')
            text = post.get('text', '').lower()
            if user in ['@KarachiRain', '@CitizenReport', '@IslamabadAlert', '@KarachiLive']:
                social_scores.append(0.75)
            elif user == '@TrollAccount':
                social_scores.append(0.20)
                suspicious_sources.append(user)
            else:
                social_scores.append(0.50)

            keywords = ['flood', 'rain', 'stuck', 'water', 'heatwave', 'smoke', 'blocked', 'accident']
            if any(kw in text for kw in keywords):
                mention_velocity += 1

            if ('no rain' in text or 'everything is fine' in text or 'fine' in text) and weather_data:
                if weather_data.get('data', {}).get('warning_level') == 'Red':
                    contradictory_signal = True
                    suspicious_sources.append(user)

    if social_scores:
        credibility['social_avg'] = round(sum(social_scores) / len(social_scores), 2)
    else:
        credibility['social_avg'] = 0.5

    weather_score = credibility['weather']
    traffic_score = credibility['traffic']
    social_score = credibility['social_avg']
    confidence = (weather_score * 0.40) + (traffic_score * 0.35) + (social_score * 0.25)
    if mention_velocity > 5:
        confidence += 0.20
    elif mention_velocity > 2:
        confidence += 0.10
    if contradictory_signal:
        confidence -= 0.15

    if degraded_mode:
        confidence -= 0.20

    confidence = max(0.0, min(1.0, confidence))

    severity = 0
    if weather_data:
        w = weather_data.get('data', {})
        if w.get('warning_level') == 'Red':
            severity += 50
        if w.get('current_rain_mm', 0) > 30:
            severity += 20
        if w.get('heatwave_risk', '').lower() == 'high':
            severity += 25
    if traffic_data:
        t = traffic_data.get('data', {})
        if t.get('status') == 'Blocked':
            severity += 40
        if t.get('delay_minutes', 0) > 60:
            severity += 20
        if 'accident' in t.get('cause', '').lower():
            severity += 20

    severity += mention_velocity * 5
    severity = min(150, severity)

    crisis_type = infer_crisis_type(weather_data.get('data', {}) if weather_data else None,
                                    traffic_data.get('data', {}) if traffic_data else None,
                                    social_signals)

    location = None
    if traffic_data:
        location = traffic_data.get('data', {}).get('location')
    if not location and social_signals:
        location = social_signals[0].get('location')
    location = location or 'Unknown Location'

    return {
        'crisis_detected': severity > 50,
        'crisis_type': crisis_type,
        'location': location,
        'severity_score': severity,
        'confidence_score': round(confidence, 2),
        'confidence_explanation': f"Multi-source fusion gives a confidence of {round(confidence, 2)} with {mention_velocity} matched signals. Contradictions: {contradictory_signal}. Degraded mode: {degraded_mode}.",
        'contradictory_signals': contradictory_signal,
        'contradictory_sources': list(set(suspicious_sources)),
        'credibility_breakdown': credibility,
        'mention_velocity': mention_velocity,
        'degraded_mode': degraded_mode,
        'recommended_action': 'DISPATCH EMERGENCY RESPONSE' if severity > 80 else 'MONITOR SITUATION'
    }


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
    weather_path = 'mock_signals/weather_alerts.json'
    traffic_path = 'mock_signals/traffic_updates.json'

    twitter_data = load_json(twitter_path)
    weather_data = load_json(weather_path)
    traffic_data = load_json(traffic_path)

    weather_missing = weather_data is None
    traffic_missing = traffic_data is None

    if weather_missing:
        weather_data = fallback_signal_data('weather')
    if traffic_missing:
        traffic_data = fallback_signal_data('traffic')

    social_signals = []
    if twitter_data and 'data' in twitter_data:
        social_signals = agents["social"].process_signals(twitter_data['data'])

    weather_analysis = agents["weather"].analyze(weather_data.get('data') if weather_data else {})
    traffic_analysis = agents["traffic"].analyze(traffic_data.get('data') if traffic_data else {})

    degraded_mode = weather_missing or traffic_missing
    fused_report = fuse_signals(weather_data, traffic_data, social_signals, degraded_mode=degraded_mode)

    # Step 2: Traffic Arterial Monitoring
    traffic_jams = agents["grid"].get_jams()

    # Step 3: Crisis Detection
    detected_crisis = agents["detection"].detect(fused_report)

    # Step 4: Reasoning and Conflict Handling
    conflict_decision = agents["reasoning"].handle_conflict(fused_report)
    if fused_report.get('contradictory_signals'):
        detected_crisis['recommended_action'] = "VERIFY BEFORE DISPATCH"
        detected_crisis['confidence'] = round(min(detected_crisis['confidence'], 0.75), 2)

    # Step 5: Safety Protocols
    safety_checklist = agents["safety"].get_checklist(detected_crisis["type"])

    # Step 5: Drone Dispatch Logic
    agents["drone"].verify(24.8607, 67.0011)

    # ── Antigravity / Gemini Reasoning Layer ─────────────────────────────────
    # Call Google Gemini to generate a natural-language strategic reasoning
    # summary for this crisis — this is the Antigravity intelligence layer.
    ai_reasoning = antigravity_reasoning(
        crisis_type=detected_crisis["type"],
        location=detected_crisis["location"],
        confidence=detected_crisis["confidence"],
        severity=detected_crisis["severity"]
    )
    print(f"\n[ANTIGRAVITY] {ai_reasoning}\n")
    # ─────────────────────────────────────────────────────────────────────────

    # Step 6: Severity & Impact
    impact_score = agents["severity"].calculate_impact(85, 1200, 480)
    efficiency_stats = agents["severity"].calculate_resource_savings(45)

    # Step 7: Multi-Crisis Response Planning
    secondary_crisis = {
        "type": "Heatwave",
        "location": "Lyari",
        "severity": 72,
        "confidence": 0.84,
        "recommended_action": "DEPLOY_MEDICAL_OUTREACH"
    }
    primary_crisis = {
        "type": detected_crisis["type"],
        "location": detected_crisis["location"],
        "severity": detected_crisis["severity"],
        "confidence": detected_crisis["confidence"],
        "recommended_action": detected_crisis["recommended_action"]
    }
    crises = [primary_crisis, secondary_crisis]
    priority_matrix = agents["planning"].generate_priority_matrix(crises)

    resource_snapshot = agents["resource"].get_status()
    plan_result = agents["planning"].plan(crises, resource_snapshot)

    dispatch_actions = plan_result["actions"]
    for action in dispatch_actions:
        for unit, count in action["resources_allocated"].items():
            if count > 0:
                agents["resource"].dispatch(unit, count)

    dispatch_result = agents["dispatch"].execute(plan_result)

    # Step 8: Action Simulation and Evaluation
    simulation_result = agents["simulation"].simulate(plan_result)
    outcome_status = agents["outcome"].evaluate(simulation_result)

    ticker_logs = []
    ticker_logs.append(agents["dispatch"].generate_ticker_log("Drone", "Drone scanning Surjani sectors..."))
    ticker_logs.append(agents["dispatch"].generate_ticker_log("Traffic", "Shahrah-e-Faisal BLOCKED due to water."))
    ticker_logs.append(agents["dispatch"].generate_ticker_log("SOS", "Alerting Edhi (115) and Chhipa (1020)..."))

    # Step 9: Save Final Trace for Pakistan Emergency App
    full_trace = {
        "timestamp": datetime.datetime.now().isoformat(),
        "crisis_type": detected_crisis["type"],
        "antigravity_reasoning": ai_reasoning,          # ← Gemini-generated reasoning
        "impact_score": impact_score,
        "resources_remaining": agents["resource"].get_status(),
        "dispatch_result": dispatch_result,
        "simulation": simulation_result,
        "outcome_status": outcome_status,
        "traffic_jams": traffic_jams,
        "safety_checklist": safety_checklist,
        "degraded_mode": fused_report.get('degraded_mode', False),
        "conflict_decision": conflict_decision,
        "fused_report": fused_report,
        "optimization_metrics": {
            "efficiency": efficiency_stats,
            "priority_logic": priority_matrix,
            "ticker_logs": ticker_logs
        },
        "status": outcome_status
    }
    
    with open('agent_trace.json', 'w') as f:
        json.dump(full_trace, f, indent=4)

    print("\n=== CIRO PAKISTAN ORCHESTRATION COMPLETE ===")
    print(f"Alert: {detected_crisis['type']} | Efficiency: {efficiency_stats['efficiency']}%")

if __name__ == "__main__":
    run_ciro_system("PAKISTAN_APP_V2")
