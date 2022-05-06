from flask import Blueprint, request, render_template, url_for, redirect, session
from flask_login import login_user, logout_user
from app.views.blue_main import blue_main
from app.models.sqlite import User
#
blue_auth = Blueprint('blue_auth', __name__, url_prefix='/auth')

@blue_auth.route('/login/', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        next_page = request.args.get('next')
        return render_template('auth_login.html', next_page=next_page)
    username = request.form.get('username')
    password = request.form.get('password')
    next_page = request.form.get('next')
    user = User.query.filter_by(username = username).first()
    if not user or not user.verify_password(password):
        return render_template('auth_login.html', warning='login failed')
    login_user(user, remember=False)
    session['username'] = user.username
    return redirect(next_page or url_for('blue_main.index'))

@blue_auth.route('/logout/')
def logout():
    logout_user()
    return redirect(url_for('blue_auth.login'))

