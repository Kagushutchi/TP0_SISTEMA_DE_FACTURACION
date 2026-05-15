CREATE DATABASE if not exists sistema_facturacion;
USE sistema_facturacion;


CREATE TABLE E01_CLIENTE (
    nro_cliente INT PRIMARY KEY,
    nombre VARCHAR(45),
    apellido VARCHAR(45),
    direccion VARCHAR(45),
    activo TINYINT
);


CREATE TABLE E01_TELEFONO (
    codigo_area INT(3),
    nro_telefono INT(7),
    tipo CHAR(1),
    nro_cliente INT,
    PRIMARY KEY (codigo_area, nro_telefono),
    FOREIGN KEY (nro_cliente) REFERENCES E01_CLIENTE(nro_cliente)
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


