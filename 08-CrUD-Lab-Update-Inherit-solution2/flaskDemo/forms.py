from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField, IntegerField, DateField, SelectField, HiddenField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError,Regexp
from wtforms_sqlalchemy.fields import QuerySelectField
from flaskDemo import db
from flaskDemo.models import Person, User, Performance, Venue, Role #Department, Works_On, Employee,Project, getDepartment, getDepartmentFactory
from wtforms.fields import DateField

ssn = Person.query.with_entities(Person.PersonID,Person.FirstName,Person.LastName).distinct()
performances = Performance.query.with_entities(Performance.PerformanceID,Performance.PerformanceDate,Performance.PerformanceTime).join(Venue,Performance.VenueID == Venue.VenueID).add_columns(Venue.Name)

result=list()
performList = list()
def updateSSN():
    ssn = Person.query.with_entities(Person.PersonID,Person.FirstName,Person.LastName).distinct()
    result = list()
    for rows in ssn:
        rowDict = rows._asdict()
        result.append(rowDict)
    choices = [(rows['PersonID'],str(rows['PersonID']) + "-" + rows['FirstName'] + " " +rows["LastName"]) for rows in result]
    return choices

for rows in ssn:
    rowDict = rows._asdict()
    result.append(rowDict)

for rows in performances:
    rowDict = rows._asdict()
    performList.append(rowDict)


choices = [(rows['PersonID'],str(rows['PersonID']) + " - " + rows['FirstName'] + " " +rows["LastName"]) for rows in result]
performChoices = [(rows['PerformanceID'],str(rows['PerformanceID']) + " - " + rows['Name']  + " (" + str(rows["PerformanceDate"]) \
+ " " + str(rows["PerformanceTime"]) + ")") for rows in performList]
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
    email = StringField('Email',validators=[DataRequired(),Email()])
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
    id = IntegerField('Employee ID')
    firstname = StringField("First Name",validators = [Length(min=1,max=35)])
    middlename = StringField("Middle Initial",validators = [Length(max=35)])
    lastname = StringField("Last Name",validators = [Length(min=1,max=35)])
    title = StringField("Title",validators = [Length(max=30)])
    personType = StringField("Person Type",validators = [Length(min=1,max=20)])
    hired = DateField("Date Hired")
    phoneNumber = StringField("Phone Number",validators = [Length(min=8,max=12)])
    address = StringField("Address",validators = [Length(min=1,max=70)])
    email = StringField("Email",validators = [Length(max=30),Email()]) # email in database can be set to null, do we want that?
    instrument = StringField("Instrument",validators = [Length(max=30)])
    submit = SubmitField('Add this employee')

    #class WorkerForm(FlaskForm):
    #id = IntegerField('Project Number')
    #firstname = StringField("First Name",validators = [Length(min=1,max=35)])
    #middlename = StringField("Middle Initial",validators = [Length(max=35)])
    #lastname = StringField("Last Name",validators = [Length(min=1,max=35)])
    #personType = StringField("Person Type",validators = [Length(min=1,max=25)])
    #hired = DateField("Date Hired")
    #phoneNumber = StringField("Phone Number",validators = [Length(min=8,max=12)])
    #address = StringField("Address",validators = [Length(min=1,max=70)])
    #title = StringField("Title",validators = [Length(max=30)])
    #email = StringField("Email",validators = [Length(max=30)]) # email in database can be set to null, do we want that?
    #instrument = StringField("Instrument",validators = [Length(max=30)])
    #submit = SubmitField('Update this department')
    
    def validate_id(self,id):
      # print(Person.PersonID.property.columns[0].type.length)
        maxLength = 6
        assign = Person.query.filter_by(PersonID = id.data).first()
        if (assign):
            raise ValidationError("That ID already exists. Choose another.")
        elif(len(str(id.data)) > maxLength):
            raise ValidationError(f"Pick a number that is less than "+ str(maxLength) +" digits")

class DeleteWorker(FlaskForm):
    choice = updateSSN()
    print(choice)
    id = SelectField('Employee ID',choices = choice)
    submit = SubmitField('Delete this worker')
    def validate_id(self,id):
        if(id == current_user.id):
            raise ValidationError("Can not delete yourself")
    def __init__(self):  
        self.name = name 

class EmployeeLookup(FlaskForm):
    #ssn = Person.query.with_entities(Person.PersonID,Person.FirstName,Person.LastName).distinct()
    #result = list()
    #for rows in ssn:
    #    rowDict = rows._asdict()
    #    result.append(rowDict)
    #choices = [(rows['PersonID'],str(rows['PersonID']) + "-" + rows['FirstName'] + " " +rows["LastName"]) for rows in result]
    print("is anythin g even working on this ")

    id = SelectField('Employee ID',choices = choices)
    submit = SubmitField('Lookup employee')

    def __init__(self, *args, **kwargs):
        super(EmployeeLookup, self).__init__(*args, **kwargs)
        self.id.choices = [(rows['PersonID'],str(rows['PersonID']) + "-" + rows['FirstName'] + " " +rows["LastName"]) for rows in Person.query.with_entities(Person.PersonID,Person.FirstName,Person.LastName).distinct()
]
    
class RoleForm(FlaskForm):
    roleID = StringField("Role ID",validators = [Length(min=1)])
    roleName = StringField("Role Name",validators = [Length(min=1)]) 
    personID = SelectField('Employee ID',choices = choices)       
    performanceID = SelectField('Performance ID',choices = performChoices)    
    submit = SubmitField('Submit')
    
    def validate_roleID(self,id):
        assign = Role.query.filter_by(RoleID = id.data).first()
        if (assign):
            raise ValidationError("That ID already exists. Choose another.")

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
    performanceID = SelectField('Performance ID',choices = performChoices)    
    submit = SubmitField('Submit')

    

