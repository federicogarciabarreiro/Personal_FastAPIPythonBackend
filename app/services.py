import re
import logging
from supabase import Client
from .database import supabase
from .models import User
from gotrue.errors import AuthRetryableError, AuthApiError
from .db_config import is_valid_table, is_valid_column

logging.basicConfig(level=logging.INFO)

def is_valid_email(email: str) -> bool:
    pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    return re.match(pattern, email) is not None

async def register_user(email: str, password: str, user_name: str):

    if not is_valid_email(email):
        return {"error": "El formato del correo electrónico es inválido."}

    if len(password) != 6:
        return {"error": "La contraseña debe tener exactamente 6 caracteres."}

    try:
        response = supabase.auth.sign_up({"email": email, "password": password})

        if response.user:
            access_token = response.session.access_token
            refresh_token = response.session.refresh_token
            user_info = {
                "email": email,
                "user_name": user_name,
                "access_token": access_token,
                "refresh_token": refresh_token,
            }
            logging.info(f"Registro exitoso. Información del usuario: {user_info}")
            return user_info
        else:
            logging.error("Error desconocido en la respuesta de registro")
            return {"error": "Error desconocido en la respuesta de registro"}

    except AuthRetryableError as e:
        logging.error(f"Error de autenticación temporario: {str(e)}")
        return {"error": "Error de autenticación temporario"}
    except AuthApiError as e:
        logging.error(f"Error de autenticación de API: {str(e)}")
        return {"error": str(e)}
    except Exception as e:
        logging.error(f"Error inesperado: {str(e)}")
        return {"error": "Error inesperado. Verifique tamaño de la contraseña o correo electrónico."}


async def login_user(email: str, password: str):
    if not is_valid_email(email):
        return {"error": "El formato del correo electrónico es inválido."}

    if len(password) != 6:
        return {"error": "La contraseña debe tener exactamente 6 caracteres."}

    try:
        response = supabase.auth.sign_in_with_password({
            "email": email,
            "password": password
        })

        if response.user:
            access_token = response.session.access_token
            return {
                "message": "Inicio de sesión exitoso",
                "user": {
                    "email": response.user.email,
                    "user_name": response.user.user_metadata.get("user_name"),
                    "access_token": access_token,
                }
            }
        else:
            return {"error": "No se pudo iniciar sesión."}
    except Exception as e:
        logging.error(f"Error inesperado en inicio de sesión: {str(e)}")
        return {"error": "Error en inicio de sesión."}


async def select_data(table: str, column: str, value: str):
    if not is_valid_table(table):
        return {"status": "error", "message": "Tabla no válida."}
    
    if not is_valid_column(table, column):
        return {"status": "error", "message": "Columna no válida."}

    response = supabase.table(table).select("*").eq(column, value).execute()

    logging.info(f"Response: {response}")

    if response.data is None:
        return {
            "status": "error",
            "message": "Error al ejecutar la consulta.",
            "details": response.error
        }

    return {
        "status": "success",
        "data": response.data
    }

async def insert_data(table: str, data: dict):
    if not is_valid_table(table):
        return {"status": "error", "message": "Tabla no válida."}

    response = supabase.table(table).insert(data).execute()

    if response.error:
        return {
            "status": "error",
            "message": response.error['message'],
        }

    return {
        "status": "success",
        "data": response.data
    }

async def update_data(table: str, data: dict, column: str, value: str):
    if not is_valid_table(table):
        return {"status": "error", "message": "Tabla no válida."}

    if not is_valid_column(table, column):
        return {"status": "error", "message": "Columna no válida."}

    response = supabase.table(table).update(data).eq(column, value).execute()

    if response.error:
        return {
            "status": "error",
            "message": response.error['message'],
        }

    return {
        "status": "success",
        "data": response.data
    }

async def delete_data(table: str, column: str, value: str):
    if not is_valid_table(table):
        return {"status": "error", "message": "Tabla no válida."}

    if not is_valid_column(table, column):
        return {"status": "error", "message": "Columna no válida."}

    response = supabase.table(table).delete().eq(column, value).execute()

    if response.error:
        return {
            "status": "error",
            "message": response.error['message'],
        }

    return {
        "status": "success",
        "data": response.data
    }