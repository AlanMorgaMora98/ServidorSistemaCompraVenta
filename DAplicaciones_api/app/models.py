from . import db

class Usuario( db.Model ):
	clave_usuario = db.Column( db.Integer, primary_key=True, autoincrement=True )
	nombres = db.Column( db.String( 30 ), nullable=False )
	apellidos = db.Column( db.String( 50 ), nullable=False )
	nombre_usuario = db.Column( db.String( 50 ), nullable=False, unique=True )
	contrasena = db.Column( db.Text, nullable=False )
	correo_electronico = db.Column( db.String( 50 ), nullable=False )
	telefono = db.Column( db.String( 10 ) )
	tipo_usuario = db.Column( db.Integer )
	calificacion = db.Column( db.Float )

	@property
	def identity( self ):
		return self.clave_usuario

	@property
	def rolenames( self ):
		return []
	
	@property
	def password(self):
		return self.contrasena

	@classmethod
	def lookup( cls, username ):
		return cls.query.filter_by( nombre_usuario=username ).one_or_none()

	@classmethod
	def identify( cls, id ):
		return cls.query.filter_by( clave_usuario=id ).one_or_none()

	def __repr__( self ):
		return f"Usuario( nombres = { self.nombres }, apellidos = { self.apellidos }, nombre_usuario = { self.nombre_usuario }, contrasena = { self.contrasena }, correo_electronico = { self.correo_electronico }, telefono = { self.telefono }, tipo_usuario = { self.tipo_usuario }, calificacion = { self.calificacion } )"

class Publicacion( db.Model ):
	clave_publicacion = db.Column( db.Integer, primary_key=True, autoincrement=True )
	nombre = db.Column( db.String( 50 ), nullable=False )
	descripcion = db.Column( db.String( 200 ), nullable=False )
	categoria = db.Column( db.Integer, nullable=False )
	precio = db.Column( db.Float, nullable=False )
	cantidad_disponible = db.Column( db.Integer, nullable=False )
	calificacion_general = db.Column( db.Float )
	unidad_medida = db.Column( db.String( 100 ), nullable=False )
	numero_ventas = db.Column( db.Integer )
	imagen = db.Column( db.Text )  

	def __repr__( self ):
		return f"Publicacion( clave_publicacion = { self.clave_publicacion }, nombre = { self.nombre }, descripcion = { self.descripcion }, categoria = { self.categoria }, precio = { self.precio }, cantidad_disponible = { self.cantidad_disponible }, calificacion_general = { self.calificacion_general }, unidad_medida = { self.unidad_medida }, numero_ventas = { self.numero_ventas }, imagen = { self.imagen } )"

class Transaccion( db.Model ):
	clave_transaccion = db.Column( db.Integer, primary_key=True, autoincrement=True )
	clave_vendedor = db.Column( db.Integer, nullable=False )
	direccion_comprador = db.Column( db.String( 150 ) )
	fecha_venta = db.Column( db.Date )
	total = db.Column( db.Float, nullable=False )
	usuario_evaluado = db.Column( db.Boolean )

	def __repr__( self ):
		return f"Transaccion( clave_transaccion = { self.clave_transaccion }, clave_vendedor = { self.clave_vendedor }, direccion_comprador = { self.direccion_comprador }, fecha_venta = { self.fecha_venta }, total = { self.total }, usuario_evaluado = { self.usuario_evaluado } )"

class Reporte( db.Model ):
	folio = db.Column( db.Integer, primary_key=True, autoincrement=True )
	contenido = db.Column( db.String( 300 ), nullable=False )
	tipo_reporte = db.Column( db.Integer, nullable=False )
	fecha_reporte = db.Column( db.Date )

	def __repr__( self ):
		return f"Reporte( folio = { self.folio }, contenido = { self.contenido }, tipo_reporte = { self.tipo_reporte }, fecha_reporte = { self.fecha_reporte } )"

