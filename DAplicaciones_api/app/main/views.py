from flask import jsonify
from flask_restful import Resource, reqparse, abort, fields, marshal_with
from flask_praetorian import auth_required
from . import main
from .. import db
from ..models import *
from ..extensions import guard

login_put_args = reqparse.RequestParser()
login_put_args.add_argument( "username", type=str, help="Se requiere un nombre de usuario", required=True )
login_put_args.add_argument( "password", type=str, help="Se requiere una contraseña", required=True )

usuario_put_args = reqparse.RequestParser()
usuario_put_args.add_argument( "nombres", type=str, help="Nombres son requeridos", required=True )
usuario_put_args.add_argument( "apellidos", type=str, help="Apellidos son requeridos", required=True )
usuario_put_args.add_argument( "nombre_usuario", type=str, help="Nombre de usuario es requerido", required=True )
usuario_put_args.add_argument( "contrasena", type=str, help="Contrasena es requerida", required=True )
usuario_put_args.add_argument( "correo_electronico", type=str, help="Correo es requerida", required=True )
usuario_put_args.add_argument( "telefono", type=str, help="Telefono es requerida", required=True )
usuario_put_args.add_argument( "tipo_usuario", type=int, help="El tipo de usuario es requerido", required=True )
usuario_put_args.add_argument( "calificacion", type=float, help="Calificacion es requerida", required=True )

publicacion_put_args = reqparse.RequestParser()
publicacion_put_args.add_argument( "nombre", type=str, help="Nombre es requerido", required=True )
publicacion_put_args.add_argument( "descripcion", type=str, help="La descripcion es requerida", required=True )
publicacion_put_args.add_argument( "categoria", type=int, help="La categoria es requerida", required=True )
publicacion_put_args.add_argument( "precio", type=float, help="El precio es requerido", required=True )
publicacion_put_args.add_argument( "cantidad_disponible", type=int, help="Se requiere la cantidad disponible", required=True )
publicacion_put_args.add_argument( "calificacion_general", type=float, help="Calificacion es requerido", required=True )
publicacion_put_args.add_argument( "unidad_medida", type=str, help="Se require la unidad de medida", required=True )
publicacion_put_args.add_argument( "numero_ventas", type=int, help="Cantidad ventas son requeridas", required=True )
publicacion_put_args.add_argument( "imagen", type=str, help="Imagen del producto es requerido", required=True )

transaccion_put_args = reqparse.RequestParser()
transaccion_put_args.add_argument( "clave_vendedor", type=int, help="Clave de vendedor es requerida", required=True )
transaccion_put_args.add_argument( "direccion_comprador", type=str, help="Direccion de comprador es requerida", required=True )
transaccion_put_args.add_argument( "fecha_venta", help="Fecha es requerida", required=True )
transaccion_put_args.add_argument( "total", type=float, help="Total de venta es requerida", required=True )
transaccion_put_args.add_argument( "usuario_evaluado", type=bool )
transaccion_put_args.add_argument( "claves_productos", type=int, action='append' )

reporte_put_args = reqparse.RequestParser()
reporte_put_args.add_argument( "clave_usuario", type=int, help="Clave del usuario es requerida", required=True )
reporte_put_args.add_argument( "contenido", type=str, help="Contenido de reporte es requerido", required=True )
reporte_put_args.add_argument( "tipo_reporte", type=int, help="Tipo de reporte es requerido", required=True )
reporte_put_args.add_argument( "fecha_reporte", help="Fecha de reporte es requerido", required=True )

devolucion_put_args = reqparse.RequestParser()
devolucion_put_args.add_argument( "descripcion_devolucion", type=str, help="Descripcion de devolucion es requerida", required=True )
devolucion_put_args.add_argument( "fecha_devolucion", help="Fecha de devolucion es requerida", required=True )
devolucion_put_args.add_argument( "motivo", type=int, help="Motivo de devolucion es requerido", required=True )
devolucion_put_args.add_argument( "clave_transaccion", type=int, help="Fecha de devolucion es requerido", required=True )

domicilio_put_args = reqparse.RequestParser()
domicilio_put_args.add_argument( "clave_usuario", type=int, help="clave de usuario es requerida", required=True )
domicilio_put_args.add_argument( "calle", type=str, help="Calle de domicilio es requerida", required=True )
domicilio_put_args.add_argument( "colonia", type=str, help="Colonia de domicilio es requerida", required=True )
domicilio_put_args.add_argument( "municipio", type=str, help="Municipio de domicilio es requerido", required=True )
domicilio_put_args.add_argument( "codigo_postal", type=str, help="Codigo postal de domicilio es requerido", required=True )
domicilio_put_args.add_argument( "estado", type=str, help="Estado de domicilio es requerido", required=True )
domicilio_put_args.add_argument( "numero_interno", type=int, help="Numero interno de domicilio es requerido", required=True )
domicilio_put_args.add_argument( "numero_externo", type=int, help="Numero externo de domicilio es requerido", required=True )
domicilio_put_args.add_argument( "descripcion", type=str, help="Descripcion de domicilio es requerida", required=True )

tarjeta_put_args = reqparse.RequestParser()
tarjeta_put_args.add_argument( "clave_usuario", type=int, help="Clave de usuario es requerida", required=True )
tarjeta_put_args.add_argument( "nombre_tarjeta_habiente", type=str, help="Nombre tarjeta habiente es requerida", required=True )
tarjeta_put_args.add_argument( "numero", type=str, help="Numero de tarjeta es requerido", required=True )
tarjeta_put_args.add_argument( "fecha_vencimiento", help="Fecha de vencimiento de tarjeta es requerida", required=True )
tarjeta_put_args.add_argument( "tipo_tarjeta", type=int, help="Tipo de tarjeta es requerida", required=True )

