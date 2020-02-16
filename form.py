from wtforms import Form, BooleanField, StringField, validators

class RegistrationForm(Form):
    username = StringField('Username', [validators.Length(min=4,max=24)])