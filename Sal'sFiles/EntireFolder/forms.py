from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField, IntegerField, DateField, SelectField, HiddenField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError,Regexp
from wtforms_sqlalchemy.fields import QuerySelectField
from flaskDemo import db
from flaskDemo.models import Person, User, Performance, Venue, Role #Department, Works_On, Employee,Project, getDepartment, getDepartmentFactory
from wtforms.fields import DateField

ssn = Person.query.with_entities(Person.id).distinct()
performances = Performance.query.with_entities(Performance.PerformanceID).distinct()

result=list()
performList = list()
for rows in ssn:
    rowDict = rows._asdict()
    result.append(rows)

for rows in performances:
    rowDict = rows._asdict()
    performList.append(rows)

choices = [(rows['id'],rows['id']) for rows in result]
performChoices = [(rows['PerformanceID'],rows['PerformanceID']) for rows in performList]
regex1='^((((19|20)(([02468][048])|([13579][26]))-02-29))|((20[0-9][0-9])|(19[0-9][0-9]))-((((0[1-9])'
regex2='|(1[0-2]))-((0[1-9])|(1\d)|(2[0-8])))|((((0[13578])|(1[02]))-31)|(((0[1,3-9])|(1[0-2]))-(29|30)))))$'
regex=regex1 + regex2


class RegistrationForm(FlaskForm):
    username = StringField('Username',validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('That username is taken. Please choose a different one.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('That email is taken. Please choose a different one.')


class LoginForm(FlaskForm):
    id = StringField('ID')
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')


class UpdateAccountForm(FlaskForm):
    username = StringField('Username',validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',validators=[DataRequired(), Email()])
    picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Update')

    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('That username is taken. Please choose a different one.')

    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('That email is taken. Please choose a different one.')

class PostForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    content = TextAreaField('Content', validators=[DataRequired()])
    submit = SubmitField('Post')

    
class WorkerForm(FlaskForm):
    id = IntegerField('Project Number')
    firstname = StringField("First Name",validators = [Length(min=1)])
    middlename = StringField("Middle Initial")
    lastname = StringField("Last Name",validators = [Length(min=1)])
    title = StringField("Title",validators = [Length(min=1)])
    hired = DateField("Date Hired")
    phoneNumber = StringField("Phone Number",validators = [Length(min=7)])
    address = StringField("Address",validators = [Length(min=1)])
    email = StringField("Username",validators = [Length(min=1)])
    password = StringField("Password",validators = [Length(min=1)])
    instrument = StringField("Instrument")
    submit = SubmitField('Update this department')
    
    def validate_id(self,id):
        assign = Person.query.filter_by(id = id.data).first()
        if (assign):
            raise ValidationError("That ID already exists. Choose another.")
        elif(len(str(id))>11):
            raise ValidationError("Pick a number that is less than 12 digits")

   
    def validate_dname(self, dname):
        if not dname:
            raise ValidationError('You need a department name idiot')
        dept = Department.query.filter_by(dname=dname.data).first()
        if dept and (str(dept.dnumber) != str(self.dnumber.data)):
             raise ValidationError('That department name is already being used. Please choose a different name.')

class DeleteWorker(FlaskForm):
    dnumber = SelectField('Employee ID',choices = choices)
    submit = SubmitField('Update this department')
    def validate_dnumber(self,dnumber):
        if(dnumber == current_user.id):
            raise ValidationError("Cant delete yourself stupid")


class EmployeeLookup(FlaskForm):
    id = SelectField('Employee ID',choices = choices)
    submit = SubmitField('Search')

    
class RoleForm(FlaskForm):
    roleID = StringField("Role Name",validators = [Length(min=1)]) 
    personID = SelectField('Employee ID',choices = choices)       
    performanceID = SelectField('Performance ID',choices = performChoices)    
    submit = SubmitField('Submit')

class WorkerUpdateForm(FlaskForm):
    id = IntegerField('d Number')
    firstname = StringField("First Name",validators = [Length(min=1)])
    middlename = StringField("Middle Initial")
    lastname = StringField("Last Name",validators = [Length(min=1)])
    title = StringField("Title",validators = [Length(min=1)])
    hired = DateField("Date Hired")
    phoneNumber = StringField("Phone Number",validators = [Length(min=7)])
    address = StringField("Address",validators = [Length(min=1)])
    email = StringField("Username",validators = [Length(min=1)])
    password = StringField("Password",validators = [Length(min=1)])
    instrument = StringField("Instrument")
    submit = SubmitField('Update')

class RoleUpdateForm(FlaskForm):
    personID = SelectField('Employee ID',choices = choices)       
    performanceID = SelectField('Performance ID',choices = performChoices)    
    submit = SubmitField('Submit')

    

