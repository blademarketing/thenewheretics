# The New Heretics Blog

A modern blog platform built with Flask and SQLite, designed for LLM agent integration via Flowise. Features a RESTful API for blog management with API key authentication.

**Live Site**: [https://thenewheretics.blog](https://thenewheretics.blog)

---

## 🚀 Features

- **RESTful API** - Complete CRUD operations for blog posts
- **SQLite Database** - Lightweight, local database storage
- **API Authentication** - Secure API key-based authentication
- **LLM Agent Integration** - Pre-built Flowise tools for AI-powered blog management
- **Draft System** - Create drafts before publishing
- **Tagging System** - Organize posts with tags
- **Auto-generated Slugs** - URL-friendly slugs from titles
- **Search & Filtering** - Search by content, filter by tags, published status
- **Postman Collection** - Ready-to-use API testing collection

---

## 🛠️ Tech Stack

- **Backend**: Python 3.12, Flask 3.1.2
- **Database**: SQLite with SQLAlchemy ORM
- **Web Server**: Nginx (reverse proxy)
- **WSGI Server**: Gunicorn (3 workers)
- **Process Manager**: systemd
- **SSL**: Let's Encrypt (certbot)
- **Environment**: Python venv, python-dotenv

---

## 📋 Requirements

- Python 3.12+
- nginx
- systemd
- certbot (for SSL)

---

## 🔧 Installation & Setup

### 1. Clone the Repository

```bash
git clone https://github.com/blademarketing/thenewheretics.git
cd thenewheretics
```

### 2. Create Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate  # On Linux/Mac
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables

Create a `.env` file:

```bash
echo "API_KEY=your-api-key-here" > .env
```

**Current API Key**: `98vQa7KezwhRAhq1N67SgAL7LDv30w-yGq411t5klVM`

### 5. Initialize Database

The database is automatically created when the app first runs:

```bash
python3 app.py
```

This creates `blog.db` in the project root.

---

## 🚀 Deployment

### Production Setup (systemd + nginx)

#### 1. Systemd Service

Service file located at: `/etc/systemd/system/thenewheretics.service`

```bash
sudo systemctl daemon-reload
sudo systemctl enable thenewheretics.service
sudo systemctl start thenewheretics.service
sudo systemctl status thenewheretics.service
```

**Service Configuration**:
- Runs on: `127.0.0.1:7701` (localhost only)
- Workers: 3 Gunicorn workers
- Auto-restart on failure

#### 2. Nginx Configuration

Config file: `/etc/nginx/sites-available/thenewheretics.blog`

```bash
sudo nginx -t                    # Test configuration
sudo systemctl reload nginx      # Reload nginx
```

**Nginx Setup**:
- Reverse proxy to `127.0.0.1:7701`
- SSL via Let's Encrypt
- Cache disabled for development
- Proxies requests to Flask backend

#### 3. SSL Certificate

Managed by certbot:

```bash
sudo certbot --nginx -d thenewheretics.blog -d www.thenewheretics.blog
```

Auto-renewal is configured.

---

## 📡 API Documentation

### Base URL

```
https://thenewheretics.blog
```

### Authentication

Protected endpoints require API key in header:

```http
X-API-Key: 98vQa7KezwhRAhq1N67SgAL7LDv30w-yGq411t5klVM
```

### Endpoints

#### Public Endpoints (No Auth Required)

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/api/posts` | List all posts (with optional filters) |
| `GET` | `/api/posts/<id>` | Get single post by ID |
| `GET` | `/api/posts/slug/<slug>` | Get post by slug |
| `GET` | `/api/posts/published` | Get all published posts |

**Query Parameters for `/api/posts`**:
- `published=true` - Filter to published posts only
- `search=keyword` - Search in title and content
- `tag=tagname` - Filter by tag
- `limit=10` - Limit number of results

#### Protected Endpoints (Auth Required)

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/api/posts` | Create new post |
| `PUT` | `/api/posts/<id>` | Update post |
| `PATCH` | `/api/posts/<id>/publish` | Toggle publish status |
| `DELETE` | `/api/posts/<id>` | Delete post |
| `GET` | `/api/posts/drafts` | Get draft posts |
| `GET` | `/api/posts/stats` | Get blog statistics |

### Example Requests

#### Create a Post

```bash
curl -X POST https://thenewheretics.blog/api/posts \
  -H "Content-Type: application/json" \
  -H "X-API-Key: 98vQa7KezwhRAhq1N67SgAL7LDv30w-yGq411t5klVM" \
  -d '{
    "title": "My First Post",
    "content": "This is the content of my post.",
    "excerpt": "A brief summary",
    "tags": ["technology", "philosophy"],
    "is_published": false
  }'
```

#### List Published Posts

```bash
curl https://thenewheretics.blog/api/posts?published=true
```

#### Toggle Publish Status

```bash
curl -X PATCH https://thenewheretics.blog/api/posts/1/publish \
  -H "X-API-Key: 98vQa7KezwhRAhq1N67SgAL7LDv30w-yGq411t5klVM"
```

### Post Object Schema

```json
{
  "id": 1,
  "title": "Post Title",
  "slug": "post-title",
  "content": "Full post content...",
  "excerpt": "Brief summary",
  "author": "The New Heretics",
  "is_published": true,
  "published_at": "2025-10-03T12:00:00",
  "created_at": "2025-10-03T11:00:00",
  "updated_at": "2025-10-03T12:00:00",
  "tags": ["tag1", "tag2"]
}
```

---

## 🤖 LLM Agent Integration (Flowise)

Pre-built Flowise tools are available in the `flowise-tools/` directory.

### Available Tools

1. **List Blog Posts** (`list-blog-posts.js`)
   - Browse and search posts
   - No authentication required

2. **Create Blog Post** (`create-post.js`)
   - Create new blog posts
   - Requires `nh_api_key` variable

3. **Toggle Publish Post** (`toggle-publish-post.js`)
   - Publish/unpublish posts
   - Requires `nh_api_key` variable

4. **Delete Post** (`delete-post.js`)
   - Permanently delete posts
   - Requires `nh_api_key` variable

### Setup in Flowise

1. Go to Flowise Settings → Variables
2. Add custom variable:
   - **Name**: `nh_api_key`
   - **Value**: `98vQa7KezwhRAhq1N67SgAL7LDv30w-yGq411t5klVM`

3. Import tools from `flowise-tools/` directory
4. Configure Input Schema properties as documented in each tool

See [flowise-tools/README.md](flowise-tools/README.md) for detailed instructions.

---

## 📮 Postman Collection

Import the ready-to-use Postman collection:

**File**: `The_New_Heretics_Blog_API.postman_collection.json`

- API key pre-configured
- All endpoints included
- Example requests with documentation
- Organized into folders (Public, Management, Admin)

---

## 🗂️ Project Structure

```
thenewheretics.blog/
├── app.py                          # Main Flask application
├── models.py                       # SQLAlchemy database models
├── requirements.txt                # Python dependencies
├── .env                           # Environment variables (not in git)
├── .gitignore                     # Git ignore rules
├── blog.db                        # SQLite database (not in git)
├── templates/
│   └── index.html                 # Coming soon page
├── flowise-tools/                 # Flowise LLM agent tools
│   ├── README.md                  # Flowise tools documentation
│   ├── list-blog-posts.js         # List/search posts
│   ├── create-post.js             # Create new posts
│   ├── toggle-publish-post.js     # Publish/unpublish
│   ├── delete-post.js             # Delete posts
│   └── flowise-tool-example.js    # Example tool structure
└── The_New_Heretics_Blog_API.postman_collection.json
```

---

## 🔒 Security

### API Key Management

- API key stored in `.env` file (excluded from git)
- Required for all write operations (POST, PUT, PATCH, DELETE)
- Transmitted via `X-API-Key` header
- Read operations (GET) for published content are public

### Network Security

- Flask app bound to `127.0.0.1:7701` (localhost only)
- Only accessible via nginx reverse proxy
- SSL/TLS encryption via Let's Encrypt
- HTTPS enforced (HTTP redirects to HTTPS)

### Best Practices

- ✅ API key in environment variable (not hardcoded)
- ✅ Database file excluded from git
- ✅ Application not exposed to internet directly
- ✅ Regular SSL certificate auto-renewal
- ✅ Input validation on all endpoints

---

## 🧪 Development

### Running Locally

```bash
# Activate virtual environment
source venv/bin/activate

# Run development server
python3 app.py
```

App runs on `http://127.0.0.1:7701`

### Making Changes

```bash
# Make changes to code
# ...

# Restart service in production
sudo systemctl restart thenewheretics.service

# Reload nginx if config changed
sudo systemctl reload nginx
```

### Database Management

```bash
# Database is auto-created on first run
# Located at: blog.db

# To reset database (CAUTION: deletes all data)
rm blog.db
python3 app.py  # Creates fresh database
```

---

## 📝 Database Schema

### BlogPost Model

| Field | Type | Description |
|-------|------|-------------|
| `id` | Integer | Primary key |
| `title` | String(255) | Post title |
| `slug` | String(255) | URL-friendly slug (unique, indexed) |
| `content` | Text | Full post content |
| `excerpt` | Text | Short summary |
| `author` | String(100) | Author name |
| `is_published` | Boolean | Published status (indexed) |
| `published_at` | DateTime | Publication timestamp |
| `created_at` | DateTime | Creation timestamp |
| `updated_at` | DateTime | Last update timestamp |
| `tags` | String(500) | Comma-separated tags |

---

## 🐛 Troubleshooting

### Service Not Starting

```bash
# Check service status
sudo systemctl status thenewheretics.service

# View logs
sudo journalctl -u thenewheretics.service -n 50

# Common issues:
# - Virtual environment path incorrect
# - Missing dependencies
# - Port already in use
```

### Database Issues

```bash
# Check if database file exists
ls -la blog.db

# Verify permissions
sudo chown root:root blog.db  # Match service user

# Recreate database
rm blog.db
python3 app.py
```

### Nginx Issues

```bash
# Test configuration
sudo nginx -t

# Check error logs
sudo tail -f /var/log/nginx/thenewheretics.blog_error.log

# Common issues:
# - Backend not running
# - Port mismatch
# - SSL certificate issues
```

### API Authentication Errors

- Verify API key in `.env` matches your requests
- Check `X-API-Key` header is present
- Ensure `.env` file is being loaded (check app logs)

---

## 📄 License

This project is proprietary software for The New Heretics blog.

---

## 🤝 Contributing

This is a private project. For issues or suggestions, contact the repository owner.

---

## 📞 Support

- **GitHub**: [blademarketing/thenewheretics](https://github.com/blademarketing/thenewheretics)
- **Website**: [https://thenewheretics.blog](https://thenewheretics.blog)

---

## 🎯 Roadmap

### Current Features
- ✅ RESTful API with authentication
- ✅ SQLite database
- ✅ Draft and publish workflow
- ✅ Tagging system
- ✅ Search and filtering
- ✅ Flowise LLM agent tools
- ✅ Production deployment
- ✅ SSL encryption

### Future Enhancements
- [ ] Frontend blog interface
- [ ] Rich text editor integration
- [ ] Image upload support
- [ ] Categories/taxonomies
- [ ] Comments system
- [ ] RSS feed
- [ ] Analytics integration
- [ ] Multi-author support
- [ ] SEO optimization
- [ ] Markdown support

---

**Built with ❤️ for thought-provoking content**
