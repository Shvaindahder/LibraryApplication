from flask_wtf import FlaskForm

from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError

from app.models import UserAccount


class Login(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign in')


class Registration(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField('Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = UserAccount.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please, use another username')

    def validate_email(self, email):
        user = UserAccount.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please, use another email')