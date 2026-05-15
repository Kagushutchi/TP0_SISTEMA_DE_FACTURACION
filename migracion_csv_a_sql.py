import pandas as pd
from sqlalchemy import create_engine

#Colocar los datos de conexión a tu base de datos MySQL
USER = "root"
PASSWORD = "contraseña" 
HOST = "localhost"
PORT = "3306" 
DATABASE = "sistema_facturacion"

engine = create_engine(f"mysql+mysqlconnector://{USER}:{PASSWORD}@{HOST}:{PORT}/{DATABASE}")

def importar_csv(archivo, tabla):
    try:
        print(f"Procesando {archivo}...")
        df = pd.read_csv(archivo, sep=';', encoding='latin-1')
        df.to_sql(name=tabla, con=engine, if_exists='append', index=False)
        print(f"Datos cargados exitosamente en {tabla}\n")
    except Exception as e:
        print(f"Error al cargar {archivo} en {tabla}: {e}\n")
        
#No cambiar el orden de las importaciones, ya que hay relaciones entre las tablas
importar_csv('e01_cliente.csv', 'E01_CLIENTE')
importar_csv('e01_producto.csv', 'E01_PRODUCTO')
importar_csv('e01_telefono.csv', 'E01_TELEFONO')
importar_csv('e01_factura.csv', 'E01_FACTURA')
importar_csv('e01_detalle_factura.csv', 'E01_DETALLE_FACTURA')