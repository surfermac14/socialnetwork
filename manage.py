from flask import Flask,render_template,flash,redirect,url_for,request
from flask.ext.script import Manager
from flask.ext.bootstrap import Bootstrap
from flask.ext.wtf import Form
from wtforms import StringField, SubmitField,PasswordField,RadioField
from wtforms.validators import Required,Email

app = Flask(__name__)
app.config['SECRET_KEY'] = 'This is super strong secret key'
manager = Manager(app)
bootstrap = Bootstrap(app)

class RegistrationForm(Form):
	fname = StringField(u'First Name',validators =[Required()])
	lname = StringField(u'Last Name',validators=[Required()])
	email = StringField(u'Email Id',validators=[Required(),Email()])
	password = PasswordField(u'Password',validators=[Required()])
	sex = RadioField(u'Sex',choices=[('Male','Male'),('Female','Female')],validators=[Required()])
	submit = SubmitField(u'Register')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/user/<name>')
def user(name):
	return render_template('user.html',name=name)

@app.route('/registration',methods=['GET','POST'])
def registration():
	form = RegistrationForm()
	if form.validate_on_submit() :
		
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