from schemas.monitor import SensorData
from models.tables import DataSensor, User
from fastapi import  Request
from sqlalchemy import func, text


def create_sensor_data(data: SensorData, db):
    sensor_data = DataSensor(**data.model_dump())
    db.add(sensor_data)
    db.commit()
    db.refresh(sensor_data)
    return sensor_data

def get_sensor_data(db):
    return db.query(DataSensor).order_by(DataSensor.id.desc()).first()

# obtener el ultimo registro de la tabla sensor_data que ingreso
def get_last_sensor_data(db):
    data =  db.query(DataSensor).order_by(DataSensor.id.desc()).first()
    return data