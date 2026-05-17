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
        result = {
            "detected": fused_data.get("crisis_detected", False),
            "type": fused_data.get("crisis_type", "Unknown Incident"),
            "confidence": fused_data.get("confidence_score", 0.0),
            "severity": fused_data.get("severity_score", 0),
            "location": fused_data.get("location", "Unknown Location"),
            "recommended_action": fused_data.get("recommended_action", "MONITOR SITUATION")
        }
        self.log(
            f"Detection complete: {result['type']} at {result['location']}.",
            reasoning=f"Confidence {result['confidence']} from fused multi-source evidence.",
            confidence=result['confidence'],
            metadata={"severity": result['severity'], "recommended_action": result['recommended_action']}
        )
        return result

class ReasoningAgent(CIROAgent):
    def __init__(self):
        super().__init__("ReasoningAgent", "Decision Logic")

    def handle_conflict(self, fused_data):
        notes = []
        matrix = None

        if fused_data.get('degraded_mode'):
            notes.append("Degraded mode engaged: fallback data used for missing source(s).")

        if fused_data.get('contradictory_signals'):
            notes.append("Contradictory social signals detected against official warnings.")
            notes.append("Verification required before full public alert.")
            matrix = {
                "Official Warning": {"Confidence": fused_data.get('credibility_breakdown', {}).get('weather', 0.0), "Action": "Verify"},
                "Social Reports": {"Confidence": fused_data.get('credibility_breakdown', {}).get('social_avg', 0.0), "Action": "Flag for manual review"}
            }
            decision = "VERIFY_AND_HOLD_ALERT"
        else:
            notes.append("No major conflicts detected; proceeding with planned response.")
            decision = "CONFIRM_ALERT"

        self.log(
            "Reasoning completed for crisis situation.",
            reasoning="; ".join(notes),
            metadata={"conflict_matrix": matrix, "decision": decision}
        )
        return {"decision": decision, "notes": notes, "matrix": matrix}

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
            c_risk = "High" if c['type'] in ['Heatwave', 'Urban Flooding'] else "Medium"
            i_risk = "High" if c['type'] in ['Flood', 'Urban Flooding', 'Infrastructure Failure'] else "Medium"
            matrix.append({
                "type": c['type'],
                "location": c.get('location'),
                "severity": c.get('severity', 0),
                "confidence": c.get('confidence', 0),
                "casualty_risk": c_risk,
                "infra_risk": i_risk
            })
        sorted_list = sorted(crisis_list, key=lambda x: (x.get('severity', 0) * x.get('confidence', 0)), reverse=True)
        top = sorted_list[0] if sorted_list else None
        decision = f"Prioritizing {top['type']} at {top.get('location')} based on highest weighted urgency." if top else "No crisis to prioritize."
        self.log(decision, reasoning="Ranking crises by severity and confidence to allocate constrained resources.", metadata={"matrix": matrix})
        return {"matrix": matrix, "priority_order": [c['type'] for c in sorted_list], "decision": decision}

    def plan(self, crisis_list, resource_status):
        self.log("Generating coordinated response plan for simultaneous incidents.")
        available = resource_status.copy()
        actions = []
        for crisis in sorted(crisis_list, key=lambda x: (x.get('severity', 0) * x.get('confidence', 0)), reverse=True):
            resources = {}
            if crisis['type'] in ['Urban Flooding', 'Flood']:
                resources = {"ambulances": 2, "fire_trucks": 1, "boats": 2}
            elif crisis['type'] == 'Heatwave':
                resources = {"ambulances": 3, "fire_trucks": 0, "boats": 0}
            elif crisis['type'] == 'Industrial Fire':
                resources = {"ambulances": 2, "fire_trucks": 3, "boats": 0}
            elif crisis['type'] == 'Road Blockage':
                resources = {"ambulances": 1, "fire_trucks": 1, "boats": 0}
            else:
                resources = {"ambulances": 1, "fire_trucks": 0, "boats": 0}

            allocated = {}
            shortages = {}
            for unit, requested in resources.items():
                available_count = available.get(unit, 0)
                allocated[unit] = min(requested, available_count)
                shortages[unit] = requested - allocated[unit]
                available[unit] = available_count - allocated[unit]

            crisis_actions = ["Send alert to public", "Notify nearest hospital", "Verify incident via drone"]
            if crisis['type'] in ['Urban Flooding', 'Flood']:
                crisis_actions.insert(0, "Reroute traffic away from flooded corridors")
                crisis_actions.append("Deploy rescue boats")
            if crisis['type'] == 'Heatwave':
                crisis_actions.insert(0, "Open cooling shelters")
                crisis_actions.append("Deploy medical outreach units")
            if crisis['type'] == 'Industrial Fire':
                crisis_actions.insert(0, "Deploy fire brigade units")
                crisis_actions.append("Isolate nearby power grid")
            if crisis['type'] == 'Road Blockage':
                crisis_actions.insert(0, "Notify traffic authorities")
                crisis_actions.append("Provide alternate route guidance")

            plan_entry = {
                "type": crisis['type'],
                "location": crisis.get('location'),
                "severity": crisis.get('severity', 0),
                "confidence": crisis.get('confidence', 0),
                "actions": crisis_actions,
                "resources_requested": resources,
                "resources_allocated": allocated,
                "shortages": shortages,
                "recommended_action": crisis.get('recommended_action')
            }
            actions.append(plan_entry)

        self.log("Coordinated response plan created.", metadata={"actions": actions, "remaining_resources": available})
        return {"actions": actions, "remaining_resources": available}

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
        self.log("Executing dispatch plan for coordinated emergency response.")
        tickets = []
        for entry in plan.get('actions', []):
            ticket_id = f"TKT-{random.randint(900,999)}{random.randint(10,99)}"
            tickets.append({
                "crisis": entry['type'],
                "location": entry['location'],
                "ticket_id": ticket_id,
                "resources": entry['resources_allocated']
            })
            self.log(f"Created ticket {ticket_id} for {entry['type']} at {entry['location']}.", metadata={"resources": entry['resources_allocated']})

        return {"status": "Dispatched", "tickets": tickets, "sos": self.sos_list}

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
    def simulate(self, plan_summary):
        self.log("Simulating response execution and estimating outcome impacts.")
        actions = plan_summary.get('actions', [])
        total_actions = sum(len(entry['actions']) for entry in actions)
        total_resources = sum(sum(entry['resources_allocated'].values()) for entry in actions)

        before = {
            "congestion_level": "Critical",
            "response_delay_mins": 45,
            "public_alerts": "Not sent",
            "status": "Unresolved"
        }
        after = {
            "congestion_level": "Moderate",
            "response_delay_mins": max(10, 45 - total_actions * 3),
            "public_alerts": "Sent",
            "status": "Stabilizing"
        }

        if any(entry['type'] == 'Heatwave' for entry in actions):
            after['response_delay_mins'] = max(8, after['response_delay_mins'] - 5)
        if any(entry['type'] in ['Urban Flooding', 'Flood'] for entry in actions):
            after['congestion_level'] = "High to Moderate"

        side_effects = []
        if len(actions) > 1:
            side_effects.append("Simultaneous alerts may generate short-term evacuation congestion on alternate routes.")
        if total_resources < 5:
            side_effects.append("Limited ambulance availability may delay response to lower-priority incidents.")

        simulation = {
            "before": before,
            "after": after,
            "expected_improvement": {
                "congestion_reduction": "20-35%",
                "response_time_saving": f"{45 - after['response_delay_mins']} minutes"
            },
            "resources_used": total_resources,
            "side_effects": side_effects,
            "actions_executed": [entry['actions'] for entry in actions]
        }
        self.log("Simulation complete.", metadata=simulation)
        return simulation

class OutcomeEvaluationAgent(CIROAgent):
    def __init__(self):
        super().__init__("OutcomeAgent", "Verification")
    def evaluate(self, simulation):
        outcome = "Monitoring"
        if simulation.get('after', {}).get('status') == 'Stabilizing':
            outcome = "Contained"
        self.log(f"Outcome evaluation: {outcome}.", metadata={"simulation": simulation})
        return outcome
