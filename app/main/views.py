from flask import render_template,redirect,flash,url_for,request,session
from . import main
from .forms import RegistrationForm,LoginForm
from .. import db
from ..models import User,Message,Friends,FriendRequest,Testimonial


@main.route('/')
def index():
	if 'email' in session :
		user = User.query.filter_by(email=session['email']).first()
		return render_template('userprofile.html',user=user,testi=readtesti())
	return render_template('index.html')

@main.route('/user',methods=['GET','POST'])
def user():
	friendemail=request.form['friendsemail'] 
	useremail = session['email']
	friend = User.query.filter_by(email=friendemail).first()
	status=isFriend(useremail,friendemail)
	return render_template('friendprofile.html',friend=friend,status=status)

@main.route('/registration',methods=['GET','POST'])
def registration():
	if 'email' in session :
		user = User.query.filter_by(email=session['email']).first()
		return render_template('userprofile.html',user=user,testi=readtesti())
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
		return render_template('userprofile.html',user=user,testi=readtesti())
		
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
		testi= readtesti()
		return render_template('userprofile.html',user=user,testi=readtesti())
	return redirect(url_for('.login'))


@main.route('/addfriend',methods=['POST'])
def addfriend():
	useremail = session['email']
	friendemail = request.form['friendemail']
	fr = FriendRequest(senderName=useremail,receiverName=friendemail)
	db.session.add(fr)
	db.session.commit()
	
	return redirect(url_for('.profile'))

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




@main.route("/sendmsg",methods=['post'])
def sendmsg():
	to = request.form['to']
	friend = User.query.filter_by(email=to).first()
	if friend is None:
		flash("No such user")
		return redirect(url_for(".messages"))
	msg= request.form['msg']
	email = session['email']
	if isFriend(email,to) is not "Friends":
		flash("You are not friends. Cant send message")
		return redirect(url_for('.messages'))
	newmsg = Message(senderName=email,receiverName=to,message=msg)
	db.session.add(newmsg)
	db.session.commit();
	return redirect(url_for('.messages'))

@main.route("/writetesti",methods=['POST'])
def writetesti():
	testi = request.form['testi']
	friendemail = request.form['friendemail']
	email = session['email']
	if isFriend(email,friendemail) is not "Friends":
		flash("You are not friends. Cant write Testimonials")
		#session['friendemail'] = friendemail
		return redirect(url_for('.user'))
	testimonial = Testimonial(senderName=email,receiverName=friendemail,testimonial=testi)
	db.session.add(testimonial)
	db.session.commit()

	return redirect(url_for('.profile'))


@main.route("/viewfriends",methods=['GET','POST'])
def viewfriends():
	if 'email' not in session:
		flash("You are not logged in")
		return redirect(url_for(".index"))
	email= session['email']
	friends=Friends.query.filter_by(senderName=email ).all()
	friends2=Friends.query.filter_by(receiverName=email).all()
	print(friends)
	print(friends2)
	friendrequests = FriendRequest.query.filter_by(receiverName=email).all()
	return render_template("/friends.html",friends=friends,friends2=friends2,friendrequests=friendrequests)




def readtesti():
	email = session['email']
	testi = Testimonial.query.filter_by(receiverName=email).all()
	return testi

def isFriend(useremail,friendemail):
	friend = User.query.filter_by(email=friendemail).first()
	if friend is None:
		flash("no such user")
		return redirect(url_for('.profile'))
	status="None"
	isafriend = Friends.query.filter_by(senderName=useremail,receiverName=friend.email).first() or Friends.query.filter_by(senderName=friend.email,receiverName=useremail).first() 
	if isafriend is None:
		temp = FriendRequest.query.filter_by(senderName=useremail,receiverName=friend.email).first() 
		if temp:
			status="Awaiting Response"
	else:
		status="Friends"
	return status

	