carrito_put_args = reqparse.RequestParser()
carrito_put_args.add_argument( "clave_usuario_usuario", type=int, help="Clave de usuario es requerida", required=True )

productos_carrito_put_args = reqparse.RequestParser()
productos_carrito_put_args.add_argument( "clave_usuario_usuario", type=int, help="Clave del usuario es requerida", required=True )
productos_carrito_put_args.add_argument( "clave_producto_producto", type=int, help="Clave de producto es requerido", required=True )

productos_favoritos_put_args = reqparse.RequestParser()
productos_favoritos_put_args.add_argument( "clave_usuario_usuario", type=int, help="Clave de usuario es requerida", required=True )
productos_favoritos_put_args.add_argument( "clave_producto_producto", type=int, help="Clave de producto es requerida", required=True )

evaluacion_usuario_put_args = reqparse.RequestParser()
evaluacion_usuario_put_args.add_argument( "clave_usuario", type=int, help="Clave de usuario es requerida", required=True )
evaluacion_usuario_put_args.add_argument( "clave_evaluador_de_usuario", type=int, help="Clave de evaluador es requerida", required=True )
evaluacion_usuario_put_args.add_argument( "evaluacion", type=str, help="Evaluacion es requerida", required=True )
evaluacion_usuario_put_args.add_argument( "calificacion", type=int, help="Calificacion es requerida", required=True )
evaluacion_usuario_put_args.add_argument( "clave_transaccion", type=int, help="Transaccion es requerida", required=True )

resena_put_args = reqparse.RequestParser()
resena_put_args.add_argument( "clave_publicacion", type=int, help="Clave de publicacion es requerida", required=True )
resena_put_args.add_argument( "clave_evaluador_de_producto", type=int, help="Clave de evaluador es requerida", required=True )
resena_put_args.add_argument( "resena", type=str, help="Resena de producto es requerida", required=True )
resena_put_args.add_argument( "calificacion", type=int, help="Calificacion de producto es requerida", required=True )

pregunta_put_args = reqparse.RequestParser()
pregunta_put_args.add_argument( "clave_publicacion_publicacion", type=int, help="Clave de publicacion es requerida", required=True )
pregunta_put_args.add_argument( "pregunta", type=str, help="Pregunta es requerida", required=True )
pregunta_put_args.add_argument( "respuesta", type=str, help="Respuesta es requerida", required=True )

usuario_fields = {
	'clave_usuario': fields.Integer,
	'nombres': fields.String,
	'apellidos': fields.String,
	'nombre_usuario': fields.String,
	'contrasena': fields.String,
	'correo_electronico': fields.String,
	'telefono': fields.String,
	'tipo_usuario': fields.Integer,
	'calificacion': fields.Float
}

publicacion_fields = {
	'clave_publicacion': fields.Integer,
	'nombre': fields.String,
	'descripcion': fields.String,
	'categoria': fields.Integer,
	'precio': fields.Float,
	'cantidad_disponible': fields.Integer,
	'calificacion_general': fields.Float,
	'unidad_medida': fields.String,
	'numero_ventas': fields.Integer,
	'imagen': fields.String
}

domicilio_fields = {
	'discriminante_domicilio': fields.Integer,
	'clave_usuario': fields.Integer,
	'calle': fields.String,
	'colonia': fields.String,
	'municipio': fields.String,
	'codigo_postal': fields.String,
	'estado': fields.String,
	'numero_interno': fields.Integer,
	'numero_externo': fields.Integer,
	'descripcion': fields.String
}

tarjeta_fields = {
	'discriminante_tarjeta': fields.Integer,
	'clave_usuario': fields.Integer,
	'nombre_tarjeta_habiente': fields.String,
	'numero': fields.String,
	'fecha_vencimiento': fields.String,
	'tipo_tarjeta': fields.Integer
}

carrito_fields = {
	'discriminante_carrito': fields.Integer,
	'clave_usuario_usuario': fields.Integer
}

transaccion_fields = {
	'clave_transaccion': fields.Integer,
	'clave_vendedor': fields.Integer,
	'direccion_comprador': fields.String,
	'fecha_venta': fields.String,
	'total': fields.Float,
	'usuario_evaluado': fields.Boolean
}

productos_carrito_fields = {
	'clave_usuario_usuario': fields.Integer,
	'clave_producto_producto': fields.Integer
}

favoritos_fields = {
	'clave_usuario_usuario': fields.Integer,
	'clave_producto_producto': fields.Integer
}

evaluacion_fields = {
	'discriminante_evaluacion': fields.Integer,
	'clave_usuario': fields.Integer,
	'clave_evaluador_de_usuario': fields.Integer,
	'evaluacion': fields.String,
	'calificacion': fields.Integer
}

reporte_fields = {
	'folio': fields.Integer,
	'contenido': fields.String,
	'tipo_reporte': fields.Integer,
	'fecha_reporte': fields.String
}

devolucion_fields = {
	'clave_devolucion': fields.Integer,
	'descripcion_devolucion': fields.String,
	'fecha_devolucion': fields.String,
	'motivo': fields.Integer,
	'clave_transaccion': fields.Integer
}

resena_fields = {
	'discriminante_resena': fields.Integer,
	'clave_publicacion': fields.Integer,
	'clave_evaluador_de_producto': fields.Integer,
	'resena': fields.String,
	'calificacion': fields.Integer
}

