import datetime

def simulate_response(location, severity_score):
    print(f"--- CIRO Action Execution Log ---")
    print(f"Timestamp: {datetime.datetime.now()}")
    print(f"Executing response for {location} (Score: {severity_score})")
    
    # 1. Traffic Rerouting Simulation
    print("[ACTION] Updating Mock Navigation API: Rerouting traffic from G-10 to Sector I-9.")
    
    # 2. Stakeholder Notification
    print("[ACTION] Dispatching SMS Alert: 'URGENT: Flooding in G-10. Avoid Main Blvd. Emergency teams deployed.'")
    
    # 3. Resource Allocation
    ticket_id = f"REQ-{datetime.datetime.now().strftime('%M%S')}"
    print(f"[ACTION] Emergency Ticket {ticket_id} created in Rescue 1122 Dispatch System.")
    
    print("--- Execution Successful: System State Updated ---")

if __name__ == "__main__":
    # Simulate receiving the score from the previous step
    simulate_response("G-10", 110)