class Devolucion( db.Model ):
	clave_devolucion = db.Column( db.Integer, primary_key=True, autoincrement=True )
	descripcion_devolucion = db.Column( db.String( 200 ), nullable=False )
	fecha_devolucion = db.Column( db.Date )
	motivo = db.Column( db.Integer, nullable=False )
	clave_transaccion = db.Column( db.Integer, nullable=False )

	def __repr__( self ):
		return f"Devolucion( clave_devolucion = { self.clave_devolucion }, descripcion_devolucion = { self.descripcion_devolucion }, fecha_devolucion = { self.fecha_devolucion }, motivo = { self.motivo }, clave_transaccion = { self.clave_transaccion } )"

class Domicilio( db.Model ):
	discriminante_domicilio = db.Column( db.Integer, primary_key=True, autoincrement=True )
	clave_usuario = db.Column( db.Integer, primary_key=True )
	calle = db.Column( db.String( 25 ), nullable=False )
	colonia = db.Column( db.String( 30 ), nullable=False )
	municipio = db.Column( db.String( 30 ), nullable=False )
	codigo_postal = db.Column( db.String( 5 ), nullable=False )
	estado = db.Column( db.String( 20 ), nullable=False )
	numero_interno = db.Column( db.Integer, nullable=True )
	numero_externo = db.Column( db.Integer, nullable=True )
	descripcion = db.Column( db.String( 200 ), nullable=False )

	def __repr__( self ):
		return f"Domicilio( discriminante_domicilio = { self.discriminante_domicilio }, clave_usuario = { self.clave_usuario }, calle = { self.calle }, colonia = { self.colonia }, municipio = { self.municipio }, codigo_postal = { self.codigo_postal }, estado = { self.estado }, numero_interno = { self.numero_interno }, numero_externo = { self.numero_externo }, descripcion = { self.descripcion } )"

class Tarjeta( db.Model ):
	discriminante_tarjeta = db.Column( db.Integer, primary_key=True, autoincrement=True )
	clave_usuario = db.Column( db.Integer, nullable=False )
	nombre_tarjeta_habiente = db.Column( db.String( 80 ), nullable=False )
	numero = db.Column( db.String( 16 ), nullable=False )
	fecha_vencimiento = db.Column( db.Date, nullable=False )
	tipo_tarjeta = db.Column( db.Integer, nullable=False )

	def __repr__( self ):
		return f"Tarjeta( discriminante_tarjeta = { self.discriminante_tarjeta }, clave_usuario = { self.clave_usuario }, nombre_tarjeta_habiente = { self.nombre_tarjeta_habiente }, numero = { self.numero }, fecha_vencimiento = { self.fecha_vencimiento }, tipo_tarjeta = { self.tipo_tarjeta } )"

class Carrito( db.Model ):
	discriminante_carrito = db.Column( db.Integer, primary_key=True, autoincrement=True )
	clave_usuario_usuario = db.Column( db.Integer, nullable=False )

	def __repr__( self ):
		return f"Carrito( discriminante_carrito = { self.discriminante_carrito }, clave_usuario_usuario = { self.clave_usuario_usuario } )"

class ProductosCarrito( db.Model ):
	clave_registro = db.Column( db.Integer, primary_key=True, autoincrement=True )
	clave_producto_producto = db.Column( db.Integer, nullable=False )
	clave_usuario_usuario = db.Column( db.Integer, nullable=False )

	def __repr__( self ):
		return f"ProductosCarrito( clave_registro = { self.clave_registro }, clave_producto_producto = { self.clave_producto_producto }, clave_usuario_usuario = { self.clave_usuario_usuario } )"

class ProductosFavoritos( db.Model ):
	clave_registro = db.Column( db.Integer, primary_key=True, autoincrement=True )
	clave_usuario_usuario = db.Column( db.Integer, nullable=False )
	clave_producto_producto = db.Column( db.Integer, nullable=False )

	def __repr__( self ):
		return f"ProductosFavoritos( clave_registro = { self.clave_registro }, clave_usuario_usuario = { self.clave_usuario_usuario }, clave_producto_producto = { self.clave_producto_producto } )"

