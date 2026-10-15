from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from flask_login import login_user, logout_user, login_required, current_user
from extensions import db, limiter
from models import User
from utils.security import clean_text

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')


@auth_bp.route('/login', methods=['GET', 'POST'])
@limiter.limit('10 per minute', methods=['POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('public.index'))

    if request.method == 'POST':
        email = clean_text(request.form.get('email', ''), max_len=120).lower()
        password = request.form.get('password', '')

        user = User.query.filter_by(email=email).first()

        # Constant-time-ish: always call check_password even when user is None
        # by short-circuiting on a dummy check. Simpler: just return the same
        # message whether email exists or password is wrong.
        if not user or not user.check_password(password):
            flash('Invalid email or password.', 'danger')
            return render_template('auth/login.html'), 401

        if not user.is_active_flag:
            flash('Account disabled. Contact admin.', 'danger')
            return render_template('auth/login.html'), 403

        login_user(user, remember=False)
        user.update_last_login()
        db.session.commit()
        session.permanent = True

        return redirect(url_for('admin.dashboard') if user.is_admin
                        else url_for('chat.dashboard'))

    return render_template('auth/login.html')


@auth_bp.route('/register', methods=['GET', 'POST'])
@limiter.limit('5 per hour', methods=['POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('public.index'))

    if request.method == 'POST':
        username = clean_text(request.form.get('username', ''), max_len=80)
        email = clean_text(request.form.get('email', ''), max_len=120).lower()
        password = request.form.get('password', '')
        confirm = request.form.get('confirm_password', '')
        full_name = clean_text(request.form.get('full_name', ''), max_len=100)
        phone = clean_text(request.form.get('phone', ''), max_len=20)

        errors = []
        if not all((username, email, password)):
            errors.append('Username, email, and password are required.')
        if len(username) < 3:
            errors.append('Username must be at least 3 characters.')
        if '@' not in email or '.' not in email.split('@')[-1]:
            errors.append('Enter a valid email.')
        if len(password) < 8:
            errors.append('Password must be at least 8 characters.')
        if password != confirm:
            errors.append('Passwords do not match.')

        if not errors:
            if User.query.filter_by(username=username).first():
                errors.append('Username already taken.')
            if User.query.filter_by(email=email).first():
                errors.append('Email already registered.')

        if errors:
            for e in errors:
                flash(e, 'danger')
            return render_template('auth/register.html'), 400

        user = User(username=username, email=email,
                    full_name=full_name or None, phone=phone or None)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()

        flash('Account created. Please sign in.', 'success')
        return redirect(url_for('auth.login'))

    return render_template('auth/register.html')


@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Signed out.', 'info')
    return redirect(url_for('public.index'))