pregunta_fields = {
	'discriminante_pregunta': fields.Integer,
	'clave_publicacion_publicacion': fields.Integer,
	'pregunta': fields.String,
	'respuesta': fields.String
}

# Definicion de los recursos del API del SistemaCompraVenta

#Recurso que maneja inicio de sesiones
class Login( Resource ):
	def post( self ):
		args = login_put_args.parse_args()
		user = guard.authenticate( args[ 'username' ], args[ 'password' ] )
		token = guard.encode_jwt_token( user )
		return jsonify( { 'clave_usuario': user.clave_usuario, 'access_token': token } )

# Recursos para manejar métodos GET, POST, PUT, DELETE de usuario
class UsuarioGeneralResource( Resource ):
	@auth_required
	@marshal_with( usuario_fields )
	def get( self ):
		result = Usuario.query.all()
		return result, 200

	@marshal_with( usuario_fields )
	def post( self ):
		args = usuario_put_args.parse_args()
		usuario_existe = Usuario.query.filter_by( nombre_usuario=args[ 'nombre_usuario' ] ).one_or_none()
		if usuario_existe:
			abort( 409, message="Usuario ya existe." )

		usuario = Usuario( nombres=args[ 'nombres' ], apellidos=args[ 'apellidos' ], nombre_usuario=args[ 'nombre_usuario' ], contrasena=guard.hash_password( args[ 'contrasena' ] ), correo_electronico=args[ 'correo_electronico' ], telefono=args[ 'telefono' ], tipo_usuario=args[ 'tipo_usuario' ], calificacion=args[ 'calificacion' ] )
		db.session.add( usuario )
		db.session.commit()

		carrito = Carrito( clave_usuario_usuario=usuario.clave_usuario )
		db.session.add( carrito )
		db.session.commit()
		return usuario, 201

class UsuarioEspecificoResource( Resource ):
	@auth_required
	@marshal_with( usuario_fields )
	def get( self, clave_usuario ):
		result = Usuario.query.filter_by( clave_usuario=clave_usuario ).one_or_none()
		if not result:
			abort( 404, message="No se encontro el usuario especificado" )
		return result, 200

	@auth_required
	@marshal_with( usuario_fields )
	def put( self, clave_usuario ):
		args = usuario_put_args.parse_args()
		usuario = Usuario.query.filter_by( clave_usuario=clave_usuario ).one_or_none()
		if not usuario:
			abort( 404, message="No se encontro el usuario especificado" )

		usuario.nombres = args[ 'nombres' ]
		usuario.apellidos = args[ 'apellidos' ]
		usuario.nombre_usuario = args[ 'nombre_usuario' ]
		usuario.contrasena = args[ 'contrasena' ]
		usuario.correo_electronico = args[ 'correo_electronico' ]
		usuario.telefono = args[ 'telefono' ]
		usuario.tipo_usuario = args[ 'tipo_usuario' ]
		usuario.calificacion = args[ 'calificacion' ]
		db.session.commit()
		return usuario, 200

	@auth_required
	def delete( self, clave_usuario ):
		usuario = Usuario.query.filter_by( clave_usuario=clave_usuario ).first()
		if not usuario:
			abort( 404, message="No se encontro un usuario con esa clave" )

		db.session.delete( usuario )
		db.session.commit()	
		return {}, 200

class PublicacionGeneralResource( Resource ):
	@marshal_with( publicacion_fields )
	def get( self ):
		result = Publicacion.query.all()
		return result, 200

class PublicacionUsuarioResource( Resource ):
	@auth_required
	@marshal_with( publicacion_fields )
	def get( self, clave_usuario ):
		publicaciones = db.session.query( Publicacion ).join( UsuarioPublicacion, UsuarioPublicacion.clave_publicacion_publicacion==Publicacion.clave_publicacion ).filter( UsuarioPublicacion.clave_usuario_usuario==clave_usuario ).all()
		return publicaciones, 200

	@auth_required
	@marshal_with( publicacion_fields )
	def post( self, clave_usuario ):
		args = publicacion_put_args.parse_args()
		usuario = Usuario.query.filter_by( clave_usuario=clave_usuario ).one_or_none()
		if not usuario:
			abort( 404, message="No se encontro el usuario especificado" )
		publicacion = Publicacion( nombre=args[ 'nombre' ], descripcion=args[ 'descripcion' ], categoria=args[ 'categoria' ], precio=args[ 'precio' ], cantidad_disponible=args[ 'cantidad_disponible' ], calificacion_general=args[ 'calificacion_general' ], unidad_medida=args[ 'unidad_medida' ], numero_ventas=args[ 'numero_ventas' ], imagen=args[ 'imagen' ] )
		db.session.add( publicacion )
		db.session.commit()

		registro = UsuarioPublicacion( clave_publicacion_publicacion=publicacion.clave_publicacion, clave_usuario_usuario=clave_usuario )
		db.session.add( registro )
		db.session.commit()
		return publicacion, 201

