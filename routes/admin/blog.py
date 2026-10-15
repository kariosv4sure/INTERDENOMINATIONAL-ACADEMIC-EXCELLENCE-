from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify, abort
from flask_login import login_required, current_user
from extensions import db
from models import BlogPost
from utils import admin_required, slugify, unique_slug, clean_text

blog_bp = Blueprint('blog', __name__, url_prefix='/blog')


@blog_bp.route('/')
@login_required
@admin_required
def index():
    posts = BlogPost.query.order_by(BlogPost.created_at.desc()).all()
    return render_template('admin/blog.html', posts=posts)


@blog_bp.route('/new', methods=['GET', 'POST'])
@login_required
@admin_required
def new():
    if request.method == 'POST':
        data = _read_form()
        if data['errors']:
            for e in data['errors']:
                flash(e, 'danger')
            return render_template('admin/blog_editor.html', post=None), 400

        post = BlogPost(
            slug=unique_slug(slugify(data['title'])),
            title=data['title'],
            excerpt=data['excerpt'],
            body=data['body'],
            category=data['category'],
            cover_image=data['cover_image'] or None,
            read_minutes=data['read_minutes'],
            published=data['published'],
            author_id=current_user.id,
        )
        db.session.add(post)
        db.session.commit()
        flash('Post created.', 'success')
        return redirect(url_for('admin.blog.index'))

    return render_template('admin/blog_editor.html', post=None)


@blog_bp.route('/<int:post_id>/edit', methods=['GET', 'POST'])
@login_required
@admin_required
def edit(post_id):
    post = db.session.get(BlogPost, post_id)
    if not post:
        abort(404)

    if request.method == 'POST':
        data = _read_form()
        if data['errors']:
            for e in data['errors']:
                flash(e, 'danger')
            return render_template('admin/blog_editor.html', post=post), 400

        post.title = data['title']
        post.excerpt = data['excerpt']
        post.body = data['body']
        post.category = data['category']
        post.cover_image = data['cover_image'] or None
        post.read_minutes = data['read_minutes']
        post.published = data['published']
        post.slug = unique_slug(slugify(data['title']), exclude_id=post.id)
        db.session.commit()
        flash('Post updated.', 'success')
        return redirect(url_for('admin.blog.index'))

    return render_template('admin/blog_editor.html', post=post)


@blog_bp.route('/<int:post_id>/delete', methods=['POST'])
@login_required
@admin_required
def delete(post_id):
    post = db.session.get(BlogPost, post_id)
    if not post:
        abort(404)
    db.session.delete(post)
    db.session.commit()
    return jsonify({'success': True})


@blog_bp.route('/<int:post_id>/toggle', methods=['POST'])
@login_required
@admin_required
def toggle(post_id):
    post = db.session.get(BlogPost, post_id)
    if not post:
        abort(404)
    post.published = not post.published
    db.session.commit()
    return jsonify({'success': True, 'published': post.published})


def _read_form():
    title = clean_text(request.form.get('title', ''), max_len=200)
    excerpt = clean_text(request.form.get('excerpt', ''), max_len=300)
    body = request.form.get('body', '').strip()      # don't strip HTML from body
    category = clean_text(request.form.get('category', 'General'), max_len=40)
    cover_image = clean_text(request.form.get('cover_image', ''), max_len=300)
    read_minutes = request.form.get('read_minutes', 5, type=int) or 5
    published = bool(request.form.get('published'))

    errors = []
    if not title:
        errors.append('Title is required.')
    if not excerpt:
        errors.append('Excerpt is required.')
    if not body:
        errors.append('Body is required.')
    if read_minutes < 1 or read_minutes > 60:
        errors.append('Read time must be 1-60 minutes.')

    return {
        'title': title, 'excerpt': excerpt, 'body': body,
        'category': category or 'General',
        'cover_image': cover_image, 'read_minutes': read_minutes,
        'published': published, 'errors': errors,
    }