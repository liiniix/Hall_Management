from flask import Flask, request, render_template
from flask_wtf import FlaskForm
from wtforms import StringField, validators, SubmitField
from flask_bootstrap import Bootstrap

class ContactForm(FlaskForm):
    name = StringField("Name", validators=[validators.DataRequired(),validators.Length(min=4,max=24)])
    submit = SubmitField("Submit")

app = Flask(__name__)
Bootstrap(app)
app.secret_key = 'devvelopment key'

@app.route('/contact', methods=['GET','POST'])
def contact():
    print(request.headers)
    form = ContactForm()
    if request.method == 'GET':
        return render_template('fcontact.html', form=form)
    elif request.method == 'POST':
        if form.validate():
            return "OK"
        else:
            return render_template('fcontact.html', form=form)