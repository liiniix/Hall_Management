from flask import Flask, request, render_template
from flask_wtf import FlaskForm
from wtforms import TextField, validators, ValidationError, SubmitField
from flask_bootstrap import Bootstrap

app = Flask(__name__)
Bootstrap(app)

app.secret_key = 'devvelopment key'

class ContactForm(FlaskForm):
    name = TextField("Name of Student", [validators.DataRequired(),validators.Length(min=6, max=35)])
    submit = SubmitField("send")


@app.route('/contact', methods=['GET','POST'])
def contact():
    form = ContactForm()
    if request.method == 'POST':
        if form.validate() == False:
            return render_template('contact.html', form = form)
        else:
            return render_template('success.html',  request = request)
    elif request.method == 'GET':
        return render_template('contact.html', form = form)
