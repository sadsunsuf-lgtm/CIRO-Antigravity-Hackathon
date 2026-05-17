"""
CIRO API — /api/trace
Vercel Serverless Function (Python)
Returns a pre-built agent trace demonstrating the CIRO orchestration pipeline.
"""
from http.server import BaseHTTPRequestHandler
import json

STATIC_TRACE = {
    "agent_trace": {
        "timestamp": "2026-05-17T22:00:00+05:00",
        "crisis_type": "Urban Flooding",
        "location": "G-10, Islamabad / Surjani Town, Karachi",
        "impact_score": 89,
        "severity_score": 115,
        "confidence_score": 0.87,
        "resources_remaining": {
            "ambulances": 12,
            "fire_trucks": 6,
            "boats": 3,
            "rescue_teams": 8
        },
        "dispatch_result": {
            "status": "Dispatched",
            "units_deployed": ["Ambulance x3", "Rescue Boat x2", "Drone Unit x1", "Fire Truck x2"]
        },
        "simulation": {
            "lives_saved_estimate": 47,
            "response_time_minutes": 8,
            "flood_containment_pct": 72
        },
        "outcome_status": "Crisis Contained — 87% Efficiency",
        "degraded_mode": False,
        "fused_report": {
            "crisis_detected": True,
            "crisis_type": "Urban Flooding",
            "confidence_score": 0.87,
            "mention_velocity": 9,
            "contradictory_signals": False,
            "credibility_breakdown": {
                "weather": 0.91,
                "traffic": 0.85,
                "social_avg": 0.76
            }
        },
        "optimization_metrics": {
            "efficiency": {"efficiency": 87},
            "priority_logic": {"decision": "Urban Flooding → Heatwave (triage cascade)"},
            "ticker_logs": [
                "[AGENT:Social] 9 high-velocity signals detected",
                "[AGENT:Weather] PMD Red Alert — 72mm rainfall in 3hrs",
                "[AGENT:Traffic] Shahrah-e-Faisal BLOCKED — 3km backup",
                "[AGENT:Drone] Verification scan initiated at 24.86°N 67.01°E",
                "[AGENT:Detection] CRISIS CONFIRMED — Severity 115/150",
                "[AGENT:Reasoning] Confidence 0.87 — No contradictions",
                "[AGENT:Planning] Primary: Flood Response | Secondary: Heatwave Monitor",
                "[AGENT:Dispatch] 3 Ambulances + 2 Boats + Drone deployed",
                "[AGENT:Simulation] ETA 8 min | 47 lives in risk zone",
                "[AGENT:Outcome] 87% efficiency — Crisis Contained"
            ]
        },
        "status": "Crisis Contained — 87% Efficiency"
    },
    "live_stream": [
        {"time": "22:00:01", "agent": "Social", "msg": "9 urgent signals detected from Twitter/X — Flood keywords spiking"},
        {"time": "22:00:03", "agent": "Weather", "msg": "PMD Red Alert: 72mm rainfall/3hrs — Flood risk CRITICAL"},
        {"time": "22:00:05", "agent": "Traffic", "msg": "Shahrah-e-Faisal BLOCKED — waterlogging reported at 5 points"},
        {"time": "22:00:07", "agent": "Drone", "msg": "Drone dispatched to 24.86N 67.01E for visual verification"},
        {"time": "22:00:09", "agent": "Detection", "msg": "CRISIS CONFIRMED: Urban Flooding — Severity 115/150"},
        {"time": "22:00:11", "agent": "Dispatch", "msg": "3 Ambulances + 2 Rescue Boats + Drone deployed to Surjani Town"},
        {"time": "22:00:13", "agent": "Simulation", "msg": "8-minute ETA — 47 civilians in immediate flood zone"},
        {"time": "22:00:15", "agent": "Outcome", "msg": "87% efficiency — Crisis Contained. Resources: 12 Amb, 6 Trucks, 3 Boats remaining"}
    ]
}

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        response_body = json.dumps(STATIC_TRACE).encode()
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Content-Length", str(len(response_body)))
        self.end_headers()
        self.wfile.write(response_body)

    def log_message(self, format, *args):
        pass
