from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, current_user
from extensions import limiter
from models import User

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['GET', 'POST'])
@limiter.limit('10 per minute', methods=['POST'])
def login():
    if current_user.is_authenticated and current_user.is_admin:
        return redirect(url_for('admin.dashboard.dashboard'))

    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')

        admin = User.query.filter_by(is_admin=True).first()
        if admin and admin.username == username and admin.check_password(password):
            login_user(admin)
            flash('Admin signed in.', 'success')
            return redirect(url_for('admin.dashboard.dashboard'))
        flash('Invalid admin credentials.', 'danger')

    return render_template('admin/login.html')