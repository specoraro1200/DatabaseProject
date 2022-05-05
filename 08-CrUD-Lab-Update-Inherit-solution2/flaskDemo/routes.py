import os
import secrets
from flask import render_template, url_for, flash, redirect, request, abort
from flaskDemo import app, db, bcrypt
from flaskDemo.forms import RegistrationForm, LoginForm, UpdateAccountForm, WorkerForm,WorkerUpdateForm, EmployeeLookup, LoginForm, RoleForm,RoleUpdateForm
from flaskDemo.models import Person, Performance, Role, Venue ,User
from flask_login import login_user, current_user, logout_user, login_required
from datetime import datetime
import mysql.connector
from mysql.connector import Error

currentPerson = None

def get_schedule():
    results = Person.query.filter(Person.email == current_user.email).join(Role, Person.PersonID == Role.PersonID).add_columns(Person.PersonID, Role.PerformanceID, Role.RoleName) \
            .join(Performance, Role.PerformanceID==Performance.PerformanceID).add_columns(Performance.VenueID, Performance.PerformanceDate, Performance.PerformanceTime)\
            .join(Venue, Venue.VenueID == Performance.VenueID).add_columns(Venue.Name, Venue.Latitude, Venue.Longitude).order_by(Performance.PerformanceDate, Performance.PerformanceTime).all()

    results = [r._asdict() for r in results]
    for r in results:
        r.pop('Person')
        r['PerformanceDate'] = r['PerformanceDate'].strftime('%x')
        r['PerformanceTime'] = r['PerformanceTime'].strftime('%I:%M %p %Z')

    mydata = {}
    for r in results:
        place = r['Name'] + ' {"lat": ' + str(r['Latitude']) + ', "lng": ' + str(r['Longitude']) + '}'
        keys2 = ['RoleName', 'PerformanceDate', 'PerformanceTime']
        content = {k: r[k] for k in keys2}
        if place not in mydata.keys():
            mydata[place] = []
        mydata[place] += [content]

    return mydata

def check_employee_schedule(store):
    results = Person.query.filter(Person.email == store.email).join(Role, Person.PersonID == Role.PersonID).add_columns(Person.FirstName,Person.LastName,Person.PersonID, Role.PersonID,Role.PerformanceID, Role.RoleName,Role.RoleID,Role.PersonID) \
            .join(Performance, Role.PerformanceID==Performance.PerformanceID).add_columns(Performance.VenueID, Performance.PerformanceDate, Performance.PerformanceTime)\
            .join(Venue, Venue.VenueID == Performance.VenueID).add_columns(Venue.Name, Venue.Latitude, Venue.Longitude).order_by(Performance.PerformanceDate, Performance.PerformanceTime).all()

    results = [r._asdict() for r in results]
    for r in results:
        r.pop('Person')
        r['PerformanceDate'] = r['PerformanceDate'].strftime('%x')
        r['PerformanceTime'] = r['PerformanceTime'].strftime('%I:%M %p %Z')
        if r['PerformanceTime'][0:1] == "1":
            r['PerformanceTime'] = r['PerformanceTime'][1:]

    mydata = {}
    for r in results:
        place = r['Name'] + ' {Lat: ' + str(r['Latitude']) + ' Lng: ' + str(r['Longitude']) + '}'
        keys2 = ['RoleName', 'PerformanceDate', 'PerformanceTime','PersonID','RoleID','FirstName','LastName']
        content = {k: r[k] for k in keys2}
        if place not in mydata.keys():
            mydata[place] = []
        mydata[place] += [content]
    return mydata

