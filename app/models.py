from app import db
from flask.ext.sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

class User(db.Model):
	__tablename__ = 'users'
	id = db.Column(db.Integer, primary_key= True)
	fname = db.Column(db.String(30),nullable=False)
	lname = db.Column(db.String(30),nullable=False)
	email = db.Column(db.String(50),unique=True,nullable=False)
	password=db.Column(db.String(50))
	#passwordhash = db.Column(db.String(128))
	sex = db.Column(db.Boolean(),nullable=False)

	'''@property
	def password(self):
	    raise AttributeError('password is not a readable attribute')
	@password.setter
	def password(self, password):
	    self.password_hash = generate_password_hash(password)
	def verify_password(self,password):
		return check_password_hash(self.passwordhash,password)
	def __repr__(self):
		return '<User %r' % self.fname'''

class FriendRequest(db.Model):
	__tablename__ = 'friendRequest'
	id=db.Column(db.Integer,primary_key=True)
	senderName = db.Column(db.String(50),nullable=False)
	receiverName = db.Column(db.String(50),nullable=False)

class Friends(db.Model):
	__tablename__ = 'friends'
	id=db.Column(db.Integer,primary_key=True)
	senderName = db.Column(db.String(50),nullable=False)
	receiverName = db.Column(db.String(50),nullable=False)

class Message(db.Model):
	__tablename__= 'messages'
	id=db.Column(db.Integer,primary_key=True)
	senderName = db.Column(db.String(50),nullable=False)
	receiverName = db.Column(db.String(50),nullable=False)
	message = db.Column(db.String(500),nullable=False)