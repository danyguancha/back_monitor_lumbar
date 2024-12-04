from pydantic import BaseModel

class SensorData(BaseModel):
    accel_x: float
    accel_y: float
    gyro_x: float
    gyro_y: float
    timestamp: int

    model_config = {"from_attributes": True}