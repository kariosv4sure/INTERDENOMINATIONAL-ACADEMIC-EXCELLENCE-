from flask import Blueprint, render_template, request, abort
from models import BlogPost

blog_bp = Blueprint('blog', __name__, url_prefix='/blog')


@blog_bp.route('/')
def index():
    page = request.args.get('page', 1, type=int)
    category = request.args.get('category')

    q = BlogPost.query.filter_by(published=True)
    if category:
        q = q.filter_by(category=category)

    posts = (q.order_by(BlogPost.created_at.desc())
             .paginate(page=page, per_page=9, error_out=False))

    categories = (db_categories())  # helper below
    return render_template('public/blog.html',
                           posts=posts,
                           categories=categories,
                           active_category=category)


@blog_bp.route('/<slug>')
def post(slug):
    p = BlogPost.query.filter_by(slug=slug, published=True).first()
    if not p:
        abort(404)

    prev_post = (BlogPost.query
                 .filter(BlogPost.published.is_(True),
                         BlogPost.created_at < p.created_at)
                 .order_by(BlogPost.created_at.desc()).first())
    next_post = (BlogPost.query
                 .filter(BlogPost.published.is_(True),
                         BlogPost.created_at > p.created_at)
                 .order_by(BlogPost.created_at.asc()).first())

    return render_template('public/blog_post.html',
                           post=p, prev_post=prev_post, next_post=next_post)


def db_categories():
    from extensions import db
    rows = (db.session.query(BlogPost.category)
            .filter_by(published=True).distinct().all())
    return [r[0] for r in rows if r[0]]