class PublicacionEspecificaResource( Resource ):
	@marshal_with( publicacion_fields )
	def get( self, clave_publicacion ):
		result = Publicacion.query.filter_by( clave_publicacion=clave_publicacion ).one_or_none()
		if not result:
			abort( 404, message="No se encontro la publicacion especificada" )
		return result, 200

	@auth_required
	def put( self, clave_publicacion ):
		args = publicacion_put_args.parse_args()
		publicacion = Publicacion.query.filter_by( clave_publicacion=clave_publicacion ).one_or_more()
		if not publicacion:
			abort( 404, message="No se encontro la publicacion con la clave especificada" )

		publicacion.nombre = args[ 'nombre' ]
		publicacion.descripcion = args[ 'descripcion' ]
		publicacion.categoria = args[ 'categoria' ]
		publicacion.precio = args[ 'precio' ]
		publicacion.cantidad_disponible = args[ 'cantidad_disponible' ]
		publicacion.calificacion_general = args[ 'calificacion_general' ]
		publicacion.unidad_medida = args[ 'unidad_medida' ]
		publicacion.numero_ventas = args[ 'numero_ventas' ]
		publicacion.imagen = args[ 'imagen' ]
		db.session.commit()
		return {}, 200

	@auth_required
	def delete( self, clave_publicacion ):
		publicacion = Publicacion.query.filter_by( clave_publicacion=clave_publicacion ).first()
		if not publicacion:
			abort( 404, message="No se encontro la publicacion con la clave especificada" )

		registro = UsuarioPublicacion.query.filter_by( clave_publicacion_publicacion=clave_publicacion ).first()
		db.session.delete( registro )
		db.session.delete( publicacion )
		db.session.commit()
		return {}, 200

# Recursos para manejar métodos GET, POST, PUT, DELETE de domicilio
class DomicilioGeneralResource( Resource ):
	@auth_required
	@marshal_with( domicilio_fields )
	def get( self, clave_usuario ):
		usuario = Usuario.query.filter_by( clave_usuario=clave_usuario ).one_or_none()
		if not usuario:
			abort( 404, message="No se encontro un usuario con esa clave" )

		domicilios = Domicilio.query.filter_by( clave_usuario=clave_usuario ).all()
		if not domicilios:
			abort( 404, message="No hay domicilios que mostrar" )
		return domicilios, 200

	@auth_required
	@marshal_with( domicilio_fields )
	def post( self, clave_usuario ):
		usuario = Usuario.query.filter_by( clave_usuario=clave_usuario ).one_or_none()
		if not usuario:
			abort( 404, message="No se encontro un usuario con esa clave" )

		args = domicilio_put_args.parse_args()
		domicilio = Domicilio( clave_usuario=clave_usuario, calle=args[ 'calle' ], colonia=args[ 'colonia' ], municipio=args[ 'municipio' ], codigo_postal=args[ 'codigo_postal' ], estado=args[ 'estado' ], numero_interno=args[ 'numero_interno' ], numero_externo=args[ 'numero_externo' ], descripcion=args[ 'descripcion' ] )
		db.session.add( domicilio )
		db.session.commit()
		return domicilio, 201

class DomicilioEspecificoResource( Resource ):
	@auth_required
	@marshal_with( domicilio_fields )
	def get( self, clave_usuario, discriminante_domicilio ):
		usuario = Usuario.query.filter_by( clave_usuario=clave_usuario ).one_or_none()
		if not usuario:
			abort( 404, message="No se encontro un usuario con esa clave" )

		domicilios = Domicilio.query.filter_by( clave_usuario=clave_usuario ).all()
		domicilio_discriminado = None
		for domicilio in domicilios:
			if domicilio.discriminante_domicilio == discriminante_domicilio:
				domicilio_discriminado = domicilio

		if not domicilio_discriminado:
			abort( 404, message="No se encontro un domicilio con ese discriminante" )

		return domicilio_discriminado, 200

	@auth_required
	@marshal_with( domicilio_fields )
	def put( self, clave_usuario, discriminante_domicilio ):
		usuario = Usuario.query.filter_by( clave_usuario=clave_usuario ).one_or_none()
		if not usuario:
			abort( 404, message="No se encontro un usuario con esa clave" )

		domicilio = Domicilio.query.filter_by( clave_usuario=clave_usuario ).filter_by( discriminante_domicilio=discriminante_domicilio ).first()

		args = domicilio_put_args.parse_args()
		domicilio.clave_usuario = args[ 'clave_usuario' ]
		domicilio.calle = args[ 'calle' ]
		domicilio.colonia = args[ 'colonia' ]
		domicilio.municipio = args[ 'municipio' ]
		domicilio.codigo_postal = args[ 'codigo_postal' ]
		domicilio.estado = args[ 'estado' ]
		domicilio.numero_interno = args[ 'numero_interno' ]
		domicilio.numero_externo = args[ 'numero_externo' ]
		domicilio.descripcion = args[ 'descripcion' ]
		db.session.commit()
		return domicilio, 200

	@auth_required
	def delete( self, clave_usuario, discriminante_domicilio ):
		usuario = Usuario.query.filter_by( clave_usuario=clave_usuario ).one_or_none()
		if not usuario:
			abort( 404, message="No se encontro un usuario con esa clave" )

		domicilio = Domicilio.query.filter_by( clave_usuario=clave_usuario ).filter_by( discriminante_domicilio=discriminante_domicilio ).first()

		if not domicilio:
			abort( 404, message="No se encontro un domicilio con ese discriminante" )

		db.session.delete( domicilio )
		db.session.commit()
		return {}, 200

