#import wtforms.ext.sqlalchemy.fields
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField, IntegerField, DateField, SelectField, HiddenField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError,Regexp
from wtforms_sqlalchemy.fields import QuerySelectField
from flaskDemo import db
#import sql_alchemy
from flaskDemo.models import Person, User, Performance, Venue, Role #Department, Works_On, Employee,Project, getDepartment, getDepartmentFactory
from wtforms.fields import DateField

#ssns = Department.query.with_entities(Department.mgr_ssn).distinct()
ssn = Person.query.with_entities(Person.id).distinct()
performances = Performance.query.with_entities(Performance.PerformanceID).distinct()

#print(ssns)
#print("HHEREHEREHEREHEREHEREHEREHEREHEREHEREHEREHEREHEREHEREHEREHEREHEREHEREHEREHEREHEREHEREHEREHEREHEREHEREHEREHEREHE")
#  or could have used ssns = db.session.query(Department.mgr_ssn).distinct()
# for that way, we would have imported db from flaskDemo, see above

#myChoices2 = [(row[0],row[0]) for row in ssns]  # change
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
#myChoices = [(row['mgr_ssn'],row['mgr_ssn']) for row in results]
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
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
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

    
class DeptForm(FlaskForm):

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
    
    def validate_id(self,id):
        assign = Person.query.filter_by(id = id.data).first()
        if(assign):
            raise ValidationError("That ID already exists. Choose another.")


    

    #        raise ValidationError("That ID already exists. Choose another.")
  #  dname=StringField('Department Name:', validators=[DataRequired(),Length(max=15)])
#  Commented out using a text field, validated with a Regexp.  That also works, but a hassle to enter ssn.
#    mgr_ssn = StringField("Manager's SSN", validators=[DataRequired(),Regexp('^(?!000|666)[0-8][0-9]{2}(?!00)[0-9]{2}(?!0000)[0-9]{4}$', message="Please enter 9 digits for a social security.")])

#  One of many ways to use SelectField or QuerySelectField.  Lots of issues using those fields!!
   # mgr_ssn = SelectField("Employee's SSN",choices = )  # myChoices defined at top
    
# the regexp works, and even gives an error message
#    mgr_start=DateField("Manager's Start Date:  yyyy-mm-dd",validators=[Regexp(regex)])
   # mgr_start = DateField("Manager's Start Date")

#    mgr_start=DateField("Manager's Start Date", format='%Y-%m-%d')
  #  mgr_start = DateField("Manager's start date:", format='%Y-%m-%d')  # This is using the html5 date picker (imported)
    submit = SubmitField('Update this department')
   
# got rid of def validate_dnumber
    def validate_dname(self, dname):    # apparently in the company DB, dname is specified as unique
         dept = Department.query.filter_by(dname=dname.data).first()
         if dept and (str(dept.dnumber) != str(self.dnumber.data)):
             raise ValidationError('That department name is already being used. Please choose a different name.')

class DeleteForm(FlaskForm):
    dnumber = SelectField('Employee ID',choices = choices)
    #mgr_ssn = SelectField("Employee's SSN",choices = )  # myChoices defined at top
    submit = SubmitField('Update this department')
    def validate_dnumber(self,dnumber):
        if(dnumber == current_user.id):
            raise ValidationError("Cant delete yourself stupid")
    #  def validate_id(self,id):         
    #    if(id.data == current_user.id):
    #        raise ValidationError("Cant add yourself stupid")

class EmployeeLookup(FlaskForm):
    id = SelectField('Employee ID',choices = choices)
    submit = SubmitField('Search')
    
    #def validate_dnumber(self,dnumber):
    #    if(dnumber == current_user.id):
    #        raise ValidationError("Cant delete yourself stupid")
    #  def validate_id(self,id):         
    #    if(id.data == current_user.id):
    #        raise ValidationError("Cant add yourself stupid")
    
class RoleForm(FlaskForm):
    roleID = StringField("Role Name",validators = [Length(min=1)]) #unique
    personID = SelectField('Employee ID',choices = choices)        # drop down
    performanceID = SelectField('Performance ID',choices = performChoices)     # drop down
    submit = SubmitField('Submit')

    #def validate_dnumber(self,dnumber):
    #    if(dnumber == current_user.id):
    #        raise ValidationError("Cant delete yourself stupid")
    #  def validate_id(self,id):         
    #    if(id.data == current_user.id):
    #        raise ValidationError("Cant add yourself stupid")

class DeptUpdateForm(FlaskForm):
   # dnumber = SelectField('Project Number',choices = pchoices)
   # mgr_ssn = SelectField("Employee's SSN", choices = choices)  # myChoices defined at top
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
    
    #def validate_id(self, id):
    #    assign = Person.query.filter_by(id = id.data).first()
    #    if(assign):
    #        raise ValidationError("That ID already exists. Choose another.")


    

