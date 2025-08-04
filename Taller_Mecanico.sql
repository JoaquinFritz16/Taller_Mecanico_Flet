CREATE DATABASE IF NOT EXISTS `Taller_Mecanico`;
USE `Taller_Mecanico`;

CREATE TABLE IF NOT EXISTS `Clientes` (
    `DNI` VARCHAR(50) PRIMARY KEY,
    `Nombre` VARCHAR(50),
    `Apellido` VARCHAR(50),
    `Direccion` VARCHAR(50),
    `Telefono` VARCHAR(50)
);

CREATE TABLE IF NOT EXISTS `Vehiculos` (
    `Patente` VARCHAR(50) PRIMARY KEY,
    `DNI` VARCHAR(50),
    `Marca` VARCHAR(50),
    `Modelo` VARCHAR(50),
    `Color` VARCHAR(50),
    FOREIGN KEY (`DNI`) REFERENCES `Clientes`(`DNI`)
);

CREATE TABLE IF NOT EXISTS `Mecanicos` (
    `Legajo` VARCHAR(50) PRIMARY KEY,
    `Nombre` VARCHAR(50),
    `Apellido` VARCHAR(50),
    `Rol` VARCHAR(50),
    `Estado` VARCHAR(50)
);

CREATE TABLE IF NOT EXISTS `Reparaciones` (
    `ID` VARCHAR(50) PRIMARY KEY,
    `Patente` VARCHAR(50),
    `DNI` VARCHAR(50),
    `Legajo` VARCHAR(50),
    `Fecha` DATE,
    FOREIGN KEY (`Patente`) REFERENCES `Vehiculos`(`Patente`),
    FOREIGN KEY (`DNI`) REFERENCES `Clientes`(`DNI`),
    FOREIGN KEY (`Legajo`) REFERENCES `Mecanicos`(`Legajo`)
);

CREATE TABLE IF NOT EXISTS `Repuestos` (
    `ID` VARCHAR(50),
    `Codigo_repuesto` VARCHAR(50) PRIMARY KEY,
    `Precio` FLOAT,
    `Cant_rep` INT,
    `Importe` FLOAT GENERATED ALWAYS AS ( `Precio` *  `Cant_rep`) STORED,
    `Descripcion` VARCHAR(50),
    FOREIGN KEY (`ID`) REFERENCES `Reparaciones`(`ID`)
);
drop database taller_mecanico;
