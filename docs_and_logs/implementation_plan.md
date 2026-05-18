# CIRO Hackathon Winning Implementation Plan

Transform CIRO into a state-of-the-art Agentic AI System using multi-agent orchestration, robust signal fusion (including misinformation detection), resource allocation, and a "Mission Control" UI.

## User Review Required

> [!IMPORTANT]
> I will implement a multi-agent system where agents "communicate" and "negotiate". The UI will be updated to show these "Agent Traces" which is 25% of your score.

## Proposed Changes

### 1. Agentic Logic Layer (Python)

#### [NEW] [agents.py](file:///c:/Users/LENOVO/Desktop/CIRO_Antigravity_Hackathon/antigravity_logic/agents.py)
- **SignalAnalystAgent**: Fuses Weather, Traffic, and Social Media. Includes credibility scoring (flags `@TrollAccount`).
- **SituationIntelligenceAgent**: Predicts evolution (radius, population affected).
- **ResourceCoordinatorAgent**: Manages a pool of resources (10 Ambulances, 5 Police Units). Handles prioritization if multiple crises occur.
- **ResponseOrchestratorAgent**: Generates the final plan and simulations.

#### [MODIFY] [ciro_orchestrator.py](file:///c:/Users/LENOVO/Desktop/CIRO_Antigravity_Hackathon/antigravity_logic/ciro_orchestrator.py)
- Refactor to use the new multi-agent classes.
- Generate a detailed "Agent Trace" JSON to be consumed by the UI.

### 2. Incredible UI (Mobile/Web)

#### [MODIFY] [index.html](file:///c:/Users/LENOVO/Desktop/CIRO_Antigravity_Hackathon/mobile_app/index.html)
- Add **Live Resource Tracking** (Ambulances, Police, Drones).
- Add a **Strategic Map View** (SVG-based interactive map of G-10).
- Add **Agent Reasoning Feed** (Real-time logs of agent decisions).
- Add **Impact Prediction Chart**.

#### [MODIFY] [style.css](file:///c:/Users/LENOVO/Desktop/CIRO_Antigravity_Hackathon/mobile_app/style.css)
- Enhance the "Mission Control" aesthetic (more glassmorphism, neon highlights).
- Add animations for map hotspots and resource counters.

#### [MODIFY] [script.js](file:///c:/Users/LENOVO/Desktop/CIRO_Antigravity_Hackathon/mobile_app/script.js)
- Implement logic to handle multiple "Simulation States" (Before vs After).
- Dynamic resource depletion/allocation animations.
- Misinformation flagging visuals.

## Verification Plan

### Automated Tests
- Run `ciro_orchestrator.py` and verify the agent trace output handles the `@TrollAccount` correctly (confidence reduction).

### Manual Verification
- Open the UI and verify that clicking "Simulate Response" triggers resource depletion and map updates.
- Ensure the "Incredible UI" works on mobile viewport.
