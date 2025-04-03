from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from livereload import Server
from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, FloatField, FileField, SubmitField
from wtforms.validators import DataRequired



app = Flask(__name__)
app.config['SECRET_KEY'] = 'my_name_is_prime'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///digital_register.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

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

    def __str__(self):
        return f'<Worker {self.first_name}>'
    

    


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

@app.route('/add_workers')
def add_workers():
    return render_template('add_workers.html')

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


# ________________________________________________________________________________________________________
# if __name__ == '__main__':
#     app.run(host='0.0.0.0', port=5000,debug=True)

# --- livereload integration ---
if __name__ == '__main__':
    with app.app_context():
        db.create_all()

    server = Server(app.wsgi_app)
    server.watch('*.py')
    # Watch all template files
    server.watch('templates/*.*')  # All files in templates and subdirectories
    server.watch('static/**/*.*')     # All static files    # Watch static files
    server.watch('**/*.*', delay=1)
    server.watch('*.html')

    
    server.serve(port=5000, host='0.0.0.0', debug=True)


