import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
	SECRET_KEY = 'This is super strong secret key'
	#SQLALCHEMY_DATABASE_URI ='sqlite:///'+os.path.join(basedir,'data.sqlite')
	SQLALCHEMY_DATABASE_URI = 'postgresql://admin8znz69x:TM8F9ck_CGz4@$OPENSHIFT_POSTGRESQL_DB_HOST:$OPENSHIFT_POSTGRESQL_DB_PORT/mysn'
	#SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL'] or 'postgresql://postgres:miriyala@localhost/socialnetwork'
	#SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:password@localhost/socialnetwork'
	SQLALCHEMY_COMMIT_ON_TEARDOWN = True
	DEBUG = True

	def init_app(app):
		pass

config ={'default':Config() }
