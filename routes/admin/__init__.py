from flask import Blueprint
from .dashboard import dashboard_bp
from .users import users_bp
from .chats import chats_bp
from .blog import blog_bp as admin_blog_bp
from .auth import auth_bp

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')
admin_bp.register_blueprint(dashboard_bp)
admin_bp.register_blueprint(users_bp)
admin_bp.register_blueprint(chats_bp)
admin_bp.register_blueprint(admin_blog_bp)
admin_bp.register_blueprint(auth_bp)