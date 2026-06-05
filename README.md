# TPO - Sistema de Facturación

**Materia:** Base de Datos 2 (Ingeniería de Datos II) - 1er cuatrimestre 2026

**Integrantes:**
- De Biase Dion Ramiro
- Jofre Maximo Ezequiel

---

## Descripción

Sistema de facturación con **persistencia políglota**: integración de una base de datos **SQL (MySQL)** y una base de datos **NoSQL (MongoDB)** a través de una **API REST** unificada construida con **FastAPI**.

Los datos maestros (clientes, productos y teléfonos) se almacenan en MySQL, aprovechando las relaciones y restricciones de integridad referencial. Las facturas con su detalle se almacenan como documentos embebidos en MongoDB, lo que permite consultar la factura completa sin necesidad de JOINs.

---

## Estructura del Proyecto

```
TP0_SISTEMA_DE_FACTURACION/
│
├── e01_cliente.csv              # Dataset: clientes
├── e01_producto.csv             # Dataset: productos
├── e01_telefono.csv             # Dataset: teléfonos
├── e01_factura.csv              # Dataset: cabecera de facturas
├── e01_detalle_factura.csv      # Dataset: detalle de facturas
│
├── creacion de base de datos.sql   # Script de creación de DB MySQL
├── migracion_csv_a_sql.py          # Script: carga CSVs → MySQL
├── requirements.txt                # Dependencias del proyecto
├── README.md                       # Este archivo
│
└── api/                            # API REST (FastAPI)
    ├── main.py                     # Punto de entrada de FastAPI
    ├── config.py                   # Configuración de conexiones
    │
    ├── database/
    │   ├── mysql.py                # Conexión y helpers para MySQL
    │   └── mongodb.py              # Conexión a MongoDB
    │
    ├── models/
    │   └── schemas.py              # Modelos Pydantic (validación)
    │
    ├── routes/
    │   ├── clientes.py             # Endpoints de clientes (Req 1-6, 13)
    │   ├── productos.py            # Endpoints de productos (Req 8, 12, 14)
    │   ├── facturas.py             # Endpoints de facturas (Req 7, 9, 11)
    │   └── reportes.py             # Endpoint de reportes (Req 10)
    │
    └── scripts/
        └── migrar_a_mongodb.py     # Script: migra datos MySQL → MongoDB
```

---

## Requisitos Previos

- **Python 3.12+**
- **MySQL 8+** corriendo y accesible
- **MongoDB 7+** corriendo y accesible
- **pip** (gestor de paquetes de Python)

---

## Instalación

### 1. Clonar el repositorio

```bash
git clone <url-del-repositorio>
cd TPO_SISTEMA_DE_FACTURACION
```

### 2. Crear y activar entorno virtual

```bash
python3 -m venv venv
source venv/bin/activate   # Linux/Mac
# O en Windows: venv\Scripts\activate
```

### 3. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 4. Configurar credenciales

Editar `api/config.py` con los datos de conexión:

```python
MYSQL_PASSWORD = "tu_contraseña_mysql"
MONGO_URI = "mongodb://localhost:27017"   # o la URI de tu MongoDB
```

---

## Carga de Datos

### 1. Crear la base de datos MySQL

Opción A — desde la terminal:
```bash
mysql -u root -p < "creacion de base de datos.sql"
```

Opción B — desde MySQL Workbench o similar:
Ejecutar el contenido de `creacion de base de datos.sql`

### 2. Cargar CSVs a MySQL

```bash
source venv/bin/activate
cd /ruta/del/proyecto
python migracion_csv_a_sql.py
```

Esto lee los 5 archivos CSV y los inserta en sus tablas correspondientes respetando el orden de las relaciones (cliente → producto → teléfono → factura → detalle_factura).

### 3. Migrar datos a MongoDB

```bash
source venv/bin/activate
python -m api.scripts.migrar_a_mongodb
```

Este script:
1. Lee las tablas `E01_FACTURA` y `E01_DETALLE_FACTURA` de MySQL
2. Combina cada factura con sus items en un único documento embebido
3. Enriquece los items con datos del producto (marca, nombre, precio)
4. Inserta los documentos en la colección `facturas` de MongoDB
5. Crea la vista `facturas_por_fecha` (facturas ordenadas cronológicamente)

---

## Uso de la API

### Iniciar el servidor

```bash
source venv/bin/activate
uvicorn api.main:app --host 0.0.0.0 --port 8000
```

### Documentación interactiva (Swagger)

