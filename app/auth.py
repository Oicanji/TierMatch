from flask import Blueprint
from flask import request, render_template, url_for, redirect, flash
from flask_login import logout_user, current_user
from .models import User

auth = Blueprint('auth', __name__)

@auth.route('/login' , methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        confirmed_login = User._validate_user_login(request.form)
        if confirmed_login:
            flash('Logado com sucesso!', category='success')
            return redirect(url_for('views.home'))
    return render_template("pages/login.html", user=current_user)

@auth.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

@auth.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        confirmed_creation = User._validate_user_exists(request.form)
        if confirmed_creation:
            flash('Conta criada!', category='success')
            return redirect(url_for('views.home'))
        return render_template("pages/singup.html", user=current_user)
