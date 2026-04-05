from models import Observation, Action

class BMSEnv:
    def __init__(self, task_id="easy_charge_node"):
        self.task_id = task_id
        self.reset()

    def reset(self) -> Observation:
        self.step_count = 0
        self.temp = 25.0
        return Observation(battery_temp=self.temp, step_count=self.step_count)

    def step(self, action: Action) -> tuple[Observation, float, bool, dict]:
        self.step_count += 1
        
        if action.cmd == "FAN_ON":
            self.temp -= 2.0
        else:
            self.temp += 5.0
            
        done = self.step_count >= 10
        reward = 1.0 if self.temp < 60.0 else 0.0
        
        obs = Observation(battery_temp=self.temp, step_count=self.step_count)
        return obs, reward, done, {}