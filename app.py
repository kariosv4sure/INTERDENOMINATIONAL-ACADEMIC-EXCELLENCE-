import os
import requests
from functools import wraps
from datetime import datetime, timedelta, timezone
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from dotenv import load_dotenv

# Import models
from models import db, User, Chat

# ========================================
# APP INITIALIZATION
# ========================================
load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-key-change-me')
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///iae.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize extensions
db.init_app(app)

login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message = 'Please login to access this page.'

# ========================================
# DECORATORS
# ========================================
def admin_required(f):
    """Decorator to require admin privileges"""
    @wraps(f)
    def decorated(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.is_admin:
            flash('Admin access required.', 'danger')
            return redirect(url_for('index'))
        return f(*args, **kwargs)
    return decorated

# ========================================
# USER LOADER
# ========================================
@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))

# ========================================
# AI SERVICE
# ========================================
class AIService:
    """Handle AI responses with fallback"""

    @staticmethod
    def get_response(user_message, username):
        api_key = os.environ.get('GROQ_API_KEY')

        if not api_key:
            return AIService._get_fallback(user_message, username)

        try:
            response = requests.post(
                os.environ.get('GROQ_API_URL', 'https://api.groq.com/openai/v1/chat/completions'),
                headers={
                    'Authorization': f'Bearer {api_key}',
                    'Content-Type': 'application/json'
                },
                json={
                    'model': 'openai/gpt-oss-120b',
                    'messages': [
                        {'role': 'system', 'content': AIService._system_prompt()},
                        {'role': 'user', 'content': user_message}
                    ],
                    'temperature': 0.7,
                    'max_tokens': 500
                },
                timeout=30
            )
            response.raise_for_status()
            return response.json()['choices'][0]['message']['content']

        except requests.exceptions.Timeout:
            return AIService._get_fallback(user_message, username) + "\n\n*Note: Response generated offline due to timeout.*"
        except Exception as e:
            print(f"AI Error: {e}")
            return AIService._get_fallback(user_message, username)

    @staticmethod
    def _system_prompt():
        """Full system prompt with I.A.E context"""
        return """You are I.A.E Assistant, the official AI helper for INTERDENOMINATIONAL ACADEMIC EXCELLENCE (I.A.E™), founded by Mr. Daniel Moses, a passionate educator with over 12 years of experience helping Nigerian students achieve academic success.

About I.A.E:
- Founded by Mr. Daniel Moses to provide quality education to Nigerian students
- Specializes in JAMB, WAEC, NECO, and admission guidance
- Has helped over 25,000 students gain admission to universities
- Known for excellence, integrity, and personalized mentorship

Your personality:
- Friendly, encouraging, and professional
- Keep responses concise (2-3 paragraphs max)
- Always mention Mr. Daniel or I.A.E when relevant to the conversation
- Focus on Nigerian education context (JAMB, WAEC, Post-UTME, university admissions)
- Provide practical, actionable advice

Remember: You represent I.A.E, founded by Mr. Daniel Moses. Be helpful, knowledgeable, and inspiring!"""

    @staticmethod
    def _get_fallback(user_message, username):
        """Fallback responses when API is unavailable"""
        msg = user_message.lower()

        # Founder mentions
        if any(w in msg for w in ['founder', 'mr daniel', 'owner', 'who created']):
            return "I.A.E™ was founded by Mr. Daniel Moses, a passionate educator with over 12 years of experience. His vision was to create a platform that helps Nigerian students achieve academic excellence through personalized mentorship and quality resources. Mr. Daniel personally oversees our programs and remains committed to every student's success! 🎓"

        # I.A.E questions
        if any(w in msg for w in ['what is iae', 'iae', 'your company']):
            return "I.A.E™ (INTERDENOMINATIONAL ACADEMIC EXCELLENCE) is Nigeria's trusted academic partner, founded by Mr. Daniel Moses. We specialize in JAMB, WAEC, and admission guidance, having helped over 25,000 students achieve their academic dreams. Our founder, Mr. Daniel, brings over 12 years of educational expertise to ensure every student succeeds! 📚"

        # JAMB
        if 'jamb' in msg:
            return "For JAMB success, I.A.E™ (founded by Mr. Daniel Moses) recommends: 1) Start early with past questions, 2) Focus on your weak subjects, 3) Take mock exams, 4) Join our tutorial program! We've helped thousands score 280+. Would you like to know more about our JAMB preparation packages? 🎯"

        # WAEC
        if 'waec' in msg:
            return "WAEC preparation with I.A.E™ (established by Mr. Daniel Moses) focuses on: past question analysis, time management, and intensive mock exams. Our students consistently achieve excellent results! Ready to join our WAEC success program? 📝"

        # Admissions
        if any(w in msg for w in ['admission', 'university']):
            return "Getting admission in Nigeria can be challenging, but I.A.E™ (founded by Mr. Daniel Moses) has helped over 6,200 students secure university placements. We offer personalized admission guidance, course selection help, and CAPS support. Let me know your preferred course and I'll guide you! 🏛️"

        # Greetings
        if any(w in msg for w in ['hello', 'hi', 'hey', 'good morning']):
            return f"Hello {username}! Welcome to I.A.E™, founded by Mr. Daniel Moses. I'm your AI academic assistant. Whether you need help with JAMB, WAEC, or admission guidance, I'm here to help! What would you like to know today? 😊"

        # Default
        return f"Thank you for reaching out to I.A.E™, founded by Mr. Daniel Moses! I'm here to help you with any academic questions. Could you please specify what you'd like assistance with? Whether it's JAMB, WAEC, admission guidance, or general study tips, I'm ready to help! 📚✨"

