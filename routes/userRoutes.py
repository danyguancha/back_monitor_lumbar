from fastapi import APIRouter, Depends, HTTPException, Request, status
from schemas.user import  UserLogin, UserCreate
from config.db import get_db
from sqlalchemy.orm import Session
from controllers.emailController import send_welcome_email
from controllers.userController import create_user, validate_token, email_validation, validate_password, password_context, exist_user, exist_token

router = APIRouter()

# create new user
@router.post("/register_user/")
async def register(new_user: UserCreate, db: Session = Depends(get_db)):
    email_validation(new_user.email)
    validate_password(new_user.password)
    if exist_user(new_user.email, db):
        raise HTTPException(status_code=400, detail="User already exist")
    if not email_validation(new_user.email):
        raise HTTPException(status_code=400, detail="Email not valid")
    if not validate_password(new_user.password):
        raise HTTPException(status_code=400, detail="Password not valid")
    await send_welcome_email(new_user.email, new_user.name, Request)
    token = create_user(new_user, db)
    return {"message": "User created successfully"}




# login User
@router.post("/login_user/")
async def login_user(user: UserLogin, db: Session = Depends(get_db)):
    email_validation(user.email)
    usr = exist_user(user.email, db)
    if not usr:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Usuario no existe"
        )
    if not password_context.verify(user.password, usr.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Contraseña incorrecta"
        )
    token = exist_token(user.email, user.password, db)
    return {"token": token}
    