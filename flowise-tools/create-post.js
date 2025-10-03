/*
* Tool: Create Blog Post
* Description: Create a new blog post on The New Heretics blog
*
* REQUIRED VARIABLES (set in Flowise):
* - nh_api_key: Your blog API key (98vQa7KezwhRAhq1N67SgAL7LDv30w-yGq411t5klVM)
*   Set this as a custom variable in Flowise: $vars.nh_api_key
*
* REQUIRED INPUT SCHEMA PROPERTIES:
* - title (string): The title of the blog post
* - content (string): The full content/body of the blog post
*
* OPTIONAL INPUT SCHEMA PROPERTIES:
* - excerpt (string): A short summary or excerpt of the post
* - author (string): Author name (defaults to "The New Heretics")
* - tags (string): Comma-separated tags (e.g., "philosophy,technology,ai")
* - is_published (boolean): Whether to publish immediately (default: false/draft)
*
* EXAMPLE USAGE IN FLOWISE:
* - Input Schema: Add properties "title" (string), "content" (string)
* - Optional: Add "excerpt", "author", "tags", "is_published"
* - When user says "create a post titled 'Hello World' with content '...'"
* - Or "write a blog post about AI and philosophy"
*
* FEATURES:
* - Automatically generates URL-friendly slug from title
* - Creates as draft by default (is_published: false)
* - Set is_published: true to publish immediately
* - Supports tags for categorization
*
* Returns: JSON string containing the created blog post with ID and details
*/

const fetch = require('node-fetch');

// CONFIGURATION - Update if needed
const BASE_URL = 'https://thenewheretics.blog';
const API_KEY = $vars.nh_api_key; // Set this variable in Flowise custom variables

// Validate required fields
if (typeof $title === 'undefined' || !$title) {
    return 'Error: title is required. Please provide a title for the blog post.';
}

if (typeof $content === 'undefined' || !$content) {
    return 'Error: content is required. Please provide the content/body for the blog post.';
}

// Build the request body
const postData = {
    title: $title,
    content: $content
};

// Add optional fields if provided
if (typeof $excerpt !== 'undefined' && $excerpt) {
    postData.excerpt = $excerpt;
}

if (typeof $author !== 'undefined' && $author) {
    postData.author = $author;
}

if (typeof $tags !== 'undefined' && $tags) {
    // If tags is a string, convert to array by splitting on comma
    if (typeof $tags === 'string') {
        postData.tags = $tags.split(',').map(tag => tag.trim());
    } else {
        postData.tags = $tags;
    }
}

if (typeof $is_published !== 'undefined') {
    postData.is_published = $is_published;
}

const url = `${BASE_URL}/api/posts`;

const options = {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json',
        'X-API-Key': API_KEY
    },
    body: JSON.stringify(postData)
};

try {
    const response = await fetch(url, options);

    if (response.status === 401) {
        return 'Error: Authentication failed. Please check your API key is set correctly in Flowise variables.';
    }

    if (response.status === 400) {
        const error = await response.json();
        return `Error: ${error.error || 'Invalid request data'}`;
    }

    if (response.status === 409) {
        const error = await response.json();
        return `Error: ${error.error || 'A post with this slug already exists'}`;
    }

    if (!response.ok) {
        return `Error: Unable to create post. Status: ${response.status} - ${response.statusText}`;
    }

    const data = await response.json();

    // Format success message
    const status = data.is_published ? 'published' : 'saved as draft';
    const message = `Success: Blog post "${data.title}" has been created and ${status}!`;

    return `${message}

Post Details:
- ID: ${data.id}
- Slug: ${data.slug}
- URL: ${BASE_URL}/blog/${data.slug}
- Status: ${data.is_published ? 'Published' : 'Draft'}
- Author: ${data.author}
- Tags: ${data.tags.join(', ') || 'None'}
- Created: ${data.created_at}

Full Post Data:
${JSON.stringify(data, null, 2)}`;

} catch (error) {
    console.error('Error creating blog post:', error);
    return `Error: ${error.message}`;
}
