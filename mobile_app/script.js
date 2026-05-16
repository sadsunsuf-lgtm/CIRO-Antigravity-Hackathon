/**
 * CIRO | Enterprise Crisis Intelligence Orchestrator
 * Visual Orchestration & Simulation Engine
 */

document.addEventListener('DOMContentLoaded', () => {
    // UI Elements
    const systemTime = document.getElementById('system-time');
    const runBtn = document.getElementById('run-orchestrator');
    const traceLog = document.getElementById('trace-log');
    const notificationFeed = document.getElementById('notification-feed');
    const severityVal = document.getElementById('severity-val');
    const severityGauge = document.getElementById('severity-gauge');
    const confPerc = document.getElementById('conf-perc');
    const resAmb = document.getElementById('res-amb');
    const resPol = document.getElementById('res-pol');
    const resRes = document.getElementById('res-res');
    const allocReasoning = document.getElementById('allocation-reasoning');
    const contradictionFlag = document.getElementById('contradictory-flag');
    const activeIncidents = document.getElementById('active-incidents');
    const progressFill = document.getElementById('progress-fill');
    
    const impPop = document.getElementById('impact-pop');
    const impPeak = document.getElementById('impact-peak');
    const impDuration = document.getElementById('impact-duration');
    const impUncertainty = document.getElementById('impact-uncertainty');

    // Before/After Elements
    const afterCongestion = document.getElementById('after-congestion');
    const afterTeams = document.getElementById('after-teams');
    const afterStranded = document.getElementById('after-stranded');
    const afterAwareness = document.getElementById('after-awareness');
    const afterTime = document.getElementById('after-time');
    const afterRisk = document.getElementById('after-risk');
    const speedBadge = document.getElementById('speed-badge');

    // State
    let currentScenario = 'DUAL_CRISIS';
    let isRunning = false;
    let resources = { amb: 10, pol: 5, res: 8 };

    // Scenario Configuration
    const SCENARIOS = {
        'DUAL_CRISIS': {
            name: 'Dual Metropolitan Crisis',
            incidents: [
                { id: 'ISB-FLOOD-01', city: 'ISB', type: 'Urban Flood', sev: 110, conf: 92, pop: '25k', peak: 'T+30m', dur: '6h', unc: '10%' },
                { id: 'KHI-HEAT-04', city: 'KHI', type: 'Heat Emergency', sev: 145, conf: 88, pop: '180k', peak: 'T+1h', dur: '12h', unc: '5%' }
            ],
            steps: [
                { agent: 'SocialSignal', msg: 'Ingesting signals from Karachi & Islamabad...', delay: 800, cred: 0.75 },
                { agent: 'SocialSignal', msg: 'Merged 12 duplicate reports for KHI.', delay: 1000, cred: 0.75 },
                { agent: 'SocialSignal', msg: '@TrollAccount — "No rain in G-10!"', delay: 500, cred: 0.20, flagged: true },
                { agent: 'WeatherAgent', msg: 'Satellite alert: 45mm/hr rain intensity.', delay: 1200, cred: 0.95 },
                { agent: 'Reasoning', msg: 'ORCHESTRATION PLAN: Prioritizing Karachi Heatwave.', delay: 1500 },
                { agent: 'Dispatch', msg: 'Mobilizing Resource Units.', delay: 1000 }
            ],
            after: {
                congestion: 'REDUCED 60%',
                teams: '3 DEPLOYED',
                stranded: '12 (35 rescued)',
                awareness: 'HIGH (3,200 alerts)',
                time: '8 min',
                risk: 'LOW'
            }
        },
        'FALSE_ALARM': {
            name: 'Contradictory Signal Analysis',
            incidents: [
                { id: 'LHR-FIRE-02', city: 'LHR', type: 'Industrial Fire', sev: 20, conf: 15, pop: '0', peak: 'N/A', dur: 'RESCINDED', unc: 'N/A' }
            ],
            steps: [
                { agent: 'SocialSignal', msg: 'Urgent reports of "Dhamaka" in Lahore.', delay: 800, cred: 0.50 },
                { agent: 'DetectionAgent', msg: 'No seismic/noise spikes found.', delay: 1200 },
                { agent: 'Reasoning', msg: 'CONFIDENCE DROP: Contradictory evidence.', delay: 1500, action: 'showContradiction' },
                { agent: 'Orchestrator', msg: 'RETRACTING ALERT: False Alarm.', delay: 1800 }
            ],
            after: {
                congestion: 'NORMAL',
                teams: '0 (STANDBY)',
                stranded: '0',
                awareness: 'N/A (RESCINDED)',
                time: 'N/A',
                risk: 'ZERO'
            }
        },
        'API_FAIL': {
            name: 'Degraded Mode / API Failure',
            incidents: [
                { id: 'PEW-STORM-01', city: 'PEW', type: 'Dust Storm', sev: 85, conf: 65, pop: '40k', peak: 'T+2h', dur: '4h', unc: '30%' }
            ],
            steps: [
                { agent: 'System', msg: 'CRITICAL: MET-OFFICE API Timed Out (504).', delay: 1000, action: 'degradeSensors' },
                { agent: 'System', msg: 'FALLBACK: Using cached historical data.', delay: 1200 },
                { agent: 'Reasoning', msg: 'High uncertainty due to missing feed.', delay: 1500 }
            ],
            after: {
                congestion: 'MODERATE',
                teams: '2 DEPLOYED',
                stranded: '5',
                awareness: 'MEDIUM',
                time: '15 min',
                risk: 'MODERATE'
            }
        },
        'RESOURCE_SHORTAGE': {
            name: 'Constrained Resource Allocation',
            incidents: [
                { id: 'QTA-COLD-01', city: 'QTA', type: 'Cold Wave', sev: 120, conf: 95, pop: '15k', peak: 'T+4h', dur: '48h', unc: '5%' }
            ],
            steps: [
                { agent: 'ResourceCoord', msg: 'Resource Request: 8x Amb, 4x Police.', delay: 1000 },
                { agent: 'ResourceCoord', msg: 'SHORTAGE: Only 5x Amb available.', delay: 1500, action: 'showShortage' },
                { agent: 'Reasoning', msg: 'Trade-off: Prioritizing elderly care.', delay: 1800 }
            ],
            after: {
                congestion: 'IMPROVED',
                teams: '5 DEPLOYED',
                stranded: '8',
                awareness: 'HIGH',
                time: '22 min',
                risk: 'LOW'
            }
        }
    };

    // Core Logic
    window.setScenario = (id) => {
        currentScenario = id;
        document.querySelectorAll('.scenario-btn').forEach(b => b.classList.remove('active'));
        document.getElementById(`btn-${id}`).classList.add('active');
        resetSystem();
    };

    window.initiateOrchestration = async () => {
        if (isRunning) return;
        isRunning = true;
        runBtn.disabled = true;
        runBtn.innerText = 'ORCHESTRATING...';
        traceLog.innerHTML = '';
        notificationFeed.innerHTML = '';
        
        // Progress Bar Animation (8 seconds)
        progressFill.style.transition = 'none';
        progressFill.style.width = '0%';
        setTimeout(() => {
            progressFill.style.transition = 'width 8s linear';
            progressFill.style.width = '100%';
        }, 50);

        // Reset After Panel
        [afterCongestion, afterTeams, afterStranded, afterAwareness, afterTime, afterRisk].forEach(el => el.innerText = '---');
        speedBadge.classList.remove('visible');

        const scenario = SCENARIOS[currentScenario];
        
        // Phase 1: Detection
        setLifecycle('detected');
        await runSteps(scenario.steps.slice(0, 2));
        
        // Update Incident View
        activeIncidents.innerHTML = '';
        scenario.incidents.forEach(inc => {
            const node = document.createElement('div');
            node.className = 'incident-node active';
            node.innerHTML = `
                <div class="inc-header"><span class="inc-id">${inc.id}</span><span class="inc-status">${inc.type}</span></div>
                <div class="inc-mini-stats"><span>SEV: ${inc.sev}</span><span>CONF: ${inc.conf}%</span></div>
            `;
            activeIncidents.appendChild(node);
            showHotspot(inc.city);
        });

        // Phase 2: Verification
        await wait(1000);
        setLifecycle('verified');
        await runSteps(scenario.steps.slice(2, 4));
        
        const mainInc = scenario.incidents[0];
        updateGauges(mainInc.sev, mainInc.conf);
        updateImpact(mainInc);

        // Phase 3: Reasoning & Planning
        await wait(1200);
        setLifecycle('responding');
        await runSteps(scenario.steps.slice(4));

        // Animate After Panel
        await animateAfterPanel(scenario.after);

        // Final Actions
        if (currentScenario !== 'FALSE_ALARM') {
            generateNotifications(scenario.incidents);
            updateResources(mainInc.sev);
            showRoute(mainInc.city);
        } else {
            setLifecycle('recovered');
            updateGauges(5, 5);
        }

        isRunning = false;
        runBtn.disabled = false;
        runBtn.innerText = 'RE-RUN MISSION';
    };

    async function runSteps(steps) {
        if (!steps) return;
        for (const step of steps) {
            await wait(step.delay || 800);
            logTrace(step.agent, step.msg, step.cred, step.flagged);
            
            if (step.action === 'showContradiction') {
                contradictionFlag.classList.remove('hidden');
                updateGauges(20, 15);
            }
            if (step.action === 'degradeSensors') {
                updateHealth('sensor', 30);
            }
            if (step.action === 'showShortage') {
                document.getElementById('node-amb').classList.add('depleted');
                allocReasoning.innerText = 'RESOURCE SHORTAGE: Re-routing units from non-critical sectors.';
            }
        }
    }

    async function animateAfterPanel(data) {
        const sequence = [
            { el: afterCongestion, val: data.congestion },
            { el: afterTeams, val: data.teams },
            { el: afterStranded, val: data.stranded },
            { el: afterAwareness, val: data.awareness },
            { el: afterTime, val: data.time },
            { el: afterRisk, val: data.risk }
        ];

        for (const item of sequence) {
            await wait(400);
            item.el.innerText = item.val;
            item.el.classList.add('flash');
            setTimeout(() => item.el.classList.remove('flash'), 400);
        }
        
        await wait(400);
        speedBadge.classList.add('visible');
    }

    // UI Helpers
    function logTrace(agent, msg, cred, flagged) {
        const line = document.createElement('div');
        line.className = 'trace-line';
        
        let credHtml = '';
        if (cred !== undefined) {
            const icon = flagged ? '✗ FLAGGED' : '✓';
            const cls = flagged ? 'cross' : 'check';
            credHtml = `<span class="trace-cred ${cls}">credibility: ${cred} ${icon}</span>`;
        }

        line.innerHTML = `<span class="trace-agent">${agent}</span><span class="trace-msg">${msg}</span>${credHtml}`;
        traceLog.prepend(line);
    }

    function generateNotifications(incidents) {
        notificationFeed.innerHTML = '';
        const targets = ['PUBLIC', 'HOSPITALS', 'RESCUE', 'LESCO'];
        incidents.forEach(inc => {
            targets.forEach(t => {
                const item = document.createElement('div');
                item.className = 'notify-item';
                item.innerHTML = `<span class="n-target">${t}</span><span class="n-msg">ALERT: ${inc.type} detected in ${inc.city}. Evacuate zone ${inc.id}.</span>`;
                notificationFeed.prepend(item);
            });
        });
    }

    function setLifecycle(id, isReset = false) {
        const steps = ['detected', 'verified', 'escalated', 'responding', 'contained', 'recovered'];
        const targetIndex = steps.indexOf(id);
        steps.forEach((s, i) => {
            const el = document.getElementById(`step-${s}`);
            if (isReset) {
                el.classList.remove('active', 'completed');
                if (i === 0) el.classList.add('active');
                return;
            }
            if (i < targetIndex) el.classList.add('completed'), el.classList.remove('active');
            else if (i === targetIndex) el.classList.add('active'), el.classList.remove('completed');
            else el.classList.remove('active', 'completed');
        });
    }

    function updateGauges(sev, conf) {
        animateValue(severityVal, sev, 1500);
        animateValue(confPerc, conf, 1000, '%');
        const offset = 283 - (Math.min(sev, 150) / 150) * 283;
        severityGauge.style.strokeDashoffset = offset;
    }

    function updateImpact(data) {
        impPop.innerText = data.pop;
        impPeak.innerText = data.peak;
        impDuration.innerText = data.dur;
        impUncertainty.innerText = data.unc;
    }

    function updateResources(sev) {
        const usage = sev > 100 ? { a: 7, p: 3, r: 5 } : { a: 2, p: 1, r: 2 };
        animateValue(resAmb, 10 - usage.a, 1000);
        animateValue(resPol, 5 - usage.p, 1000);
        animateValue(resRes, 8 - usage.r, 1000);
        allocReasoning.innerText = `Allocated ${usage.a}x AMB, ${usage.p}x POL based on ${sev > 100 ? 'High' : 'Low'} severity impact.`;
    }

    function updateHealth(type, val) {
        const bar = document.getElementById(`${type}-health`);
        bar.style.width = `${val}%`;
        if (val < 50) bar.classList.add('warning');
    }

    function showHotspot(id) {
        const el = document.getElementById(`hotspot-${id.toLowerCase()}`);
        if (el) el.classList.add('active');
    }

    function showRoute(id) {
        const el = document.getElementById(`route-${id.toLowerCase()}`);
        if (el) el.classList.add('active');
    }

    function resetSystem() {
        traceLog.innerHTML = '<div class="trace-line system"><span class="trace-agent">SYSTEM</span><span class="trace-msg">Standing by for signal fusion...</span></div>';
        notificationFeed.innerHTML = '<div class="notify-placeholder">Awaiting mobilization...</div>';
        activeIncidents.innerHTML = '<div class="incident-node active"><span>Awaiting Trigger...</span></div>';
        updateGauges(0, 0);
        setLifecycle('detected', true);
        contradictionFlag.classList.add('hidden');
        document.querySelectorAll('.map-hotspot, .map-route').forEach(el => el.classList.remove('active'));
        document.getElementById('node-amb').classList.remove('depleted');
        updateHealth('core', 98);
        updateHealth('sensor', 95);
        allocReasoning.innerText = 'Awaiting resource request...';
        [afterCongestion, afterTeams, afterStranded, afterAwareness, afterTime, afterRisk].forEach(el => el.innerText = '---');
        speedBadge.classList.remove('visible');
        progressFill.style.transition = 'none';
        progressFill.style.width = '0%';
    }

    function animateValue(el, target, duration, suffix = '') {
        let start = parseInt(el.innerText) || 0;
        let startTime = null;
        function step(timestamp) {
            if (!startTime) startTime = timestamp;
            const progress = Math.min((timestamp - startTime) / duration, 1);
            const val = Math.floor(progress * (target - start) + start);
            el.innerText = isNaN(val) ? target : val + suffix;
            if (progress < 1) window.requestAnimationFrame(step);
        }
        window.requestAnimationFrame(step);
    }

    function wait(ms) { return new Promise(r => setTimeout(r, ms)); }

    // Time
    setInterval(() => { systemTime.innerText = new Date().toLocaleTimeString('en-GB'); }, 1000);
});

// Layer Toggle
window.toggleLayer = (type) => {
  const layer = document.getElementById('layer-' + type);
  const btn = document.getElementById('toggle-' + type);
  if (layer) {
    layer.classList.toggle('active');
    btn.classList.toggle('active');
  }
};
