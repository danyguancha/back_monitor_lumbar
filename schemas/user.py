from pydantic import BaseModel

class User(BaseModel):
    name: str
    email: str


class UserCreate(User):
    password: str

class UserLogin(BaseModel):
    email: str
    password: str

class UserOut(User):
    id: int
    token:str
    