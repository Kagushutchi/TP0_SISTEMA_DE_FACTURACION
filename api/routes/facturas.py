from fastapi import APIRouter, HTTPException

from api.database.mysql import execute_query
from api.database.mongodb import facturas as facturas_col
from api.models.schemas import FacturaOut

router = APIRouter(prefix="/facturas", tags=["Facturas"])


@router.get("/cliente", response_model=list[FacturaOut])
def get_facturas_por_cliente(nombre: str, apellido: str):
    """Req 7: Facturas compradas por un cliente (nombre + apellido)"""
    clientes = execute_query(
        "SELECT nro_cliente FROM E01_CLIENTE WHERE nombre = :nombre AND apellido = :apellido",
        {"nombre": nombre, "apellido": apellido},
    )
    if not clientes:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")

    nro_cliente = clientes[0]["nro_cliente"]
    docs = list(facturas_col.find({"nro_cliente": nro_cliente}, {"_id": 0}))
    return docs


@router.get("/marca", response_model=list[FacturaOut])
def get_facturas_por_marca(marca: str):
    """Req 9: Facturas que contienen productos de una marca específica"""
    productos = execute_query(
        "SELECT codigo_producto FROM E01_PRODUCTO WHERE marca LIKE :marca",
        {"marca": f"%{marca}%"},
    )
    if not productos:
        return []

    codigos = {p["codigo_producto"] for p in productos}
    docs = list(facturas_col.find({}, {"_id": 0}))
    resultado = []
    for doc in docs:
        if any(item["codigo_producto"] in codigos for item in doc.get("items", [])):
            resultado.append(doc)
    return resultado


@router.get("/ordenadas-por-fecha", response_model=list[FacturaOut])
def get_facturas_ordenadas():
    """Req 11: Vista de facturas ordenadas por fecha (desde MongoDB)"""
    docs = list(facturas_col.find({}, {"_id": 0}).sort("fecha", 1))
    return docs
