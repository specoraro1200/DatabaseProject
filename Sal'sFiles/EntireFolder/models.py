from datetime import datetime
from flaskDemo import db, login_manager
from flask_login import UserMixin
from functools import partial
from sqlalchemy import orm

db.Model.metadata.reflect(db.engine)

@login_manager.user_loader
def load_user(user_id):
    return Person.query.get(int(user_id))
#ALTER TABLE person Modify column PersonID int;  

class Person(db.Model,UserMixin):
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.String(60), primary_key=True)
   # username = db.Column(db.String(50), nullable = False)
    password = db.Column(db.String(64))
    Title = db.Column(db.String(50))
    
    #def __repr__(self):
    #return f"Person('{self.id}', '{self.username}', '{self.password}')"
    #roles = db.relationship('Role', secondary='user_roles')

#class Role(db.Model):
#        __table_args__ = {'extend_existing': True} 
#        __tablename__ = 'roles'
#        id = db.Column(db.Integer(), primary_key=True)
#        name = db.Column(db.String(50), unique=True)

#class UserRoles(db.Model):
#        __tablename__ = 'user_roles'
#        id = db.Column(db.Integer(), primary_key=True)
#        user_id = db.Column(db.Integer(), db.ForeignKey('Person.id', ondelete='CASCADE'))
#        role_id = db.Column(db.Integer(), db.ForeignKey('Role.id', ondelete='CASCADE'))

    
class User(db.Model, UserMixin):
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
   # image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    #posts = db.relationship('Post', backref='author', lazy=True)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"


#class Post(db.Model):
#     __table_args__ = {'extend_existing': True}
#     id = db.Column(db.Integer, primary_key=True)
#     title = db.Column(db.String(100), nullable=False)
#     date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
#     content = db.Column(db.Text, nullable=False)
#     user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

 #    def __repr__(self):
  #       return f"Post('{self.title}', '{self.date_posted}')"


class Performance(db.Model):
    __table__ = db.Model.metadata.tables['performance']

#class Person(db.Model):
#    __table__ = db.Model.metadata.tables['person']
    
class Role(db.Model):
    __table__ = db.Model.metadata.tables['role']

class Venue(db.Model):
    __table__ = db.Model.metadata.tables['venue']


#class Dependent(db.Model):
#    __table__ = db.Model.metadata.tables['dependent']
    
#class Department(db.Model):
#    __table__ = db.Model.metadata.tables['department']

# used for query_factory
#def getDepartment(columns=None):
#    u = Department.query
#    if columns:
#        u = u.options(orm.load_only(*columns))
#    return u

#def getDepartmentFactory(columns=None):
#    return partial(getDepartment, columns=columns)

#class Dept_Locations(db.Model):
#    __table__ = db.Model.metadata.tables['dept_locations']
    
#class Employee(db.Model):
#    __table__ = db.Model.metadata.tables['employee']
#class Project(db.Model):
#    __table__ = db.Model.metadata.tables['project']
#class Works_On(db.Model):
#    __table__ = db.Model.metadata.tables['works_on']

    

  
