from datetime import datetime, timedelta, timezone
from flask import Blueprint, render_template
from flask_login import login_required
from extensions import db
from models import User, Chat
from utils import admin_required

dashboard_bp = Blueprint('dashboard', __name__)


@dashboard_bp.route('/')
@login_required
@admin_required
def dashboard():
    now = datetime.now(timezone.utc)

    total_users = User.query.filter_by(is_admin=False).count()
    total_chats = Chat.query.count()
    active_today = User.query.filter(
        User.last_login >= now - timedelta(days=1)
    ).count()

    user_growth = []
    for i in range(6, -1, -1):
        d = now - timedelta(days=i)
        start = d.replace(hour=0, minute=0, second=0, microsecond=0)
        end = d.replace(hour=23, minute=59, second=59, microsecond=999999)
        count = User.query.filter(
            User.created_at >= start,
            User.created_at <= end,
            User.is_admin.is_(False),
        ).count()
        user_growth.append({'date': d.strftime('%b %d'), 'count': count})

    return render_template('admin/dashboard.html',
                           total_users=total_users,
                           total_chats=total_chats,
                           active_today=active_today,
                           user_growth=user_growth,
                           recent_users=(User.query.filter_by(is_admin=False)
                                         .order_by(User.created_at.desc())
                                         .limit(10).all()),
                           recent_chats=(Chat.query
                                         .order_by(Chat.created_at.desc())
                                         .limit(20).all()))