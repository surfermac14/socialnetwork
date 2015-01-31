from flask import render_template,redirect,flash,url_for,request,session
from . import main
from .forms import RegistrationForm,LoginForm,EditProfileForm	
from .. import db
from ..models import User,Message,Friends,FriendRequest,Testimonial
import gviz_api
import json


@main.route('/')
def index():
	if 'email' in session :
		email=session['email']
		user = User.query.filter_by(email=session['email']).first()
		return render_template('userprofile.html',user=user,testi=readtesti(),jscode=getJScode(email))
	return render_template('index.html')

@main.route('/user',methods=['GET','POST'])
def user():
	friendemail=request.form['friendsemail'] 
	useremail = session['email']
	user = User.query.filter_by(email=session['email']).first()
	friend = User.query.filter_by(email=friendemail).first()
	status=isFriend(useremail,friendemail)
	return render_template('friendprofile.html',friend=friend,status=status,user=user)

@main.route('/registration',methods=['GET','POST'])
def registration():
	if 'email' in session :
		user = User.query.filter_by(email=session['email']).first()
		return render_template('userprofile.html',user=user,testi=readtesti())
	form = RegistrationForm()
	user = User()
	if form.validate_on_submit() :

		possibleuser=db.session.query(User).filter_by(email=form.email.data).first()
		u = User(fname = form.fname.data,lname=form.lname.data,email=form.email.data,password=form.password.data,sex=form.sex.data,address=form.address.data,phoneno=form.phoneno.data)
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
		email = session['email']
		user = User.query.filter_by(email=email).first()
		
		return render_template('userprofile.html',user=user,testi=readtesti(),jscode=getJScode(email))
		
	if request.method == 'GET':
		return render_template('login.html')
	email = request.form['email']
	password = request.form['password']
	user = User.query.filter_by(email=email,password=password).first()
	if user is None :#or not user.verify_password(password):
		flash("Wrong Email or password")
		return redirect(url_for('.login'))
	session['email'] = user.email

	return render_template('userprofile.html',user=user,testi=readtesti(),jscode=getJScode(email))

@main.route('/profile',methods=['GET'])
#@login_required
def profile():
	if 'email' in session :
		email=session['email']
		user = User.query.filter_by(email=session['email']).first()
		return render_template('userprofile.html',user=user,testi=readtesti(),jscode=getJScode(email))
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
		return render_template('messages.html',user=user)
	elif 'email' not in session:
		flash("You are not logged in")
		return redirect(url_for(".index"))

@main.route('/getSent',methods=['GET'])
def getSent():
	if 'email' in session:
		user = User.query.filter_by(email=session['email']).first()
		sentMessages = Message.query.filter_by(senderName=session['email']).all()
		lst = []
		for message in sentMessages:
			d={}
			d['message'] = message.message
			d['name'] = message.receiverName
			lst.append(d)
		
		return json.dumps(lst)

@main.route('/getReceived',methods=['GET'])
def getReceived():
	if 'email' in session:
		user = User.query.filter_by(email=session['email']).first()
		sentMessages = Message.query.filter_by(receiverName=session['email']).all()
		lst = []
		for message in sentMessages:
			d={}
			d['message'] = message.message
			d['name'] = message.senderName
			lst.append(d)
		
		return json.dumps(lst)




@main.route("/sendmsg",methods=['post'])
def sendmsg():

	to = request.form['name']
	print(to)
	friend = User.query.filter_by(email=to).first()
	if friend is None:
		flash("No such user")
		return redirect(url_for(".messages"))
	msg= request.form['message']
	email = session['email']
	if isFriend(email,to) is not "Friends":
		flash("You are not friends. Cant send message")
		return redirect(url_for('.messages'))
	newmsg = Message(senderName=email,receiverName=to,message=msg)
	db.session.add(newmsg)
	db.session.commit();
	msgs = Message.query.filter_by(senderName=email,receiverName=to).all()
	msg = msgs[-1]
	message ={
		"id":msg.id,
		"senderName":msg.senderName,
		"receiverName":msg.receiverName,
		"message":msg.message
	}
	return json.dumps(message)

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
	user = User.query.filter_by(email=session['email']).first()
	friends=Friends.query.filter_by(senderName=email ).all()
	friends2=Friends.query.filter_by(receiverName=email).all()
	print(friends)
	print(friends2)
	friendrequests = FriendRequest.query.filter_by(receiverName=email).all()
	return render_template("/friends.html",friends=friends,friends2=friends2,friendrequests=friendrequests,user=user)

