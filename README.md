# The New Heretics Blog

A dark, minimalist blog platform built with Flask and SQLite, featuring AI-powered content management through Flowise LLM agents. Designed for Hedvig D. Knox's fearless essays on culture, ideology, and truth.

**Live Site**: [https://thenewheretics.blog](https://thenewheretics.blog)
**Admin Panel**: [https://thenewheretics.blog/admin](https://thenewheretics.blog/admin) (Password: `mayaspayas`)

**Tagline**: *"Where the need for belonging ends, truth begins."*

---

## 🚀 Features

### Blog Frontend
- **Dark Minimalist Design** - Black (#0A0A0A) background with red (#E10600) accents
- **Home Page** - Hero tagline + featured post + recent posts list
- **Post Pages** - Clean, readable typography with markdown rendering
- **Archive Page** - All posts grouped by year
- **RSS Feed** - Standard RSS 2.0 feed
- **Social Sharing** - Copy link, X/Twitter, LinkedIn share buttons
- **SEO Optimized** - Meta tags, Open Graph, Twitter cards, canonical URLs
- **Mobile Responsive** - Mobile-first design, works on all devices
- **Accessibility** - WCAG AA+ compliant, skip links, keyboard navigation

### Admin Panel
- **Password Protected** - Session-based authentication (`/admin`)
- **AI Chat Interface** - Full-page Flowise chatbot embed
- **Dark Theme** - Matches main blog aesthetic
- **Conversational Management** - Create, list, publish, delete posts via chat
- **Automatic Metadata** - AI generates tags and excerpts automatically
- **Mobile Optimized** - Responsive design for all devices

### API Backend
- **RESTful API** - Complete CRUD operations for blog posts
- **SQLite Database** - Lightweight, local database storage
- **API Authentication** - Secure API key-based authentication
- **LLM Agent Integration** - Pre-built Flowise tools
- **Draft System** - Create drafts before publishing
- **Tagging System** - Organize posts with tags
- **Auto-generated Slugs** - URL-friendly slugs from titles
- **Search & Filtering** - Search by content, filter by tags, published status
- **Markdown Support** - Rich text formatting with markdown
- **Postman Collection** - Ready-to-use API testing collection

---

## 🛠️ Tech Stack

- **Backend**: Python 3.12, Flask 3.1.2, Flask-SQLAlchemy
- **Database**: SQLite with SQLAlchemy ORM
- **Templates**: Jinja2
- **Content**: Markdown (python-markdown library)
- **Web Server**: Nginx (reverse proxy)
- **WSGI Server**: Gunicorn (3 workers on port 7701)
- **Process Manager**: systemd service
- **SSL**: Let's Encrypt (certbot, auto-renewal)
- **LLM Integration**: Flowise AI agent with custom tools
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

1. **Set Custom Variable**:
   - Go to Flowise Settings → Variables
   - Add: `nh_api_key` = `98vQa7KezwhRAhq1N67SgAL7LDv30w-yGq411t5klVM`

2. **Import System Prompt**:
   - Copy content from `flowise-tools/SYSTEM_PROMPT.md`
   - Paste into your Flowise agent's system prompt
   - Enables automatic metadata generation and user-friendly interactions

3. **Import Tools**:
   - Import each `.js` file from `flowise-tools/` as a Custom Tool
   - Configure Input Schema properties as documented in comments

4. **Configure Chatflow**:
   - Enable conversation memory for context
   - Connect all 4 tools to your agent
   - Deploy to get chatflow ID

See [flowise-tools/README.md](flowise-tools/README.md) and [flowise-tools/SYSTEM_PROMPT.md](flowise-tools/SYSTEM_PROMPT.md) for detailed instructions.

### Admin Panel Usage

1. Navigate to [https://thenewheretics.blog/admin](https://thenewheretics.blog/admin)
2. Login with password: `mayaspayas`
3. Use the AI chat interface to:
   - Create posts: "Write a post about [topic]"
   - List posts: "Show me all blog titles"
   - Publish: "Publish post 1" or "Publish my latest draft"
   - Delete: "Delete post 3"
   - The AI automatically generates tags and excerpts

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
├── app.py                          # Main Flask application with routes
├── models.py                       # SQLAlchemy database models
├── requirements.txt                # Python dependencies
├── .env                           # Environment variables (not in git)
├── .gitignore                     # Git ignore rules
├── blog.db                        # SQLite database (not in git)
├── templates/                     # Jinja2 templates
│   ├── base.html                  # Base layout with header/footer
│   ├── home.html                  # Homepage (hero + featured + recent)
│   ├── post.html                  # Individual post page
│   └── archive.html               # Archive page (posts by year)
├── static/                        # Static assets
│   ├── css/
│   │   └── style.css              # Main stylesheet (dark theme)
│   └── images/
│       └── nh-logo.png            # The New Heretics logo
├── admin/                         # Admin panel (static HTML)
│   └── index.html                 # Password-protected admin interface
├── flowise-tools/                 # Flowise LLM agent tools
│   ├── README.md                  # Flowise tools documentation
│   ├── SYSTEM_PROMPT.md           # System prompt for Flowise agent
│   ├── list-blog-posts.js         # List/search posts tool
│   ├── create-post.js             # Create new posts tool
│   ├── toggle-publish-post.js     # Publish/unpublish tool
│   ├── delete-post.js             # Delete posts tool
│   └── chatbot-embed-config.html  # Example embed configuration
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

## 🎨 Design Philosophy

**Visual Identity** (per `the-new-heretics-dev-spec.md`):
- **Dark minimalist aesthetic** - Black background, white text, red accents
- **Typography**: Inter/Helvetica for headings, Georgia serif for body
- **Color Palette**: #0A0A0A (bg), #F5F5F5 (text), #E10600 (accent red)
- **Text-first** - No stock images, pure content focus
- **Mobile-first** - Responsive design prioritizing readability

**Persona**: Hedvig D. Knox - Intellectual but rebellious, fearless essays

---

## 🎯 System Architecture

### Frontend (User-Facing Blog)
- **Home** (`/`) - Hero + featured post + recent posts
- **Posts** (`/posts/{slug}/`) - Individual post pages with sharing
- **Archive** (`/archive/`) - Chronological post index grouped by year
- **RSS** (`/rss.xml`) - RSS 2.0 feed for subscribers

### Admin Panel
- **Login** (`/admin/`) - Password-protected access
- **AI Chat Interface** - Full-page Flowise chatbot embed
- **Conversational Management** - Natural language blog management
- **Features**: Create, list, publish, delete posts through conversation

### API Backend
- **REST Endpoints** - Full CRUD for blog posts
- **Authentication** - API key header (`X-API-Key`)
- **Database** - SQLite with SQLAlchemy ORM
- **Server** - Gunicorn (3 workers) on port 7701 (localhost only)
- **Reverse Proxy** - Nginx with SSL (Let's Encrypt)

### LLM Agent Integration
- **4 Flowise Tools** - List, Create, Publish, Delete
- **System Prompt** - Optimized for non-technical users
- **Auto-Metadata** - Agent generates tags/excerpts automatically
- **Memory-Enabled** - Conversational context across interactions

---

## 🎯 Current Status

### ✅ Completed Features
- Dark minimalist blog design with logo
- Full blog frontend (home, posts, archive, RSS)
- Admin panel with AI chat interface
- RESTful API with authentication
- 4 Flowise tools for LLM management
- Social sharing buttons
- Markdown content support
- SEO optimization
- SSL encryption
- Production deployment
- Mobile responsive design
- Password-protected admin access

### 🔮 Future Enhancements
- [ ] Rich text editor for manual editing
- [ ] Image upload and management
- [ ] Comments system
- [ ] Analytics integration
- [ ] Newsletter/email subscription
- [ ] Multi-author support
- [ ] Category taxonomies beyond tags

---

**Built with ❤️ for fearless, thought-provoking essays**
