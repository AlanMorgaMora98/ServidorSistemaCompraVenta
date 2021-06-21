import os
basedir = os.path.abspath( os.path.dirname( __file__ ) )

class Config:
	SECRET_KEY = os.environ.get( 'SECRET_KEY' ) or 'xA&87sdusaxhXIpx3a56hdsad'
	JWT_ACCESS_LIFESPAN = { "hours": 24 }
	JWT_REFRESH_LIFESPAN = { "days": 30 }
	SQLALCHEMY_TRACK_MODIFICATIONS = False

	@staticmethod
	def init_app( app ):
		pass

class DevelopmentConfig( Config ):
	DEBUG = True
	SQLALCHEMY_DATABASE_URI = os.environ.get( 'DEV_DATABASE_URL' ) or \
		"mysql://@localhost:3306/SistemaCompraVenta"

class TestingConfig():
	TESTING = True
	JWT_ACCESS_LIFESPAN = { "minutes": 1 }
	JWT_REFRESH_LIFESPAN = { "days": 0 }
	SQLALCHEMY_DATABASE_URI = os.environ.get( 'TEST_DATABASE_URL' ) or \
		"mysql://@localhost:3306/TestSistemaCompraVenta"

class ProductionConfig():
	SQLALCHEMY_DATABASE_URI = os.environ.get( 'DATABASE_URL' ) or \
		"mysql://@localhost:3306/SistemaCompraVenta"

config = {
	'development': DevelopmentConfig,
	'testing': TestingConfig,
	'production': ProductionConfig,

	'default': DevelopmentConfig
}