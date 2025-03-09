from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
from werkzeug.security import check_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user

auth = Blueprint('auth', __name__)

@auth.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        login_type = request.form.get('login_type')  
        email = request.form.get('email')
        password = request.form.get('password')

        # Check for empty fields
        if not email:
            flash('Please enter your email.', category='error')
            return render_template("login.html", user=current_user)
        if not password:
            flash('Please enter your password.', category='error')
            return render_template("login.html", user=current_user)
        
        user = User.query.filter_by(email=email).first()
        
        if user:
            if check_password_hash(user.password, password):
                # Role-based redirection
                if login_type == 'user' and user.is_admin == False:
                    login_user(user)
                    flash('Logged in successfully', category='success')
                    return redirect(url_for('views.teacher_dashboard'))
                elif login_type == 'admin' and user.is_admin == True:
                    login_user(user)
                    flash('Logged in successfully', category='success')
                    return redirect(url_for('views.admin_dashboard'))
                else:
                    flash('Access denied: invalid role for this login type.', category='error')
                    logout_user()
            else:
                flash('Incorrect password, try again.', category='error')
        else:
            flash('Email does not exist.', category='error')

    return render_template("login.html", user=current_user)



@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))
