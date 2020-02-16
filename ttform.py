from flask import Flask, request, render_template
from flask_wtf import FlaskForm
from wtforms import StringField, validators, SubmitField
from flask_bootstrap import Bootstrap

app = Flask(__name__)
Bootstrap(app)
app.secret_key = 'dswwr'

class Contact(FlaskForm):
    name = StringField('Name', validators=[validators.DataRequired(),validators.Length(min=3,max=6)])
    submit = SubmitField('Submit')

@app.route('/contact', methods=['GET','POST'])
def contact():
    form = Contact()
    if request.method=='POST' and form.validate():
        return 'ok'
    else:
        return render_template('ttcontact.html', form = form)