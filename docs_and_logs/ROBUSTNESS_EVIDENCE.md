# Evidence: Robustness & Degraded Mode (API Failure)

As per the hackathon requirement for **Robustness**, CIRO includes a dedicated scenario to handle API downtime.

## Scenario: API Failure (Quetta Node)
In this scenario, the primary satellite data feed (`NASA_API`) returns a `500 ERROR`. The **SignalAnalyst Agent** detects this failure mid-orchestration and automatically shifts the signal fusion strategy to utilize **CIRO_DB (Historical Archive)** and local **Field Reports**.

### Captured Trace Log
```text
[13:33:05] [SignalAnalyst] Ingesting multi-source signals for API Failure (Cached Data Mode)
[13:33:06] [SignalAnalyst] Evaluating credibility of sources: NASA_API, CIRO_DB, RESCUE_FIELD
[13:33:06] [SignalAnalyst] API FAILURE DETECTED: Satellite data unavailable. Switching to historical vulnerability maps.
[13:33:07] [SituationIntel] Calculating crisis classification & severity scores...
[13:33:08] [SituationIntel] PREDICTED: Type: Urban Crisis, Severity: 95, Conf: 65%
[13:33:09] [SituationIntel] Evolution Analysis: Radius 4km, Affected Pop: 35,000
```

### Rationale for Action
1.  **Failure Detection**: The system identifies that a high-confidence source (`NASA_API`) is offline.
2.  **Mitigation**: To prevent response paralysis, the agent pivots to **degraded mode**. It uses historical flood vulnerability maps for Quetta to estimate the "Expected State" and cross-references this with low-latency field reports.
3.  **Result**: The confidence score is slightly lowered (65% vs the standard 90%+), but the orchestration continues, allowing resource allocation to proceed based on the best available alternate data.

---
*This trace serves as evidence for CIRO's ability to maintain operations during critical system failures.*
