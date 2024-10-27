from fastapi import APIRouter, HTTPException
from app.models import User
from app.services import register_user, login_user, insert_data, select_data, update_data, delete_data
from fastapi.responses import JSONResponse

router = APIRouter()

@router.post("/auth/register")
async def register(user: User):
    response = await register_user(user.email, user.password, user.user_name)

    if "error" in response:
        raise HTTPException(status_code=400, detail=response["error"])

    return JSONResponse(status_code=201, content=response)

@router.post("/auth/login")
async def login(user: User):
    response = await login_user(user.email, user.password)

    if "error" in response:
        raise HTTPException(status_code=400, detail=response["error"])

    return JSONResponse(status_code=200, content=response)


@router.get("/data/select")
async def select_data_route(table: str, column: str, value: str):
    response = await select_data(table, column, value)

    if response["status"] == "error":
        raise HTTPException(status_code=500, detail=response["message"])

    return JSONResponse(status_code=200, content=response["data"])

@router.post("/data/insert")
async def insert_data_route(table: str, data: dict):
    response = await insert_data(table, data)
    if response["status"] == "error":
        raise HTTPException(status_code=400, detail=response["message"])
    return JSONResponse(status_code=201, content=response["data"])

@router.put("/data/update")
async def update_data_route(table: str, data: dict, column: str, value: str):
    response = await update_data(table, data, column, value)
    if response["status"] == "error":
        raise HTTPException(status_code=400, detail=response["message"])
    return JSONResponse(status_code=200, content=response["data"])

@router.delete("/data/delete")
async def delete_data_route(table: str, column: str, value: str):
    response = await delete_data(table, column, value)
    if response["status"] == "error":
        raise HTTPException(status_code=400, detail=response["message"])
    return JSONResponse(status_code=200, content=response["data"])