# Recursos para manejar métodos GET, POST, PUT, DELETE de tarjeta
class TarjetaGeneralResource( Resource ):
	@auth_required
	@marshal_with( tarjeta_fields )
	def get( self, clave_usuario ):
		usuario = Usuario.query.filter_by( clave_usuario=clave_usuario ).one_or_none()
		if not usuario:
			abort( 404, message="No se encontro un usuario con esa clave" )

		tarjetas = Tarjeta.query.filter_by( clave_usuario=clave_usuario ).all()
		if not tarjetas:
			abort( 404, message="No se encontraron tarjetas de este usuario" )
		return tarjetas, 200

	@auth_required
	def post( self, clave_usuario ):
		usuario = Usuario.query.filter_by( clave_usuario=clave_usuario ).one_or_none()
		if not usuario:
			abort( 404, message="No se encontro un usuario con esa clave" )

		args = tarjeta_put_args.parse_args()
		tarjeta = Tarjeta( clave_usuario=clave_usuario, nombre_tarjeta_habiente=args[ 'nombre_tarjeta_habiente' ], numero=args[ 'numero' ], fecha_vencimiento=args[ 'fecha_vencimiento' ], tipo_tarjeta=args[ 'tipo_tarjeta' ] )
		db.session.add( tarjeta )
		db.session.commit()
		return {}, 201

class TarjetaEspecificoResource( Resource ):
	@auth_required
	@marshal_with( tarjeta_fields )
	def get( self, clave_usuario, discriminante_tarjeta ):
		usuario = Usuario.query.filter_by( clave_usuario=clave_usuario ).one_or_none()
		if not usuario:
			abort( 404, message="No se encontro un usuario con esa clave" )

		tarjeta = Tarjeta.query.filter_by( clave_usuario=clave_usuario ).filter_by( discriminante_tarjeta=discriminante_tarjeta ).first()

		if not tarjeta:
			abort( 404, message="No se encontro la tarjeta especificada" )

		return tarjeta, 200

	@auth_required
	def put( self, clave_usuario, discriminante_tarjeta ):
		usuario = Usuario.query.filter_by( clave_usuario=clave_usuario ).one_or_none()
		if not usuario:
			abort( 404, message="No se encontro un usuario con esa clave" )

		tarjeta = Tarjeta.query.filter_by( clave_usuario=clave_usuario ).filter_by( discriminante_tarjeta=discriminante_tarjeta ).first()

		if not tarjeta:
			abort( 404, message="No se encontro la tarjeta especificada" )

		args = tarjeta_put_args.parse_args()
		tarjeta.clave_usuario = args[ 'clave_usuario' ]
		tarjeta.nombre_tarjeta_habiente = args[ 'nombre_tarjeta_habiente' ]
		tarjeta.numero = args[ 'numero' ]
		tarjeta.fecha_vencimiento = args[ 'fecha_vencimiento' ]
		tarjeta.tipo_tarjeta = args[ 'tipo_tarjeta' ]
		db.session.commit()
		return {}, 200

	@auth_required
	def delete( self, clave_usuario, discriminante_tarjeta ):
		usuario = Usuario.query.filter_by( clave_usuario=clave_usuario ).one_or_none()
		if not usuario:
			abort( 404, message="No se encontro un usuario con esa clave" )

		tarjeta = Tarjeta.query.filter_by( clave_usuario=clave_usuario ).filter_by( discriminante_tarjeta=discriminante_tarjeta ).first()

		if not tarjeta:
			abort( 404, message="No se encontro la tarjeta especificada" )

		db.session.delete( tarjeta )
		db.session.commit()
		return {}, 200

# Recursos para manejar métodos GET, POST, PUT, DELETE de carrito
class CarritoGeneralResource( Resource ):
	@auth_required
	@marshal_with( publicacion_fields )
	def get( self, clave_usuario ):
		usuario = Usuario.query.filter_by( clave_usuario=clave_usuario ).one_or_none()
		if not usuario:
			abort( 404, message="No se encontro un usuario con esa clave" )

		publicaciones = db.session.query( Publicacion ).join( ProductosCarrito, ProductosCarrito.clave_producto_producto==Publicacion.clave_publicacion ).filter( ProductosCarrito.clave_usuario_usuario==clave_usuario ).all()
		#publicaciones = Publicacion.query.join( ProductosCarrito, ProductosCarrito.clave_producto_producto==Publicacion.clave_publicacion ).filter_by( ProductosCarrito.clave_usuario_usuario==clave_usuario ).all()
		if not publicaciones:
			abort( 404, message="No hay productos en el carrito del usuario" )
		return publicaciones, 200

	@auth_required
	def post( self, clave_usuario ):
		usuario = Usuario.query.filter_by( clave_usuario=clave_usuario ).one_or_none()
		if not usuario:
			abort( 404, message="No se encontro un usuario con esa clave" )

		args = productos_carrito_put_args.parse_args()
		producto_carrito_existe = ProductosCarrito.query.filter_by( clave_usuario_usuario=clave_usuario ).filter_by( clave_producto_producto=args[ 'clave_producto_producto' ] ).first()
		if producto_carrito_existe:
			abort( 409, message="El producto ya se encuentra en el carrito del usuario" )  

		producto_carrito = ProductosCarrito( clave_producto_producto=args[ 'clave_producto_producto' ], clave_usuario_usuario=args[ 'clave_usuario_usuario' ] )
		db.session.add( producto_carrito )
		db.session.commit()
		return {}, 201

