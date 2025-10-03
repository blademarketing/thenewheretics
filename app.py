from flask import Flask, render_template, request, jsonify
from datetime import datetime
from models import db, BlogPost
import re

app = Flask(__name__)

# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize database
db.init_app(app)

# Create tables
with app.app_context():
    db.create_all()

def generate_slug(title):
    """Generate URL-friendly slug from title"""
    slug = title.lower()
    slug = re.sub(r'[^\w\s-]', '', slug)
    slug = re.sub(r'[-\s]+', '-', slug)
    return slug.strip('-')

# Frontend route
@app.route('/')
def index():
    return render_template('index.html')

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
        is_published=data.get('is_published', False)
    )

    if post.is_published and not post.published_at:
        post.published_at = datetime.utcnow()

    db.session.add(post)
    db.session.commit()

    return jsonify(post.to_dict()), 201

@app.route('/api/posts/<int:post_id>', methods=['PUT'])
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
def delete_post(post_id):
    """Delete a blog post"""
    post = BlogPost.query.get_or_404(post_id)

    db.session.delete(post)
    db.session.commit()

    return jsonify({'message': 'Post deleted successfully'}), 200

@app.route('/api/posts/drafts', methods=['GET'])
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
