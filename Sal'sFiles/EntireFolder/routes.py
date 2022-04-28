import os
import secrets
from PIL import Image
from flask import render_template, url_for, flash, redirect, request, abort
from flaskDemo import app, db, bcrypt
from flaskDemo.forms import RegistrationForm, LoginForm, UpdateAccountForm, PostForm, WorkerForm,WorkerUpdateForm, EmployeeLookup, LoginForm, RoleForm
from flaskDemo.models import Person, Performance, Role, Venue 
from flask_login import login_user, current_user, logout_user, login_required
from flask_user import roles_required
from datetime import datetime

@app.route('/map')
def render_map():        
    return render_template('map_home.html')

@app.route("/")
@app.route("/home")
def home():
    if(hasattr(current_user,'Admin')):
        return render_template('layoutAdmin.html', title='Join')
    return render_template('layout.html', title='Join')
41545454
@app.route("/adminHome")
def adminHome():
    print("where the hell am i")
    return render_template('layoutAdmin.html', title='Join')

@app.route("/about")
def about():
    return render_template('about.html', title='About')

@app.route("/adminAbout")
def adminAbout():
    return render_template('adminAbout.html', title='About')

@app.route("/layoutAdmin")
def layoutAdmin():
    return render_template('layoutAdmin.html', title='About')

@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = Person.query.filter_by(id=form.id.data).first()
        if not user:
            flash('Login Unsuccessful. Please check email and password', 'danger')
            return render_template('login.html', title='Login', form=form)
        password = bcrypt.generate_password_hash(user.password).decode('utf-8')
        if user and bcrypt.check_password_hash(password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            if(user.Title == 'Chief'):
                return redirect(next_page) if next_page else redirect(url_for('layoutAdmin'))
            else:
                return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))

def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/profile_pics', picture_fn)

    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn


@app.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        #current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Your account has been updated!', 'success')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.username.data = current_user.User
        form.email.data = current_user.email
    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    return render_template('account.html', title='Account',
                           image_file=image_file, form=form)


@app.route("/dept/new", methods=['GET', 'POST'])
@login_required
def new_worker():
    form = WorkerForm()
    if form.validate_on_submit():      
        assign = Person(id=form.id.data, FirstName=form.firstname.data, MInit = form.middlename.data, LastName = form.lastname.data, PersonType = form.title.data, DateHired = form.hired.data, \
        PhoneNumber = form.phoneNumber.data, Address = form.address.data, email = form.email.data,Instrument = form.instrument.data, password = form.password.data, )
        db.session.add(assign)
        db.session.commit()
        flash('You have added a new worker!', 'success')
        return redirect(url_for('layoutAdmin'))
    return render_template('create_worker.html', title='New Assign', form=form, legend='Add Workers')

@app.route("/roles", methods=['GET', 'POST'])
@login_required
def roles():
    form = RoleForm()
    if form.validate_on_submit():
        assign = Role(RoleID = form.roleID.data, PersonID = form.personID.data, PerformanceID = form.performanceID.data)
        db.session.add(assign)
        db.session.commit()
        print("SUCCESS?""")
        flash('You have added a new role!', 'success')
        return redirect(url_for('adminHome'))
    return render_template('roles.html', title='Emloyee',form = form, legend='Add New Role')


@app.route("/lookup", methods=['GET', 'POST'])
@login_required
def lookup():
    form = EmployeeLookup()
    if form.validate_on_submit():
        worker = Person.query.get_or_404(form.id.data)
        return redirect(url_for('selected',id = worker.id))
    return render_template('lookup.html', title='Emloyee',form = form, legend='Employee Lookup')

@app.route("/lookup/<id>", methods=['GET', 'POST'])
@login_required
def selected(id):
    worker = Person.query.get_or_404(id)
    roles = Role.query.join(Person,Role.PersonID == worker.id)
    return render_template('worker.html', title=worker.FirstName, worker=worker, join = roles, now=datetime.utcnow(), a = current_user.id, b = worker.id)

  
@app.route("/assign/new", methods=['GET', 'POST'])
@login_required
def new_assign():
    form = AssignForm()
    if form.validate_on_submit():
        db.session.add(assign)
        db.session.commit()
        flash('You have added a new assign!', 'success')
        return redirect(url_for('home'))
    return render_template('create_assign.html', title='New Assign',
                           form=form, legend='New Assign')

