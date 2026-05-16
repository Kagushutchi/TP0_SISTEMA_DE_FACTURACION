##TPO-Pre-Entrega-Sistema de Facturacion

##Integrantes:
*De biase Dion Ramiro
*Jofre Maximo Ezequiel

## Dependencias usadas
* **Python 3.x**
* **Pandas**: Para la lectura, manipulación y limpieza de los datasets.
* **SQLAlchemy**: Para la gestión de la conexión y el mapeo seguro hacia el motor de base de datos.
* **MySQL**: Como motor de base de datos

## Estructura del Proyecto

Datasets TPO2c2026/
* e01_cliente.csv          # Datos de los clientes (Tabla Padre)
* e01_producto.csv         # Catálogo de productos (Tabla Padre)
* e01_telefono.csv         # Teléfonos vinculados al cliente (1:N)
* e01_factura.csv          # Cabecera de facturas vinculadas al cliente (1:N)
* e01_detalle_factura.csv  # Detalle de productos por factura (N:M)

* creacion de base de datos.sql           # Script de creación de tablas en MySQL
* migracion_csv_a_sql.py   # Script para insertar los datos de los csv a la tablas de la base de datos en Python
* requirements.txt # Archivo txt que muestra las dependecias que tenemos instaladas por mas que no las usemos a todas

## Instrucciones del codigo

* ** Tener instalado python poder crear la venv y el gestor de paquetes pip
* ** Activar la venv dependiendo del sistema operativo
* ** Luego hacer `pip install pandas sqlalchemy mysql-connector-python`
* ** Ejecutar el scrip de sql por partes:
  * Primero ejecutar la creacion de la base de datos, verificando que no exista una que se llame igual
  * Segundo ejecuar el uso de la base de datos y cada creacion de las tablas respetando el orden
* ** En el script de python cargue las credenciales correspodientes de su motor de base datos
* ** Por ultimo ejecutar este comando `python migracion_csv_a_sql.py`
