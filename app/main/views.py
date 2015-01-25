from flask import render_template,redirect,flash,url_for,request,session
from . import main
from .forms import RegistrationForm,LoginForm
from .. import db
from ..models import User,Message,Friends,FriendRequest


@main.route('/')
def index():
	if 'email' in session :
		user = User.query.filter_by(email=session['email']).first()
		return render_template('userprofile.html',user=user)
	return render_template('index.html')

@main.route('/user',methods=['POST'])
def user():
	friendemail=request.form['friendsemail']
	useremail = session['email']
	friend = User.query.filter_by(email=friendemail).first()
	if friend is None:
		flash("no such user")
		return redirect(url_for('.profile'))
	status=None
	isafriend = Friends.query.filter_by(senderName=useremail,receiverName=friend.email).first() or Friends.query.filter_by(senderName=friend.email,receiverName=useremail).first() 
	if isafriend is None:
		isafriend= FriendRequest.query.filter_by(senderName=friend.email,receiverName=useremail).first()
	if isafriend is not None:
		success = Friends(senderName=isafriend.senderName,receiverName=isafriend.receiverName)
		db.session.add(success)
		db.session.delete(isafriend)
		db.session.commit()
		status="Friends"
	else:
		status="Awaiting Response"

	return render_template('friendprofile.html',friend=friend,status=status)

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


@main.route('/addfriend',methods=['POST'])
def addfriend():
	email = 'mac.abhinav@gmail.com'
	return render_template('addfriends.html',email=email)

@main.route('/logout',methods=['GET'])
def logout():
	session.pop('email',None)
	return redirect(url_for('.index'))

@main.route('/messages')
def messages():
	if 'email' in session :
		user = User.query.filter_by(email=session['email']).first()
		sentMessages = Message.query.filter_by(senderName=session['email']).all()
		receivedMessages = Message.query.filter_by(receiverName=session['email']).all()
		return render_template('messages.html',sentMessages=sentMessages,receivedMessages=receivedMessages)
	elif 'email' not in session:
		flash("You are not logged in")
		return redirect(url_for(".index"))



	