def get_schedule_admin():
    """ Connect to MySQL database """
    try:
        conn = mysql.connector.connect(host='localhost',
                                       database='theatre',
                                       user='sal',
                                       password='password',
                                    connect_timeout=1000)

        if conn.is_connected():
            cursor = conn.cursor(dictionary=True)
        cursor.execute('set global max_allowed_packet=67108864')
        cursor.execute("SELECT Person.FirstName, Person.LastName,Role.RoleID, Role.RoleName, Role.PersonID, Performance.PerformanceDate, \
                       Performance.PerformanceTime, Venue.Name, Venue.Longitude, Venue.Latitude FROM Person, Role, Performance, Venue \
                       WHERE Person.PersonID = Role.PersonID AND Performance.PerformanceID = Role.PerformanceID AND Venue.VenueID = Performance.VenueID \
                       ORDER BY Performance.PerformanceDate, Performance.PerformanceTime, RoleName")

        r = cursor.fetchone()
        mydata = {}
        while r is not None:
            r['PerformanceDate'] = r['PerformanceDate'].strftime('%x')
            time = (datetime.min + r['PerformanceTime']).time()
            r['PerformanceTime'] = time.strftime("%I:%M %p %Z")[1:]
            keys = ['RoleName', 'FirstName', 'LastName','PersonID','RoleID']
            content = {k: r[k] for k in keys}
            place = r['Name'] + ' {"lat": ' + str(r['Latitude']) + ', "lng": ' + str(r['Longitude']) + '}'

            if place not in mydata.keys():
                mydata[place] = {}

            perf = r['PerformanceDate'] + ' ' + r['PerformanceTime']
            perfs = [k for d in mydata.values() for k in d.keys()]
            if perf not in perfs:
                mydata[place][perf] = []

            mydata[place][perf] += [content]
            r = cursor.fetchone()

    except Error as e:
        conn.ping(True)
        print('*************',e)

   # print(numberOfEmployees['Count'])

    conn.close()
    cursor.close()
    return mydata #,numberOfEmployees

def getPerformanceCount():
    try:
        conn = mysql.connector.connect(host='localhost',
                                       database='theatre',
                                       user='sal',
                                       password='password',
                                       connect_timeout=1000)

        if conn.is_connected():
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT count(PerformanceID) as 'Count' from performance")
            numberOfEmployees = cursor.fetchone()

    except Error as e:
        conn.ping(True)
        print('*************',e)

    print(numberOfEmployees)
    print("HERERERERE")
    print("HERERERERE")
    print("HERERERERE")
    return numberOfEmployees

@app.route('/map')
@login_required
def map_home():
    global currentPerson;
    currentPerson = Person.query.filter_by(email = current_user.email).first()

    if currentPerson.PersonType == 'Admin':
        mydata=get_schedule_admin()
        return render_template('map_admin.html', title='Map', mydata=mydata)
    else:
        mydata=get_schedule()
        return render_template('map_home.html', title='Map',mydata=mydata)


@app.route('/map')
def render_map():
    return render_template('map_home.html')#


@app.route("/")
@app.route("/home")
@login_required
def home():
    global currentPerson;
    currentPerson = Person.query.filter_by(email = current_user.email).first()
    count = getPerformanceCount()
    if currentPerson.PersonType == 'Admin':
        mydata=get_schedule_admin()
        return render_template('adminhome.html', title='Home', mydata=mydata,count = count["Count"])
    else:
        mydata=get_schedule()
        return render_template('home.html', title='Home',mydata=mydata)


@app.route("/about")
def about():
    return render_template('about.html', title='About')


@app.route("/adminAbout")
def adminAbout():
    return render_template('adminAbout.html', title='About')


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
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check username and password', 'danger')
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


@app.route("/lookup", methods=['GET', 'POST'])
@login_required
def lookup():
    form = EmployeeLookup()
    if form.validate_on_submit():
        worker = Person.query.get_or_404(form.id.data)
        return redirect(url_for('selected',id = worker.PersonID))
    return render_template('lookup.html', title='Emloyee',form = form, legend='Employee Lookup')


@app.route("/lookup/<id>", methods=['GET', 'POST'])
@login_required
def selected(id):
    worker = Person.query.get_or_404(id)
    currentPerson = Person.query.filter_by(email = current_user.email).first()
    roles = Role.query.join(Person,Role.PersonID == worker.PersonID)
    mydata = check_employee_schedule(worker)
    return render_template('worker.html', mydata = mydata, worker=worker, join = roles, \
    now=datetime.utcnow(), a = currentPerson.PersonID, b = worker.PersonID)


@app.route("/dept/new", methods=['GET', 'POST'])
@login_required
def new_worker():
    form = WorkerForm()
    if form.validate_on_submit():
        assign = Person(PersonID=form.id.data, FirstName=form.firstname.data, MInit = form.middlename.data, LastName = form.lastname.data, PersonType = form.personType.data, DateHired = form.hired.data, \
        PhoneNumber = form.phoneNumber.data, Address = form.address.data, email = form.email.data,Instrument = form.instrument.data,Title = form.title.data)
        db.session.add(assign)
        db.session.commit()
        flash('You have added a new worker!', 'success')
        return redirect(url_for('home'))
    return render_template('create_worker.html', title='New Assign', form=form, legend='Add Workers')


