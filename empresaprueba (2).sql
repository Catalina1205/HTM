-- phpMyAdmin SQL Dump
-- version 5.2.0
-- https://www.phpmyadmin.net/
--
-- Servidor: 127.0.0.1:3306
-- Tiempo de generación: 29-02-2024 a las 11:54:27
-- Versión del servidor: 8.0.33
-- Versión de PHP: 8.0.26

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de datos: `empresaprueba`
--

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `empleados`
--

DROP TABLE IF EXISTS `empleados`;
CREATE TABLE IF NOT EXISTS `empleados` (
  `id` int NOT NULL AUTO_INCREMENT,
  `nombre` varchar(40) NOT NULL,
  `apellido` varchar(40) NOT NULL,
  `tipo_documento` varchar(40) NOT NULL,
  `documento` varchar(40) NOT NULL,
  `fecha_nacimiento` date NOT NULL,
  `area` varchar(50) NOT NULL,
  `cargo` varchar(50) NOT NULL,
  `eps` varchar(40) NOT NULL,
  `correo` varchar(60) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Volcado de datos para la tabla `empleados`
--

INSERT INTO `empleados` (`id`, `nombre`, `apellido`, `tipo_documento`, `documento`, `fecha_nacimiento`, `area`, `cargo`, `eps`, `correo`) VALUES
(3, 'Juan Pablo', 'Sanchez', 'Cédula ciudadanía', '7777777', '2023-11-01', 'RRHH', 'Jefe de RRHH', 'Sura', 'juanpablo@gmail.com'),
(4, 'Angelica', 'Ramirez', 'Cédula ciudadanía', '39157295', '2023-11-07', 'RRHH', 'Auxiliar', 'Sanitas', 'angelica@gmail.com'),
(5, 'Arnaldo', 'Sanmartin', 'Cédula ciudadanía', '70419102', '2023-11-20', 'Producción', 'Auxiliar', 'Sura', 'arnaldo@gmail.com'),
(6, 'Liliana Andrea', 'Sanmartin Ramirez', 'Cédula ciudadanía', '1017254069', '1998-01-02', 'RRHH', 'Coordinadora de Area', 'Sura', 'lilosanmartin2@gmail.com'),
(7, 'Yennifer', 'Barreneche', 'cedula ciudadania', '1023625484', '2005-02-01', 'Base datos', 'Administradora', 'Nueva eps', 'catalinab1205@gmail.com');
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
