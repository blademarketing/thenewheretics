/*
* Tool: Delete Blog Post
* Description: Permanently delete a blog post from The New Heretics blog
*
* REQUIRED VARIABLES (set in Flowise):
* - API_KEY: Your blog API key (98vQa7KezwhRAhq1N67SgAL7LDv30w-yGq411t5klVM)
*   Set this as a custom variable in Flowise: $vars.API_KEY
*
* REQUIRED INPUT SCHEMA PROPERTIES:
* - postId (number): The ID of the blog post to delete
*
* EXAMPLE USAGE IN FLOWISE:
* - Input Schema: Add property "postId" (type: number)
* - When user says "delete post 1", the postId should be extracted and passed as 1
* - When user says "remove blog post 5", the postId should be 5
*
* WARNING: This action is permanent and cannot be undone!
*
* Returns: Success or error message
*/

const fetch = require('node-fetch');

// CONFIGURATION - Update if needed
const BASE_URL = 'https://thenewheretics.blog';
const API_KEY = $vars.API_KEY; // Set this variable in Flowise custom variables

// Validate postId is provided
if (typeof $postId === 'undefined' || !$postId) {
    return 'Error: postId is required. Please provide the ID of the post to delete.';
}

const url = `${BASE_URL}/api/posts/${$postId}`;

const options = {
    method: 'DELETE',
    headers: {
        'Content-Type': 'application/json',
        'X-API-Key': API_KEY
    }
};

try {
    const response = await fetch(url, options);

    if (response.status === 401) {
        return 'Error: Authentication failed. Please check your API key is set correctly in Flowise variables.';
    }

    if (response.status === 404) {
        return `Error: Post with ID ${$postId} not found. It may have already been deleted.`;
    }

    if (!response.ok) {
        return `Error: Unable to delete post. Status: ${response.status} - ${response.statusText}`;
    }

    const data = await response.json();

    return `Success: ${data.message || 'Post deleted successfully'}\n\nPost ID ${$postId} has been permanently removed from the blog.`;

} catch (error) {
    console.error('Error deleting blog post:', error);
    return `Error: ${error.message}`;
}
