from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField, IntegerField, DateField, SelectField, HiddenField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError,Regexp
from wtforms_sqlalchemy.fields import QuerySelectField
from flaskDemo import db
import mysql.connector
from flaskDemo.models import Person, User, Performance, Venue, Role #Department, Works_On, Employee,Project, getDepartment, getDepartmentFactory
from wtforms.fields import DateField

ssn = Person.query.with_entities(Person.PersonID,Person.FirstName,Person.LastName).distinct()
conn = mysql.connector.connect(host='localhost',
                                       database='theatre',
                                       user='sal',
                                       password='password',
                                    connect_timeout=1000)
if conn.is_connected():
    cursor = conn.cursor(dictionary=True)
    cursor.execute('set global max_allowed_packet=67108864')
    cursor.execute("SELECT performance.`PerformanceID` AS `PerformanceID`, performance.`PerformanceDate` AS \
    `PerformanceDate`, performance.`PerformanceTime` AS `PerformanceTime`, venue.`Name` AS `Name` \
    FROM performance INNER JOIN venue ON performance.`VenueID` = venue.`VenueID`;")
    performList = cursor.fetchall()


result=list()

for rows in ssn:
    rowDict = rows._asdict()
    result.append(rowDict)

choices = [(rows['PersonID'],str(rows['PersonID']) + " - " + rows['FirstName'] + " " +rows["LastName"]) for rows in result]
performChoices = [(rows['PerformanceID'],str(rows['PerformanceID']) + " - " + rows['Name']  + " (" + str(rows["PerformanceDate"]) \
+ " " + str(rows["PerformanceTime"]) + ")") for rows in performList]


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
    email = StringField('Email',validators=[DataRequired(),Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')


class UpdateAccountForm(FlaskForm):
    email = StringField('Email',validators=[DataRequired(), Email()])


class WorkerForm(FlaskForm):
    id = IntegerField('Employee ID')
    firstname = StringField("First Name",validators = [Length(min=1,max=35)])
    middlename = StringField("Middle Initial",validators = [Length(max=35)])
    lastname = StringField("Last Name",validators = [Length(min=1,max=35)])
    title = StringField("Title",validators = [Length(max=30)])
    personType = StringField("Person Type",validators = [Length(min=1,max=20)])
    hired = DateField("Date Hired")
    phoneNumber = StringField("Phone Number",validators = [Length(min=8,max=12)])
    address = StringField("Address",validators = [Length(min=1,max=70)])
    email = StringField("Email",validators = [Length(max=30),Email()])
    instrument = StringField("Instrument",validators = [Length(max=30)])
    submit = SubmitField('Add this employee')
    
    def validate_id(self,id):
        maxLength = 6
        assign = Person.query.filter_by(PersonID = id.data).first()
        if (assign):
            raise ValidationError("That ID already exists. Choose another.")
        elif(len(str(id.data)) > maxLength):
            raise ValidationError(f"Pick a number that is less than "+ str(maxLength) +" digits")


class DeleteWorker(FlaskForm):
    id = SelectField('Employee ID',choices = choices)
    submit = SubmitField('Delete this worker')

    def validate_id(self,id):
        if(id == current_user.id):
            raise ValidationError("Can not delete yourself")

    def __init__(self):  
        self.name = name 


class EmployeeLookup(FlaskForm):
    id = SelectField('Employee ID',choices = choices)
    submit = SubmitField('Lookup employee')

    def __init__(self, *args, **kwargs):
        super(EmployeeLookup, self).__init__(*args, **kwargs)
        self.id.choices = [(rows['PersonID'],str(rows['PersonID']) + " - " + rows['FirstName'] + " " +rows["LastName"]) for \
        rows in Person.query.with_entities(Person.PersonID,Person.FirstName,Person.LastName).distinct()]


class RoleForm(FlaskForm):
    roleID = StringField("Role ID",validators = [Length(min=1)])
    roleName = StringField("Role Name",validators = [Length(min=1)]) 
    personID = SelectField('Employee ID',choices = choices)       
    performanceID = SelectField('Performance ID',choices = performChoices)    
    submit = SubmitField('Submit')
    
    def validate_roleID(self,roleID):
       assign = Role.query.filter_by(RoleID = roleID.data).first()
       if (assign):
           raise ValidationError("That ID already exists. Please choose another.")

    def validate_personID(self,personID):
       test = Role.query.filter_by(PersonID = personID.data, PerformanceID = self.performanceID.data).add_columns(Role.PersonID, Role.RoleName).first()
       if test:
           raise ValidationError(
               "This actor already has a role in this performance. Please remove the role named " + test.RoleName + " or edit it to add another role")

    def validate_roleName(self,roleName):
       name = Role.query.filter_by(RoleName = roleName.data,PerformanceID = self.performanceID.data).first()
       if name:
           raise ValidationError(
               "There already exists a role name of " + name.RoleName + " in this performance. Please pick another name.")

    def __init__(self, *args, **kwargs):
        super(RoleForm, self).__init__(*args, **kwargs)
        self.personID.choices = [(rows['PersonID'], str(rows['PersonID']) + " - " + rows['FirstName'] + " " + rows["LastName"])
                           for rows in Person.query.with_entities(Person.PersonID, Person.FirstName, Person.LastName).distinct()]
# ADD A ROUTE NAME TO HTML FOR DELETING ROLE, BECAUSE YOU MAY WANT TO RETURN TO HOME PAGE IF YOU DELTED A ROLE FROM HOME INSETEAD OF LOOKUP IDIOT

class WorkerUpdateForm(FlaskForm):
    id = IntegerField('Employee ID')
    firstname = StringField("First Name",validators = [Length(min=1,max=35)])
    middlename = StringField("Middle Initial",validators = [Length(max=35)])
    lastname = StringField("Last Name",validators = [Length(min=1,max=35)])
    personType = StringField("Person Type",validators = [Length(min=1,max=25)])
    hired = DateField("Date Hired")
    phoneNumber = StringField("Phone Number",validators = [Length(min=8,max=12)])
    address = StringField("Address",validators = [Length(min=1,max=70)])
    title = StringField("Title",validators = [Length(max=30)])
    email = StringField("Email",validators = [Length(max=30)]) # email in database can be set to null, do we want that?
    instrument = StringField("Instrument",validators = [Length(max=30)])
    submit = SubmitField('Update')


class RoleUpdateForm(FlaskForm):
    personID = SelectField('Employee ID',choices = choices)
    roleName = StringField("Role Name",validators = [Length(min=1)])
    submit = SubmitField('Submit')