from flask_login import login_user, login_required, logout_user, current_user

from app import db
from app.email import send_email
from app.models import User
from . import auth
from flask import render_template, request, url_for, redirect, flash
from .forms import LoginForm, RegistrationForm, ChangePasswordForm, ResetPasswordForm, ResetPasswordRequestForm, \
    ChangeEmailForm


@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user, form.remember_me.data)
            next = request.args.get('next')
            if next is None or next.startswith('/'):
                next = url_for('main.index')
            return redirect(next)
        flash('无效的用户名或密码')
    return render_template('auth/login.html', form=form)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('登出成功')
    return redirect(url_for('main.index'))


@auth.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(email=form.email.data, username=form.username.data, password=form.password.data)
        db.session.add(user)
        db.session.commit()
        token = user.generate_confirmed_token()
        send_email(user.email, 'Confirm your accout', 'auth/email/confirm', user=user, token=token)
        flash('注册成功，邮箱验证已发送')
        return redirect(url_for('auth.login'))
    return render_template('auth/register.html', form=form)


@auth.route('/confirm/<token>')
@login_required
def confirm(token):
    if current_user.confirmed:
        return redirect(url_for('main.index'))
    if current_user.confirm(token):
        db.session.commit()
        flash('邮箱验证成功')
    else:
        flash('邮箱验证无效')
    return redirect(url_for('main.index'))


@auth.before_app_request
def before_request():
    if current_user.is_authenticated \
            and not current_user.confirmed \
            and request.blueprint != 'auth' \
            and request.endpoint != 'static':
        return redirect(url_for('auth.unconfirmed'))


@auth.route('/unconfirmed')
def unconfirmed():
    if current_user.is_anonymous or current_user.confirmed:
        return redirect(url_for('main.index'))
    return render_template('auth/unconfirmed.html')


@auth.route('/confirm')
@login_required
def resend_confirmation():
    token = current_user.genetate_confirmation_token()
    send_email(current_user.send_email, 'Confirm your Account', 'auth/email/confirm', user=current_user, token=token)
    flash('验证邮件已发送')
    return redirect(url_for('main.index'))


@auth.route('/change_password', methods=['GET', 'POST'])
@login_required
def change_password():
    form = ChangePasswordForm()
    if form.validate_on_submit():
        old_password = form.old_password.data
        if current_user.verify_password(old_password):
            current_user.password = form.password.data
            db.session.commit()
            flash('密码修改成功')
            return redirect(url_for('main.index'))
        else:
            flash('密码修改失败')
    return render_template('auth/change_password.html', form=form)


# 重置密码
@auth.route('/reset', methods=['GET', 'POST'])
def reset_password_request():
    if not current_user.is_anonymous:
        return redirect(url_for('main.index'))

    form = ResetPasswordRequestForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            token = user.generate_reset_password_token()
            send_email(user.email, '重置密码', 'auth/email/rest_password', user=user, token=token)
            flash('重置密码邮件已发送')
        return redirect(url_for('auth.login'))
    return render_template('auth/reset_password.html', form=form)


@auth.route('/reset/<token>', methods=['GET', 'POST'])
def reset_password(token):
    if not current_user.is_anonymous:
        return redirect(url_for('main.index'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        if User.password_reset(token, form.password.data):
            flash('重置密码成功')
            return redirect(url_for('auth.login'))
        else:
            return redirect(url_for('main.index'))
    return render_template('auth/reset_password.html', form=form)


@auth.route('/change_email', methods=['GET', 'POST'])
@login_required
def change_email_request():
    form = ChangeEmailForm()
    if form.validate_on_submit():
        if current_user.verify_password(form.password.data):
            # 邮箱唯一在模型类中约束过
            email = form.email.data
            token = current_user.generate_email_token(email)
            send_email(email, '更换邮箱', 'auth/email/change_email', user=current_user, token=token)
            flash('更换邮箱验证邮件已发送')
            return redirect(url_for('main.index'))
        else:
            flash('密码错误')
    return render_template('auth/change_email.html', form=form)


@auth.route('/change_email/<token>')
@login_required
def change_email(token):
    if current_user.change_email(token):
        flash('邮箱更换成功')
    else:
        flash('链接已失效，邮箱更换失败')
    return redirect(url_for('main.index'))
