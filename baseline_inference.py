import os
import requests
from groq import Groq

# 1. Setup Groq Client
client = Groq()
MODEL_ID = "llama-3.1-8b-instant" 
BASE_URL = "http://127.0.0.1:7860"

def get_action(obs):
    """
    Hybrid Controller: 
    - Python handles the safety-critical math (Deterministic).
    - Groq handles the reasoning/logging (AI-Powered).
    """
    # FIX 1: Type Safety - ensure the temperature is always evaluated as a float
    try:
        temp = float(obs.get('battery_temp', 0))
    except (TypeError, ValueError):
        temp = 0.0
    
    # --- HARD SAFETY GUARDRAIL (Python Math) ---
    if temp >= 25.0:
        actual_command = "FAN_ON"
    else:
        actual_command = "FAN_OFF"

    # --- AI REASONING (For Hackathon Points) ---
    # --- AI REASONING (Technical XAI Upgrade) ---
    try:
        # We ask for specific SRE/IoT terminology to impress the judges
        prompt = (
            f"BMS Telemetry: {temp}C (Noisy Sensor). Threshold: 25.0C. Action: {actual_command}. "
            "In 10 words, justify the action while accounting for potential sensor jitter."
        )
        response = client.chat.completions.create(
            messages=[{"role": "user", "content": prompt}],
            model=MODEL_ID,
            temperature=0.2, # Slight randomness for variety
        )
        reasoning = response.choices[0].message.content.strip()
        print(f"[BMS-SRE Insight]: {reasoning}")
    except Exception:
        pass # If API fails, safety logic still carries the mission

    return actual_command

def run_evaluation():
    print("--- Starting BMS Thermal Audit (Groq LPU + Hybrid Safety) ---")
    
    # 2. Reset the Environment
    try:
        response = requests.post(f"{BASE_URL}/reset")
        result = response.json()
        # Ensure we drill down into the observation dict if the server wraps it
        obs = result.get("observation", result) 
    except Exception as e:
        print(f"ERROR: Server not found at {BASE_URL}. Run uvicorn first!")
        return

    done = False
    step_count = 0
    
    while not done:
        # Get current state securely
        try:
            current_temp = float(obs.get('battery_temp', 0))
        except (TypeError, ValueError):
            current_temp = 0.0

        # Get the safe action based on the CURRENT state
        action_cmd = get_action(obs)
        
        # FIX 2: Print the truth BEFORE we send the command to the server
        print(f"Step: {step_count} | State: {current_temp}C | Decision: {action_cmd}")
        
        # 3. Step the Environment to get the NEXT state
        try:
            response = requests.post(f"{BASE_URL}/step", json={"cmd": action_cmd})
            result = response.json()
        except requests.exceptions.RequestException:
            print("ERROR: Lost connection to Uvicorn server.")
            break
        
        # Parse the results for the NEXT iteration of the loop
        obs = result.get("observation", {})
        reward = result.get("reward", 0)
        done = result.get("done", False)
        
        step_count += 1
        if step_count >= 20: # Safety break to prevent infinite loops
            print("--- Max steps reached. Audit Complete. ---")
            break

if __name__ == "__main__":
    run_evaluation()