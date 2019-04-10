from flask import render_template, flash, redirect, url_for, request
from flask_login import login_user, logout_user

from app import db
from app.models import UserAccount
from app.auth import bp
from app.auth.forms import Registration, Login

from werkzeug.urls import url_parse


@bp.route('/registration', methods=['GET', 'POST'])
def register():
    form = Registration()
    if form.validate_on_submit():
        user = UserAccount(form.username.data, form.email.data)
        user.password = user.set_password_hash(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Registration completed successfully!')
        return redirect(url_for('auth.login'))
    return render_template('auth/registration.html', form=form)


@bp.route('/auth', methods=['GET', 'POST'])
def login():
    form = Login()
    if form.validate_on_submit():
        user = UserAccount.query.filter_by(username=form.username.data).first()
        if not user or user.check_password(form.password.data) == False:
            flash('Incorrect username or password. Try again!')
            return redirect(url_for('auth.login'))
        else:
            login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != None:
            next_page = url_for('main.index')
        return redirect(next_page)
    return render_template('auth/login.html', form=form, headline='Sign in', col_md_pos=2)


@bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('auth.login'))



