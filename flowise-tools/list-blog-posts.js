/*
* Tool: List Blog Posts
* Description: Retrieve all blog posts from The New Heretics blog with optional filtering
*
* REQUIRED VARIABLES (set in Flowise):
* - API_KEY: Your blog API key (98vQa7KezwhRAhq1N67SgAL7LDv30w-yGq411t5klVM)
*   Set this as a custom variable in Flowise: $vars.API_KEY
*
* OPTIONAL INPUT SCHEMA PROPERTIES:
* - published (boolean): Filter to only published posts (true/false)
* - search (string): Search term to find in title and content
* - tag (string): Filter posts by tag
* - limit (number): Maximum number of posts to return
*
* EXAMPLE USAGE IN FLOWISE:
* - To list all posts: No properties needed
* - To list published posts: Add property "published" = true
* - To search: Add property "search" = "keyword"
* - To limit results: Add property "limit" = 10
*
* Returns: JSON string containing array of blog posts
*/

const fetch = require('node-fetch');

// CONFIGURATION - Update if needed
const BASE_URL = 'https://thenewheretics.blog';
const API_KEY = $vars.API_KEY; // Set this variable in Flowise custom variables

// Build query parameters
const params = new URLSearchParams();

// Add optional filters if provided
if (typeof $published !== 'undefined') {
    params.append('published', $published);
}
if (typeof $search !== 'undefined' && $search) {
    params.append('search', $search);
}
if (typeof $tag !== 'undefined' && $tag) {
    params.append('tag', $tag);
}
if (typeof $limit !== 'undefined' && $limit) {
    params.append('limit', $limit);
}

// Build URL with query parameters
const queryString = params.toString();
const url = `${BASE_URL}/api/posts${queryString ? '?' + queryString : ''}`;

const options = {
    method: 'GET',
    headers: {
        'Content-Type': 'application/json'
        // Note: This endpoint is public and doesn't require authentication
    }
};

try {
    const response = await fetch(url, options);

    if (!response.ok) {
        return `Error: Unable to fetch posts. Status: ${response.status} - ${response.statusText}`;
    }

    const data = await response.json();

    // Format the response for better readability
    if (Array.isArray(data) && data.length === 0) {
        return 'No blog posts found.';
    }

    return JSON.stringify(data, null, 2);

} catch (error) {
    console.error('Error fetching blog posts:', error);
    return `Error: ${error.message}`;
}