@app.route("/assignn/<pno>/<essn>")
@login_required
def assignn(pno,essn):
    assign = Works_On.query.get_or_404([essn,pno])
    return render_template('assign.html', title=str(assign.essn)+"_" + str(assign.pno),assign=assign,now=datetime.utcnow())

@app.route("/dept/<dnumber>")
@login_required
def dept(dnumber):
    dept = Department.query.get_or_404(dnumber)
    return render_template('dept.html', title=dept.dname, dept=dept, now=datetime.utcnow())

@app.route("/assign/<pno>/<essn>/delete", methods=['POST'])
@login_required
def delete_assign(essn,pno):
    assign = Works_On.query.get_or_404([essn,pno])
    db.session.delete(assign)
    db.session.commit()
    flash('The assign has been deleted!', 'success')
    return redirect(url_for('home'))

@app.route("/assign/<pno>/<essn>/update", methods=['GET', 'POST'])
@login_required
def update_assign(pno,essn):
    assign = Works_On.query.get_or_404([essn,pno])
    currentDept = dept.dname

    form = DeptUpdateForm()
    if form.validate_on_submit():         
        if currentDept !=form.dname.data:
            dept.dname=form.dname.data
        dept.mgr_ssn=form.mgr_ssn.data
        dept.mgr_start=form.mgr_start.data
        db.session.commit()
        flash('Your department has been updated!', 'success')
        return redirect(url_for('dept', dnumber=dnumber))
    elif request.method == 'GET':              

        form.dnumber.data = dept.dnumber
        form.dname.data = dept.dname
        form.mgr_ssn.data = dept.mgr_ssn
        form.mgr_start.data = dept.mgr_start
    return render_template('create_dept.html', title='Update Department',
                           form=form, legend='Update Department')


@app.route("/dept/<id>/update", methods=['GET', 'POST'])
@login_required
def update_worker(id):
    dept = Person.query.get_or_404(id)
    currentDept = dept.id
    form = WorkerUpdateForm()
    if form.validate_on_submit():
        print("here")
        dept.id=id
        dept.FirstName = form.firstname.data
        dept.MInit = form.middlename.data
        dept.LastName = form.lastname.data
        dept.Title = form.title.data
        dept.DateHired = form.hired.data
        dept.PhoneNumber = form.phoneNumber.data
        dept.Address = form.address.data
        dept.email = form.email.data
        dept.password = form.password.data
        dept.Instrument = form.instrument.data
        db.session.commit()
        flash('Your worker has been updated!', 'success')
        return redirect(url_for('layoutAdmin', id=id))
    elif request.method == 'GET':           
        form.id.data = dept.id
        form.firstname.data = dept.FirstName
        form.middlename.data = dept.MInit
        form.lastname.data = dept.LastName
        form.title.data = dept.Title
        form.hired.data = dept.DateHired
        form.phoneNumber.data = dept.PhoneNumber
        form.address.data = dept.Address
        form.email.data = dept.email
        form.password.data = dept.password
        form.instrument.data = dept.Instrument
    return render_template('create_worker.html', title='Update Workers',
                           form=form, legend='Modify Workers')

@app.route("/dept/<id>/delete", methods=['POST'])
@login_required
def delete_worker(id):
    print("I hate html so much")
    dept = Person.query.get_or_404(id)
    db.session.delete(dept)
    db.session.commit()
    flash('The worker has been deleted!', 'success')
    return redirect(url_for('adminHome'))

@app.route("/dept/<id>/<roleid>/deleteRole", methods=['POST'])
@login_required
def delete_role(id,roleid):
    print(roleid)
    role = Role.query.get_or_404(roleid)
    db.session.delete(role)
    db.session.commit()
    flash('The role has been deleted!', 'success')
    return redirect(url_for('selected',id = id))

@app.route("/dept/<id>/<roleid>/updateRole", methods=['GET', 'POST'])
@login_required
def update_role(id,roleid):
    role = Role.query.get_or_404(roleid)
    form = RoleUpdateForm()
    if form.validate_on_submit():
        role.RoleID = roleid
        role.PersonID = form.personID.data
        role.PerformanceID = role.performanceID.data
        
        db.session.commit()
        flash('Your role has been updated!', 'success')
        return redirect(url_for('layoutAdmin', id=id))
    elif request.method == 'GET':           
        form.id.data = dept.id
        form.firstname.data = dept.FirstName
    return render_template('create_worker.html', title='Update Workers',
                           form=form, legend='Modify Workers')

