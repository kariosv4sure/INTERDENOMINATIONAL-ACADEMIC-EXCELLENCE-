from flask import Blueprint, render_template, abort
from flask_login import login_required
from extensions import db
from models import User, Chat
from utils import admin_required

chats_bp = Blueprint('chats', __name__)


@chats_bp.route('/chats/<int:user_id>')
@login_required
@admin_required
def user_chats(user_id):
    user = db.session.get(User, user_id)
    if not user:
        abort(404)
    chats = (Chat.query.filter_by(user_id=user_id)
             .order_by(Chat.created_at.desc()).all())
    return render_template('admin/user_chats.html', user=user, chats=chats)