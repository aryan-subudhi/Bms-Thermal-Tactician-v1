import os
import requests
from groq import Groq

# Setup Groq Client
client = Groq()
MODEL_ID = "llama-3.1-8b-instant" 
BASE_URL = "http://127.0.0.1:7860"

def get_action(obs):
    """
    Hybrid Controller: 
    - Python handles the safety-critical math (Deterministic).
    - Groq handles the reasoning/logging (AI-Powered XAI).
    """
    try:
        temp = float(obs.get('battery_temp', 0))
    except (TypeError, ValueError):
        temp = 0.0
    
    # --- HARD SAFETY GUARDRAIL ---
    if temp >= 25.0:
        actual_command = "FAN_ON"
    else:
        actual_command = "FAN_OFF"

    # --- TECHNICAL XAI REASONING ---
    try:
        prompt = (
            f"BMS Telemetry: {temp}C (Noisy Sensor). Threshold: 25.0C. Action: {actual_command}. "
            "In 10 words, justify the action while accounting for potential sensor jitter."
        )
        response = client.chat.completions.create(
            messages=[{"role": "user", "content": prompt}],
            model=MODEL_ID,
            temperature=0.2, 
        )
        reasoning = response.choices[0].message.content.strip()
        print(f"[BMS-SRE Insight]: {reasoning}")
    except Exception:
        pass # Safety logic carries the mission if API fails

    return actual_command

def run_evaluation():
    print("--- Starting BMS Thermal Audit (Groq LPU + Hybrid Safety) ---")
    
    try:
        response = requests.post(f"{BASE_URL}/reset")
        result = response.json()
        obs = result.get("observation", result) 
    except Exception as e:
        print(f"ERROR: Server not found at {BASE_URL}. Run uvicorn first!")
        return

    done = False
    step_count = 0
    
    while not done:
        try:
            current_temp = float(obs.get('battery_temp', 0))
        except (TypeError, ValueError):
            current_temp = 0.0

        action_cmd = get_action(obs)
        print(f"Step: {step_count} | State: {current_temp}C | Decision: {action_cmd}")
        
        try:
            response = requests.post(f"{BASE_URL}/step", json={"cmd": action_cmd})
            result = response.json()
        except requests.exceptions.RequestException:
            print("ERROR: Lost connection to server.")
            break
        
        obs = result.get("observation", {})
        reward = result.get("reward", 0)
        done = result.get("done", False)

        # --- EMERGENCY SHUTDOWN CHECK ---
        if done and reward < 0:
            print(f"\n🚨 [SYSTEM KILLED] Emergency Shutdown Triggered! Final Reward: {reward}")
            print("--- SIMULATION TERMINATED TO PREVENT HARDWARE DAMAGE ---")
            break  
        
        step_count += 1
        if step_count >= 20: 
            print("--- Max steps reached. Audit Complete. ---")
            break

if __name__ == "__main__":
    run_evaluation()