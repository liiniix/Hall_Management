from flask import Flask, render_template, redirect, request, flash, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, validators, PasswordField, SubmitField, ValidationError
from flask_bootstrap import Bootstrap
from flask_login import LoginManager, current_user, login_user, login_required, logout_user

app = Flask(__name__)
Bootstrap(app)
app.secret_key = 'abul'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////home/thaki/ABUL/Hall_Management/test.py'
db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)






class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80))
    email = db.Column(db.String(120))
    password = db.Column(db.String(50))

    def __init__(self, un, em, pas):
        self.username = un
        self.email = em
        self.password = pas

    def __repr__(self):
        return "<User(%s, %s, %s)>" % (self.username, self.email, self.password)

    def is_active(self):
        return True

    def get_id(self):
        return str(self.id)

    def is_authenticated(self):
        return True

    def is_anonymous(self):
        return False


@login_manager.user_loader
def user_loader(user_id):
    return User.query.get(int(user_id))



class LoginForm(FlaskForm):
    username = StringField('Username', validators=[validators.DataRequired(),validators.Length(min=5,max=10)])
    password = PasswordField('Password', validators=[validators.DataRequired(),validators.Length(min=8)])
    submit = SubmitField('Submit')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is None:
            raise ValidationError('Please Register')



class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[validators.DataRequired(),validators.Length(min=5,max=10)])
    email = StringField('Email', validators=[validators.DataRequired(),validators.Length(min=5,max=50),validators.Email()])
    password = PasswordField('Password', validators=[validators.DataRequired(),validators.Length(min=8)])
    submit = SubmitField('Submit')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')

def insert_user():
    a = User(request.form['username'], request.form['email'], request.form['password'])
    db.session.add(a)
    db.session.commit()

def user_pass_matched():
    user = User.query.filter_by(username=request.form['username']).first()
    if user.password == request.form['password']:
        login_user(user, remember=True)
        return True
    return False

@app.route('/')
@app.route('/index')
def index():
    if current_user.is_authenticated:
        flash('already logged in')
        return redirect('/verified')
    return render_template('index.html')






@app.route('/login', methods=['GET','POST'])
def login():
    if current_user.is_authenticated:
        flash('you are logged in already')
        return redirect('/verified')
    form = LoginForm()
    if request.method=='POST' and form.validate_on_submit():
        if user_pass_matched():
            flash('Login success')
            return redirect('/verified')
        else:
            flash('Password Error')
    return render_template('login.html', form=form)



@app.route('/register', methods=['GET','POST'])
def register():
    if current_user.is_authenticated:
        flash('You are logged in already')
        return redirect('/verified')
    form = RegisterForm()
    if request.method=='POST' and form.validate_on_submit():
        insert_user()
        flash('register success. Now log in')
        return redirect('/login')
    
    return render_template('register.html', form=form)
    


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('logout success')
    return redirect('/index')

@app.route('/verified')
@login_required
def verified():
    return render_template('/verified.html')