from flask import Blueprint, render_template
from models import BlogPost

public_bp = Blueprint('public', __name__)


@public_bp.route('/')
def index():
    latest_posts = (BlogPost.query
                    .filter_by(published=True)
                    .order_by(BlogPost.created_at.desc())
                    .limit(3).all())
    return render_template('public/index.html', latest_posts=latest_posts)


@public_bp.route('/about')
def about():
    return render_template('public/about.html')


@public_bp.route('/services')
def services():
    return render_template('public/services.html')


@public_bp.route('/jamb')
def jamb():
    return render_template('public/jamb.html')


@public_bp.route('/waec')
def waec():
    return render_template('public/waec.html')


@public_bp.route('/testimonials')
def testimonials():
    return render_template('public/testimonials.html')


@public_bp.route('/contact')
def contact():
    return render_template('public/contact.html')


@public_bp.route('/feedback')
def feedback():
    return render_template('public/feedback.html')