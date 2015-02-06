import os
from app import create_app,db
from app.models import User
from flask.ext.script import Manager, Shell
from flask.ext.migrate import Migrate, MigrateCommand

app = create_app('default')


if __name__ == '__main__':
	app.run()