Abrir en el navegador: [http://localhost:8000/docs](http://localhost:8000/docs)

### Endpoints disponibles

| # | Requerimiento | Método | Endpoint | Base de datos |
|---|---|---|---|---|
| 1 | Clientes con teléfonos | GET | `/clientes/telefonos` | MySQL |
| 2 | Buscar cliente por nombre y apellido | GET | `/clientes/buscar?nombre=&apellido=` | MySQL |
| 3 | Teléfonos con datos del cliente | GET | `/clientes/telefonos-lista` | MySQL |
| 4 | Clientes con al menos 1 factura | GET | `/clientes/con-facturas` | MySQL |
| 5 | Clientes sin facturas | GET | `/clientes/sin-facturas` | MySQL |
| 6 | Todos los clientes + cantidad de facturas | GET | `/clientes/cantidad-facturas` | **Ambas** |
| 7 | Facturas de un cliente | GET | `/facturas/cliente?nombre=&apellido=` | **Ambas** |
| 8 | Productos facturados al menos 1 vez | GET | `/productos/facturados` | **Ambas** |
| 9 | Facturas con productos de una marca | GET | `/facturas/marca?marca=` | **Ambas** |
| 10 | Gasto total por cliente (con IVA) | GET | `/reportes/gasto-por-cliente` | **Ambas** |
| 11 | Facturas ordenadas por fecha (vista) | GET | `/facturas/ordenadas-por-fecha` | MongoDB |
| 12 | Productos no facturados (vista) | GET | `/productos/no-facturados` | **Ambas** |
| 13 | Crear cliente | POST | `/clientes/` | MySQL |
| 13 | Modificar cliente | PUT | `/clientes/{nro_cliente}` | MySQL |
| 13 | Eliminar cliente | DELETE | `/clientes/{nro_cliente}` | MySQL |
| 14 | Crear producto | POST | `/productos/` | MySQL |
| 14 | Modificar producto | PUT | `/productos/{codigo_producto}` | MySQL |

---

## Arquitectura del Sistema

### Persistencia Políglota

| Base de datos | Almacena | Justificación |
|---|---|---|
| **MySQL** (SQL) | `E01_CLIENTE`, `E01_TELEFONO`, `E01_PRODUCTO` | Datos con relaciones rígidas (claves foráneas, 1:N, integridad referencial). Operaciones CRUD y consultas que requieren joins. |
| **MongoDB** (NoSQL) | `facturas` (con items embebidos), `productos` (copia para agilizar consultas) | Las facturas son documentos jerárquicos naturales: una cabecera con N items. Almacenarlas como documentos embebidos evita JOINs complejos y permite consultar la factura completa en una sola lectura. |

### Flujo de datos

```
Cliente (navegador / curl / Postman)
        │
        ▼
    ┌──────────┐
    │  FastAPI  │  ← Decide qué base consultar según el endpoint
    └────┬─────┘
         │
    ┌────┴────┬──────────┐
    │         │          │
    ▼         ▼          ▼
  MySQL    MongoDB    Ambas
(clientes,  (facturas  (la API
 productos,  con       orquesta
 teléfonos)  items)    y combina)
```

### Ejemplo de documento en MongoDB

```json
{
  "nro_factura": 1,
  "fecha": "2016-05-28",
  "total_sin_iva": 294369.60,
  "iva": 21.0,
  "total_con_iva": 356187.22,
  "nro_cliente": 4,
  "items": [
    {
      "nro_item": 37,
      "codigo_producto": 9,
      "cantidad": 93,
      "producto_marca": "Posuere LLP",
      "producto_nombre": "pet supplies",
      "producto_precio": 184.12
    },
    ...
  ]
}
```

---

## Detener la API

```bash
Ctrl + C    # si está en primer plano
# O si está en background:
ps aux | grep uvicorn
kill -9 <PID>
```

---

## Esquema de Base de Datos MySQL

```
E01_CLIENTE (nro_cliente PK, nombre, apellido, direccion, activo)
    │
    ├── E01_TELEFONO (codigo_area, nro_telefono PK, tipo, nro_cliente FK)
    │
    └── E01_FACTURA (nro_factura PK, fecha, total_sin_iva, iva, total_con_iva, nro_cliente FK)
            │
            └── E01_DETALLE_FACTURA (nro_factura FK, nro_item PK, cantidad, codigo_producto FK)

E01_PRODUCTO (codigo_producto PK, marca, nombre, descripcion, precio, stock)
    │
    └── E01_DETALLE_FACTURA (codigo_producto FK)
```
