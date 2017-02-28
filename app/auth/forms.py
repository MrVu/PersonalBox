from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, ValidationError
from wtforms.validators import Required, Length, Email, Regexp, EqualTo, DataRequired
from ..models import User


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Length(1, 64), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember me')
    submit = SubmitField('Log In')


class RegisterForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Length(1, 64), Email()])
    username = StringField('User name',
                           validators=[DataRequired(), Length(1, 64), Regexp('^[A-Za-z][A-Za-z0-9_. ]*$', 0, 'Wrongformat')])
    password = PasswordField('Password', validators=[DataRequired(), EqualTo('password2', message="Not match")])
    password2 = PasswordField('Comfirm password', validators=[DataRequired()])
    submit = SubmitField('Register')


class EditForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Length(1, 64), Email()])
    username = StringField('User name',
                           validators=[DataRequired(), Length(1, 64), Regexp('^[A-Za-z][A-Za-z0-9_. ]*$', 0, 'Wrongformat')])
    submit = SubmitField('Submit')


class ChangePassword(FlaskForm):
    current_password = PasswordField('Password', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired(), EqualTo('password2', message="Not match")])
    password2 = PasswordField('Comfirm password', validators=[DataRequired()])
    submit = SubmitField('Submit')
