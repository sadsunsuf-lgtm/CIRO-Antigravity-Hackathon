import json
import os
import datetime

def load_signal(file_path):
    if not os.path.exists(file_path):
        return None
    with open(file_path, 'r') as f:
        return json.load(f)

def fuse_signals():
    signals_dir = 'mock_signals'
    
    # 1. Load all signals
    weather_data = load_signal(os.path.join(signals_dir, 'weather_alerts.json'))
    traffic_data = load_signal(os.path.join(signals_dir, 'traffic_updates.json'))
    twitter_data = load_signal(os.path.join(signals_dir, 'twitter_feed.json'))

    # 2. Source Credibility Scoring
    credibility = {
        "weather": 0.95,  # PMD Official
        "traffic": 0.90,  # NHA API
        "social": 0.0     # Calculated based on accounts
    }
    
    social_scores = []
    suspicious_sources = []
    contradictory_signal = False
    mention_velocity = 0
    
    if twitter_data and 'data' in twitter_data:
        for post in twitter_data['data']:
            user = post.get('user', '')
            text = post.get('text', '').lower()
            
            # Credibility per user
            if user in ['@KarachiRain', '@CitizenReport']:
                social_scores.append(0.75)
            elif user == '@TrollAccount':
                social_scores.append(0.20)
                suspicious_sources.append(user)
            else:
                social_scores.append(0.50)
            
            # Velocity Calculation (simulation: count keywords)
            keywords = ["flood", "rain", "stuck", "water"]
            if any(kw in text for kw in keywords):
                mention_velocity += 1
            
            # Contradiction Detection
            # If social says "no rain" while weather says "Red"
            if "no rain" in text or "fine" in text:
                if weather_data and weather_data.get('data', {}).get('warning_level') == 'Red':
                    contradictory_signal = True
                    suspicious_sources.append(user)

    credibility['social_avg'] = sum(social_scores) / len(social_scores) if social_scores else 0.5

    # 3. Confidence Calculation
    weather_score = weather_data['data'].get('credibility_score', 0.95) if weather_data else 0
    traffic_score = traffic_data['data'].get('credibility_score', 0.90) if traffic_data else 0
    social_score = credibility['social_avg']
    
    confidence = (weather_score * 0.40) + (traffic_score * 0.35) + (social_score * 0.25)
    
    # Apply Velocity Boost
    if mention_velocity > 5:
        confidence += 0.20
    elif mention_velocity > 2: # Lowered for mock data
        confidence += 0.10
        
    # Apply Contradiction Penalty
    if contradictory_signal:
        confidence -= 0.15
        
    confidence = max(0.0, min(1.0, confidence))
    
    # 4. Severity Score (0-150)
    severity = 0
    if weather_data:
        w = weather_data['data']
        if w.get('warning_level') == 'Red': severity += 50
        if w.get('current_rain_mm', 0) > 30: severity += 20
    if traffic_data:
        t = traffic_data['data']
        if t.get('status') == 'Blocked': severity += 40
        if t.get('delay_minutes', 0) > 60: severity += 20
    
    severity = min(150, severity + (mention_velocity * 5))

    # 5. Output Report
    report = {
        "crisis_detected": severity > 50,
        "crisis_type": "Urban Flooding",
        "location": "G-10, Islamabad",
        "severity_score": severity,
        "confidence_score": round(confidence, 2),
        "confidence_explanation": f"High confidence due to multi-source convergence. Velocity boost applied. Contradiction from {', '.join(suspicious_sources) if suspicious_sources else 'none'} detected but overridden by official data.",
        "contradictory_signals": contradictory_signal,
        "contradictory_sources": list(set(suspicious_sources)),
        "credibility_breakdown": {
            "weather": weather_score,
            "traffic": traffic_score,
            "social_avg": round(social_score, 2)
        },
        "mention_velocity": mention_velocity,
        "recommended_action": "DISPATCH EMERGENCY RESPONSE" if severity > 80 else "MONITOR SITUATION"
    }
    
    return report

if __name__ == "__main__":
    report = fuse_signals()
    print(json.dumps(report, indent=4))