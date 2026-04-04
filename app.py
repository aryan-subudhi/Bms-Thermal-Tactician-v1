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

@app.post("/step")
def step(action: Action):
    obs, reward, done, info = env.step(action)
    
    # --- ADD TELEMETRY JITTER ---
    # Add a random noise value between -0.5 and +0.5 degrees
    jitter = random.uniform(-0.5, 0.5)
    obs.battery_temp = round(obs.battery_temp + jitter, 2)
    
    return {"observation": obs.dict(), "reward": reward, "done": done}

def main():
    """Main entry point for the OpenEnv validator."""
    uvicorn.run("server.app:app", host="0.0.0.0", port=7860, reload=False)

if __name__ == "__main__":
    import uvicorn
    # Change "server.app" to just "app"
    uvicorn.run("app:app", host="0.0.0.0", port=7860, reload=True)