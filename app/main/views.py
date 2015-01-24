from flask import render_template,redirect,flash,url_for,request,session
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
	if 'email' in session :
		user = User.query.filter_by(email=session['email']).first()
		return render_template('userprofile.html',user=user)
	form = RegistrationForm()
	user = User()
	if form.validate_on_submit() :

		possibleuser=db.session.query(User).filter_by(email=form.email.data).first()
		u = User(fname = form.fname.data,lname=form.lname.data,email=form.email.data,password=form.password.data,sex=form.sex.data)
		print(u.fname)
		if possibleuser is None:
			db.session.add(u)
			db.session.commit()
			flash('Successfully registered. Please proceed to login page.')
			return redirect(url_for('.index'))
		else:
			flash('Email id already exists')
			return redirect(url_for('.registration'))
	return render_template('registration.html',form=form)

@main.route('/login',methods=['GET','POST'])
def login():
	if 'email' in session :
		user = User.query.filter_by(email=session['email']).first()
		return render_template('userprofile.html',user=user)
		
	if request.method == 'GET':
		return render_template('login.html')
	email = request.form['email']
	password = request.form['password']
	user = User.query.filter_by(email=email,password=password).first()
	if user is None :#or not user.verify_password(password):
		flash("Wrong Email or password")
		return redirect(url_for('.login'))
	session['email'] = user.email

	return redirect(url_for('.profile'))

@main.route('/profile',methods=['GET'])
#@login_required
def profile():
	if 'email' in session :
		user = User.query.filter_by(email=session['email']).first()
		return render_template('userprofile.html',user=user)
	return redirect(url_for('.login'))


@main.route('/addfriends',methods=['GET','POST'])
def addfriends():
	email = 'mac.abhinav@gmail.com'
	return render_template('addfriends.html',email=email)

@main.route('/logout',methods=['GET'])
def logout():
	session.pop('email',None)
	return redirect(url_for('.index'))