class EvaluacionUsuario( db.Model ):
	discriminante_evaluacion = db.Column( db.Integer, primary_key=True, autoincrement=True )
	clave_usuario = db.Column( db.Integer, nullable=False )
	clave_evaluador_de_usuario = db.Column( db.Integer, nullable=False )
	evaluacion = db.Column( db.String( 1000 ), nullable=False )
	calificacion = db.Column( db.Integer, nullable=False )

	def __repr__( self ):
		return f"EvaluacionUsuario( discriminante_evaluacion = { self.discriminante_evaluacion }, clave_usuario = { self.clave_usuario }, clave_evaluador_de_usuario = { self.clave_evaluador_de_usuario }, evaluacion = { self.evaluacion }, calificacion = { self.calificacion } )"

class ResenaProducto( db.Model ):
	discriminante_resena = db.Column( db.Integer, primary_key=True, autoincrement=True )
	clave_publicacion = db.Column( db.Integer, nullable=False )
	clave_evaluador_de_producto = db.Column( db.Integer, nullable=False )
	resena = db.Column( db.String( 200 ), nullable=False )
	calificacion = db.Column( db.Integer, nullable=False )

	def __repr__( self ):
		return f"ResenaProducto( discriminante_resena = { self.discriminante_resena }, clave_publicacion = { self.clave_publicacion }, clave_evaluador_de_producto = { self.clave_evaluador_de_producto }, resena = { self.resena }, calificacion = { self.calificacion } )"

class Pregunta( db.Model ):
	discriminante_pregunta = db.Column( db.Integer, primary_key=True, autoincrement=True )
	clave_publicacion_publicacion = db.Column( db.Integer, nullable=False )
	pregunta = db.Column( db.String( 100 ), nullable=False )
	respuesta = db.Column( db.String( 200 ), nullable=False )

	def __repr__( self ):
		return f"Pregunta( discriminante_pregunta = { self.discriminante_pregunta }, clave_publicacion_publicacion = { self.clave_publicacion_publicacion }, pregunta = { self.pregunta }, respuesta { self.respuesta } )"

class ListaProductos( db.Model ):
	registro_id = db.Column( db.Integer, primary_key=True, autoincrement=True )
	clave_transaccion = db.Column( db.Integer )
	producto = db.Column( db.Integer )

	def __repr__( self ):
		return f"ListaProductos( clave_transaccion = { self.clave_transaccion }, producto = { self.producto } )"

class UsuarioPublicacion( db.Model ):
	clave_publicacion_publicacion = db.Column( db.Integer, primary_key=True )
	clave_usuario_usuario = db.Column( db.Integer, primary_key=True )

	def __repr__( self ):
		return f"UsuarioPublicacion( clave_publicacion_publicacion = { self.clave_publicacion_publicacion }, clave_usuario_usuario = { self.clave_usuario_usuario } )"

class UsuarioTransaccion( db.Model ):
	clave_usuario_usuario = db.Column( db.Integer, primary_key=True )
	clave_transaccion_transaccion = db.Column( db.Integer, primary_key=True )

	def __repr__( self ):
		return f"UsuarioTransaccion( clave_usuario_usuario = { self.clave_usuario_usuario }, clave_transaccion_transaccion = { self.clave_transaccion_transaccion } )"

class UsuarioReporte( db.Model ):
	clave_usuario_usuario = db.Column( db.Integer, primary_key=True )
	folio_reporte = db.Column( db.Integer, primary_key=True )

	def __repr__( self ):
		return f"UsuarioReporte( clave_usuario_usuario = { self.clave_usuario_usuario }, folio_reporte = { self.folio_reporte } )"