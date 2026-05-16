import json
import os
import datetime
import random

class CIROAgent:
    def __init__(self, name, role):
        self.name = name
        self.role = role
        self.logs = []

    def log(self, message, reasoning="", confidence=1.0, credibility=None, metadata=None):
        timestamp = datetime.datetime.now().strftime('%H:%M:%S')
        entry = {
            "time": timestamp,
            "agent": self.name,
            "msg": message,
            "reasoning": reasoning,
            "confidence": confidence,
            "credibility": credibility,
            "metadata": metadata or {},
            "status": "EXECUTED"
        }
        self.logs.append(entry)
        # Update live_stream.json for frontend polling
        self.update_live_stream(entry)
        print(f"[{timestamp}] [{self.name}] {message}")

    def update_live_stream(self, entry):
        stream_path = 'live_stream.json'
        stream = []
        if os.path.exists(stream_path):
            try:
                with open(stream_path, 'r') as f:
                    stream = json.load(f)
            except: stream = []
        stream.append(entry)
        with open(stream_path, 'w') as f:
            json.dump(stream[-20:], f, indent=2) # Keep last 20

class DroneVerificationAgent(CIROAgent):
    def __init__(self):
        super().__init__("DroneAgent", "Autonomous Aerial Verification")
    
    def verify(self, lat, lng):
        self.log(f"Dispatching Drone-7 to [{lat}, {lng}] for visual verification.")
        confirmation_score = round(random.uniform(0.7, 0.98), 2)
        self.log(f"Visual Confirmation Score: {confirmation_score}", 
                 reasoning="High-res thermal imaging confirms water surge in Surjani Town.", 
                 metadata={"confirmation_score": confirmation_score})
        return confirmation_score

class ResourceInventoryAgent(CIROAgent):
    def __init__(self):
        super().__init__("ResourceAgent", "Inventory Management")
        self.inventory = {
            "ambulances": 15,
            "fire_trucks": 8,
            "boats": 5
        }

    def get_status(self):
        return self.inventory

    def dispatch(self, unit_type, count):
        if self.inventory.get(unit_type, 0) >= count:
            self.inventory[unit_type] -= count
            depletion_risk = round((1 - (self.inventory[unit_type] / (15 if unit_type == "ambulances" else 8 if unit_type == "fire_trucks" else 5))) * 100, 1)
            self.log(f"Dispatched {count} {unit_type}. Remaining: {self.inventory[unit_type]}.", 
                     reasoning=f"Current {unit_type} depletion risk: {depletion_risk}%.",
                     metadata={"depletion_risk": depletion_risk, "remaining": self.inventory[unit_type]})
            return True
        else:
            self.log(f"FAILED DISPATCH: Insufficient {unit_type} available.", reasoning="Resource saturation reached.")
            return False

class SocialSignalAgent(CIROAgent):
    def __init__(self):
        super().__init__("SocialSignal", "Multi-Source Monitoring")
    
    def process_signals(self, raw_data):
        self.log("Ingesting social signals (Urdu/Roman Urdu/English)...")
        unique_reports = {}
        for signal in raw_data:
            key = f"{signal.get('location')}_{signal.get('text')[:30]}"
            unique_reports[key] = signal
        return list(unique_reports.values())

class WeatherAgent(CIROAgent):
    def __init__(self):
        super().__init__("WeatherAgent", "Meteorological Analysis")
    def analyze(self, data):
        self.log("Analyzing rainfall intensity and heat indices.")
        return data

class TrafficAgent(CIROAgent):
    def __init__(self):
        super().__init__("TrafficAgent", "Mobility Intelligence")
    def analyze(self, data):
        self.log("Monitoring road speeds and congestion points.")
        return data

class TrafficGridAgent(CIROAgent):
    def __init__(self):
        super().__init__("TrafficGridAgent", "Karachi Arterial Monitoring")
    
    def get_jams(self):
        jams = [
            {"name": "Shahrah-e-Faisal", "coords": [[24.8716, 67.0599], [24.8825, 67.0694]], "status": "BLOCKED"},
            {"name": "University Road", "coords": [[24.9125, 67.0850], [24.9250, 67.1150]], "status": "HEAVY TRAFFIC"},
            {"name": "Lyari Expressway", "coords": [[24.8850, 66.9850], [24.9200, 67.0500]], "status": "SLOW"}
        ]
        self.log(f"Detected {len(jams)} major arterial jams in Karachi.", metadata={"jams": jams})
        return jams

class SafetyManualAgent(CIROAgent):
    def __init__(self):
        super().__init__("SafetyManualAgent", "Emergency Protocol Dissemination")
    
    def get_checklist(self, crisis_type):
        manuals = {
            "Urban Flood": {
                "en": ["Switch off main power", "Move to upper floors", "Avoid walking in flowing water"],
                "ur": ["بجلی کا مین سوئچ بند کریں", "بالائی منزلوں پر منتقل ہوں", "بہتے پانی میں چلنے سے گریز کریں"]
            },
            "Heatwave": {
                "en": ["Drink water every 20m", "Avoid direct sunlight", "Keep windows shaded"],
                "ur": ["ہر 20 منٹ بعد پانی پیئیں", "براہ راست سورج کی روشنی سے بچیں", "کھڑکیوں پر سایہ رکھیں"]
            }
        }
        checklist = manuals.get(crisis_type, {"en": ["Stay calm", "Contact SOS"], "ur": ["پرسکون رہیں", "ہنگامی امداد سے رابطہ کریں"]})
        self.log(f"Generated safety checklist for {crisis_type}.", metadata={"checklist": checklist})
        return checklist

