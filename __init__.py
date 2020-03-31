from flask import Flask, render_template, redirect, request, flash, url_for, abort
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, validators, TextAreaField, PasswordField, SubmitField, ValidationError, Label
from flask_bootstrap import Bootstrap
from flask_login import LoginManager, current_user, login_user, login_required, logout_user
from flask_table import Table, Col, LinkCol,ButtonCol



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
    seat_info = db.Column(db.String(100))

    def __lt__(self, other):
         return self.reg < other.reg

class Students_Table( Table ):
    reg = Col('Registration')
    name = Col('Name')
    dept = Col('Department')
    hall = Col('Hall')
    roll = Col('Roll')
    address = Col('Address')
    merit_score = Col('Merit Score')
    seat_info = Col('Seat Info')
    allot = LinkCol('Allot', 'allot', url_kwargs=dict(id='reg'), anchor_attrs={'class': 'btn btn-outline-success'})




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
            flash("You are not registered")
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

import datetime
class Posts(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(13))
    body = db.Column(db.String(100))
    time = db.Column(db.DateTime, default=db.func.now())


@app.route('/')
@app.route('/index')
def index():
    posts = None
    if current_user.is_authenticated:
        posts = Posts.query.all()
    return render_template('index.html', posts=posts)


class CreateForm(FlaskForm):
    title = StringField('Title', validators=[validators.DataRequired()])
    body = TextAreaField('Body')
    save = SubmitField('Save')


@app.route('/create', methods=['GET', 'POST'])
def create():
    form = CreateForm()
    if request.method == 'POST' and form.validate_on_submit():
        db.session.add(Posts(title = request.form['title'], body = request.form['body']))
        db.session.commit()
        return redirect('/index')
    return render_template('create.html', form=form)


def UpdateForm(post):
    class updateform(FlaskForm):
        title = StringField('Title', validators=[validators.DataRequired()], render_kw={'value': "%s"%post.title})
        body = TextAreaField('Body', default = "%s"%post.body)
        save = SubmitField('Save')
    return updateform()

@app.route('/update/<int:id>', methods=['GET','POST'])
def update(id):
    post = Posts.query.filter_by(id=id).first()
    form = UpdateForm(post)
    if request.method=='POST':
        if request.form['save']=='Delete':
            db.session.delete(post)
            db.session.commit()
        else:
            post.title = request.form['title']
            post.body = request.form['body']
            db.session.commit()
        return redirect('/index')
    return render_template('update.html', post = post, form=form)



@app.route('/login', methods=['GET','POST'])
def login():
    if current_user.is_authenticated:
        flash('you are logged in already')
        return redirect('/verified')
    form = LoginForm()
    if request.method=='POST' and form.validate_on_submit():
        if reg_pass_matched():
            flash('Login success')
            return redirect('/')
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

@app.route('/showall', methods=['GET','POST'])
@login_required
def showall():
    if current_user.get_id() == 'admin':
        data = Students.query.all()
        if request.method=='POST':
            if request.form['submit']=='Sort':
                flash('Table sorted')
                data.sort()
        table_data = Students_Table(data, classes=['table', 'table-striped', 'table-hover', 'success'], thead_classes=["bg-success"])
        table_data.border = True
        return render_template('showall.html',table_data = table_data)
    else:
        abort(404)
        return "404"

def allotform(data):
    class AllotForm(FlaskForm):
        reg = StringField('Registration No', render_kw={'readonly': True, 'placeholder': "%s" % data.reg})
        name = StringField('Name', render_kw={'class ':'border-0', 'readonly': True, 'placeholder': "%s" % data.name})
        dept = StringField('Dept', render_kw={'readonly': True, 'placeholder': "%s" % data.dept})
        hall = StringField('Hall', render_kw={'readonly': True, 'placeholder': "%s" % data.hall})
        roll = StringField('Roll', render_kw={'readonly': True, 'placeholder': "%s" % data.roll})
        address = StringField('Address', render_kw={'readonly': True, 'placeholder': "%s" % data.address})
        merit_score = StringField('Merit_score', render_kw={'readonly': True, 'placeholder': "%s" % data.merit_score})
        seat_info = StringField('Update Seat Information')
        submit = SubmitField('Submit')
    return AllotForm()


@login_required 
@app.route('/item/<id>', methods=['GET', 'POST'])
def allot(id):
    if current_user.get_id()=='admin':
        if request.method=='GET':
            stu = Students.query.filter_by(reg=id).first()
            form = allotform(data=stu)
            return render_template('allot.html', form=form)
        elif request.method=='POST':
            stu = Students.query.filter_by(reg=id).first()
            stu.seat_info = request.form['seat_info']
            db.session.commit()
            return redirect('/showall')
    elif current_user.get_id() == id:
        if request.method=='GET':
            stu = Students.query.filter_by(reg=id).first()
            form = allotform(data=stu)
            form.seat_info.render_kw = {'readonly': True}
            form.submit.render_kw = {'type':"hidden"}
            form.seat_info.label.text = "Seat Information"
            return render_template('allot.html', form=form)
    else:
        abort(404)

@app.route('/profile')
@login_required
def profile():
    if current_user.get_id() != 'admin':
        return redirect("/item/%s" % current_user.get_id())

if __name__ == '__main__':
    app.run()