class CarritoEspecificoResource( Resource ):
	@auth_required
	@marshal_with( carrito_fields )
	def get( self, clave_usuario, clave_publicacion ):
		usuario = Usuario.query.filter_by( clave_usuario=clave_usuario ).one_or_none()
		if not usuario:
			abort( 404, message="No se encontro un usuario con esa clave" )

		carrito = Carrito.query.filter_by( clave_usuario_usuario=clave_usuario ).one_or_none()
		if not carrito:
			abort( 404, message="No se encontro un carrito para este usuario" )
		return carrito, 200

	@auth_required
	def delete( self, clave_usuario, clave_publicacion ):
		usuario = Usuario.query.filter_by( clave_usuario=clave_usuario ).one_or_none()
		if not usuario:
			abort( 404, message="No se encontro un usuario con esa clave" )

		publicacion = ProductosCarrito.query.filter_by( clave_usuario_usuario=clave_usuario ).filter_by( clave_producto_producto=clave_publicacion ).one_or_none()
		if not publicacion:
			abort( 404, message="No se encontro una publicacion con esa clave" )
		db.session.delete( publicacion )
		db.session.commit()
		return {}, 200

# Recursos para manejar métodos GET, POST, PUT, DELETE de favoritos
class FavoritoGeneralResource( Resource ):
	@auth_required
	@marshal_with( publicacion_fields )
	def get( self, clave_usuario ):
		usuario = Usuario.query.filter_by( clave_usuario=clave_usuario ).one_or_none()
		if not usuario:
			abort( 404, message="No se encontro el usuario especficado" )

		publicaciones = db.session.query( Publicacion ).join( ProductosFavoritos, ProductosFavoritos.clave_producto_producto==Publicacion.clave_publicacion ).filter( ProductosFavoritos.clave_usuario_usuario==clave_usuario ).all()
		if not publicaciones:
			abort( 404, message="No hay productos en el carrito del usuario" )
		return publicaciones, 200

	@auth_required
	def post( self, clave_usuario ):
		usuario = Usuario.query.filter_by( clave_usuario=clave_usuario ).one_or_none()
		if not usuario:
			abort( 404, message="No se encontro un usuario con esa clave" )
			
		args = productos_favoritos_put_args.parse_args()
		favorito_existe = ProductosFavoritos.query.filter_by( clave_usuario_usuario=clave_usuario ).filter_by( clave_producto_producto=args[ 'clave_producto_producto' ] ).first()
		if favorito_existe:
			abort( 409, message="El favorito ya existe" )

		favorito = ProductosFavoritos( clave_usuario_usuario=clave_usuario, clave_producto_producto=args[ 'clave_producto_producto' ] )
		db.session.add( favorito )
		db.session.commit()
		return {}, 201

class FavoritoEspecificoResource( Resource ):
	@auth_required
	def delete( self, clave_usuario, clave_publicacion ):
		usuario = Usuario.query.filter_by( clave_usuario=clave_usuario ).one_or_none()
		if not usuario:
			abort( 404, message="No se encontro el usuario especificado" )

		favorito = ProductosFavoritos.query.filter_by( clave_usuario_usuario=clave_usuario ).filter_by( clave_producto_producto=clave_publicacion ).first()

		if not favorito:
			abort( 404, message="No se encontro el favorito especificado" )

		db.session.delete( favorito )
		db.session.commit()
		return {}, 200

# Recursos para manejar métodos GET, POST, PUT, DELETE de evaluaciones
class EvaluacionGeneralResource( Resource ):
	@marshal_with( evaluacion_fields )
	def get( self, clave_usuario ):
		usuario = Usuario.query.filter_by( clave_usuario=clave_usuario ).one_or_none()
		if not usuario:
			abort( 404, message="No se encontro el usuario especficado" )

		evaluaciones = EvaluacionUsuario.query.filter_by( clave_usuario=clave_usuario ).all()
		if not evaluaciones:
			abort( 404, message="No hay evaluaciones para este usuario" )
		return evaluaciones, 200

	@auth_required
	def post( self, clave_usuario ):
		usuario = Usuario.query.filter_by( clave_usuario=clave_usuario ).one_or_none()
		if not usuario:
			abort( 404, message="No se encontro el usuario especficado" )

		args = evaluacion_usuario_put_args.parse_args()
		evaluacion = EvaluacionUsuario( clave_usuario=args[ 'clave_usuario' ], clave_evaluador_de_usuario=args[ 'clave_evaluador_de_usuario' ], evaluacion=args[ 'evaluacion' ], calificacion=args[ 'calificacion' ] )
		db.session.add( evaluacion )

		transaccion = Transaccion.query.filter_by( clave_transaccion=args[ 'clave_transaccion' ] ).one_or_none()
		transaccion.usuario_evaluado = True
		db.session.commit()
		return {}, 201

class EvaluacionEspecificoResource( Resource ):
	@marshal_with( evaluacion_fields )
	def get( self, clave_usuario, discriminante_evaluacion ):
		usuario = Usuario.query.filter_by( clave_usuario=clave_usuario ).one_or_none()
		if not usuario:
			abort( 404, message="No se encontro el usuario especficado" )

		evaluacion = EvaluacionUsuario.query.filter_by( clave_usuario=clave_usuario ).filter_by( discriminante_evaluacion=discriminante_evaluacion ).one_or_none()
		if not evaluacion:
			abort( 404, message="No hay evaluaciones para este usuario" )
		return evaluacion, 200

