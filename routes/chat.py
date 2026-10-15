from flask import Blueprint, render_template, request, jsonify
from flask_login import login_required, current_user
from extensions import db, limiter
from models import Chat
from services import AIService
from utils.security import clean_text

chat_bp = Blueprint('chat', __name__)


@chat_bp.route('/dashboard')
@login_required
def dashboard():
    chats = (Chat.query
             .filter_by(user_id=current_user.id)
             .order_by(Chat.created_at.desc())
             .limit(20).all())
    total = Chat.query.filter_by(user_id=current_user.id).count()
    return render_template('user/dashboard.html',
                           chats=chats, total_chats=total)


@chat_bp.route('/chat', methods=['GET', 'POST'])
@login_required
@limiter.limit('30 per hour', methods=['POST'])
def chat():
    if request.method == 'POST':
        message = clean_text(request.form.get('message', ''), max_len=2000)
        if not message:
            return jsonify({'error': 'Message is required'}), 400

        reply = AIService.get_response(message, current_user.username)
        record = Chat(user_id=current_user.id,
                      user_message=message, bot_response=reply)
        db.session.add(record)
        db.session.commit()

        return jsonify({
            'response': reply,
            'chat_id': record.id,
            'timestamp': record.created_at.strftime('%Y-%m-%d %H:%M:%S'),
        })

    history = (Chat.query
               .filter_by(user_id=current_user.id)
               .order_by(Chat.created_at).all())
    return render_template('user/chat.html', history=history)