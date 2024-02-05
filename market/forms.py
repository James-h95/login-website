# Forms to be displayed on templates
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, PasswordField, SubmitField


class RegisterForm(FlaskForm):
    username = StringField(label='username')
    email = StringField(label='email')
    password1 = PasswordField(label='password1')
    password2 = PasswordField(label='password2')
    submit = SubmitField(label='submit')