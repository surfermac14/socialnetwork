from flask import render_template,redirect,flash,url_for
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
		try:
			db.session.add(user)
			db.session.commit()
			flash('Successfully registered. Please proceed to login page.')
			return redirect(url_for('.index'))
		except Exception as e:
			flash('Email id already exists')
			db.session.rollback()
	return render_template('registration.html',form=form)

@main.route('/login',methods=['GET','POST'])
def login():
	form = LoginForm()
	if form.validate_on_submit():
		q=db.session.query(User).filter_by(email = form.email.data,password = form.password.data).first()
		if(q is None):
			flash("Wrong Username or password")
			return redirect(url_for('.login'))
		else:
			flash("Welcome %s"%(q.fname))
			return redirect(url_for('.index'))
		
		
	return render_template('login.html',form=form)
