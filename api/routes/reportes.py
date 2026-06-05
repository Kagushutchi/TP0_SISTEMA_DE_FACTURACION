from fastapi import APIRouter

from api.database.mongodb import facturas as facturas_col
from api.models.schemas import GastoCliente

router = APIRouter(prefix="/reportes", tags=["Reportes"])


@router.get("/gasto-por-cliente", response_model=list[GastoCliente])
def get_gasto_por_cliente():
    """Req 10: Nombre y apellido de cada cliente con total gastado (IVA incluido)"""
    from api.database.mysql import execute_query

    clientes = execute_query("SELECT nro_cliente, nombre, apellido FROM E01_CLIENTE")
    mapa_clientes = {c["nro_cliente"]: c for c in clientes}

    pipeline = [
        {
            "$group": {
                "_id": "$nro_cliente",
                "total_gastado": {"$sum": "$total_con_iva"},
            }
        }
    ]
    gastos = list(facturas_col.aggregate(pipeline))

    resultado = []
    for g in gastos:
        c = mapa_clientes.get(g["_id"])
        if c:
            resultado.append(
                {
                    "nro_cliente": c["nro_cliente"],
                    "nombre": c["nombre"],
                    "apellido": c["apellido"],
                    "total_gastado": round(g["total_gastado"], 2),
                }
            )

    resultado.sort(key=lambda x: x["nro_cliente"])
    return resultado
