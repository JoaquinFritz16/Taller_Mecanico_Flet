-- Crear la base de datos
CREATE DATABASE IF NOT EXISTS Taller_Mecanico;
USE Taller_Mecanico;

-- Tabla Persona (base para Cliente)
CREATE TABLE IF NOT EXISTS Persona (
    DNI VARCHAR(50) PRIMARY KEY,
    Nombre VARCHAR(50),
    Apellido VARCHAR(50),
    Direccion VARCHAR(50),
    Tele_Contac VARCHAR(50)
);

CREATE TABLE IF NOT EXISTS Cliente (
    Cod_Cliente VARCHAR(50) PRIMARY KEY,
    DNI VARCHAR(50),
    FOREIGN KEY (DNI) REFERENCES Persona(DNI)
);

-- Tabla Vehiculos (relacionada con Cliente/Persona por DNI)
CREATE TABLE IF NOT EXISTS Vehiculos (
    Patente VARCHAR(50) PRIMARY KEY,
    DNI VARCHAR(50),
    Marca VARCHAR(50),
    Modelo VARCHAR(50),
    Color VARCHAR(50),
    FOREIGN KEY (DNI) REFERENCES Persona(DNI)
);

-- Tabla Mecanicos
CREATE TABLE IF NOT EXISTS Mecanicos (
    Legajo VARCHAR(50) PRIMARY KEY,
    Nombre VARCHAR(50),
    Apellido VARCHAR(50),
    Rol VARCHAR(50),
    Estado VARCHAR(50)
);

-- Tabla Reparaciones (relaciona Cliente, Vehículo y Mecánico)
CREATE TABLE IF NOT EXISTS Reparaciones (
    ID VARCHAR(50) PRIMARY KEY,
    Patente VARCHAR(50),
    DNI VARCHAR(50),
    Legajo VARCHAR(50),
    Fecha DATE,
    FOREIGN KEY (Patente) REFERENCES Vehiculos(Patente),
    FOREIGN KEY (DNI) REFERENCES Persona(DNI),
    FOREIGN KEY (Legajo) REFERENCES Mecanicos(Legajo)
);

-- Tabla Repuestos (asociados a Reparaciones)
CREATE TABLE IF NOT EXISTS Repuestos (
    Codigo_Repuesto VARCHAR(50) PRIMARY KEY,
    ID VARCHAR(50),  -- ID de Reparación
    Precio FLOAT,
    Cant_Rep INT,
    Importe FLOAT GENERATED ALWAYS AS (Precio * Cant_Rep) STORED,
    Descripcion VARCHAR(50),
    FOREIGN KEY (ID) REFERENCES Reparaciones(ID)
);
CREATE TABLE IF NOT EXISTS usuario (
    id_usuario INT AUTO_INCREMENT PRIMARY KEY,
    nombre_usuario VARCHAR(50) NOT NULL UNIQUE,
    contrasena VARCHAR(255) NOT NULL,
    nombre_completo VARCHAR(100),
    rol VARCHAR(50) COMMENT 'Ej: Administrador, Mecanico',
    estado VARCHAR(20) COMMENT 'Ej: Activo, Inactivo'
);

INSERT INTO usuario (nombre_usuario, contrasena, nombre_completo, rol, estado)
VALUES ('admin', 'admin123', 'Administrador Principal', 'Administrador', 'Activo')
ON DUPLICATE KEY UPDATE nombre_completo = 'Administrador Principal';

