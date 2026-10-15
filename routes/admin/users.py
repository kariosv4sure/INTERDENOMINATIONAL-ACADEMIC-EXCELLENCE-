from flask import Blueprint, render_template, jsonify, abort, request
from flask_login import login_required
from extensions import db, csrf
from models import User, Chat
from utils import admin_required

users_bp = Blueprint('users', __name__)


@users_bp.route('/users')
@login_required
@admin_required
def list_users():
    users = (User.query.filter_by(is_admin=False)
             .order_by(User.created_at.desc()).all())
    return render_template('admin/users.html', users=users)


@users_bp.route('/users/<int:user_id>/toggle', methods=['POST'])
@login_required
@admin_required
def toggle_user(user_id):
    user = db.session.get(User, user_id)
    if not user:
        abort(404)
    if user.is_admin:
        abort(400)

    user.is_active_flag = not user.is_active_flag
    db.session.commit()
    return jsonify({'success': True, 'is_active': user.is_active_flag})


@users_bp.route('/users/<int:user_id>/delete', methods=['POST'])
@login_required
@admin_required
def delete_user(user_id):
    user = db.session.get(User, user_id)
    if not user:
        abort(404)
    if user.is_admin:
        abort(400)

    db.session.delete(user)   # cascade handles chats
    db.session.commit()
    return jsonify({'success': True})