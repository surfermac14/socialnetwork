from flask import render_template,redirect,flash,url_for,request
from . import main
from .forms import RegistrationForm,LoginForm
from .. import db
from ..models import User


@main.route('/')
def index():
    return render_template('index.html')

@main.route('/user/<name>')
def user(name):
	return render_template('user.html',name=name)

@main.route('/registration',methods=['GET','POST'])
def registration():
	form = RegistrationForm()
	user = User()
	if form.validate_on_submit() :
		user.fname = form.fname.data
		user.lname = form.lname.data
		user.email  = form.email.data
		user.password = form.password.data
		user.sex = form.sex.data
		
		mail=db.session.query(User).filter_by(email=user.email).first()
		
		if mail is None:
			db.session.add(user)
			db.session.commit()
			flash('Successfully registered. Please proceed to login page.')
			return redirect(url_for('.index'))
		else:
			flash('Email id already exists')
			return redirect(url_for('.registration'))
	return render_template('registration.html',form=form)


