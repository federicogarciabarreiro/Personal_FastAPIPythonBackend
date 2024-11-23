from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import JSONResponse
from .models import UserLogin, UserRegister, InsertRequestModel, UpdateRequestModel, SelectRequestModel
from .services import register_user, login_user, insert_data, select_data, update_data, get_top_scores_data, insert_keep_alive
from .db_config import is_data_valid, is_valid_table, is_valid_column

router = APIRouter()

@router.post("/auth/register")
async def register(user: UserRegister):
    response = await register_user(user.email, user.password, user.user_name)

    if "error" in response:
        raise HTTPException(status_code=400, detail=response["error"])

    return JSONResponse(status_code=201, content=response)

@router.post("/auth/login")
async def login(user: UserLogin):
    response = await login_user(user.email, user.password)

    if "error" in response:
        raise HTTPException(status_code=400, detail=response["error"])

    return JSONResponse(status_code=200, content=response)

@router.post("/data/insert")
async def insert_data_route(request_data: InsertRequestModel):
    table = request_data.table
    data = request_data.data

    if not is_valid_table(table) or not is_data_valid(table, data):
        raise HTTPException(status_code=400, detail="Tabla o datos inválidos.")

    response = await insert_data(table, data)
    if response["status"] == "error":
        raise HTTPException(status_code=400, detail=response["message"])

    return JSONResponse(status_code=201, content=response["data"])


@router.put("/data/update")
async def update_data_route(request_data: UpdateRequestModel):
    table = request_data.table
    data = request_data.data
    column = request_data.column
    value = request_data.value

    if not is_valid_table(table) or not is_data_valid(table, data):
        raise HTTPException(status_code=400, detail="Tabla o datos inválidos.")

    response = await update_data(table, data, column, value)
    if response["status"] == "error":
        raise HTTPException(status_code=400, detail=response["message"])
    
    return JSONResponse(status_code=200, content=response["data"])


@router.get("/data/select")
async def select_data_route(request_data: SelectRequestModel = Depends()):
    table = request_data.table
    column = request_data.column
    value = request_data.value

    if not is_valid_table(table) or not is_valid_column(table, column):
        raise HTTPException(status_code=400, detail="Tabla o columna inválidas.")

    response = await select_data(table, column, value)
    if response["status"] == "error":
        raise HTTPException(status_code=500, detail=response["message"])

    return JSONResponse(status_code=200, content=response["data"])


@router.get("/scores/top")
async def get_top_scores_route(game_name: str):
    response = await get_top_scores_data(game_name)

    if response["status"] == "error":
        raise HTTPException(status_code=500, detail=response["message"])

    return JSONResponse(status_code=200, content=response["data"])


@router.post("/keep_alive")
async def keep_alive():
    response = await insert_keep_alive()
    if response["status"] == "error":
        raise HTTPException(status_code=500, detail=response["message"])
    return response