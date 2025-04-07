from flask import Flask, render_template, request, redirect, url_for,flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
# from livereload import Server
from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, FloatField, FileField, SubmitField, DateField,TimeField
from wtforms.validators import DataRequired
from flask_wtf.file import FileAllowed
import os
from werkzeug.utils import secure_filename
import random

import datetime
# from datetime import datetime
from datetime import date
from sqlalchemy import or_





app = Flask(__name__)
app.config['SECRET_KEY'] = 'my_name_is_prime'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///digital_register.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = 'media/uploads'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)





db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

from flask_migrate import Migrate

migrate = Migrate(app, db)


#user model:
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    role = db.Column(db.String(20), nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)

    def __str__(self):
        return f'<User {self.username}>'
    
class Group(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    group_name = db.Column(db.String(50), nullable=False)

    def __str__(self):
        return f'<Group {self.group_name}>'
    
class Events(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    event_name = db.Column(db.String(50), nullable=False)
    event_day = db.Column(db.String(50), nullable=True)
    event_start_time = db.Column(db.String(50), nullable=False)
    event_late_time = db.Column(db.String(50), nullable=False)
    # worker = db.relationship('Workers', backref='events', lazy=True, nullable=True)
    # worker_id = db.Column(db.Integer, db.ForeignKey('workers.id'), nullable=True)


    def __str__(self):
        return f'<Group {self.event_name}>'
    
class Event_register(db.Model):
    id =  db.Column(db.Integer, primary_key=True)
    event = db.relationship('Events', backref='event_register', lazy=True)
    event_id = db.Column(db.Integer, db.ForeignKey('events.id'), nullable=False)
    worker = db.relationship('Workers', backref='event_register', lazy=True)
    worker_id = db.Column(db.Integer, db.ForeignKey('workers.id'), nullable=False)
    early = db.Column(db.Boolean, default=False)
    present = db.Column(db.Boolean, default=False)
    month = db.Column(db.String(50), nullable=False)
    year = db.Column(db.String(50), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.datetime.now)
    
# event form
class EventForm(FlaskForm):
    event_name = StringField('Event Name', validators=[DataRequired()])
    event_day = SelectField('Event Day', choices=[('Monday', 'Monday'), ('Tuesday', 'Tuesday'), ('Wednesday', 'Wednesday'), ('Thursday', 'Thursday'), ('Friday', 'Friday'), ('Saturday', 'Saturday'), ('Sunday', 'Sunday')], validators=[DataRequired()])
    event_start_time = TimeField('Start Time', format='%H:%M', validators=[DataRequired()])
    event_late_time = TimeField('Lateness Deadline', format='%H:%M', validators=[DataRequired()])

    
# group form
class GroupForm(FlaskForm):
    group_name = StringField('Group Name', validators=[DataRequired()])
    
    
class Position(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    position_name = db.Column(db.String(50), nullable=False)

    def __str__(self):
        return f'<Position {self.position_name}>'   

class PositionForm(FlaskForm):
    position_name = StringField('Position Name', validators=[DataRequired()])

    def __str__(self):
        return f'<Position {self.position_name}>'




    
class Workers(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    phone_number = db.Column(db.String(15), unique=True, nullable=False)
    phone_number_2 = db.Column(db.String(15), unique=True, nullable=False)
    whatsapp_number = db.Column(db.String(15), unique=True, nullable=False)
    address = db.Column(db.String(200), nullable=True)
    dept = db.Column(db.String(50), nullable=False)
    falculty = db.Column(db.String(50), nullable=False)
    level = db.Column(db.String(5), nullable=False)
    next_of_kin = db.Column(db.String(50), nullable=False)
    group = db.relationship('Group', backref='workers', lazy=True)
    group_id = db.Column(db.Integer, db.ForeignKey('group.id'), nullable=False)
    position_id = db.Column(db.Integer, db.ForeignKey('position.id'), nullable=False)
    position = db.relationship('Position', backref='workers', lazy=True)
    gender = db.Column(db.String(10), nullable=False)
    date_of_birth = db.Column(db.String(20), nullable=False)
    passport_image = db.Column(db.String(200), nullable=False)
    unique_id = db.Column(db.String(50), unique=True, nullable=False)

    def __str__(self):
        return f'<Worker {self.first_name}>'
    
class WorkerForm(FlaskForm):
    first_name = StringField('First name', validators=[DataRequired()])
    last_name = StringField('Last name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired()])
    phone_number = StringField('Phone Number', validators=[DataRequired()])
    phone_number_2 = StringField('Phone Number 2', validators=[DataRequired()])
    whatsapp_number = StringField('Whatsapp Number', validators=[DataRequired()])
    address = StringField('Address', validators=[DataRequired()])
    dept = StringField('Department', validators=[DataRequired()])
    falculty = StringField('Falculty', validators=[DataRequired()])
    level = SelectField('Gender',choices=[('100lv', '100lv'), ('200lv', '200lv'), ('300lv', '300lv'), ('400lv', '400lv'), ('500lv', '500lv')],validators=[DataRequired()])
    next_of_kin = StringField('Next of kin', validators=[DataRequired()])
    group = SelectField('Group',coerce=int, validators=[DataRequired()])
    position = SelectField('Position',coerce=int, validators=[DataRequired()])
    gender = SelectField('Gender',choices=[('male', 'Male'), ('female', 'Female')],validators=[DataRequired()])
    date_of_birth = DateField('Date of birth', format='%Y-%m-%d', validators=[DataRequired()])
    passport_image = FileField('Passport Photo', validators=[FileAllowed(['jpg','png','jpeg','HEIC'])])

    def __str__(self):
        return f'{self.first_name} with {self.position} position'
    



    






    

    


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))  # Adjust based on your ORM

# ________________________________________________________________________________________________________
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/signup')
def signup():
    return render_template('signup.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/add_workers',methods=['GET', 'POST'])
def add_workers():
    form = WorkerForm()
    form.group.choices = [(g.id, g.group_name) for g in Group.query.all()]
    form.position.choices = [(p.id, p.position_name) for p in Position.query.all()]


    if form.validate_on_submit():
        filename = None
        date_obj = date.today()
        year = date_obj.year

        random_number = random.randint(100000, 999999)
        unique_id = f"vor/{year}/{random_number}"
        

        # print('image detected', f'filename {form.passport_image.data}')

        if form.passport_image.data:
            filename = secure_filename(form.passport_image.data.filename)
            form.passport_image.data.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            print('image detected', f'filename {filename}')

        new_worker = Workers(
            first_name=form.first_name.data,
            last_name=form.last_name.data,
            email=form.email.data,
            phone_number=form.phone_number.data,
            phone_number_2=form.phone_number_2.data,
            whatsapp_number=form.whatsapp_number.data,
            address = form.address.data,
            dept = form.dept.data,
            falculty = form.falculty.data,
            level = form.level.data,
            next_of_kin = form.next_of_kin.data,
            group_id = form.group.data,
            position_id = form.position.data,
            gender = form.gender.data,
            date_of_birth = str(form.date_of_birth.data),
            passport_image = filename,
            unique_id = unique_id
        )
        db.session.add(new_worker)
        db.session.commit()
        return redirect(url_for('add_workers'))
    
    elif form.errors:
        for field, errors in form.errors.items():
            for error in errors:
                flash(f"{field.capitalize()}: {error}", 'error')
    

    return render_template('add_workers.html', form = form)

@app.route('/add_group', methods=['GET', 'POST'])
def add_group():
    form = GroupForm()
    if form.validate_on_submit():
        group_name = form.group_name.data
        new_group = Group(group_name=group_name)
        db.session.add(new_group)
        db.session.commit()
        return redirect(url_for('add_group'))
    
    groups = Group.query.all()
    return render_template('add_group.html', form=form, group=groups)

@app.route('/add_position',methods=['GET','POST'])
def add_position():
    form = PositionForm()
    
    if form.validate_on_submit():
        position_name = form.position_name.data
        new_position = Position(position_name = position_name)
        db.session.add(new_position)
        db.session.commit()
        return redirect(url_for('add_position'))
    
    positions = Position.query.all()
    return render_template('add_position.html',form=form, position = positions)

@app.route('/workers_records')
def workers_record():
    workers = Workers.query.all()
    print(f'---------------------------{workers}')

    return render_template('workers_record.html', workers=workers)

from flask import send_from_directory

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)


@app.route('/add_event', methods=['GET', 'POST'])
def add_event():
    form = EventForm()

    if form.validate_on_submit():
        event_name = form.event_name.data
        event_day = form.event_day.data
        event_start_time = form.event_start_time.data
        event_late_time = form.event_late_time.data
        new_event = Events(event_name=event_name, event_day=event_day, event_start_time=str(event_start_time), event_late_time=str(event_late_time))
        db.session.add(new_event)
        db.session.commit()
        return redirect(url_for('add_event'))
    
    elif form.errors:
        for field, errors in form.errors.items():
            for error in errors:
                flash(f"{field.capitalize()}: {error}", 'error')
        
    events = Events.query.all()
    return render_template('add_event.html', form=form, events=events)
    
from datetime import datetime

@app.route('/register', methods=['GET', 'POST'])
def register():
    events = Events.query.all()
    events_days = [event.event_day for event in events]
    print(f'---------------------------{events_days}')


    current_day = datetime.now().strftime("%A")
    current_month = datetime.now().strftime("%B")
    print(f'---------------------------{current_day}')
    print(f'---------------------------{current_month}')

    current_day = 'Sunday'
    event_day_id = Events.query.filter(Events.event_day == current_day).first()



    if request.method == 'POST':
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")
        current_time_obj = datetime.strptime(current_time, "%H:%M:%S")
        
        e = Events.query.filter(Events.event_day == current_day).first()
        deadline_time = e.event_late_time
        print(f'---------------------------{deadline_time}')
        deadline_time_obj = datetime.strptime(deadline_time, "%H:%M:%S")
        

        if current_time_obj < deadline_time_obj:
            deadline_state = False
            if_present = True
        else:
            deadline_state = True
            if_present = False
        
        if current_day in events_days:
            query = request.form['query']
            if query:
                results = Workers.query.filter(or_(Workers.first_name.contains(query),Workers.unique_id.contains(query))).first()

                mark = Event_register(
                    event_id = event_day_id.id,
                    worker_id = results.id,
                    month = current_month,
                    year = datetime.now().year,
                    early = deadline_state,
                    present = if_present
                )
                db.session.add(mark)
                db.session.commit()

                print(f'---------------------------{results}')
            else:
                results = []
            return render_template('register.html', results=results)
        else:
            return render_template('register.html',msg='No event for today')
        

    return render_template('register.html')

@app.route('/events_register')
def events_register():
    events = Event_register.query.all()
    return render_template('events_register.html', events=events)
    



# ________________________________________________________________________________________________________
if __name__ == '__main__':
    with app.app_context():
        db.session.remove()  # Close any existing sessions
        # db.drop_all()        # Drop all tables defined in your models
        db.create_all()
    app.run(host='0.0.0.0', port=8000,debug=True )

# --- livereload integration ---    
# if __name__ == '__main__':
#     with app.app_context():
#         # db.session.remove()  # Close any existing sessions
#         # db.drop_all()        # Drop all tables defined in your models
#         db.create_all()

#     server = Server(app.wsgi_app)
#     server.watch('*.py')
#     # Watch all template files
#     server.watch('templates/*.*')  # All files in templates and subdirectories
#     server.watch('static/**/*.*')     # All static files    # Watch static files
#     server.watch('**/*.*', delay=1)
#     server.watch('*.html')

    
#     server.serve(port=5000, host='0.0.0.0', debug=True)
 

