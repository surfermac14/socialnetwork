from app import db
from flask.ext.sqlalchemy import SQLAlchemy

class User(db.Model):
	__tablename__ = 'users'
	id = db.Column(db.Integer, primary_key= True)
	fname = db.Column(db.String(30),nullable=False)
	lname = db.Column(db.String(30),nullable=False)
	email = db.Column(db.String(50),unique=True,nullable=False)
	password = db.Column(db.String(50),nullable=False)
	sex = db.Column(db.Boolean(),nullable=False)
	
	def __repr__(self):
		return '<User %r' % self.fname
