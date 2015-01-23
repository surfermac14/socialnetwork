from flask import Flask,render_template,flash,redirect,url_for,request
from flask.ext.script import Manager
from flask.ext.bootstrap import Bootstrap
from flask.ext.wtf import Form
from wtforms import StringField, SubmitField,PasswordField,RadioField
from wtforms.validators import Required,Email
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.migrate import Migrate, MigrateCommand
import os

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config['SECRET_KEY'] = 'This is super strong secret key'
app.config['SQLALCHEMY_DATABASE_URI'] ='sqlite:///'+os.path.join(basedir,'data.sqlite')
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
manager = Manager(app)
bootstrap = Bootstrap(app)
db = SQLAlchemy(app)
migrate = Migrate(app,db)


# Models

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

		
#Form Classes
class RegistrationForm(Form):
	fname = StringField(u'First Name',validators =[Required()])
	lname = StringField(u'Last Name',validators=[Required()])
	email = StringField(u'Email Id',validators=[Required(),Email()])
	password = PasswordField(u'Password',validators=[Required()])
	sex = RadioField(u'Sex',choices=[('0','Male'),('1','Female')],validators=[Required()])
	submit = SubmitField(u'Register')
#Non Route functions
def make_shell_context():
	return dict(app=app,User=User)


manager.add_command('db',MigrateCommand)

#route functions
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/user/<name>')
def user(name):
	return render_template('user.html',name=name)

@app.route('/registration',methods=['GET','POST'])
def registration():
	form = RegistrationForm()
	user = User()
	if form.validate_on_submit() :
		user.fname = form.fname.data
		user.lname = form.lname.data
		user.email  = form.email.data
		user.password = form.password.data
		user.sex = form.sex.data
		db.session.add(user)
		db.session.commit()
		flash('Successfully registered. Please proceed to login page.')
		return redirect(url_for('index'))
	return render_template('registration.html',form=form)

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500
	
	

	


if __name__ == '__main__':
	manager.run()