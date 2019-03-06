from wtforms import Form, BooleanField, StringField, PasswordField, validators

class RegistrationForm(Form):
    first_name = StringField('First Name', [validators.Length(min=4, max=25)])
    username = StringField('Username', [validators.Length(min=4, max=25)])
    last_name = StringField('Last Name', [validators.Length(min=4, max=25)])
    # username = StringField('Username', [validators.Length(min=4, max=25)])
    email = StringField('Email Address', [validators.Length(min=6, max=35)])
    password = PasswordField('New Password', [
        validators.DataRequired(),
        validators.EqualTo('password_repeat', message='Passwords must match')
    ])
    password_repeat = PasswordField('Repeat Password')
    # accept_tos = BooleanField('I accept the TOS', [validators.DataRequired()])