# Recursos para manejar métodos GET, POST, PUT, DELETE de transacción
class TransaccionGeneralResource( Resource ):
	@auth_required
	@marshal_with( transaccion_fields )
	def get( self, clave_usuario ):
		usuario = Usuario.query.filter_by( clave_usuario=clave_usuario ).one_or_none()
		if not usuario:
			abort( 404, message="No se encontro un usuario con la clave especificada." )

		transacciones = db.session.query( Transaccion ).join( UsuarioTransaccion, UsuarioTransaccion.clave_transaccion_transaccion==Transaccion.clave_transaccion ).filter( UsuarioTransaccion.clave_usuario_usuario==clave_usuario ).all()
		if not transacciones:
			abort( 404, message="No se encontraron transacciones" )

		return transacciones, 200

	@auth_required
	def post( self, clave_usuario ):
		args = transaccion_put_args.parse_args()
		usuario = Usuario.query.filter_by( clave_usuario=clave_usuario ).one_or_none()
		if not usuario:
			abort( 404, message="La clave del comprador debe ser de un usuario existente" )

		usuario = Usuario.query.filter_by( clave_usuario=args[ 'clave_vendedor' ] ).one_or_none()
		if not usuario:
			abort( 404, message="La clave del vendedor debe ser de un usuario existente" )

		transaccion = Transaccion( clave_vendedor=args[ 'clave_vendedor' ], direccion_comprador=args[ 'direccion_comprador' ], fecha_venta=args[ 'fecha_venta' ], total=args[ 'total' ], usuario_evaluado=args[ 'usuario_evaluado' ] )
		db.session.add( transaccion )
		db.session.commit()

		registro = UsuarioTransaccion( clave_usuario_usuario=clave_usuario, clave_transaccion_transaccion=transaccion.clave_transaccion )
		db.session.add( registro )

		for producto in args[ 'claves_productos' ]:
			lista_producto = ListaProductos( clave_transaccion=transaccion.clave_transaccion, producto=producto )
			db.session.add( lista_producto )
			productoConMenosCantidad = Publicacion.query.filter_by( clave_publicacion=producto ).one_or_none()
			productoConMenosCantidad.cantidad_disponible = productoConMenosCantidad.cantidad_disponible - 1

			productoCarrito = ProductosCarrito.query.filter_by( clave_usuario_usuario=clave_usuario ).filter_by( clave_producto_producto=producto ).one_or_none()
			db.session.delete( productoCarrito )
		db.session.commit()
		return {}, 201

class TransaccionEspecificoResource( Resource ):
	@auth_required
	@marshal_with( transaccion_fields )
	def get( self, clave_usuario, clave_transaccion ):
		transaccion = Transaccion.query.join( UsuarioTransaccion, UsuarioTransaccion.clave_transaccion_transaccion==Transaccion.clave_transaccion ).filter_by( clave_usuario_usuario=clave_usuario ).filter_by( clave_transaccion_transaccion=clave_transaccion ).one_or_none()
		if not transaccion:
			abort( 404, message="No se encontro la transaccion especificada" )
		return transaccion, 200

	@auth_required
	def delete( self, clave_usuario, clave_transaccion ):
		transaccion = Transaccion.query.filter_by( clave_transaccion=clave_transaccion ).one_or_none()
		if not transaccion:
			abort( 404, message="No se encontro la transaccion especificada" )

		registro = UsuarioTransaccion.query.filter_by( clave_usuario_usuario=clave_usuario ).filter_by( clave_transaccion_transaccion=transaccion.clave_transaccion ).one_or_none()

		productos = ListaProductos.query.filter_by( clave_transaccion=transaccion.clave_transaccion ).all()

		db.session.delete( transaccion )
		db.session.delete( registro )
		for producto in productos:
			db.session.delete( producto )
		db.session.commit()
		return {}, 200

# Recursos para manejar métodos GET, POST, PUT, DELETE de reporte
class ReporteGeneralResource( Resource ):
	@auth_required
	@marshal_with( reporte_fields )
	def get( self ):
		reportes = Reporte.query.all()
		if not reportes:
			abort( 404, message="No se encontraron reportes registrados" )
		return reportes, 200

	@auth_required
	def post( self ):
		args = reporte_put_args.parse_args()
		reporte = Reporte( contenido=args[ 'contenido' ], tipo_reporte=args[ 'tipo_reporte' ], fecha_reporte=args[ 'fecha_reporte' ] )
		db.session.add( reporte )
		db.session.commit()
		registro = UsuarioReporte( clave_usuario_usuario=args[ 'clave_usuario' ], folio_reporte=reporte.folio )
		db.session.add( registro )
		db.session.commit()
		return {}, 201

class ReporteEspecificoResource( Resource ):
	@auth_required
	@marshal_with( reporte_fields )
	def get( self, clave_usuario, folio ):
		reporte = Reporte.query.join( UsuarioReporte, UsuarioReporte.folio_reporte==Reporte.folio ).filter_by( folio_reporte=folio ).one_or_none()
		if not reporte:
			abort( 404, message="No se encontro el reporte especificado" )
		return reporte, 200

	@auth_required
	def put( self, clave_usuario, folio ):
		reporte = Reporte.query.join( UsuarioReporte, UsuarioReporte.folio_reporte==Reporte.folio ).filter_by( folio_reporte=folio ).one_or_none()
		if not reporte:
			abort( 404, message="No se encontro el reporte especificado" )
		args = reporte_put_args.parse_args()
		reporte.contenido = args[ 'contenido' ]
		reporte.tipo_reporte = args[ 'tipo_reporte' ]
		reporte.fecha_reporte = args[ 'fecha_reporte' ]
		db.session.commit()
		return {}, 200

	@auth_required
	def delete( self, clave_usuario, folio ):
		reporte = Reporte.query.filter_by( folio=folio ).one_or_none()
		if not reporte:
			abort( 404, message="No se encontro el reporte especificado" )
		registro = UsuarioReporte.query.filter_by( folio_reporte=folio ).one_or_none()
		db.session.delete( reporte )
		db.session.delete( registro )
		db.session.commit()
		return {}, 200

