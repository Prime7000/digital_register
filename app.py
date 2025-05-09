from flask import Flask, render_template, request, redirect, url_for,flash,jsonify
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

# load user for flask-login
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

    
class Group(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    group_name = db.Column(db.String(50), nullable=False)

    def __str__(self):
        return f'<Group {self.group_name}>'
    
class Events(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    event_name = db.Column(db.String(50), nullable=False)
    event_day = db.Column(db.String(50), nullable=True)
    event_start_time = db.Column(db.Time(), nullable=False)
    event_late_time = db.Column(db.Time(), nullable=False)
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

# site settings model
class Site_settings(db.Model):
    id =  db.Column(db.Integer, primary_key=True)
    prefix = db.Column(db.String(17), default='lunafireX')




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
    level = SelectField('Level',choices=[('100lv', '100lv'), ('200lv', '200lv'), ('300lv', '300lv'), ('400lv', '400lv'), ('500lv', '500lv')],validators=[DataRequired()])
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
    if not current_user.is_authenticated:
        return redirect(url_for('login'))
    return render_template('index.html')

@app.route('/signup', methods=['POST','GET'])
def signup():
    if request.method == 'POST':
        username = request.form.get('username')
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        email = request.form.get('email')
        role = request.form.get('role')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')

        print(f'{username}---{first_name}')

        if password != confirm_password:
            return render_template('signup.html', error = 'password does not match, try again')
        
        if User.query.filter_by(username=username).first():
            return render_template('signup.html', error = 'Username already taken')
        
        encrypted_pass = generate_password_hash(password, method='pbkdf2:sha256')
        new_user = User(username = username,first_name=first_name,last_name=last_name,email=email,role=role,password_hash=encrypted_pass)
        db.session.add(new_user)
        db.session.commit()

        return redirect(url_for("login"))
        
    return render_template('signup.html')

@app.route('/login', methods = ['POST','GET'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        user = User.query.filter_by(username = username).first()

        if user and check_password_hash(user.password_hash, password):
            login_user(user)
            return redirect(url_for('index'))
        else:
            return render_template('login.html', error='Invalid username or passsword')
        
    return render_template('login.html')

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))

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
        prefix = Site_settings.query.first()
        unique_id = f"{prefix.prefix}/{year}/{random_number}"
        

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

@app.route('/edit_worker/<int:pos_id>', methods=['GET', 'POST'])
def edit_worker(pos_id):
    pos = Workers.query.get(pos_id)

    # Convert date_of_birth to a datetime.date object if it's a string
    if isinstance(pos.date_of_birth, str):
        try:
            pos.date_of_birth = datetime.strptime(pos.date_of_birth, "%Y-%m-%d").date()
        except ValueError:
            pos.date_of_birth = None

    form = WorkerForm(obj=pos)

    # ✅ Add choices to form dropdowns
    form.group.choices = [(g.id, g.group_name) for g in Group.query.all()]
    form.position.choices = [(p.id, p.position_name) for p in Position.query.all()]

    if form.validate_on_submit():
        pos.first_name = form.first_name.data
        pos.last_name = form.last_name.data
        pos.email = form.email.data
        pos.phone_number = form.phone_number.data
        pos.phone_number_2 = form.phone_number_2.data
        pos.whatsapp_number = form.whatsapp_number.data
        pos.address = form.address.data
        pos.dept = form.dept.data
        pos.falculty = form.falculty.data
        pos.level = form.level.data
        pos.next_of_kin = form.next_of_kin.data
        pos.group_id = form.group.data
        pos.position_id = form.position.data
        pos.gender = form.gender.data
        pos.date_of_birth = form.date_of_birth.data  # use as date object

        if form.passport_image.data:
            filename = secure_filename(form.passport_image.data.filename)
            form.passport_image.data.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            pos.passport_image = filename

        db.session.commit()

        return redirect(url_for('user_profile', id=pos_id))

    return render_template('edit_pages/edit_worker.html', form=form, current_user=pos)



@app.route('/delete_worker/<int:pos_id>')
def delete_worker(pos_id):
    pos = Workers.query.get(pos_id)
    if pos:
        db.session.delete(pos)
        db.session.commit()
        return redirect(url_for('workers_record'))
    else:
        msg = 'no such person'
        return render_template('workers_record.html',error = msg)

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

@app.route('/edit_group/<int:pos_id>',methods=['GET','POST'])
def edit_group(pos_id):
    pos = Group.query.get(pos_id)
    form = GroupForm(obj = pos)
    if form.validate_on_submit():
        pos.group_name = form.group_name.data
        db.session.commit()
        return redirect(url_for('add_group'))
    
    return render_template('edit_pages/edit_group.html',form=form, position = pos)

@app.route('/delete_group/<int:pos_id>')
def group_position(pos_id):
    pos = Group.query.get(pos_id)
    if pos:
        db.session.delete(pos)
        db.session.commit()
        return redirect(url_for('add_group'))
    else:
        msg = 'no such group'
        return render_template('add_group.html',error = msg)

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

@app.route('/edit_position/<int:pos_id>',methods=['GET','POST'])
def edit_position(pos_id):
    form = PositionForm()
    pos = Position.query.get(pos_id)
    if form.validate_on_submit():
        pos.position_name = form.position_name.data
        db.session.commit()
        return redirect(url_for('add_position'))
    
    return render_template('edit_pages/edit_position.html',form=form, position = pos)


@app.route('/delete_position/<int:pos_id>')
def delete_position(pos_id):
    pos = Position.query.get(pos_id)
    if pos:
        db.session.delete(pos)
        db.session.commit()
        return redirect(url_for('add_position'))
    else:
        msg = 'no such position'
        return render_template('add_position.html',error = msg)

    

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
        new_event = Events(event_name=event_name, event_day=event_day, event_start_time=event_start_time, event_late_time=event_late_time)
        db.session.add(new_event)
        db.session.commit()
        return redirect(url_for('add_event'))
    
    elif form.errors:
        for field, errors in form.errors.items():
            for error in errors:
                flash(f"{field.capitalize()}: {error}", 'error')
        
    events = Events.query.all()
    return render_template('add_event.html', form=form, events=events)

@app.route('/edit_event/<int:pos_id>',methods=['GET','POST'])
def edit_event(pos_id):
    pos = Events.query.get(pos_id)
    form= EventForm(obj=pos)
    if form.validate_on_submit():
        pos.event_name = form.event_name.data
        pos.event_day = form.event_day.data
        pos.event_start_time = form.event_start_time.data
        pos.event_late_time = form.event_late_time.data
        db.session.commit()
        return redirect(url_for('add_event'))
    
    return render_template('edit_pages/edit_events.html',form=form, position = pos)


@app.route('/delete_event/<int:pos_id>')
def delete_event(pos_id):
    pos = Events.query.get(pos_id)
    if pos:
        db.session.delete(pos)
        db.session.commit()
        return redirect(url_for('add_event'))
    else:
        msg = 'no such event'
        return render_template('add_event.html',error = msg)
    
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

    # current_day = 'Sunday'
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

                print(f'---------------------------sucessfully submitted')
            else:
                pass

            return render_template('pages/attendant_register.html')
        else:
            return render_template('pages/attendant_register.html',msg='No event for today')
        

    return render_template('pages/attendant_register.html')



@app.route('/get_individual/<ind>', methods=['GET'])
def register_ind(ind):
    results = Workers.query.filter(or_(Workers.first_name.contains(ind),Workers.unique_id.contains(ind))).first()
    if results:
        info = {
            'firstname':results.first_name,
            'lastname':results.last_name,
            'mat_num':results.unique_id,
            'dept':results.group.group_name
        }

        return jsonify(info)
    else:
        info = {
            'error':'Record not found'
        }

        return jsonify(info) 
        
@app.route('/profile/<int:id>')
def user_profile(id):
    worker = Workers.query.filter(Workers.id == id).first()

    return render_template('user_profile.html', current_user=worker)


# this section is created by ai
# Add this import at the top if you don't have it
from sqlalchemy import func # Needed for counting
from datetime import datetime, timedelta, time
from dateutil.relativedelta import relativedelta # More robust for month/year 

# ... (keep other imports and code)

@app.route('/events_register', methods=['GET'])
def events_register():
    # Get filter parameters from query string
    selected_group_id = request.args.get('group_id', 'all')
    selected_status = request.args.get('status', 'all')
    selected_period = request.args.get('period', 'all_time') # New parameter, default to 'all_time'

    # Base query
    query = Event_register.query.join(Workers).join(Group) # Join necessary tables

    # Apply Group Filter
    if selected_group_id != 'all':
        try:
            group_id_int = int(selected_group_id)
            query = query.filter(Workers.group_id == group_id_int)
        except ValueError:
            flash("Invalid Group ID selected.", "error")
            selected_group_id = 'all'

    # Apply Status Filter
    if selected_status == 'early':
        # Original logic: Early means present AND early flag is true
        query = query.filter(Event_register.present == True, Event_register.early == True)
    elif selected_status == 'late':
         # Original logic: Late means present AND early flag is false
        query = query.filter(Event_register.present == True, Event_register.early == False)
    elif selected_status == 'absent':
        # Original logic: Absent means present flag is false
        query = query.filter(Event_register.present == False)
    # 'all' status requires no additional filtering here

    # --- Apply Time Period Filter ---
    now = datetime.now()
    today_start = datetime.combine(now.date(), time.min)
    today_end = datetime.combine(now.date(), time.max)

    start_date = None
    end_date = None

    if selected_period == 'today':
        start_date = today_start
        end_date = today_end
    elif selected_period == 'yesterday':
        yesterday = now.date() - timedelta(days=1)
        start_date = datetime.combine(yesterday, time.min)
        end_date = datetime.combine(yesterday, time.max)
    elif selected_period == 'this_week':
        # Monday is 0, Sunday is 6
        start_of_week = now.date() - timedelta(days=now.weekday())
        end_of_week = start_of_week + timedelta(days=6)
        start_date = datetime.combine(start_of_week, time.min)
        end_date = datetime.combine(end_of_week, time.max)
    elif selected_period == 'last_week':
        end_of_last_week = now.date() - timedelta(days=now.weekday() + 1)
        start_of_last_week = end_of_last_week - timedelta(days=6)
        start_date = datetime.combine(start_of_last_week, time.min)
        end_date = datetime.combine(end_of_last_week, time.max)
    elif selected_period == 'this_month':
        start_of_month = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        # Go to next month, then subtract one day to get end of current month
        next_month = start_of_month + relativedelta(months=1)
        end_of_month = next_month - timedelta(seconds=1) # End of the last day
        start_date = start_of_month
        end_date = end_of_month
    elif selected_period == 'last_month':
        end_of_last_month = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0) - timedelta(seconds=1)
        start_of_last_month = end_of_last_month.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        start_date = start_of_last_month
        end_date = end_of_last_month
    elif selected_period == 'this_year':
        start_of_year = now.replace(month=1, day=1, hour=0, minute=0, second=0, microsecond=0)
        # Go to next year, subtract one second
        next_year = start_of_year + relativedelta(years=1)
        end_of_year = next_year - timedelta(seconds=1)
        start_date = start_of_year
        end_date = end_of_year
    elif selected_period == 'last_year':
        end_of_last_year = now.replace(month=1, day=1, hour=0, minute=0, second=0, microsecond=0) - timedelta(seconds=1)
        start_of_last_year = end_of_last_year.replace(month=1, day=1, hour=0, minute=0, second=0, microsecond=0)
        start_date = start_of_last_year
        end_date = end_of_last_year
    # Add more specific periods like 'year_2023' if needed
    # elif selected_period == 'year_2023':
    #     start_date = datetime(2023, 1, 1, 0, 0, 0)
    #     end_date = datetime(2023, 12, 31, 23, 59, 59, 999999)

    # Apply the date filter if start_date and end_date are set
    if start_date and end_date:
        query = query.filter(Event_register.timestamp >= start_date, Event_register.timestamp <= end_date)
    # --- End Time Period Filter ---


    # Fetch the filtered events
    filtered_events = query.order_by(Event_register.timestamp.desc()).all()

    # --- Calculate Statistics based on filtered results ---
    # (Keep the existing statistics calculation logic - it works on filtered_events)
    total_count = len(filtered_events)
    early_count = 0
    late_count = 0
    absent_count = 0

    if total_count > 0:
        for event_reg in filtered_events:
            if event_reg.present:
                if event_reg.early:
                    early_count += 1
                else:
                    late_count += 1
            else:
                absent_count += 1

        early_percentage = round((early_count / total_count) * 100, 1) if total_count else 0
        late_percentage = round((late_count / total_count) * 100, 1) if total_count else 0
        absent_percentage = round((absent_count / total_count) * 100, 1) if total_count else 0
        present_count = early_count + late_count
        present_percentage = round((present_count / total_count) * 100, 1) if total_count else 0
    else:
        early_percentage = late_percentage = absent_percentage = present_percentage = 0
        present_count = 0

    stats = {
        'total_count': total_count,
        'early_count': early_count,
        'late_count': late_count,
        'absent_count': absent_count,
        'present_count': present_count,
        'early_percentage': early_percentage,
        'late_percentage': late_percentage,
        'absent_percentage': absent_percentage,
        'present_percentage': present_percentage,
    }

    # Fetch all groups for the filter dropdown
    groups = Group.query.order_by(Group.group_name).all()

    return render_template(
        'events_register.html',
        events=filtered_events,
        stats=stats,
        groups=groups,
        selected_group_id=selected_group_id,
        selected_status=selected_status,
        selected_period=selected_period  # Pass the selected period
    )

# ... (keep other routes and the rest of the app.py code)
    
@app.route('/settings', methods=['POST','GET'])
def settings():
        data = request.form
        settings = Site_settings.query.first()

        if not settings:
            settings = Site_settings()
            db.session.add(settings)

        # update field
        settings.prefix = data.get('prefix',settings.prefix)
        db.session.commit()

        return render_template('setting.html', settings = settings)


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
 

