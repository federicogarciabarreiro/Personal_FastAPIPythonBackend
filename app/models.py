from pydantic import BaseModel
from typing import Dict, Any

class UserRegister(BaseModel):
    email: str
    password: str
    user_name: str

class UserLogin(BaseModel):
    email: str
    password: str

class InsertRequestModel(BaseModel):
    table: str
    data: Dict[str, Any]

class UpdateRequestModel(BaseModel):
    table: str
    data: Dict[str, Any]
    column: str
    value: str

class SelectRequestModel(BaseModel):
    table: str
    column: str
    value: str