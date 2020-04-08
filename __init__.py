from flask import Flask, render_template, redirect, request, flash, url_for, abort
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, validators, DecimalField, TextAreaField, PasswordField, SubmitField, ValidationError, Label
from flask_bootstrap import Bootstrap
from flask_login import LoginManager, current_user, login_user, login_required, logout_user
from flask_table import Table, Col, LinkCol,ButtonCol
#from werkzeug.middleware.dispatcher import DispatcherMiddleware
#from werkzeug.serving import run_simple


app = Flask(__name__)
Bootstrap(app)
app.secret_key = 'abul'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
#app.config["APPLICATION_ROOT"] = "/app"
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
    due = db.Column(db.Integer())

    def __lt__(self, other):
         return self.reg < other.reg

class Students_Table( Table ):
    reg = Col('Registration', column_html_attrs={'class': 'border border-info'})
    name = Col('Name', column_html_attrs={'class': 'border border-info'})
    dept = Col('Department', show=False)
    hall = Col('Hall', show=False)
    roll = Col('Roll', show=False)
    address = Col('Address', show=False)
    merit_score = Col('Merit Score', show=False)
    seat_info = Col('Seat Info', column_html_attrs={'class': 'border border-info'})
    due = Col('Due', column_html_attrs={'class': 'border border-info'})
    allot = LinkCol('Allot', 'allot', url_kwargs=dict(id='reg'), anchor_attrs={'class': 'btn btn-outline-info'}, column_html_attrs={'class': 'border border-info'})
    show_details = LinkCol('Details', 'allot', url_kwargs=dict(id='reg'), anchor_attrs={'class': 'btn btn-info'}, column_html_attrs={'class': 'border border-info'})



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

class Bkash(db.Model):
    id = db.Column(db.String(20), primary_key=True)
    amount = db.Column(db.Integer())


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
            flash('Not in student database')
            raise ValidationError('Not in Student Database')

        user = User.query.filter_by(reg=reg.data).first()
        if user is not None:
            flash('Already registered')
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
        return redirect(url_for('index'))
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
        return redirect(url_for('index'))
    return render_template('update.html', post = post, form=form)



@app.route('/login', methods=['GET','POST'])
def login():
    if current_user.is_authenticated:
        flash('you are logged in already')
        return redirect(url_for('verified'))
    form = LoginForm()
    if request.method=='POST' and form.validate_on_submit():
        if reg_pass_matched():
            flash('Login success')
            return redirect(url_for('index'))
        else:
            flash('Password Error')
    return render_template('login.html', form=form)




@app.route('/register', methods=['GET','POST'])
def register():
    if current_user.is_authenticated:
        flash('You are logged in already')
        return redirect(url_for('verified'))
    form = RegisterForm()
    if request.method=='POST' and form.validate_on_submit():
        insert_user()
        flash('register success. Now log in')
        return redirect(url_for('login'))
    
    return render_template('register.html', form=form)
    


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('logout success')
    return redirect(url_for('index'))

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
        table_data = Students_Table(data, classes=['h6', 'table', 'table-striped', 'table-hover', 'info'], thead_classes=["bg-info"])
        return render_template('showall.html',table_data = table_data)
    else:
        abort(404)
        return "404"


class Bkash_Table( Table ):
    id = Col('ID', column_html_attrs={'class': 'border border-info'})
    amount = Col('Amount', column_html_attrs={'class': 'border border-info'})
    

@app.route('/showtran', methods=['GET','POST'])
@login_required
def showtran():
    if current_user.get_id() == 'admin':
        data = Bkash.query.all()
        table_data = Bkash_Table(data, classes=['h6', 'table', 'table-striped', 'table-hover', 'info', 'border',  'border-info'], thead_classes=["bg-info"])
        return render_template('showtran.html',table_data = table_data)
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
        due = StringField('Due', render_kw={'readonly': True, 'placeholder': "%s" % data.due})
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
            db.session.add(Posts(title="Allotment", body=stu.reg + " alloted at seat " + request.form['seat_info']))
            db.session.commit()
            flash("Seat Alloted")
            return redirect(url_for('showall'))
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
        return redirect(url_for('allot', id="%s" % current_user.get_id()))

class Pay_Form(FlaskForm):
    id = StringField('Bkash ID', validators=[validators.DataRequired()])
    amount = DecimalField('Amount', validators=[validators.DataRequired(), validators.NumberRange(min=0, max=10000, message="Decimal from 0 to 10000")])
    Pay = SubmitField('Pay')

    def validate_id(self, id):
        print(id.data)
        bk = Bkash.query.filter_by(id=id.data).first()
        if bk is None:
            flash('Not in Bkash payment database')
            raise ValidationError('Not in Bkash payment Database')

@login_required 
@app.route('/pay/<id>', methods=['GET', 'POST'])
def pay(id):
    if current_user.get_id() ==id and current_user.get_id != 'admin':
        form = Pay_Form()
        if request.method=='GET':
            return render_template('pay.html', form=form)
        elif request.method=='POST' and form.validate_on_submit():
            bk = Bkash.query.filter_by(id=request.form['id']).first()
            if bk.amount < float(request.form['amount']):
                flash("Less money available")
                return render_template('pay.html', form=form)

            stu = Students.query.filter_by(reg=id).first()
            payable = min(stu.due, float(request.form['amount']))
            stu.due = stu.due - payable

            bk.amount = bk.amount - payable
            if bk.amount <=0:
                db.session.delete(bk)
                db.session.commit()
            print(payed)
            db.session.add(Posts(title="Payment", body=stu.reg + " payed " + str(payable) ))
            db.session.commit()
            flash("Payed")
            return redirect(url_for('index'))
        else:
            return render_template('pay.html', form=form)
    else:
        abort(404)



def simple(env, resp):
    resp(b'200 OK', [(b'Content-Type', b'text/plain')])
    return [b'Hello WSGI World']

#app.wsgi_app = DispatcherMiddleware(simple, {'/app': app.wsgi_app})



if __name__ == '__main__':
    app.run()