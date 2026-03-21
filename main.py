from fastapi import FastAPI, HTTPException
from schemas import ComentarioClienteCrear
from typing import Optional

import crud

app = FastAPI(
    title="Chinook API",
    version="1.0"
)


@app.get("/")
def inicio():
    return {"mensaje": "Servicio Chinook activo"}


@app.get("/clientes")
def listar_clientes():
    return crud.obtener_clientes()

@app.get("/clientes/{customer_id}")
def obtener_cliente(customer_id: int):
    cliente = crud.obtener_cliente_por_id(customer_id)

    if not cliente:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")

    return cliente

@app.get("/clientesPaginado")
def listar_clientes_paginados(
    page: int = 1,
    page_size: int = 10,
    country: Optional[str] = None,
    nombre: Optional[str] = None
):
    if page < 1 or page_size < 1:
        raise HTTPException(status_code=400, detail="Parámetros inválidos")
    
    return crud.obtener_clientes_paginado(page, page_size, country, nombre)


@app.get("/artistas")
def listar_artistas():
    return crud.obtener_artistas()


@app.get("/albumes")
def listar_albumes():
    return crud.obtener_albumes()


@app.get("/facturas")
def listar_facturas():
    return crud.obtener_facturas()


@app.get("/facturas/cliente/{customer_id}")
def listar_facturas_por_cliente(customer_id: int):
    facturas = crud.obtener_facturas_por_cliente(customer_id)

    if not facturas:
        raise HTTPException(status_code=404, detail="No se encontraron facturas para ese cliente")

    return facturas

@app.get("/comentarios")
def listar_comentarios():
    return crud.obtener_comentarios()

@app.get("/comentarios/cliente/{customer_id}")
def listar_comentarios_por_cliente(customer_id: int):
    if not crud.existe_cliente(customer_id):
        raise HTTPException(status_code=404, detail="Cliente no existe")

    return crud.obtener_comentarios_por_cliente(customer_id)

@app.post("/comentarios")
def insertar_comentario(data: ComentarioClienteCrear):
    if not crud.existe_cliente(data.customer_id):
        raise HTTPException(status_code=404, detail="Cliente no existe")

    if not data.comentario.strip():
        raise HTTPException(status_code=400, detail="El comentario no puede ir vacío")

    if len(data.comentario) > 500:
        raise HTTPException(status_code=400, detail="El comentario no puede superar 500 caracteres")

    return crud.crear_comentario(data.customer_id, data.comentario)