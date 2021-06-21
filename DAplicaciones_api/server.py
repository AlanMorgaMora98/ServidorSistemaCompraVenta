import os
from flask_restful import Api
from app.main.views import *
from app import create_app, db

app =create_app( os.getenv( 'Flask_CONFIG' ) or 'default' )

api = Api( app )

api.add_resource( Login, "/login" )

api.add_resource( UsuarioGeneralResource, "/usuarios" )
api.add_resource( UsuarioEspecificoResource, "/usuarios/<int:clave_usuario>" )

api.add_resource( PublicacionGeneralResource, "/publicaciones" )
api.add_resource( PublicacionUsuarioResource, "/publicaciones/<int:clave_usuario>" )
api.add_resource( PublicacionEspecificaResource, "/publicaciones/<int:clave_publicacion>" )

api.add_resource( DomicilioGeneralResource, "/usuarios/<int:clave_usuario>/domicilios" )
api.add_resource( DomicilioEspecificoResource, "/usuarios/<int:clave_usuario>/domicilios/<int:discriminante_domicilio>" )

api.add_resource( TarjetaGeneralResource, "/usuarios/<int:clave_usuario>/tarjetas" )
api.add_resource( TarjetaEspecificoResource, "/usuarios/<int:clave_usuario>/tarjetas/<int:discriminante_tarjeta>" )

api.add_resource( CarritoGeneralResource, "/usuarios/<int:clave_usuario>/carritos" )
api.add_resource( CarritoEspecificoResource, "/usuarios/<int:clave_usuario>/carritos/<int:clave_publicacion>" )

api.add_resource( FavoritoGeneralResource, "/usuarios/<int:clave_usuario>/favoritos" )
api.add_resource( FavoritoEspecificoResource, "/usuarios/<int:clave_usuario>/favoritos/<int:clave_publicacion>" )

api.add_resource( EvaluacionGeneralResource, "/usuarios/<int:clave_usuario>/evaluaciones" )
api.add_resource( EvaluacionEspecificoResource, "/usuarios/<int:clave_usuario>/evaluaciones/<int:discriminante_evaluacion>" )

api.add_resource( TransaccionGeneralResource, "/transacciones/<int:clave_usuario>" )
api.add_resource( TransaccionEspecificoResource, "/transacciones/<int:clave_usuario>/<int:clave_transaccion>" )

api.add_resource( ReporteGeneralResource, "/reportes" )
api.add_resource( ReporteEspecificoResource, "/reportes/<int:clave_usuario>/<int:folio>" )

api.add_resource( DevolucionGeneralResource, "/devoluciones" )
api.add_resource( DevolucionEspecificoResource, "/devoluciones/<int:clave_devolucion>" )

api.add_resource( ResenaGeneralResource, "/publicaciones/<int:clave_publicacion>/resenas" )
api.add_resource( ResenaEspecificoResource, "/publicaciones/<int:clave_publicacion>/resenas/<int:discriminante_resena>" )

api.add_resource( PreguntaGeneralResource, "/publicaciones/<int:clave_publicacion>/preguntas" )
api.add_resource( PreguntaEspecificaResource, "/publicaciones/<int:clave_publicacion>/preguntas/<int:discriminante_pregunta>" )

app.app_context().push()
db.create_all()

if __name__ == "__main__":
	app.run( debug=True, host='0.0.0.0' )