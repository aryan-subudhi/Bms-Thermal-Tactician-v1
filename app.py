import uvicorn
import random
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from env import BMSEnv
from models import Action

app = FastAPI()
env = BMSEnv()

@app.get("/", response_class=HTMLResponse)
def root():
    return """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>BMS Thermal Tactician | SRE Dashboard</title>
        <style>
            :root {
                --bg-color: #0d1117;
                --panel-bg: #161b22;
                --border-color: #30363d;
                --text-main: #c9d1d9;
                --text-muted: #8b949e;
                --accent-blue: #58a6ff;
                --accent-green: #238636;
            }
            body {
                font-family: 'Consolas', 'Courier New', monospace;
                background-color: var(--bg-color);
                color: var(--text-main);
                margin: 0;
                padding: 2rem;
                display: flex;
                justify-content: center;
                align-items: center;
                min-height: 100vh;
            }
            .dashboard {
                width: 100%;
                max-width: 900px;
                background: var(--panel-bg);
                border: 1px solid var(--border-color);
                border-radius: 12px;
                box-shadow: 0 8px 24px rgba(0,0,0,0.5);
                overflow: hidden;
            }
            .header {
                padding: 1.5rem 2rem;
                border-bottom: 1px solid var(--border-color);
                display: flex;
                justify-content: space-between;
                align-items: center;
                background: rgba(255, 255, 255, 0.02);
            }
            .header h1 {
                margin: 0;
                font-size: 1.5rem;
                color: var(--accent-blue);
                display: flex;
                align-items: center;
                gap: 10px;
            }
            .status-badge {
                display: inline-flex;
                align-items: center;
                gap: 6px;
                background: rgba(35, 134, 54, 0.1);
                color: var(--accent-green);
                padding: 6px 12px;
                border-radius: 20px;
                border: 1px solid var(--accent-green);
                font-weight: bold;
                font-size: 0.9rem;
                animation: pulse 2s infinite;
            }
            .status-dot {
                width: 8px;
                height: 8px;
                background-color: var(--accent-green);
                border-radius: 50%;
            }
            .content {
                padding: 2rem;
                display: grid;
                grid-template-columns: 1fr 1fr;
                gap: 2rem;
            }
            .card {
                background: rgba(0, 0, 0, 0.2);
                border: 1px solid var(--border-color);
                border-radius: 8px;
                padding: 1.5rem;
            }
            .card h3 {
                margin-top: 0;
                color: var(--text-muted);
                text-transform: uppercase;
                font-size: 0.85rem;
                letter-spacing: 1px;
                border-bottom: 1px solid var(--border-color);
                padding-bottom: 8px;
            }
            ul {
                list-style: none;
                padding: 0;
                margin: 0;
            }
            li {
                margin-bottom: 12px;
                display: flex;
                justify-content: space-between;
                border-bottom: 1px dashed #30363d;
                padding-bottom: 4px;
            }
            .feature-name { color: var(--text-main); }
            .feature-val { color: var(--accent-blue); font-weight: bold; }
            code {
                background: #1f2428;
                color: #ff7b72;
                padding: 3px 6px;
                border-radius: 4px;
            }
            .terminal {
                grid-column: 1 / -1;
                background: #000;
                border: 1px solid var(--border-color);
                border-radius: 6px;
                padding: 1rem;
                font-family: monospace;
                font-size: 0.9rem;
                color: #0f0;
                height: 120px;
                overflow: hidden;
                position: relative;
                line-height: 1.5;
            }
            .terminal-cursor::after {
                content: '█';
                animation: blink 1s step-end infinite;
            }
            @keyframes pulse {
                0% { box-shadow: 0 0 0 0 rgba(35, 134, 54, 0.4); }
                70% { box-shadow: 0 0 0 10px rgba(35, 134, 54, 0); }
                100% { box-shadow: 0 0 0 0 rgba(35, 134, 54, 0); }
            }
            @keyframes blink { 50% { opacity: 0; } }
            @media (max-width: 768px) {
                .content { grid-template-columns: 1fr; }
            }
        </style>
    </head>
    <body>
        <div class="dashboard">
            <div class="header">
                <h1>⚡ BMS Thermal Tactician V1</h1>
                <div class="status-badge"><div class="status-dot"></div> SYSTEM ONLINE</div>
            </div>
            <div class="content">
                <div class="card">
                    <h3>System Architecture</h3>
                    <ul>
                        <li><span class="feature-name">Core Engine</span> <span class="feature-val">FastAPI + Docker</span></li>
                        <li><span class="feature-name">AI Logic</span> <span class="feature-val">Llama 3.1 8B (Groq)</span></li>
                        <li><span class="feature-name">Guardrails</span> <span class="feature-val">Deterministic Hybrid</span></li>
                        <li><span class="feature-name">Telemetry</span> <span class="feature-val">Jitter & Penalties</span></li>
                    </ul>
                </div>
                <div class="card">
                    <h3>API Endpoints</h3>
                    <ul>
                        <li><span class="feature-name">Reinitialize State</span> <code>POST /reset</code></li>
                        <li><span class="feature-name">Execute Command</span> <code>POST /step</code></li>
                    </ul>
                    <p style="color: var(--text-muted); font-size: 0.8rem; margin-top: 15px;">
                        * Headless routing active. SRE logic executes via JSON payloads.
                    </p>
                </div>
                <div class="terminal">
                    <div id="log-output">
                        [SYS] Initializing SRE Guardrails... OK<br>
                        [SYS] Groq LPU Handshake... SECURE<br>
                        [SYS] Listening on Port 7860...<br>
                    </div>
                    <span class="terminal-cursor"></span>
                </div>
            </div>
        </div>
        <script>
            const logOutput = document.getElementById('log-output');
            const messages = [
                "[BMS] Telemetry ping received. Noise filtered.",
                "[BMS] Thermal gradient stable at optimal parameters.",
                "[AI] Awaiting sensor jitter anomalies...",
                "[SYS] Hybrid guardrail standing by for edge cases.",
                "[NET] Health check: 200 OK"
            ];
            
            setInterval(() => {
                const msg = messages[Math.floor(Math.random() * messages.length)];
                
                // FIX: Use local time instead of UTC
                const now = new Date();
                const time = now.toLocaleTimeString('en-GB', { hour12: false }); 
                
                const newLine = document.createElement('div');
                newLine.innerHTML = `[${time}] ${msg}`;
                logOutput.appendChild(newLine);
                
                if (logOutput.childElementCount > 5) {
                    logOutput.removeChild(logOutput.firstChild);
                }
            }, 3500);
                
                if (logOutput.childElementCount > 5) {
                    logOutput.removeChild(logOutput.firstChild);
                }
            }, 3500);
        </script>
    </body>
    </html>
    """

@app.post("/reset")
async def reset():
    return env.reset()

@app.post("/step")
def step(action: Action):
    obs, reward, done, info = env.step(action)
    
    # --- JITTER (Hardware Noise Simulation) ---
    jitter = random.uniform(-0.5, 0.5)
    obs.battery_temp = round(obs.battery_temp + jitter, 2)
    
    # --- MELTDOWN PENALTY (Safety Engineering) ---
    if obs.battery_temp >= 30.0:
        reward = -50.0  
        done = True     
        info["alert"] = "CRITICAL: THERMAL RUNAWAY"
    else:
        reward = 1.0    
        
    return {"observation": obs.dict(), "reward": reward, "done": done, "info": info}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host="0.0.0.0", port=7860, reload=True)