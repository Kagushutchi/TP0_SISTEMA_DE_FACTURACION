import sys
sys.path.insert(0, "/home/ramirodion/Documentos/tpo_sistema-de-facturacion/TP0_SISTEMA_DE_FACTURACION")

from api.database.mysql import execute_query
from api.database.mongodb import db
from pymongo import UpdateOne


def migrar_productos():
    productos = execute_query("SELECT * FROM E01_PRODUCTO")
    if productos:
        db["productos"].delete_many({})
        db["productos"].insert_many(productos)
        print(f"Migrados {len(productos)} productos a MongoDB")


def migrar_facturas():
    facturas = execute_query("SELECT * FROM E01_FACTURA")
    detalle = execute_query("SELECT * FROM E01_DETALLE_FACTURA")
    productos = execute_query("SELECT * FROM E01_PRODUCTO")

    prod_map = {p["codigo_producto"]: p for p in productos}

    detalle_por_factura: dict[int, list] = {}
    for d in detalle:
        detalle_por_factura.setdefault(d["nro_factura"], []).append(d)

    operaciones = []
    for f in facturas:
        items = detalle_por_factura.get(f["nro_factura"], [])
        items_enriquecidos = []
        for item in items:
            p = prod_map.get(item["codigo_producto"], {})
            items_enriquecidos.append({
                "nro_item": item["nro_item"],
                "codigo_producto": item["codigo_producto"],
                "cantidad": item["cantidad"],
                "producto_marca": p.get("marca"),
                "producto_nombre": p.get("nombre"),
                "producto_precio": p.get("precio"),
            })

        doc = {
            **f,
            "fecha": str(f["fecha"]) if f["fecha"] else None,
            "items": items_enriquecidos,
        }
        operaciones.append(
            UpdateOne({"nro_factura": doc["nro_factura"]}, {"$set": doc}, upsert=True)
        )

    if operaciones:
        db["facturas"].bulk_write(operaciones)
        print(f"Migradas {len(facturas)} facturas con {sum(len(v) for v in detalle_por_factura.values())} items a MongoDB")


def crear_vistas():
    db["facturas_por_fecha"].drop()
    pipeline = [
        {"$sort": {"fecha": 1}},
        {"$out": "facturas_por_fecha"},
    ]
    db["facturas"].aggregate(pipeline)
    print("Vista 'facturas_por_fecha' creada (facturas ordenadas por fecha)")


if __name__ == "__main__":
    print("Migrando datos de MySQL a MongoDB...")
    migrar_productos()
    migrar_facturas()
    crear_vistas()
    print("Migración completada.")
