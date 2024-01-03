from flask import Blueprint, render_template, redirect, url_for, flash, request
from werkzeug.security import generate_password_hash, check_password_hash
from ..forms import LoginForm, RegisterForm
from ..models import User
from ..extensions import db, login_manager
from flask_login import login_user, logout_user, current_user
from dotenv import load_dotenv
import os
load_dotenv()

user_bp = Blueprint(
    'user_bp', __name__, template_folder='templates', static_folder='static'
)
salt_length = os.getenv('SALT_LENGTH')


@login_manager.user_loader
def load_user(user_id):
    return db.get_or_404(User, user_id)


@user_bp.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        result = db.session.execute(
            db.select(User).where(User.email == form.email.data))
        user_email = result.scalar()

        u_result = db.session.execute(db.select(User).where(
            User.username == form.username.data))
        user_username = u_result.scalar()

        if user_email:
            flash("You've already signed up with that email, log in instead!")
            return redirect(url_for('user_bp.login'))
        elif user_username:
            flash("That username already exists, please change username")
            return redirect(request.url)
        else:
            hashed_pwd = generate_password_hash(
                form.password.data,
                method='pbkdf2:sha256',
                salt_length=int(salt_length)
            )
            new_user = User(
                email=form.email.data,
                password=hashed_pwd,
                username=form.username.data
            )
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user)

            # TODO: redirect to blog_bp.get_all_posts
            return redirect(url_for('static_views_bp.home'))
    return render_template('register.html', form=form, current_user=current_user)


@user_bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        result = db.session.execute(
            db.select(User).where(User.email == form.email.data))
        user = result.scalar()

        if not user:
            flash("That email does not exist, please try again.")
            return redirect(request.url)
        if not check_password_hash(user.password, form.password.data):
            flash('Password incorrect, please try again.')
            return redirect(request.url)
        else:
            login_user(user)

            # TODO: redirect to blog_bp.get_all_posts
            return redirect(url_for('static_views_bp.home'))
    return render_template('login.html', form=form, current_user=current_user)


@user_bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('static_views_bp.home'))
