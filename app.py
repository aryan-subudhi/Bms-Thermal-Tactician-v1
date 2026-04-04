import uvicorn
import random
from fastapi import FastAPI
from env import BMSEnv
from models import Action

app = FastAPI()
env = BMSEnv()

@app.post("/reset")
async def reset():
    return env.reset()

# Inside your @app.post("/step") endpoint:
@app.post("/step")
def step(action: Action):
    obs, reward, done, info = env.step(action)
    
    # --- OPTION A: JITTER (Keep this) ---
    jitter = random.uniform(-0.5, 0.5)
    obs.battery_temp = round(obs.battery_temp + jitter, 2)
    
    # --- OPTION B: MELTDOWN PENALTY ---
    if obs.battery_temp >= 30.0:
        reward = -50.0  # Massive penalty for thermal runaway
        done = True     # Critical Failure: Trigger Emergency Shutdown
        info["alert"] = "CRITICAL: THERMAL RUNAWAY"
    else:
        reward = 1.0    # Standard positive reward for staying alive
        
    return {"observation": obs.dict(), "reward": reward, "done": done, "info": info}

def main():
    """Main entry point for the OpenEnv validator."""
    uvicorn.run("server.app:app", host="0.0.0.0", port=7860, reload=False)

if __name__ == "__main__":
    import uvicorn
    # Change "server.app" to just "app"
    uvicorn.run("app:app", host="0.0.0.0", port=7860, reload=True)