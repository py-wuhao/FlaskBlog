from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, SubmitField, PasswordField
from wtforms.validators import DataRequired, Length, Email, Regexp, EqualTo, ValidationError

from app.models import User


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Length(1.64), Email()])
    password = StringField('password', validators=[DataRequired()])
    remember_me = BooleanField('keep me logged in')
    submit = SubmitField('Log In')


class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(1, 64), Regexp('^[A-Za-z][A-Za-z0-9_.]*$',0,'Usernames must have only letters, numbers, dots or underscores')])
    email = StringField('Email', validators=[DataRequired(), Length(1, 64), Email()])
    password = PasswordField('password',validators=[DataRequired(), EqualTo('password2',message='密码不匹配')])
    password2 = PasswordField('Confirm password',validators=[DataRequired()])
    submit = SubmitField('Register')

    def validate_email(self, field):
        if User.query.filter_by(email=field).first():
            raise ValidationError('邮箱已注册')

    def validate_usernaem(self,field):
        if User.query.filter_by(username=field).first():
            raise ValidationError('用户名已存在')