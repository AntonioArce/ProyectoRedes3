CREATE DATABASE IF NOT EXISTS administrador;
Use administrador;

CREATE TABLE IF NOT EXISTS Usuarios (
  id_usuario INT NOT NULL  AUTO_INCREMENT,
  nombre_usuario VARCHAR(20) NOT NULL,
  email VARCHAR(40) NOT NULL,
  contrasena VARCHAR(20) NOT NULL,
  is_admin TINYINT(1) NOT NULL,
  dispositivo VARCHAR(20) NULL, 
  PRIMARY KEY (id_usuario)
)
