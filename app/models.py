from pydantic import BaseModel, EmailStr

class User(BaseModel):
    email: str
    password: str
    user_name: str