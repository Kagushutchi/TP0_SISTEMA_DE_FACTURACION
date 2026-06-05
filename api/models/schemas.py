from datetime import date
from pydantic import BaseModel


class TelefonoOut(BaseModel):
    codigo_area: int
    nro_telefono: int
    tipo: str
    nro_cliente: int


class ClienteOut(BaseModel):
    nro_cliente: int
    nombre: str
    apellido: str
    direccion: str
    activo: int


class ClienteConTelefonos(ClienteOut):
    telefonos: list[TelefonoOut]


class ClienteConFacturas(ClienteOut):
    cantidad_facturas: int


class ClienteCreate(BaseModel):
    nro_cliente: int
    nombre: str
    apellido: str
    direccion: str
    activo: int


class ClienteUpdate(BaseModel):
    nombre: str | None = None
    apellido: str | None = None
    direccion: str | None = None
    activo: int | None = None


class ProductoOut(BaseModel):
    codigo_producto: int
    marca: str
    nombre: str
    descripcion: str
    precio: float
    stock: int


class ProductoCreate(BaseModel):
    codigo_producto: int
    marca: str
    nombre: str
    descripcion: str
    precio: float
    stock: int


class ProductoUpdate(BaseModel):
    marca: str | None = None
    nombre: str | None = None
    descripcion: str | None = None
    precio: float | None = None
    stock: int | None = None


class ItemFacturaOut(BaseModel):
    nro_item: int
    codigo_producto: int
    cantidad: float
    producto_marca: str | None = None
    producto_nombre: str | None = None
    producto_precio: float | None = None


class FacturaOut(BaseModel):
    nro_factura: int
    fecha: str
    total_sin_iva: float
    iva: float
    total_con_iva: float
    nro_cliente: int
    items: list[ItemFacturaOut]


class GastoCliente(BaseModel):
    nro_cliente: int
    nombre: str
    apellido: str
    total_gastado: float
