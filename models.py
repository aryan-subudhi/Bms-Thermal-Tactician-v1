from pydantic import BaseModel, Field

class Observation(BaseModel):
    battery_temp: float = Field(..., description="Current temperature of the battery")
    step_count: int

class Action(BaseModel):
    cmd: str = Field(..., description="Action command, e.g., 'FAN_ON' or 'FAN_OFF'")