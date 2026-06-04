CREATE DATABASE if not exists sistema_facturacion;
USE sistema_facturacion;


CREATE TABLE E01_CLIENTE (
    nro_cliente INT PRIMARY KEY,
    nombre VARCHAR(45),
    apellido VARCHAR(45),
    direccion VARCHAR(45),
    activo TINYINT
);


CREATE TABLE E01_PRODUCTO (
    codigo_producto INT PRIMARY KEY,
    marca VARCHAR(45),
    nombre VARCHAR(45),
    descripcion VARCHAR(45),
    precio FLOAT,
    stock INT
);


CREATE TABLE E01_FACTURA (
    nro_factura INT PRIMARY KEY,
    fecha DATE,
    total_sin_iva DOUBLE,
    iva DOUBLE,
    total_con_iva DOUBLE,
    nro_cliente INT,
    FOREIGN KEY (nro_cliente) REFERENCES E01_CLIENTE(nro_cliente)
);


CREATE TABLE E01_DETALLE_FACTURA (
    nro_factura INT,
    nro_item INT,
    cantidad FLOAT,
    codigo_producto INT,
    PRIMARY KEY (nro_factura, nro_item),
    FOREIGN KEY (nro_factura) REFERENCES E01_FACTURA(nro_factura),
    FOREIGN KEY (codigo_producto) REFERENCES E01_PRODUCTO(codigo_producto)
);


/*
CREATE TABLE E01_TELEFONO (
    codigo_area INT(3),
    nro_telefono INT(7),
    tipo CHAR(1),
    nro_cliente INT,
    PRIMARY KEY (codigo_area, nro_telefono),
    FOREIGN KEY (nro_cliente) REFERENCES E01_CLIENTE(nro_cliente)
);
*/


#1 Obtener datos de los clientes(El resto de la consulta va en mongoDB y en el backend:

SELECT * FROM E01_CLIENTE;

#2 Obtener el/los teléfono/s y el número de cliente del cliente con nombre “Jacob” y apellido “Cooper”(El resto de la consulta va en mongoDB y en el backend) . 

SELECT nro_cliente,nombre,apellido  FROM E01_CLIENTE WHERE nombre="Jacob" and Apellido = "Cooper";

#3 Mostrar todos los datos juntos a los telefonos de cada cliente(El resto de la consulta va en mongoDB y en el backend).

SELECT * FROM E01_CLIENTE;

#4 Obtener todos los clientes que tengan registrada al menos una factura. 

SELECT C.APELLIDO, C.NOMBRE FROM E01_CLIENTE C JOIN E01_FACTURA F ON C.nro_cliente = F.nro_cliente
group by C.nro_cliente
having count(F.nro_factura)>=1; #Esta es menos optima pero cumple con la consigna(es menos optima porque cuenta mas veces)

select C.APELLIDO,C.NOMBRE FROM E01_CLIENTE C 
WHERE 
EXISTS
(select * from E01_FACTURA F WHERE C.nro_cliente = F.nro_cliente);# Esta es mas optima porque no cuenta en donde encuentra una deja de buscar

#5 Los clientes que no tengan facturas

select C.APELLIDO,C.NOMBRE FROM E01_CLIENTE C WHERE NOT EXISTS(select * from E01_FACTURA F WHERE C.nro_cliente = F.nro_cliente);

# 6 Devolver todos los clientes, con la cantidad de facturas que tienen registradas (si no tienen considerar cantidad en 0) 

SELECT C.APELLIDO, C.NOMBRE, count(F.nro_factura) AS Cantidad__facturas FROM E01_CLIENTE C 
LEFT JOIN E01_FACTURA F ON C.nro_cliente = F.nro_cliente
group by C.nro_cliente;

# 7 Listar los datos de todas las facturas que hayan sido compradas por el cliente de nombre "Kai" y apellido "Bullock". 

SELECT C.APELLIDO, C.NOMBRE, F.* FROM E01_CLIENTE C right JOIN E01_FACTURA F 
ON C.nro_cliente = F.nro_cliente WHERE C.APELLIDO="Bullock"and C.NOMBRE="KAI";

# 8  Seleccionar los productos que han sido facturados al menos 1 vez. 

SELECT P.* FROM E01_PRODUCTO P where exists
(SELECT * FROM E01_FACTURA F JOIN E01_DETALLE_FACTURA D 
ON F.nro_factura=D.nro_factura 
where D.codigo_producto=P.codigo_producto);

# 9 Listar los datos de todas las facturas que contengan productos de las marcas “Ipsum”.

SELECT F.* FROM E01_FACTURA F where exists (
SELECT * FROM E01_DETALLE_FACTURA D 
JOIN E01_PRODUCTO P ON F.nro_factura=D.nro_factura 
WHERE D.codigo_producto=P.codigo_producto and P.marca LIKE "%Ipsum%"
);

# 10 Mostrar nombre y apellido de cada cliente junto con lo que gastó en total, con IVA incluido.

SELECT C.nombre , C.apellido, FORMAT(SUM(F.total_con_iva),2) AS Total 
FROM E01_CLIENTE C JOIN E01_FACTURA F on C.nro_cliente=F.nro_cliente
group by C.nro_cliente
having Total>=1;

# 11 Generar una vista para mostrar los datos de las facturas ordenaods por fechas
CREATE VIEW facturas AS
SELECT F.* FROM E01_FACTURA F 
where total_sin_iva >=1 and total_con_iva>=1 
order by F.fecha DESC ;

# 12 Generar una vista para mostrar los datos de los productos que no esten en la lista
CREATE VIEW prodcutos_no_facturados AS
SELECT P.* FROM E01_PRODUCTO  P  WHERE NOT EXISTS(
SELECT * FROM E01_DETALLE_FACTURA D 
WHERE P.codigo_producto=D.codigo_producto
);

SELECT P.* 
FROM E01_PRODUCTO P
LEFT JOIN E01_DETALLE_FACTURA D 
    ON P.codigo_producto = D.codigo_producto
WHERE D.codigo_producto IS NULL;

# 13 Crear



