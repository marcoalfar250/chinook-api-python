# =========================
# IMPORTS
# =========================
from typing import Optional

from fastapi import FastAPI, HTTPException, Depends
from fastapi.exceptions import RequestValidationError
from fastapi.security import OAuth2PasswordRequestForm
from starlette.exceptions import HTTPException as StarletteHTTPException

from auth import create_access_token
from security import get_current_user
from hashing import verify_password

import crud

from schemas import ComentarioClienteCrear

from exceptions import (
    http_exception_handler,
    validation_exception_handler,
    generic_exception_handler
)


# =========================
# APP CONFIG
# =========================
app = FastAPI(title="Chinook API", version="1.0")

app.add_exception_handler(StarletteHTTPException, http_exception_handler)
app.add_exception_handler(RequestValidationError, validation_exception_handler)
app.add_exception_handler(Exception, generic_exception_handler)


# =========================
# RUTA BASE
# =========================
@app.get("/")
def inicio():
    return {"mensaje": "Servicio Chinook activo"}


# =========================
# AUTENTICACIÓN
# =========================
@app.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    usuario = crud.obtener_usuario_por_username(form_data.username)

    if not usuario:
        raise HTTPException(status_code=401, detail="Credenciales incorrectas")

    if not usuario["activo"]:
        raise HTTPException(status_code=401, detail="Usuario inactivo")

    if not verify_password(form_data.password, usuario["password_hash"]):
        raise HTTPException(status_code=401, detail="Credenciales incorrectas")

    token = create_access_token(data={"sub": usuario["username"]})

    return {
        "access_token": token,
        "token_type": "bearer"
    }


# =========================
# CLIENTES
# =========================
@app.get("/clientes")
def listar_clientes(
    current_user: dict = Depends(get_current_user)
):
    return crud.obtener_clientes()


@app.get("/clientes/{customer_id}")
def obtener_cliente(
    customer_id: int,
    current_user: dict = Depends(get_current_user)
    ):
    cliente = crud.obtener_cliente_por_id(customer_id)

    if not cliente:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")

    return cliente


@app.get("/clientesPaginado")
def listar_clientes_paginados(
    page: int = 1,
    page_size: int = 10,
    country: Optional[str] = None,
    nombre: Optional[str] = None,
    sort_by: str = "CustomerId",
    sort_order: str = "asc",
    current_user: dict = Depends(get_current_user)
):
    if page < 1 or page_size < 1:
        raise HTTPException(status_code=400, detail="Parámetros inválidos")

    return crud.obtener_clientes_paginado(
        page, page_size, country, nombre, sort_by, sort_order
    )


# =========================
# ARTISTAS
# =========================
@app.get("/artistas")
def listar_artistas(
    current_user: dict = Depends(get_current_user)
):
    return crud.obtener_artistas()


@app.get("/artistasPaginado")
def listar_artistas_paginados(
    page: int = 1,
    page_size: int = 10,
    nombre: Optional[str] = None,
    sort_by: str = "ArtistId",
    sort_order: str = "asc",
    current_user: dict = Depends(get_current_user)
):
    if page < 1 or page_size < 1:
        raise HTTPException(status_code=400, detail="Parámetros inválidos")

    return crud.obtener_artitas_paginado(
        page, page_size, nombre, sort_by, sort_order
    )


# =========================
# ÁLBUMES
# =========================
@app.get("/albumes")
def listar_albumes(
    current_user: dict = Depends(get_current_user)
):
    return crud.obtener_albumes()


# =========================
# FACTURAS
# =========================
@app.get("/facturas")
def listar_facturas(
    current_user: dict = Depends(get_current_user)
):
    return crud.obtener_facturas()


@app.get("/facturas/cliente/{customer_id}")
def listar_facturas_por_cliente(
    customer_id: int,
    current_user: dict = Depends(get_current_user)
    ):
    facturas = crud.obtener_facturas_por_cliente(customer_id)

    if not facturas:
        raise HTTPException(
            status_code=404,
            detail="No se encontraron facturas para ese cliente"
        )

    return facturas


# =========================
# COMENTARIOS
# =========================
@app.get("/comentarios")
def listar_comentarios(
    current_user: dict = Depends(get_current_user)
):
    return crud.obtener_comentarios()


@app.get("/comentarios/cliente/{customer_id}")
def listar_comentarios_por_cliente(
    customer_id: int,
    current_user: dict = Depends(get_current_user)
    ):
    if not crud.existe_cliente(customer_id):
        raise HTTPException(status_code=404, detail="Cliente no existe")

    return crud.obtener_comentarios_por_cliente(customer_id)


@app.post("/comentarios")
def insertar_comentario(
    data: ComentarioClienteCrear,
    current_user: dict = Depends(get_current_user)
    ):
    if not crud.existe_cliente(data.customer_id):
        raise HTTPException(status_code=404, detail="Cliente no existe")

    if not data.comentario.strip():
        raise HTTPException(
            status_code=400,
            detail="El comentario no puede ir vacío"
        )

    if len(data.comentario) > 500:
        raise HTTPException(
            status_code=400,
            detail="El comentario no puede superar 500 caracteres"
        )

    return crud.crear_comentario(data.customer_id, data.comentario)