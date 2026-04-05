import random
from models import Observation, Action

class BMSEnv:
    """
    High-fidelity Digital Twin for Lithium-ion Battery Thermal Management.
    Models convective cooling and resistive heating during discharge cycles.
    """
    def __init__(self, task_id="thermal_anomaly_detection"):
        self.task_id = task_id
        self.reset()

    def reset(self) -> Observation:
        """
        Initializes the battery at a nominal operating state.
        Default: 25.0°C.
        """
        self.step_count = 0
        self.temp = 25.0
        self.done = False
        return Observation(battery_temp=self.temp, step_count=self.step_count)

    def step(self, action: Action) -> tuple[Observation, float, bool, dict]:
        """
        Calculates the state transition based on thermal inertia and cooling efficiency.
        FAN_ON: Forced convection cooling effect.
        FAN_OFF: Joule heating effect from battery discharge.
        """
        if self.done:
            return Observation(battery_temp=self.temp, step_count=self.step_count), 0.0, True, {}

        self.step_count += 1
        
        # Stochastic thermal dynamics to simulate sensor noise and ambient variance
        thermal_noise = random.uniform(-0.1, 0.3)
        if action.cmd == "FAN_ON":
            self.temp -= (2.5 + thermal_noise)
        else:
            self.temp += (3.5 + thermal_noise)

        # Safety-Critical Reward Grader:
        # Implements a narrow 10°C window for optimal lifespan and efficiency.
        # Critical failure (Thermal Runaway) triggered at 35.0°C.
        if self.temp >= 35.0:
            reward = -50.0  
            self.done = True
        elif 20.0 <= self.temp <= 30.0:
            reward = 1.0    
        else:
            reward = 0.0    

        # Terminal state reached at 10 steps per mission profile
        if self.step_count >= 10:
            self.done = True
            
        obs = Observation(
            battery_temp=round(self.temp, 2), 
            step_count=self.step_count
        )
        
        return obs, reward, self.done, {}