from . import auth
from .. import db
from ..models import User
from .. import functions, email
from flask import render_template, redirect, url_for, request, flash, abort
from .forms import LoginForm, RegisterForm, EditForm, ChangePassword, ForgotPassword, EmailResetPassword
from flask_login import login_required, logout_user, login_user, current_user


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    login_form = LoginForm()
    if login_form.validate_on_submit():
        email = login_form.email.data
        user = User.query.filter_by(email=email).first()
        if user is not None and user.verify_password(login_form.password.data):
            login_user(user, login_form.remember_me.data)
            return redirect(url_for('main.root'))
        flash('Invalid username or password.')
    return render_template('login.html', login_form=login_form)


@auth.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    register_form = RegisterForm()
    while True:
        random = functions.RandomID()
        if User.query.filter_by(userkey=random).first() is not None:
            continue
        else:
            break
    if register_form.validate_on_submit():
        user = User.query.filter_by(email=register_form.email.data).first()
        if user is None:
            user = User(email=register_form.email.data,
                        username=register_form.username.data,
                        password=register_form.password.data, userkey=random)
            db.session.add(user)
            db.session.commit()
            token = user.generate_confirm_token()
            email.send_email(user.email, 'Confirm Your Acccount', 'mails/confirm', username=user.username, token=token)
            flash("An email is sent to your account, please confirm")
            if not functions.Installed(user.userkey):
                functions.Install(user.userkey)
            return redirect(url_for('auth.login'))
        else:
            flash('Email is already taken')
            return redirect(url_for('auth.register'))
    return render_template('register.html', register_form=register_form)


@auth.route('/auth/profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    edit_form = EditForm()
    if edit_form.validate_on_submit():
        current_user.email = edit_form.email.data
        current_user.username = edit_form.username.data
        db.session.add(current_user)
        db.session.commit()
        return redirect(url_for('auth.edit_profile'))
    edit_form.email.data = current_user.email
    edit_form.username.data = current_user.username
    return render_template('edit_profile.html', edit_form=edit_form)


@auth.route('/auth/changepassword', methods=['GET', 'POST'])
@login_required
def change_password():
    password_form = ChangePassword()
    if password_form.validate_on_submit():
        if current_user.verify_password(password_form.current_password.data):
            current_user.password = password_form.password.data
            db.session.add(current_user)
            db.session.commit()
            flash('Your Password is changed')
            return redirect(url_for('auth.change_password'))
        else:
            flash('Your Password is incorrect')
            return redirect(url_for('auth.change_password'))
    return render_template('change_password.html', password_form=password_form)


@auth.route('/auth/forgot?email', methods=['GET', 'POST'])
def get_forgot_email():
    email_form = EmailResetPassword()
    if email_form.validate_on_submit():
        user = User.query.filter_by(email=email_form.email.data).first()
        if user is not None:
            token = user.generate_confirm_token()
            email.send_email(user.email, 'Reset Your Password', 'mails/reset_password', username=user.username, token=token)
            flash("An email is sent to your account to reset your password")
            return redirect(url_for('auth.get_forgot_email'))
        else:
            flash('Sorry, we cannot find your email')
        return redirect(url_for('auth.get_forgot_email'))
    return render_template('forgot_email.html', email_form=email_form)


@auth.route('/auth/password/<string:token>', methods=['GET', 'POST'])
def reset_password(token):
    user_id = User.token_load(token)
    user = User.query.get(user_id)
    login_user(user)
    forgot_password_form = ForgotPassword()
    if forgot_password_form.validate_on_submit():
        user.password = forgot_password_form.password.data
        db.session.add(user)
        db.session.commit()
        flash('Your password has been changed')
        return redirect(url_for('main.index'))
    return render_template('forgot_password.html', forgot_password_form=forgot_password_form)


@auth.route('/auth/confirm/<string:token>')
def confirm(token):
    if User.confirm(token):
        flash('You have confirmed your account, now you can login. Thanks!')
    else:
        flash('The confirmation link is invalid or has expired.')
    return redirect(url_for('auth.login'))


@auth.route('/auth/resend?email')
def resend_email():
    user = current_user._get_current_object()
    token = user.generate_confirm_token()
    email.send_email(user.email, 'Confirm Your Account', 'mails/confirm', username=user.username, token=token)
    return redirect(url_for('main.index'))


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.')
    return redirect(url_for('auth.login'))
