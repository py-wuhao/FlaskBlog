from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, SubmitField, PasswordField
from wtforms.validators import DataRequired, Length, Email, Regexp, EqualTo, ValidationError

from app.models import User


class LoginForm(FlaskForm):
    email = StringField('邮箱', validators=[DataRequired(), Length(1.64), Email()])
    password = PasswordField('密码', validators=[DataRequired()])
    remember_me = BooleanField('30天免登陆')
    submit = SubmitField('登陆')


class RegistrationForm(FlaskForm):
    username = StringField('用户名', validators=[DataRequired(), Length(1, 64), Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0,
                                                                                         'Usernames must have only letters, numbers, dots or underscores')])
    email = StringField('邮箱', validators=[DataRequired(), Length(1, 64), Email()])
    password = PasswordField('密码', validators=[DataRequired(), EqualTo('password2', message='密码不匹配')])
    password2 = PasswordField('确认密码', validators=[DataRequired()])
    submit = SubmitField('注册')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('邮箱已注册')

    def validate_usernaem(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('用户名已存在')


class ChangePasswordForm(FlaskForm):
    old_password = PasswordField('旧密码', validators=[DataRequired()])
    password = PasswordField('新密码', validators=[DataRequired(), EqualTo('password2', message='密码不匹配')])
    password2 = PasswordField('确认密码', validators=[DataRequired()])
    submit = SubmitField('提交')


class ResetPasswordRequestForm(FlaskForm):
    email = StringField('请输入邮箱', validators=[DataRequired(), Length(1, 64), Email()])
    submit = SubmitField('确认')


class ResetPasswordForm(FlaskForm):
    password = PasswordField('新密码', validators=[DataRequired(), EqualTo('password2', message='两次密码不一致')])
    password2 = PasswordField('确认密码', validators=[DataRequired()])
    submit = SubmitField('确认')


class ChangeEmailForm(FlaskForm):
    email = StringField('新邮箱', validators=[DataRequired(), Length(1, 64), Email()])
    password = PasswordField('密码', validators=[DataRequired()])
    submit = SubmitField('提交')

# class change_email()
