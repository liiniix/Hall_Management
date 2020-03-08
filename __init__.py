from flask import Flask, render_template, redirect, request, flash, url_for, abort
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, validators, PasswordField, SubmitField, ValidationError
from flask_bootstrap import Bootstrap
from flask_login import LoginManager, current_user, login_user, login_required, logout_user
from flask_table import Table, Col



app = Flask(__name__)
Bootstrap(app)
app.secret_key = 'abul'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)






class Students(db.Model):
    reg = db.Column(db.String(15), primary_key=True)
    name = db.Column(db.String(80))
    dept = db.Column(db.String(30))
    hall = db.Column(db.String(30))
    roll = db.Column(db.String(5))
    address = db.Column(db.String(50))
    merit_score = db.Column(db.String(5))

class Students_Table( Table ):
    reg = Col('Registration')
    name = Col('Name')
    dept = Col('Department')
    hall = Col('Hall')
    roll = Col('Roll')
    address = Col('Address')
    merit_score = Col('Merit Score')




class User(db.Model):
    reg = db.Column(db.String(15), primary_key=True)
    password = db.Column(db.String(50))


    def __repr__(self):
        return "<User(%s, %s)>" % (self.reg, self.password)

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


#class Information( Table ):
    



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
    password = PasswordField('Password', validators=[validators.DataRequired(),validators.Length(min=8)])
    submit = SubmitField('Submit')

    def validate_reg(self, reg):
        stu = Students.query.filter_by(reg=reg.data).first()
        if stu is None:
            raise ValidationError('Not in Student Database')

        user = User.query.filter_by(reg=reg.data).first()
        if user is not None:
            raise ValidationError('Already registered')

def insert_user():
    a = User(reg = request.form['reg'],password = request.form['password'])
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
        return redirect('/verified')
    return render_template('index.html')






@app.route('/login', methods=['GET','POST'])
def login():
    if current_user.is_authenticated:
        flash('you are logged in already')
        return redirect('/verified')
    form = LoginForm()
    if request.method=='POST' and form.validate_on_submit():
        if reg_pass_matched():
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
    return render_template('verified.html')


##gitignore

@app.route('/showall')
@login_required
def showall():
    if current_user.get_id() == 'admin':
        data = Students.query.all()
        table_data = Students_Table(data, classes=['table', 'table-striped', 'table-hover', 'h4', 'success'])
        table_data.border = True
        return render_template('showall.html',table_data = table_data)
    else:
        return "404"


@app.route('/profile')
@login_required
def profile():
    if current_user.get_id() != 'admin':
        return render_template('profile.html')

if __name__ == '__main__':
    app.run()