from sqlalchemy import Column, Integer, String, Float
from config.db import Base


class DataSensor(Base):
    __tablename__ = "sensor_data"

    id = Column(Integer, primary_key=True, index=True)
    accel_x = Column(Float)
    accel_y = Column(Float)
    gyro_x = Column(Float)
    gyro_y = Column(Float)
    timestamp = Column(Integer)

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    password = Column(String(100), nullable=False)
    token = Column(String(500), nullable=True)