import logging
from flask import Flask, render_template, request
from werkzeug.exceptions import HTTPException

from config import config_map
from extensions import db, login_manager, csrf, limiter, migrate
from models import User, BlogPost
from routes import public_bp, auth_bp, chat_bp, blog_bp, admin_bp


def create_app(config_name=None):
    import os
    config_name = config_name or os.environ.get('FLASK_ENV', 'development')

    app = Flask(__name__)
    app.config.from_object(config_map[config_name])

    # Extensions
    db.init_app(app)
    login_manager.init_app(app)
    csrf.init_app(app)
    limiter.init_app(app)
    migrate.init_app(app, db)

    # Logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s %(levelname)s %(name)s: %(message)s',
    )

    # User loader
    @login_manager.user_loader
    def load_user(user_id):
        return db.session.get(User, int(user_id))

    # Blueprints
    app.register_blueprint(public_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(chat_bp)
    app.register_blueprint(blog_bp)
    app.register_blueprint(admin_bp)

    # Security headers
    @app.after_request
    def security_headers(resp):
        resp.headers['X-Content-Type-Options'] = 'nosniff'
        resp.headers['X-Frame-Options'] = 'SAMEORIGIN'
        resp.headers['Referrer-Policy'] = 'strict-origin-when-cross-origin'
        resp.headers.setdefault(
            'Content-Security-Policy',
            "default-src 'self'; "
            "img-src 'self' data:; "
            "style-src 'self' 'unsafe-inline' https://fonts.googleapis.com https://cdnjs.cloudflare.com; "
            "font-src 'self' https://fonts.gstatic.com https://cdnjs.cloudflare.com; "
            "script-src 'self' 'unsafe-inline' https://cdnjs.cloudflare.com; "
            "connect-src 'self'; "
            "frame-ancestors 'self'"
        )
        return resp

    # Errors
    @app.errorhandler(404)
    def _404(e):
        return render_template('404.html'), 404

    @app.errorhandler(403)
    def _403(e):
        return render_template('404.html'), 403   # don't reveal route exists

    @app.errorhandler(429)
    def _429(e):
        return render_template('500.html', message='Too many requests. Try again later.'), 429

    @app.errorhandler(500)
    def _500(e):
        db.session.rollback()
        return render_template('500.html'), 500

    # Bootstrap DB + admin
    with app.app_context():
        from sqlalchemy import text
        db.create_all()
        _ensure_admin(app)

    return app


def _ensure_admin(app):
    if User.query.filter_by(is_admin=True).first():
        return
    username = app.config['ADMIN_USERNAME']
    email = app.config['ADMIN_EMAIL']
    password = app.config['ADMIN_PASSWORD']
    if not password:
        app.logger.warning(
            "No ADMIN_PASSWORD set — skipping admin bootstrap. "
            "Set one in .env before first run."
        )
        return
    admin = User(username=username, email=email,
                 full_name='System Administrator', is_admin=True)
    admin.set_password(password)
    db.session.add(admin)
    db.session.commit()
    app.logger.info('Admin bootstrap complete for %s', username)


app = create_app()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)