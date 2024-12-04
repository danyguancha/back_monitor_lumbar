from schemas.user import   UserOut
from models.tables import User
import os
from dotenv import load_dotenv
from pydantic import EmailStr
from passlib.context import CryptContext
from pydantic import EmailStr
from fastapi import HTTPException, status, Header

load_dotenv(".env")

import jwt
#from jwt import  ExpiredSignatureError, InvalidTokenError
from jwt.exceptions import ExpiredSignatureError, InvalidTokenError

password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def create_user(new_user: UserOut, db):
    hashed_password = password_context.hash(new_user.password)
    usr = User(**new_user.model_dump(exclude={"password"}), password=hashed_password)
    
    # Guardar el usuario en la base de datos
    db.add(usr)
    db.commit()
    db.refresh(usr)  # Asegurarse de que el ID sea recuperado
    
    # Generar el token
    secret_key = os.getenv("SECRET_KEY")
    algorithm = os.getenv("ALGORITHM")
    if not secret_key or not algorithm:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="SECRET_KEY o ALGORITHM no configurados"
        )
    payload = {"id": usr.id, "email": usr.email, "name": usr.name}
    token = jwt.encode(payload, secret_key, algorithm=algorithm)
    usr.token = token

    # Guardar el token en la base de datos y retornar
    db.commit()
    return usr.token


def exist_user(email: str, db):
    user = db.query(User).filter(User.email == email).first()
    if not user:
        return False
    return user

def exist_token(email: str, password: str, db):
    user = (
        db.query(User).filter(User.email == email and User.password == password).first()
    )
    if not user:
        return False
    return user.token

def validate_token(authorization: str = Header(...)) -> dict:
    """
    Valida el token recibido en el encabezado Authorization.
    """
    secret_key = os.getenv("SECRET_KEY")
    algorithm = os.getenv("ALGORITHM")

    # Validar que el encabezado Authorization esté presente y tenga el prefijo Bearer
    if not authorization.startswith("Bearer "):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Encabezado Authorization inválido, se esperaba 'Bearer <token>'"
        )
    
    token = authorization.split("Bearer ")[1]

    try:
        # Decodificar el token
        dato: dict = jwt.decode(token, secret_key, algorithms=[algorithm])
        return dato
    except ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="El token ha expirado"
        )
    except InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido"
        )



def email_validation(email: str):
    try:
        email: EmailStr._validate(email)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Correo electrónico no válido",
        )
    return True

def validate_password(password: str):
    if not any(char.isupper() for char in password):
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="La contraseña debe tener al menos una letra mayúscula",
        )
    if not any(char.islower() for char in password):
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="La contraseña debe tener al menos una letra minúscula",
        )
    if not any(char.isdigit() for char in password):
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="La contraseña debe tener al menos un número",
        )
    if not any(char in ["$", "@", "#", "%", "!", "?"] for char in password):
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="La contraseña debe tener al menos un caracter especial",
        )
    if len(password) < 8:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="La contraseña debe tener al menos 8 caracteres",
        )
    return True