# Recursos para manejar métodos GET, POST, PUT, DELETE de devoluciones
class DevolucionGeneralResource( Resource ):
	@auth_required
	@marshal_with( devolucion_fields )
	def get( self ):
		devoluciones = Devolucion.query.all()
		if not devoluciones:
			abort( 404, message="No se encontraron devoluciones" )
		return devoluciones, 200

	@auth_required
	def post( self ):
		args = devolucion_put_args.parse_args()
		devolucion = Devolucion( descripcion_devolucion=args[ 'descripcion_devolucion' ], fecha_devolucion=args[ 'fecha_devolucion' ], motivo=args[ 'motivo' ], clave_transaccion=args[ 'clave_transaccion' ] )
		db.session.add( devolucion )
		db.session.commit()
		return {}, 201

class DevolucionEspecificoResource( Resource ):
	@auth_required
	@marshal_with( devolucion_fields )
	def get( self, clave_devolucion ):
		devolucion = Devolucion.query.filter_by( clave_devolucion=clave_devolucion ).one_or_none()
		if not devolucion:
			abort( 404, message="No se encontro la devolucion especificada" )
		return devolucion, 200

# Recursos para manejar métodos GET, POST, PUT, DELETE de reseña
class ResenaGeneralResource( Resource ):
	@marshal_with( resena_fields )
	def get( self, clave_publicacion ):
		publicacion = Publicacion.query.filter_by( clave_publicacion=clave_publicacion ).one_or_none()
		if not publicacion:
			abort( 404, message="No se encontro una publicacion con esa clave de publicacion" )

		resenas = ResenaProducto.query.filter_by( clave_publicacion=clave_publicacion ).all()
		if not resenas:
			abort( 404, message="No se encontraron resenas para esta publicacion" )
		return resenas, 200

	def post( self, clave_publicacion ):
		publicacion = Publicacion.query.filter_by( clave_publicacion=clave_publicacion )
		if not publicacion:
			abort( 404, message="No se encontro una publicacion con esa clave de publicacion" )

		args = resena_put_args.parse_args()
		resena = ResenaProducto( clave_publicacion=args[ 'clave_publicacion' ], clave_evaluador_de_producto=args[ 'clave_evaluador_de_producto' ], resena=args[ 'resena' ], calificacion=args[ 'calificacion' ] )
		db.session.add( resena )
		db.session.commit()
		return {}, 201

class ResenaEspecificoResource( Resource ):
	@marshal_with( resena_fields )
	def get( self, clave_publicacion, discriminante_resena ):
		publicacion = Publicacion.query.filter_by( clave_publicacion=clave_publicacion ).one_or_none()
		if not publicacion:
			abort( 404, message="No se encontro una publicacion con esa clave de publicacion" )
		resena = ResenaProducto.query.filter_by( discriminante_resena=discriminante_resena ).first()
		if not resena:
			abort( 404, message="No se encontro la resena especificada" )
		return resena, 200

# Recursos para manejar métodos GET, POST, PUT, DELETE de preguntas
class PreguntaGeneralResource( Resource ):
	@marshal_with( pregunta_fields )
	def get( self, clave_publicacion ):
		publicacion = Publicacion.query.filter_by( clave_publicacion=clave_publicacion ).one_or_none()
		if not publicacion:
			abort( 404, message="No se encontro una publicacion con esa clave de publicacion" )

		preguntas = Pregunta.query.filter_by( clave_publicacion_publicacion=clave_publicacion ).all()
		if not preguntas:
			abort( 404, message="No se encontraron preguntas con esa clave de publicacion" )
		return preguntas, 200

	@marshal_with( pregunta_fields )
	def post( self, clave_publicacion ):
		publicacion = Publicacion.query.filter_by( clave_publicacion=clave_publicacion ).one_or_none()
		if not publicacion:
			abort( 404, message="No se encontro una publicacion con esa clave de publicacion" )

		args = pregunta_put_args.parse_args()
		pregunta = Pregunta( clave_publicacion_publicacion=args[ 'clave_publicacion_publicacion' ], pregunta=args[ 'pregunta' ], respuesta=args[ 'respuesta' ] )
		db.session.add( pregunta )
		db.session.commit()
		return pregunta, 201

class PreguntaEspecificaResource( Resource ):
	@marshal_with( pregunta_fields )
	def get( self, clave_publicacion, discriminante_pregunta ):
		publicacion = Publicacion.query.filter_by( clave_publicacion=clave_publicacion ).one_or_none()
		if not publicacion:
			abort( 404, message="No se encontro una publicacion con esa clave de publicacion" )

		pregunta = Pregunta.query.filter_by( discriminante_pregunta=discriminante_pregunta ).first()
		if not pregunta:
			abort( 404, message="No se encontro la pregunta especificada" )
		return pregunta, 200

	def put( self, clave_publicacion, discriminante_pregunta ):
		publicacion = Publicacion.query.filter_by( clave_publicacion=clave_publicacion ).one_or_none()
		if not publicacion:
			abort( 404, message="No se encontro una publicacion con esa clave de publicacion" )
		pregunta = Pregunta.query.filter_by( discriminante_pregunta=discriminante_pregunta ).first()
		if not pregunta:
			abort( 404, message="No se encontro la pregunta especificada" )
		args = pregunta_put_args.parse_args()
		pregunta.pregunta = args[ 'pregunta' ]
		pregunta.respuesta = args[ 'respuesta' ]
		db.session.commit()
		return {}, 200	