from flask import Flask, render_template, request, jsonify, Response, abort
from datetime import datetime
from models import db, BlogPost
from functools import wraps
from collections import defaultdict
import re
import os
from dotenv import load_dotenv
import markdown

# Load environment variables
load_dotenv()

app = Flask(__name__)

# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# API Key configuration
API_KEY = os.getenv('API_KEY')

def require_api_key(f):
    """Decorator to require API key authentication"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        provided_key = request.headers.get('X-API-Key')
        if not provided_key or provided_key != API_KEY:
            return jsonify({'error': 'Invalid or missing API key'}), 401
        return f(*args, **kwargs)
    return decorated_function

# Initialize database
db.init_app(app)

# Create tables
with app.app_context():
    db.create_all()

# Context processor for templates
@app.context_processor
def inject_current_year():
    return {'current_year': datetime.now().year}

def generate_slug(title):
    """Generate URL-friendly slug from title"""
    slug = title.lower()
    slug = re.sub(r'[^\w\s-]', '', slug)
    slug = re.sub(r'[-\s]+', '-', slug)
    return slug.strip('-')

def format_content(content):
    """Convert markdown to HTML and format content"""
    md = markdown.Markdown(extensions=['extra', 'nl2br'])
    return md.convert(content)

# Frontend Routes
@app.route('/')
def index():
    """Home page with featured post and recent posts"""
    # Get most recent published post for featured
    featured_post = BlogPost.query.filter_by(is_published=True).order_by(
        BlogPost.published_at.desc()
    ).first()

    # Get next 5 recent published posts
    recent_posts = BlogPost.query.filter_by(is_published=True).order_by(
        BlogPost.published_at.desc()
    ).offset(1).limit(5).all()

    return render_template('home.html', featured_post=featured_post, recent_posts=recent_posts)

@app.route('/posts/<slug>/')
def post(slug):
    """Individual post page"""
    post = BlogPost.query.filter_by(slug=slug, is_published=True).first_or_404()
    # Format content as HTML
    post.content = format_content(post.content)

    # Get 2 random posts excluding current post
    from sqlalchemy.sql.expression import func
    random_posts = BlogPost.query.filter(
        BlogPost.id != post.id,
        BlogPost.is_published == True
    ).order_by(func.random()).limit(2).all()

    return render_template('post.html', post=post, random_posts=random_posts)

@app.route('/archive/')
def archive():
    """Archive page with all posts grouped by year"""
    posts = BlogPost.query.filter_by(is_published=True).order_by(
        BlogPost.published_at.desc()
    ).all()

    # Group posts by year
    posts_by_year = defaultdict(list)
    for post in posts:
        year = post.published_at.year if post.published_at else post.created_at.year
        posts_by_year[year].append(post)

    return render_template('archive.html', posts_by_year=dict(posts_by_year))

@app.route('/rss.xml')
def rss_feed():
    """RSS feed for the blog"""
    posts = BlogPost.query.filter_by(is_published=True).order_by(
        BlogPost.published_at.desc()
    ).limit(20).all()

    rss = ['<?xml version="1.0" encoding="UTF-8"?>']
    rss.append('<rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom">')
    rss.append('<channel>')
    rss.append('<title>The New Heretics</title>')
    rss.append('<link>https://thenewheretics.blog</link>')
    rss.append('<description>Where the need for belonging ends, truth begins.</description>')
    rss.append('<atom:link href="https://thenewheretics.blog/rss.xml" rel="self" type="application/rss+xml" />')

    for post in posts:
        rss.append('<item>')
        rss.append(f'<title><![CDATA[{post.title}]]></title>')
        rss.append(f'<link>https://thenewheretics.blog/posts/{post.slug}/</link>')
        rss.append(f'<guid>https://thenewheretics.blog/posts/{post.slug}/</guid>')
        if post.excerpt:
            rss.append(f'<description><![CDATA[{post.excerpt}]]></description>')
        if post.published_at:
            rss.append(f'<pubDate>{post.published_at.strftime("%a, %d %b %Y %H:%M:%S +0000")}</pubDate>')
        rss.append('</item>')

    rss.append('</channel>')
    rss.append('</rss>')

    return Response('\n'.join(rss), mimetype='application/rss+xml')

# API Routes for Blog Management

@app.route('/api/posts', methods=['GET'])
def get_posts():
    """Get all blog posts with optional filtering"""
    # Query parameters
    published_only = request.args.get('published', 'false').lower() == 'true'
    search = request.args.get('search', '')
    tag = request.args.get('tag', '')
    limit = request.args.get('limit', type=int)

    query = BlogPost.query

    if published_only:
        query = query.filter_by(is_published=True)

    if search:
        query = query.filter(
            db.or_(
                BlogPost.title.ilike(f'%{search}%'),
                BlogPost.content.ilike(f'%{search}%')
            )
        )

    if tag:
        query = query.filter(BlogPost.tags.ilike(f'%{tag}%'))

    query = query.order_by(BlogPost.created_at.desc())

    if limit:
        query = query.limit(limit)

    posts = query.all()
    return jsonify([post.to_dict() for post in posts])

@app.route('/api/posts/<int:post_id>', methods=['GET'])
def get_post(post_id):
    """Get a single blog post by ID"""
    post = BlogPost.query.get_or_404(post_id)
    return jsonify(post.to_dict())

@app.route('/api/posts/slug/<slug>', methods=['GET'])
def get_post_by_slug(slug):
    """Get a blog post by slug"""
    post = BlogPost.query.filter_by(slug=slug).first_or_404()
    return jsonify(post.to_dict())

@app.route('/api/posts', methods=['POST'])
@require_api_key
def create_post():
    """Create a new blog post"""
    data = request.get_json()

    if not data or 'title' not in data or 'content' not in data:
        return jsonify({'error': 'Title and content are required'}), 400

    # Generate slug from title if not provided
    slug = data.get('slug', generate_slug(data['title']))

    # Check if slug already exists
    if BlogPost.query.filter_by(slug=slug).first():
        return jsonify({'error': 'A post with this slug already exists'}), 409

    post = BlogPost(
        title=data['title'],
        slug=slug,
        content=data['content'],
        excerpt=data.get('excerpt', ''),
        author=data.get('author', 'The New Heretics'),
        tags=','.join(data['tags']) if 'tags' in data and isinstance(data['tags'], list) else data.get('tags', ''),
        is_published=data.get('is_published', True)
    )

    if post.is_published and not post.published_at:
        post.published_at = datetime.utcnow()

    db.session.add(post)
    db.session.commit()

    return jsonify(post.to_dict()), 201

@app.route('/api/posts/<int:post_id>', methods=['PUT'])
@require_api_key
def update_post(post_id):
    """Update an existing blog post"""
    post = BlogPost.query.get_or_404(post_id)
    data = request.get_json()

    if not data:
        return jsonify({'error': 'No data provided'}), 400

    # Update fields if provided
    if 'title' in data:
        post.title = data['title']

    if 'slug' in data:
        # Check if new slug conflicts with another post
        existing = BlogPost.query.filter_by(slug=data['slug']).first()
        if existing and existing.id != post_id:
            return jsonify({'error': 'A post with this slug already exists'}), 409
        post.slug = data['slug']

    if 'content' in data:
        post.content = data['content']

    if 'excerpt' in data:
        post.excerpt = data['excerpt']

    if 'author' in data:
        post.author = data['author']

    if 'tags' in data:
        if isinstance(data['tags'], list):
            post.tags = ','.join(data['tags'])
        else:
            post.tags = data['tags']

    if 'is_published' in data:
        was_published = post.is_published
        post.is_published = data['is_published']

        # Set published_at when first published
        if post.is_published and not was_published:
            post.published_at = datetime.utcnow()

    post.updated_at = datetime.utcnow()

    db.session.commit()

    return jsonify(post.to_dict())

@app.route('/api/posts/<int:post_id>/publish', methods=['PATCH'])
@require_api_key
def toggle_publish(post_id):
    """Publish or unpublish a blog post"""
    post = BlogPost.query.get_or_404(post_id)

    post.is_published = not post.is_published

    if post.is_published and not post.published_at:
        post.published_at = datetime.utcnow()

    post.updated_at = datetime.utcnow()

    db.session.commit()

    return jsonify(post.to_dict())

@app.route('/api/posts/<int:post_id>', methods=['DELETE'])
@require_api_key
def delete_post(post_id):
    """Delete a blog post"""
    post = BlogPost.query.get_or_404(post_id)

    db.session.delete(post)
    db.session.commit()

    return jsonify({'message': 'Post deleted successfully'}), 200

@app.route('/api/posts/drafts', methods=['GET'])
@require_api_key
def get_drafts():
    """Get all draft (unpublished) posts"""
    drafts = BlogPost.query.filter_by(is_published=False).order_by(BlogPost.created_at.desc()).all()
    return jsonify([post.to_dict() for post in drafts])

@app.route('/api/posts/published', methods=['GET'])
def get_published():
    """Get all published posts"""
    published = BlogPost.query.filter_by(is_published=True).order_by(BlogPost.published_at.desc()).all()
    return jsonify([post.to_dict() for post in published])

@app.route('/api/posts/stats', methods=['GET'])
@require_api_key
def get_stats():
    """Get blog statistics"""
    total = BlogPost.query.count()
    published = BlogPost.query.filter_by(is_published=True).count()
    drafts = BlogPost.query.filter_by(is_published=False).count()

    return jsonify({
        'total_posts': total,
        'published_posts': published,
        'draft_posts': drafts
    })

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=7701)
