import uvicorn
from fastapi import FastAPI
from env import BMSEnv
from models import Action

app = FastAPI()
env = BMSEnv()

@app.post("/reset")
async def reset():
    return env.reset()

@app.post("/step")
async def step(action: Action):
    obs, reward, done, info = env.step(action)
    return {"observation": obs, "reward": reward, "done": done}

def main():
    """Main entry point for the OpenEnv validator."""
    uvicorn.run("server.app:app", host="0.0.0.0", port=7860, reload=False)

if __name__ == "__main__":
    import uvicorn
    # Change "server.app" to just "app"
    uvicorn.run("app:app", host="0.0.0.0", port=7860, reload=True)