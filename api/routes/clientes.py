from fastapi import APIRouter, HTTPException

from api.database.mysql import execute_query, execute_write
from api.database.mongodb import facturas as facturas_col
from api.models.schemas import (
    ClienteOut,
    ClienteConTelefonos,
    ClienteConFacturas,
    ClienteCreate,
    ClienteUpdate,
    TelefonoOut,
)

router = APIRouter(prefix="/clientes", tags=["Clientes"])


@router.get("/telefonos", response_model=list[ClienteConTelefonos])
def get_clientes_con_telefonos():
    """Req 1: Obtener los datos de los clientes junto con sus teléfonos"""
    clientes = execute_query("SELECT * FROM E01_CLIENTE")
    telefonos = execute_query("SELECT * FROM E01_TELEFONO")
    tel_por_cliente: dict[int, list] = {}
    for t in telefonos:
        tel_por_cliente.setdefault(t["nro_cliente"], []).append(t)
    return [
        {**c, "telefonos": tel_por_cliente.get(c["nro_cliente"], [])} for c in clientes
    ]


@router.get("/buscar", response_model=list[ClienteConTelefonos])
def buscar_cliente(nombre: str, apellido: str):
    """Req 2: Obtener teléfonos y datos del cliente por nombre y apellido"""
    clientes = execute_query(
        "SELECT * FROM E01_CLIENTE WHERE nombre = :nombre AND apellido = :apellido",
        {"nombre": nombre, "apellido": apellido},
    )
    if not clientes:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")
    telefonos = execute_query(
        "SELECT * FROM E01_TELEFONO WHERE nro_cliente = :nro",
        {"nro": clientes[0]["nro_cliente"]},
    )
    return [{**clientes[0], "telefonos": telefonos}]


@router.get("/telefonos-lista", response_model=list[TelefonoOut])
def get_telefonos_con_clientes():
    """Req 3: Mostrar cada teléfono junto con los datos del cliente"""
    return execute_query(
        """SELECT t.*, c.nombre, c.apellido
           FROM E01_TELEFONO t
           JOIN E01_CLIENTE c ON t.nro_cliente = c.nro_cliente"""
    )


@router.get("/con-facturas", response_model=list[ClienteOut])
def get_clientes_con_facturas():
    """Req 4: Clientes con al menos una factura"""
    return execute_query(
        """SELECT DISTINCT c.*
           FROM E01_CLIENTE c
           INNER JOIN E01_FACTURA f ON c.nro_cliente = f.nro_cliente"""
    )


@router.get("/sin-facturas", response_model=list[ClienteOut])
def get_clientes_sin_facturas():
    """Req 5: Clientes sin ninguna factura"""
    return execute_query(
        """SELECT c.*
           FROM E01_CLIENTE c
           LEFT JOIN E01_FACTURA f ON c.nro_cliente = f.nro_cliente
           WHERE f.nro_factura IS NULL"""
    )


@router.get("/cantidad-facturas", response_model=list[ClienteConFacturas])
def get_clientes_cantidad_facturas():
    """Req 6: Todos los clientes con cantidad de facturas (0 si no tienen)"""
    clientes = execute_query("SELECT * FROM E01_CLIENTE")
    pipeline = [
        {"$group": {"_id": "$nro_cliente", "total": {"$sum": 1}}},
        {"$project": {"_id": 0, "nro_cliente": "$_id", "cantidad": "$total"}},
    ]
    conteo = list(facturas_col.aggregate(pipeline))
    mapa = {c["nro_cliente"]: c["cantidad"] for c in conteo}
    return [
        {**c, "cantidad_facturas": mapa.get(c["nro_cliente"], 0)} for c in clientes
    ]


@router.post("/", response_model=ClienteOut, status_code=201)
def crear_cliente(data: ClienteCreate):
    """Req 13: Crear un nuevo cliente"""
    try:
        execute_write(
            """INSERT INTO E01_CLIENTE (nro_cliente, nombre, apellido, direccion, activo)
               VALUES (:nro_cliente, :nombre, :apellido, :direccion, :activo)""",
            data.model_dump(),
        )
        return data
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.put("/{nro_cliente}", response_model=ClienteOut)
def modificar_cliente(nro_cliente: int, data: ClienteUpdate):
    """Req 13: Modificar un cliente existente"""
    updates = {k: v for k, v in data.model_dump().items() if v is not None}
    if not updates:
        raise HTTPException(status_code=400, detail="No hay campos para actualizar")
    set_clause = ", ".join(f"{k} = :{k}" for k in updates)
    updates["nro_cliente"] = nro_cliente
    rows = execute_write(
        f"UPDATE E01_CLIENTE SET {set_clause} WHERE nro_cliente = :nro_cliente",
        updates,
    )
    if rows == 0:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")
    return execute_query(
        "SELECT * FROM E01_CLIENTE WHERE nro_cliente = :nro", {"nro": nro_cliente}
    )[0]


@router.delete("/{nro_cliente}", status_code=204)
def eliminar_cliente(nro_cliente: int):
    """Req 13: Eliminar un cliente"""
    rows = execute_write(
        "DELETE FROM E01_CLIENTE WHERE nro_cliente = :nro", {"nro": nro_cliente}
    )
    if rows == 0:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")
