from pydantic import BaseModel
from typing import Optional


class Cliente(BaseModel):
    customer_id: int
    first_name: str
    last_name: str
    country: Optional[str] = None
    email: Optional[str] = None


class Artista(BaseModel):
    artist_id: int
    name: str


class Album(BaseModel):
    album_id: int
    title: str
    artist_name: str


class Factura(BaseModel):
    invoice_id: int
    customer_id: int
    customer_name: str
    invoice_date: str
    total: float

class ComentarioClienteCrear(BaseModel):
    customer_id: int
    comentario: str

class ComentarioClienteRespuesta(BaseModel):
    id: int
    customer_id: int
    comentario: str
    fecha_registro: str