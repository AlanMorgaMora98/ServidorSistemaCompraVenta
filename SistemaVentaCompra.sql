CREATE DATABASE SistemaCompraVenta;
USE SistemaCompraVenta;
DROP DATABASE SistemaCompraVenta;
SELECT @@global.time_zone;
SET @@global.time_zone = '+00:00';

CREATE TABLE Usuario(
	claveUsuario int auto_increment,
    nombres varchar( 30 ),
    apellidos varchar( 50 ),
    nombreUsuario varchar( 50 ) unique,
    contrasena Text,
    correoElectronico varchar( 50 ),
    telefono varchar( 10 ),
    tipoUsuario int,
    calificacion float,
    PRIMARY KEY( claveusuario )
);

CREATE TABLE Publicacion(
	clavePublicacion int auto_increment,
    nombre varchar( 50 ),
    descripcion varchar( 200 ),
    categoria int,
    precio float,
    cantidadDisponible int,
    calificacionGeneral float,
    unidadMedida int,
    numeroVentas int,
    PRIMARY KEY( clavePublicacion )
);

CREATE TABLE Transaccion(
	claveTransaccion int auto_increment,
    claveVendedor int,
    direccionComprador varchar( 150 ),
    fechaVenta date,
    total float,
    usuario_evaluado bool,
    PRIMARY KEY( claveTransaccion )	
);

CREATE TABLE Devolucion(
	claveDevolucion int auto_increment,
    descripcionDevolucion varchar( 200 ),
    fechaDevolucion date,
    motivo int,
    claveTransaccion int,
    PRIMARY KEY( claveDevolucion ),
    FOREIGN KEY( claveTransaccion ) REFERENCES Transaccion( claveTransaccion )
);

CREATE TABLE Reporte(
	folio int auto_increment,
    contenido varchar( 300 ),
    tipoReporte int, 
    fechaReporte date,
    PRIMARY KEY( folio )
);

CREATE TABLE Domicilio(
	discriminanteDomicilio int auto_increment,
    claveUsuario int,
    calle varchar( 25 ),
    colonia varchar( 30 ),
    municipio varchar( 30 ),
    codigoPostal varchar( 5 ),
    estado varchar( 20 ),
    numeroInterno int,
    numeroExterno int,
    descripcion varchar( 200 ),
    PRIMARY KEY( discriminanteDomicilio, claveUsuario ),
    FOREIGN KEY( claveUsuario ) REFERENCES Usuario( claveUsuario )
);

CREATE TABLE Tarjeta(
	discriminanteTarjeta int auto_increment,
    claveUsuario int,
    nombreTarjetaHabiente varchar( 80 ),
    numero varchar( 16 ),
    fechaVencimiento date,
    tipoTarjeta int,
    PRIMARY KEY( discriminanteTarjeta, claveUsuario ),
    FOREIGN KEY( claveUsuario ) REFERENCES Usuario( claveUsuario )
);

CREATE TABLE Carrito(
	discriminanteCarrito int auto_increment,
    claveUsuario_Usuario int,
    PRIMARY KEY( discriminanteCarrito ),
    FOREIGN KEY( claveUsuario_Usuario ) REFERENCES Usuario( claveUsuario )
);

CREATE TABLE ProductosCarritos(
	claveProducto_Producto int,
    discriminanteCarrito int,
    PRIMARY KEY( claveProducto_Producto, discriminanteCarrito )
);

CREATE TABLE ProductosFavoritos(
	claveUsuario_Usuario int,
    claveProducto_Producto int,
    PRIMARY KEY( claveUsuario_Usuario, claveProducto_Producto ) 
);

CREATE TABLE EvaluacionUsuario(
	discriminanteEvaluacion int auto_increment,
    claveUsuario int,
    claveEvaluadorDeUsuario int,
    evaluacion varchar( 200 ),
    calificacion int,
    PRIMARY KEY( discriminanteEvaluacion, claveUsuario ),
    FOREIGN KEY( claveUsuario ) REFERENCES Usuario( claveUsuario )
);

CREATE TABLE ResenaProducto(
	discriminanteResena int auto_increment,
    clavePublicacion int,
    claveEvaluadorDeProducto int,
    resena varchar( 200 ),
    calificacion int,
    PRIMARY KEY( discriminanteResena, clavePublicacion ),
    FOREIGN KEY( clavePublicacion ) REFERENCES Publicacion( clavePublicacion )
);

CREATE TABLE Pregunta(
	discriminantePregunta int auto_increment,
    clavePublicacion_Publicacion int,
    pregunta varchar( 100 ),
    respuesta varchar( 200 ),
    PRIMARY KEY( discriminantePregunta, clavePublicacion_Publicacion ),
    FOREIGN KEY( clavePublicacion_Publicacion ) REFERENCES Publicacion( clavePublicacion )
);

CREATE TABLE Multimedia(
	discriminanteMultimedia int auto_increment,
    clavePublicacion int,
    imageFile mediumblob,
    PRIMARY KEY( discriminanteMultimedia, clavePublicacion ),
    FOREIGN KEY( clavePublicacion ) REFERENCES Publicacion( clavePublicacion )
);

CREATE TABLE ListaProductos(
	claveTransaccion int,
    producto int,
    PRIMARY KEY( claveTransaccion, producto ),
    FOREIGN KEY( claveTransaccion ) REFERENCES Transaccion( claveTransaccion )
);

CREATE TABLE UsuarioPublicacion(
	clavePublicacion_Publicacion int,
    claveUsuario_Usuario int,
    PRIMARY KEY( clavePublicacion_Publicacion, claveUsuario_Usuario ),
    FOREIGN KEY( clavePublicacion_Publicacion ) REFERENCES Publicacion( clavePublicacion ),
    FOREIGN KEY( claveUsuario_Usuario ) REFERENCES Usuario( claveUsuario )
);

CREATE TABLE UsuarioTransaccion(
	claveUsuario_Usuario int,
    claveTransaccion_Transaccion int,
    PRIMARY KEY( claveUsuario_Usuario, claveTransaccion_Transaccion ),
    FOREIGN KEY( claveUsuario_Usuario ) REFERENCES Usuario( claveUsuario ),
    FOREIGN KEY( claveTransaccion_Transaccion ) REFERENCES Transaccion( claveTransaccion )
);

CREATE TABLE UsuarioReporte(
	claveUsuario_Usuario int,
    folio_Reporte int,
    PRIMARY KEY( claveUsuario_Usuario, folio_Reporte )
);