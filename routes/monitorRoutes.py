from fastapi import APIRouter, Depends, HTTPException, Request, status
from schemas.monitor import SensorData
from models.tables import  User
from config.db import get_db
from sqlalchemy.orm import Session
from controllers.monitorController import create_sensor_data, get_last_sensor_data
from controllers.userController import validate_token
from controllers.emailController import send_posture_recommendation_email


router = APIRouter()
sensor_state = {"is_bad_posture": False}

@router.post("/sensor_data/")
async def receive_sensor_data(data: SensorData, db: Session = Depends(get_db)):
    create_sensor_data(data, db)
    return {"message": "Datos enviados"}

@router.get("/data_sensor")
async def get_sensor_data(
    db: Session = Depends(get_db), 
    token: str = Depends(validate_token)
):
    global sensor_state  # Usamos global si es una variable en memoria
    current_user = db.query(User).filter(User.id == token["id"]).first()
    if not current_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail="Usuario no autenticado"
        )
    
    data = get_last_sensor_data(db)
    is_bad_posture = data.accel_x < 75 or data.accel_y > 85

    # Detectar cambio de estado: de buena postura a mala postura
    if is_bad_posture and not sensor_state["is_bad_posture"]:
        await send_posture_recommendation_email(
            email=current_user.email, 
            username=current_user.name, 
            request=Request
        )
        # Actualizamos el estado a "mala postura"
        sensor_state["is_bad_posture"] = True
    
    # Si la postura se corrige, actualizamos el estado a "buena postura"
    if not is_bad_posture:
        sensor_state["is_bad_posture"] = False

    return data