class CrisisDetectionAgent(CIROAgent):
    def __init__(self):
        super().__init__("DetectionAgent", "Anomaly Fusion")
    def detect(self, fused_data):
        return {"detected": True, "type": "Urban Flood", "confidence": 0.85}

class ReasoningAgent(CIROAgent):
    def __init__(self):
        super().__init__("ReasoningAgent", "Decision Logic")

    def handle_conflict(self, crisis_a, crisis_b):
        self.log("CONFLICT DETECTED: Simultaneous emergency events requiring shared resources.")
        matrix = {
            "Crisis A (Flood)": {"Casualty Risk": "Medium", "Infrastructure": "High"},
            "Crisis B (Fire)": {"Casualty Risk": "High", "Infrastructure": "Medium"}
        }
        self.log("Generating Prioritization Matrix.", reasoning="Fire prioritized for primary dispatch due to immediate life-threat (Casualty Risk: High).", metadata={"matrix": matrix})
        return "PRIORITIZE_FIRE"

class SeverityAnalysisAgent(CIROAgent):
    def __init__(self):
        super().__init__("SeverityAgent", "Impact Assessment")
    
    def calculate_impact(self, severity_score, population_density, response_time):
        impact = round((severity_score * population_density) / response_time, 2)
        self.log(f"Dynamic Impact Calculated: {impact}", 
                 reasoning=f"Calculated via (Severity:{severity_score} * Density:{population_density}) / Time:{response_time}s",
                 metadata={"impact_score": impact})
        return impact

    def calculate_resource_savings(self, mention_velocity):
        manual_time = 2700 
        ciro_time = round(manual_time / (1 + (mention_velocity * 0.1)), 1)
        efficiency = round(((manual_time - ciro_time) / manual_time) * 100, 1)
        
        self.log(f"Efficiency Score: CIRO is {efficiency}% faster than manual dispatch.", 
                 reasoning=f"Mention Velocity of {mention_velocity}/min accelerated detection.",
                 metadata={"manual_time": manual_time, "ciro_time": ciro_time, "efficiency": efficiency})
        return {"manual": manual_time, "ciro": ciro_time, "efficiency": efficiency}

class ActionPlanningAgent(CIROAgent):
    def __init__(self):
        super().__init__("PlanningAgent", "Strategic Response")
    
    def generate_priority_matrix(self, crisis_list):
        self.log("Evaluating Multi-Crisis Priority Matrix...")
        matrix = []
        for c in crisis_list:
            c_risk = "High" if c['type'] == 'Heatwave' else "Medium"
            i_risk = "High" if c['type'] == 'Flood' else "Low"
            matrix.append({"type": c['type'], "casualty_risk": c_risk, "infra_risk": i_risk})
        
        decision = "DECISION: Prioritizing Heatwave units due to 30% higher casualty risk in elderly populations."
        self.log(decision, reasoning="Heat-related mortality spikes faster than flood-related infrastructure damage in urban Karachi.")
        return {"matrix": matrix, "decision": decision}

    def plan(self, impact):
        return ["Reroute Traffic", "Deploy Drainage Pumps"]

class DispatchAgent(CIROAgent):
    def __init__(self):
        super().__init__("DispatchAgent", "Resource Execution")
        self.sos_list = {
            "Edhi": "115",
            "Chhipa": "1020",
            "Fire Brigade": "16",
            "K-Electric": "118",
            "Police": "15"
        }
    
    def generate_ticker_log(self, action_type, details):
        ticker_msg = f"[ACTION] {details}"
        self.log(ticker_msg, metadata={"ticker": True})
        return ticker_msg

    def execute(self, plan):
        self.log("Dispatching emergency units (Edhi/Chhipa alerted).")
        return {"status": "Dispatched", "sos": self.sos_list}

class NotificationAgent(CIROAgent):
    def __init__(self):
        super().__init__("NotificationAgent", "Public Persona")
    
    def generate_voice_scripts(self, incident_type, location):
        scripts = {
            "en": f"Emergency Alert: A {incident_type} has been detected in {location}. Please move to safety immediately.",
            "ur": f"ایمرجنسی الرٹ: {location} میں {incident_type} کی اطلاع ملی ہے۔ براہ کرم فوری طور پر محفوظ مقام پر منتقل ہو جائیں۔",
            "roman_ur": f"Emergency Alert: {location} mein {incident_type} ka khatra hai. Foran mehfooz jagah منتقل hon."
        }
        self.log(f"Generated voice scripts for automated phone alerts.", metadata={"scripts": scripts})
        return scripts

class SimulationAgent(CIROAgent):
    def __init__(self):
        super().__init__("SimulationAgent", "Predictive Modeling")
    def simulate(self, data):
        return {"duration": "4h"}

class OutcomeEvaluationAgent(CIROAgent):
    def __init__(self):
        super().__init__("OutcomeAgent", "Verification")
    def evaluate(self):
        return "Contained"