@app.route("/dept/<id>/update", methods=['GET', 'POST'])
@login_required
def update_worker(id):
    dept = Person.query.get_or_404(id)
    form = WorkerUpdateForm()
    if form.validate_on_submit():
        dept.PersonID=id
        dept.FirstName = form.firstname.data
        dept.MInit = form.middlename.data
        dept.LastName = form.lastname.data
        dept.Title = form.title.data
        dept.PersonType = form.personType.data
        dept.DateHired = form.hired.data
        dept.PhoneNumber = form.phoneNumber.data
        dept.Address = form.address.data
        dept.email = form.email.data
        dept.Instrument = form.instrument.data
        db.session.commit()
        flash('Your worker has been updated!', 'success')
        return redirect(url_for('home', id=id))
    elif request.method == 'GET':
        form.id.data = dept.PersonID
        form.firstname.data = dept.FirstName
        form.middlename.data = dept.MInit
        form.lastname.data = dept.LastName
        form.title.data = dept.Title
        form.personType.data = dept.PersonType
        form.hired.data = dept.DateHired
        form.phoneNumber.data = dept.PhoneNumber
        form.address.data = dept.Address
        form.email.data = dept.email
        form.instrument.data = dept.Instrument
    return render_template('create_worker.html', title='Update Workers',
                           form=form, legend='Modify Workers')


@app.route("/dept/<id>/delete", methods=['POST'])
@login_required
def delete_worker(id):
    worker = Person.query.get_or_404(id)
    confirm = Role.query.filter(Role.PersonID == worker.PersonID).first()
    if confirm:
        flash('The worker can not be deleted, you must first ensure they have no roles left!', 'success')
        return redirect(url_for('selected',id=id))
    db.session.delete(worker)
    db.session.commit()
    flash('The worker has been deleted!', 'success')
    return redirect(url_for('home'))


@app.route("/roles", methods=['GET', 'POST'])
@login_required
def new_role():
    form = RoleForm()
    if form.validate_on_submit():
        print("here")
        assign = Role(RoleID = form.roleID.data, PersonID = form.personID.data, PerformanceID = form.performanceID.data,RoleName = form.roleName.data)
        db.session.add(assign)
        db.session.commit()
        flash('You have added a new role!', 'success')
        return redirect(url_for('home'))
    print("not working")
    return render_template('roles.html', title='Add New Role',form = form, legend='Add New Role')


@app.route("/lookup/<id>/<roleid>/role", methods=['POST'])
@login_required
def delete_role(id,roleid):
    role = Role.query.get_or_404(roleid)
    db.session.delete(role)
    db.session.commit()
    flash('The role has been deleted!', 'success')
    return redirect(url_for('selected',id = role.PersonID))


@app.route("/lookup/<id>/<roleid>/role", methods=['GET', 'POST'])
@login_required
def rolePage(id,roleid):
    role = Role.query.filter(Role.RoleID == roleid).join(Person,Role.PersonID == Person.PersonID).add_columns(Person.FirstName,Person.LastName,Role.PersonID, \
    Role.RoleID,Role.RoleName,Role.PerformanceID).join(Performance,Role.PerformanceID == Performance.PerformanceID).add_columns(Performance.PerformanceDate,Performance. \
    PerformanceTime).join(Venue,Performance.VenueID == Venue.VenueID).add_columns(Venue.Name,Venue.Longitude,Venue.Latitude)
    results = [r._asdict() for r in role]
    for r in results:
        r['PerformanceDate'] = r['PerformanceDate'].strftime('%x')
        r['PerformanceTime'] = r['PerformanceTime'].strftime('%I:%M %p %Z')
        if r['PerformanceTime'][0:1] == "1":
            r['PerformanceTime'] = r['PerformanceTime'][1:]

    return render_template('rolePage.html', title='Role Page',join=results, legend='Modify Role')

@app.route("/lookup/<id>/<roleid>/role/delete", methods=['GET', 'POST'])
@login_required
def update_role(id,roleid):
    role = Role.query.get_or_404(roleid)
    form = RoleUpdateForm()
    if form.validate_on_submit():
        role.RoleID = roleid
        role.PersonID = form.personID.data
        role.RoleName = form.roleName.data
        db.session.commit()
        flash('Your role has been updated!', 'success')
        return redirect(url_for('selected',id = id))
    elif request.method == 'GET':
        form.roleID = role.RoleID
        form.personID.data = role.PersonID
        form.roleName.data = role.RoleName
    return render_template('roles.html', title='Modify Role',
                           form=form, legend='Modify Role')