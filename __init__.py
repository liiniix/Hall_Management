from flask import Flask, render_template, redirect, request, flash, url_for, abort
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, validators, PasswordField, SubmitField, ValidationError
from flask_bootstrap import Bootstrap
from flask_login import LoginManager, current_user, login_user, login_required, logout_user
from flask_table import Table, Col, BoolCol
from flask_migrate import Migrate
from apscheduler.schedulers.background import BackgroundScheduler

app = Flask(__name__)
Bootstrap(app)
app.secret_key = 'abul'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)
migrate = Migrate(app, db)
login_manager = LoginManager()
login_manager.init_app(app)

def increment_due():
    residential_students = User.query.filter(User.residential == True)
    for residential_student in residential_students:
        residential_student.due += 500
    db.session.commit()

scheduler = BackgroundScheduler()
job = scheduler.add_job(increment_due, 'interval', minutes=1)
scheduler.start()


class User(db.Model):
    reg = db.Column(db.String(15), primary_key=True)
    username = db.Column(db.String(80))
    email = db.Column(db.String(120))
    session = db.Column(db.String(10))
    dept = db.Column(db.String(30))
    roll = db.Column(db.Integer)
    address = db.Column(db.String(50))
    serial = db.Column(db.Integer)
    password = db.Column(db.String(50))
    residential = db.Column(db.Boolean)
    due = db.Column(db.Integer)


    def __repr__(self):
        return "<User(%s, %s, %s)>" % (self.reg, self.email, self.password)

    def is_active(self):
        return True

    def get_id(self):
        return str(self.reg)

    def is_authenticated(self):
        return True

    def is_anonymous(self):
        return False


@login_manager.user_loader
def user_loader(user_id):
    return User.query.get(user_id)



class LoginForm(FlaskForm):
    reg = StringField('Registration', validators=[validators.DataRequired()])
    password = PasswordField('Password', validators=[validators.DataRequired(),validators.Length(min=8)])
    submit = SubmitField('Submit')

    def validate_reg(self, reg):
        user = User.query.filter_by(reg=reg.data).first()
        if user is None:
            raise ValidationError('Please Register')

class RegisterForm(FlaskForm):
    reg = StringField('Registration Number', [validators.DataRequired()])
    username = StringField('Username', validators=[validators.DataRequired(),validators.Length(min=5,max=10)])
    email = StringField('Email', validators=[validators.DataRequired(),validators.Length(min=5,max=50),validators.Email()])
    session = StringField('Session', validators=[validators.DataRequired()])
    dept = StringField('Department', validators=[validators.DataRequired()])
    roll = IntegerField('Class Roll', validators=[validators.DataRequired()])
    address = StringField('Address', validators=[validators.DataRequired()])
    serial = IntegerField('Serial of Admission Test', validators=[validators.DataRequired()])
    password = PasswordField('Password', validators=[validators.DataRequired(),validators.Length(min=8)])
    
    submit = SubmitField('Submit')

    def validate_reg(self, reg):
        user = User.query.filter_by(reg=reg.data).first()
        if user is not None:
            raise ValidationError('Registered Already')

def insert_user():
    a = User(reg = request.form['reg'], 
            username = request.form['username'], 
            email = request.form['email'], 
            password = request.form['password'], 
            session = request.form['session'], 
            dept = request.form['dept'], 
            roll = request.form['roll'], 
            address = request.form['address'], 
            serial = request.form['serial'],
            residential = False,
            due = 0
    )
    db.session.add(a)
    db.session.commit()

def reg_pass_matched():
    user = User.query.filter_by(reg=request.form['reg']).first()
    if user.password == request.form['password']:
        login_user(user, remember=True)
        return True
    return False

@app.route('/')
@app.route('/index')
def index():
    if current_user.is_authenticated:
        flash('already logged in')
        #return redirect('/app/verified')
        return redirect('/verified')
    return render_template('index.html')


@app.route('/login', methods=['GET','POST'])
def login():
    if current_user.is_authenticated:
        flash('you are logged in already')
        #return redirect('/app/verified')
    form = LoginForm()
    if request.method=='POST' and form.validate_on_submit():
        if reg_pass_matched():
            flash('Login success')
            #return redirect('/app/verified')
            return redirect('/verified')
        else:
            flash('Password Error')
    return render_template('login.html', form=form)


@app.route('/register', methods=['GET','POST'])
def register():
    if current_user.is_authenticated:
        flash('You are logged in already')
        #return redirect('/app/verified')
        return redirect('/verified')
    form = RegisterForm()
    if request.method=='POST' and form.validate_on_submit():
        insert_user()
        flash('register success. Now log in')
        #return redirect('/app/login')
        return redirect('/login')
    
    return render_template('register.html', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('logout success')
    #return redirect('/app/index')
    return redirect('/index')



@app.route('/verified', methods=['GET', 'POST'])
@login_required
def verified():
    #if current_user.is_authenticated:
    if current_user.reg == 'admin':
        if request.method == 'GET':
            data = User.query.filter(User.reg != 'admin')
            return render_template('admin.html', data = data)
        else:
            req = request.form.to_dict()
            print(req)
            for key, value in req.items():
                user = User.query.get(key)
                if value == 'on':
                    user.residential = True
                else:
                    user.residential = False
                db.session.commit()

    
    return render_template('verified.html')


@app.route('/profile/<reg>')
@login_required
def profile(reg):
    user = User.query.get(reg)
    print(user)
    if user is None:
        abort(404)
    if current_user.reg == 'admin':
        return render_template('profile.html', user = user)
    if user==current_user:
        return render_template('profile.html', user = user)




if __name__ == '__main__':
    app.run()
