# Flowise Tools for The New Heretics Blog

These tools enable LLM agents in Flowise to manage The New Heretics blog.

## Setup Instructions

### 1. Set Custom Variables in Flowise

Before using these tools, you must set the API key as a custom variable in Flowise:

1. Go to Flowise Settings → Variables
2. Add a new variable:
   - **Name**: `nh_api_key`
   - **Value**: `98vQa7KezwhRAhq1N67SgAL7LDv30w-yGq411t5klVM`

### 2. Import Tools into Flowise

For each tool:
1. Go to Flowise → Tools → Create Custom Tool
2. Copy the JavaScript code from the tool file
3. Set up the Input Schema properties as described in each tool

---

## Available Tools

### 1. List Blog Posts (`list-blog-posts.js`)

**Purpose**: Retrieve all blog posts with optional filtering

**Required Variables**:
- None (this is a public endpoint, no authentication needed)

**Optional Input Schema Properties**:
- `published` (boolean) - Filter to only published posts
- `search` (string) - Search term for title/content
- `tag` (string) - Filter by tag
- `limit` (number) - Maximum number of results

**Example User Commands**:
- "Show me all blog posts"
- "List published posts"
- "Find posts about technology"
- "Show me the latest 5 posts"

---

### 2. Toggle Publish Post (`toggle-publish-post.js`)

**Purpose**: Publish or unpublish a blog post (toggles current state)

**Required Variables**:
- `nh_api_key` (set in Flowise custom variables)

**Required Input Schema Properties**:
- `postId` (number) - The ID of the post to publish/unpublish

**Example User Commands**:
- "Publish post 1"
- "Unpublish post 3"
- "Make post 5 public"

---

### 3. Delete Post (`delete-post.js`)

**Purpose**: Permanently delete a blog post

**Required Variables**:
- `nh_api_key` (set in Flowise custom variables)

**Required Input Schema Properties**:
- `postId` (number) - The ID of the post to delete

**Example User Commands**:
- "Delete post 1"
- "Remove blog post 7"
- "Permanently delete post 3"

**⚠️ WARNING**: This action is permanent and cannot be undone!

---

## API Endpoints Reference

All tools connect to: `https://thenewheretics.blog`

### Authenticated Endpoints (require API key):
- `PATCH /api/posts/{id}/publish` - Toggle publish status
- `DELETE /api/posts/{id}` - Delete post

### Public Endpoints (no auth required):
- `GET /api/posts` - List all posts (with optional filters)
- `GET /api/posts/{id}` - Get single post
- `GET /api/posts/slug/{slug}` - Get post by slug
- `GET /api/posts/published` - Get all published posts

---

## Additional Tools You Can Create

Based on the API, you can create additional tools for:

- **Create Post**: `POST /api/posts` (requires: title, content)
- **Update Post**: `PUT /api/posts/{id}` (update title, content, etc.)
- **Get Post by ID**: `GET /api/posts/{id}` (get specific post details)
- **Get Drafts**: `GET /api/posts/drafts` (list all draft posts)
- **Get Statistics**: `GET /api/posts/stats` (blog statistics)

See the Postman collection for full API documentation.

---

## Security Notes

- The API key is stored in `.env` file on the server (not in git)
- API key must be set in Flowise custom variables
- All write operations (create, update, delete, publish) require authentication
- Read operations for published content are public

---

## Troubleshooting

**Error: "Authentication failed"**
- Ensure `nh_api_key` is set correctly in Flowise custom variables
- Check that the variable name is exactly `nh_api_key`

**Error: "Post not found"**
- Verify the post ID exists by listing all posts first
- Check that the post hasn't been deleted

**Error: "Invalid or missing API key"**
- The API key header is missing or incorrect
- Verify the tool is accessing `$vars.nh_api_key` correctly
