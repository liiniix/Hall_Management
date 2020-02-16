from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, validators, PasswordField, SubmitField, ValidationError
from flask_bootstrap import Bootstrap

app = Flask(__name__)
Bootstrap(app)
app.secret_key = 'abul'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'
db = SQLAlchemy(app)

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
        return True
    return False

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET','POST'])
def login():
    errors = None
    form = LoginForm()
    if request.method=='POST' and form.validate_on_submit():
        if user_pass_matched():
            return 'ok'
        else:
            errors = 'Password Error'
    return render_template('login.html', form=form, errors = errors)

@app.route('/register', methods=['GET','POST'])
def register():
    form = RegisterForm()
    if request.method=='POST' and form.validate_on_submit():
        insert_user()
        return 'ok'
    
    return render_template('register.html', form=form)
    