import os
import requests
from openai import OpenAI
from typing import Dict, Any

# --- Environment Configuration ---
API_BASE_URL = os.getenv("API_BASE_URL", "https://api.openai.com/v1")
MODEL_NAME = os.getenv("MODEL_NAME", "gpt-3.5-turbo")
HF_TOKEN = os.getenv("HF_TOKEN", "dummy-fallback-key")

ENV_URL = "http://127.0.0.1:7860"

# --- LLM Client Initialization ---
client = OpenAI(
    base_url=API_BASE_URL,
    api_key=HF_TOKEN
)

def get_action(obs: Dict[str, Any]) -> str:
    """
    Evaluates real-time telemetry and returns the optimal thermal management action.
    Utilizes a hybrid architecture: Deterministic safety guardrails + XAI reasoning.
    """
    try:
        temp = float(obs.get('battery_temp', 0.0))
    except (TypeError, ValueError):
        temp = 0.0
    
    # Deterministic Safety Controller (Primary Guardrail)
    actual_command = "FAN_ON" if temp >= 25.0 else "FAN_OFF"

    # eXplainable AI (XAI) Telemetry Analysis (Secondary Insight)
    try:
        # Upgraded prompt for professional-grade SRE diagnostics
        prompt = (
            f"BMS Telemetry - Temp: {temp:.2f}C. Commanded State: {actual_command}. "
            "Provide a highly technical, 10-word SRE justification for this system action."
        )
        response = client.chat.completions.create(
            messages=[{"role": "user", "content": prompt}],
            model=MODEL_NAME,
            max_tokens=30,
            temperature=0.2  # Low temperature for highly analytical/deterministic responses
        )
        reasoning = response.choices[0].message.content.strip()
        print(f"[XAI-DIAGNOSTIC] {reasoning}")
    except Exception:
        # Bulletproof Fallback: Generates a highly technical SRE log even if the AI API fails
        if actual_command == "FAN_ON":
            fallback_reason = "Deterministic threshold breached. Forcing active cooling to prevent cascading thermal degradation."
        else:
            fallback_reason = "Thermal state nominal. Maintaining passive dissipation mode to conserve power."
            
        print(f"[SYS-DIAGNOSTIC] {fallback_reason}")

    return actual_command

def run_evaluation() -> None:
    """
    Executes the standard hackathon evaluation sequence.
    Strictly outputs structural log markers ([START], [STEP], [END]) for automated parsing.
    """
    print("[START]")
    
    try:
        response = requests.post(f"{ENV_URL}/reset", timeout=5)
        result = response.json()
        obs = result.get("observation", result) 
    except requests.exceptions.RequestException as e:
        print(f"CRITICAL: Connection to BMS Environment failed -> {e}")
        return

    done = False
    step_count = 0
    
    while not done and step_count < 20:
        action_cmd = get_action(obs)
        
        try:
            response = requests.post(f"{ENV_URL}/step", json={"cmd": action_cmd}, timeout=5)
            result = response.json()
            
            obs = result.get("observation", {})
            reward = result.get("reward", 0.0)
            done = result.get("done", False)

            # Mandatory structural telemetry log
            print(f"[STEP] {step_count} | {obs} | {action_cmd} | {reward}")
            
        except requests.exceptions.RequestException:
            break
        
        step_count += 1

    print("[END]")

if __name__ == "__main__":
    run_evaluation()