# ========================================
# PUBLIC ROUTES
# ========================================
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/services')
def services():
    return render_template('services.html')

@app.route('/jamb')
def jamb():
    return render_template('jamb.html')

@app.route('/waec')
def waec():
    return render_template('waec.html')

@app.route('/testimonials')
def testimonials():
    return render_template('testimonials.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/feedback')
def feedback():
    return render_template('feedback.html')

# ========================================
# AUTH ROUTES
# ========================================
@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))

    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user = User.query.filter_by(email=email).first()

        if user and user.check_password(password):
            if user.is_active:
                login_user(user)
                user.last_login = datetime.now(timezone.utc)
                db.session.commit()
                flash('Welcome back!', 'success')
                return redirect(url_for('admin_dashboard' if user.is_admin else 'dashboard'))
            flash('Account disabled. Contact admin.', 'danger')
        else:
            flash('Invalid email or password.', 'danger')

    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))

    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm = request.form.get('confirm_password')

        # Validation
        if not all([username, email, password]):
            flash('All fields are required.', 'danger')
            return render_template('register.html')

        if password != confirm:
            flash('Passwords do not match.', 'danger')
            return render_template('register.html')

        if len(password) < 6:
            flash('Password must be at least 6 characters.', 'danger')
            return render_template('register.html')

        if User.query.filter_by(username=username).first():
            flash('Username already taken.', 'danger')
            return render_template('register.html')

        if User.query.filter_by(email=email).first():
            flash('Email already registered.', 'danger')
            return render_template('register.html')

        # Create user
        user = User(
            username=username,
            email=email,
            full_name=request.form.get('full_name'),
            phone=request.form.get('phone')
        )
        user.set_password(password)
        db.session.add(user)
        db.session.commit()

        flash('Registration successful! Please login.', 'success')
        return redirect(url_for('login'))

    return render_template('register.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Logged out successfully.', 'info')
    return redirect(url_for('index'))

# ========================================
# DASHBOARD & CHAT
# ========================================
@app.route('/dashboard')
@login_required
def dashboard():
    chats = Chat.query.filter_by(user_id=current_user.id).order_by(Chat.created_at.desc()).limit(20).all()
    total_chats = Chat.query.filter_by(user_id=current_user.id).count()
    return render_template('dashboard.html', 
                         chats=chats, 
                         total_chats=total_chats,
                         user=current_user)

@app.route('/chat', methods=['GET', 'POST'])
@login_required
def chat():
    if request.method == 'POST':
        message = request.form.get('message', '').strip()
        if not message:
            return jsonify({'error': 'Message is required'}), 400

        # Get AI response
        response = AIService.get_response(message, current_user.username)

        # Save chat
        chat = Chat(
            user_id=current_user.id,
            user_message=message,
            bot_response=response
        )
        db.session.add(chat)
        db.session.commit()

        return jsonify({
            'response': response,
            'chat_id': chat.id,
            'timestamp': chat.created_at.strftime('%Y-%m-%d %H:%M:%S')
        })

    # GET - Show chat page with history
    history = Chat.query.filter_by(user_id=current_user.id).order_by(Chat.created_at).all()
    return render_template('chat.html', history=history)

