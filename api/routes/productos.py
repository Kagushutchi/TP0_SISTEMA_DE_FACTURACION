from fastapi import APIRouter, HTTPException

from api.database.mysql import execute_query, execute_write
from api.database.mongodb import facturas as facturas_col
from api.models.schemas import (
    ProductoOut,
    ProductoCreate,
    ProductoUpdate,
)

router = APIRouter(prefix="/productos", tags=["Productos"])


@router.get("/facturados", response_model=list[ProductoOut])
def get_productos_facturados():
    """Req 8: Productos que han sido facturados al menos 1 vez"""
    pipeline = [
        {"$unwind": "$items"},
        {"$group": {"_id": "$items.codigo_producto"}},
    ]
    codigos = [doc["_id"] for doc in facturas_col.aggregate(pipeline)]

    if not codigos:
        return []

    placeholders = ", ".join(f":c{i}" for i in range(len(codigos)))
    params = {f"c{i}": c for i, c in enumerate(codigos)}
    return execute_query(
        f"SELECT * FROM E01_PRODUCTO WHERE codigo_producto IN ({placeholders})",
        params,
    )


@router.get("/no-facturados", response_model=list[ProductoOut])
def get_productos_no_facturados():
    """Req 12: Productos que aún no han sido facturados"""
    pipeline = [
        {"$unwind": "$items"},
        {"$group": {"_id": "$items.codigo_producto"}},
    ]
    codigos_facturados = {doc["_id"] for doc in facturas_col.aggregate(pipeline)}

    todos = execute_query("SELECT * FROM E01_PRODUCTO")
    return [p for p in todos if p["codigo_producto"] not in codigos_facturados]


@router.post("/", response_model=ProductoOut, status_code=201)
def crear_producto(data: ProductoCreate):
    """Req 14: Crear un nuevo producto"""
    try:
        execute_write(
            """INSERT INTO E01_PRODUCTO (codigo_producto, marca, nombre, descripcion, precio, stock)
               VALUES (:codigo_producto, :marca, :nombre, :descripcion, :precio, :stock)""",
            data.model_dump(),
        )
        return data
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.put("/{codigo_producto}", response_model=ProductoOut)
def modificar_producto(codigo_producto: int, data: ProductoUpdate):
    """Req 14: Modificar un producto existente"""
    updates = {k: v for k, v in data.model_dump().items() if v is not None}
    if not updates:
        raise HTTPException(status_code=400, detail="No hay campos para actualizar")
    set_clause = ", ".join(f"{k} = :{k}" for k in updates)
    updates["codigo_producto"] = codigo_producto
    rows = execute_write(
        f"UPDATE E01_PRODUCTO SET {set_clause} WHERE codigo_producto = :codigo_producto",
        updates,
    )
    if rows == 0:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    return execute_query(
        "SELECT * FROM E01_PRODUCTO WHERE codigo_producto = :cod",
        {"cod": codigo_producto},
    )[0]