@main.route("/acceptfriendrequest/<femail>",methods=['GET','POST'])
def acceptfriendrequest(femail):
	email = session['email']
	query = FriendRequest.query.filter_by(senderName=femail,receiverName=email).first()
	db.session.delete(query)
	newfriend = Friends(senderName=femail,receiverName=email)
	db.session.add(newfriend)
	db.session.commit()
	flash("Accepted friend request from %s"%(femail))
	return redirect(url_for(".profile"))
	

@main.route("/declinefriendrequest/<femail>",methods=['GET','POST'])
def declinefriendrequest(femail):
	email = session['email']
	query = FriendRequest.query.filter_by(senderName=femail,receiverName=email).first()
	db.session.delete(query)
	flash("Declined request from %s"%(femail))
	return redirect(url_for(".profile"))
	

@main.route("/users/<profile>",methods=['GET','POST'])
def users(profile):
	friendemail=profile
	useremail = session['email']
	friend = User.query.filter_by(email=friendemail).first()
	status=isFriend(useremail,friendemail)
	return render_template('friendprofile.html',friend=friend,status=status,user=user)

@main.route("/deletefriend/<femail>")
def deletefriend(femail):
	friendemail=femail
	email= session['email']
	query = Friends.query.filter_by(senderName=email,receiverName=femail).first()
	if query is None:
		query = Friends.query.filter_by(senderName=femail,receiverName=email).first()
	db.session.delete(query)
	db.session.commit()
	flash("You have deleted %s"%(femail))
	return redirect(url_for('.viewfriends'))

@main.route('/editprofile',methods=['GET','POST'])
def editprofile():
	if 'email' in session :
		email=session['email']
		user = User.query.filter_by(email=email).first()
		id = user.id
		form = EditProfileForm(fname=user.fname,lname=user.lname,password=user.password,email=user.email,address=user.address,phoneno=user.phoneno)
		
		if request.method == 'POST':
			if form.validate_on_submit():
				user.fname = request.form['fname']
				user.lname = request.form['lname']
				user.password = request.form['password']
				user.email = request.form['email']
				user.address = request.form['address']
				user.phoneno = request.form['phoneno']
				db.session.commit()
				flash("Profile Edited")
				return redirect(url_for('.profile'))
		return render_template("editprofile.html",form=form,user=user)
		
	return redirect(url_for('.profile'))
	



@main.route('/edit',methods=['POST'])
def edit():
	email = session['email']
	user = User.query.filter_by(email=email).first()


def jsonChartData():
	description = {"name": ("string", "Name"),
                 "number": ("number", "Number"),
                }


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

def getJScode(email):
	user = User.query.filter_by(email=session['email']).first()
	testi= readtesti()
	description = {"name": ("string", "Name"),"number": ("number", "Number")}
	my_data=[]
	nofriends = Friends.query.filter_by(senderName=email).count() + Friends.query.filter_by(receiverName=email).count()
	my_data.append({"name":"Friends","number":nofriends})
	nosent = Message.query.filter_by(senderName=email).count()
	my_data.append({"name":"Sent Messages","number":nosent})
	noreceived = Message.query.filter_by(receiverName=email).count()
	my_data.append({"name":"Received Messages","number":noreceived})

	data_table = gviz_api.DataTable(description)
	data_table.LoadData(my_data)

	jscode = data_table.ToJSCode("jscode_data",columns_order=("name", "number"),order_by="name")
	return jscode

	
