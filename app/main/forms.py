from flask.ext.wtf import Form
from wtforms import StringField, SubmitField,PasswordField,RadioField
from wtforms.validators import Required,Email,Regexp


class RegistrationForm(Form):
	fname = StringField(u'First Name',validators =[Required()])
	lname = StringField(u'Last Name',validators=[Required()])
	email = StringField(u'Email Id',validators=[Required(),Email()])
	password = PasswordField(u'Password',validators=[Required()])
	sex = RadioField(u'Sex',choices=[('0','Male'),('1','Female')],validators=[Required()])
	address = StringField(u'Address',validators=[Required()])
	phoneno = StringField(u'Phone Number',validators=[Required(),Regexp('[0-9]+')])
	submit = SubmitField(u'Register')

class EditProfileForm(Form):
	fname = StringField(u'First Name',validators =[Required()])
	lname = StringField(u'Last Name',validators=[Required()])
	email = StringField(u'Email Id',validators=[Required(),Email()])
	password = PasswordField(u'Password',validators=[Required()])
	address = StringField(u'Address',validators=[Required()])
	phoneno = StringField(u'Phone Number',validators=[Required(),Regexp('[0-9]+')])
	submit = SubmitField(u'Edit Profile')

class LoginForm(Form):
	email = StringField(u'Email Address',validators = [Required(),Email()])
	password = PasswordField(u'Password',validators = [Required()])
	#login = SubmitField(u'Login')