# ========================================
# ADMIN ROUTES
# ========================================
@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    if current_user.is_authenticated and current_user.is_admin:
        return redirect(url_for('admin_dashboard'))

    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        admin = User.query.filter_by(is_admin=True).first()

        if admin and admin.username == username and admin.check_password(password):
            login_user(admin)
            flash('Admin login successful!', 'success')
            return redirect(url_for('admin_dashboard'))
        flash('Invalid admin credentials.', 'danger')

    return render_template('admin_login.html')

@app.route('/admin')
@login_required
@admin_required
def admin_dashboard():
    # Stats
    total_users = User.query.filter_by(is_admin=False).count()
    total_chats = Chat.query.count()
    active_today = User.query.filter(
        User.last_login >= datetime.now(timezone.utc) - timedelta(days=1)
    ).count()

    # User growth (last 7 days)
    user_growth = []
    for i in range(6, -1, -1):
        date = datetime.now(timezone.utc) - timedelta(days=i)
        start = datetime(date.year, date.month, date.day, 0, 0, 0, tzinfo=timezone.utc)
        end = datetime(date.year, date.month, date.day, 23, 59, 59, tzinfo=timezone.utc)
        count = User.query.filter(
            User.created_at >= start,
            User.created_at <= end,
            User.is_admin == False
        ).count()
        user_growth.append({'date': date.strftime('%b %d'), 'count': count})

    return render_template('admin_dashboard.html',
        total_users=total_users,
        total_chats=total_chats,
        active_today=active_today,
        user_growth=user_growth,
        recent_users=User.query.filter_by(is_admin=False).order_by(User.created_at.desc()).limit(10).all(),
        recent_chats=Chat.query.order_by(Chat.created_at.desc()).limit(20).all()
    )

@app.route('/admin/users')
@login_required
@admin_required
def admin_users():
    users = User.query.filter_by(is_admin=False).order_by(User.created_at.desc()).all()
    return render_template('admin_users.html', users=users)

@app.route('/admin/users/<int:user_id>/toggle')
@login_required
@admin_required
def admin_toggle_user(user_id):
    user = db.session.get(User, user_id)
    if user.is_admin:
        return jsonify({'error': 'Cannot toggle admin user'}), 400

    user.is_active = not user.is_active
    db.session.commit()
    return jsonify({'success': True, 'is_active': user.is_active})

@app.route('/admin/users/<int:user_id>/delete')
@login_required
@admin_required
def admin_delete_user(user_id):
    user = db.session.get(User, user_id)
    if user.is_admin:
        return jsonify({'error': 'Cannot delete admin user'}), 400

    # Delete user's chats first
    Chat.query.filter_by(user_id=user_id).delete()
    db.session.delete(user)
    db.session.commit()
    return jsonify({'success': True})

@app.route('/admin/chats/<int:user_id>')
@login_required
@admin_required
def admin_user_chats(user_id):
    user = db.session.get(User, user_id)
    chats = Chat.query.filter_by(user_id=user_id).order_by(Chat.created_at.desc()).all()
    return render_template('admin_user_chats.html', user=user, chats=chats)

# ========================================
# ERROR HANDLERS
# ========================================
@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('500.html'), 500

# ========================================
# DATABASE INITIALIZATION
# ========================================
with app.app_context():
    db.create_all()
    print("✅ Database tables created successfully!")

    # Create admin user if not exists
    if not User.query.filter_by(is_admin=True).first():
        admin_username = os.environ.get('ADMIN_USERNAME', 'admin')
        admin_password = os.environ.get('ADMIN_PASSWORD', 'admin123')

        admin = User(
            username=admin_username,
            email='admin@iae.com',
            full_name='System Administrator',
            is_admin=True
        )
        admin.set_password(admin_password)
        db.session.add(admin)
        db.session.commit()
        print(f"✅ Admin created: {admin_username} / {admin_password}")

# ========================================
# RUN APP
# ========================================
if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=5000)
