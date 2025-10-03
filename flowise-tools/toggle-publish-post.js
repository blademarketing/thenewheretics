/*
* Tool: Toggle Publish Post
* Description: Toggle the publish status of a blog post (publish if unpublished, unpublish if published)
*
* REQUIRED VARIABLES (set in Flowise):
* - API_KEY: Your blog API key (98vQa7KezwhRAhq1N67SgAL7LDv30w-yGq411t5klVM)
*   Set this as a custom variable in Flowise: $vars.API_KEY
*
* REQUIRED INPUT SCHEMA PROPERTIES:
* - postId (number): The ID of the blog post to publish/unpublish
*
* EXAMPLE USAGE IN FLOWISE:
* - Input Schema: Add property "postId" (type: number)
* - When user says "publish post 1", the postId should be extracted and passed as 1
* - When user says "unpublish post 5", the postId should be 5
*
* Returns: JSON string containing the updated blog post with new publish status
*/

const fetch = require('node-fetch');

// CONFIGURATION - Update if needed
const BASE_URL = 'https://thenewheretics.blog';
const API_KEY = $vars.API_KEY; // Set this variable in Flowise custom variables

// Validate postId is provided
if (typeof $postId === 'undefined' || !$postId) {
    return 'Error: postId is required. Please provide the ID of the post to publish/unpublish.';
}

const url = `${BASE_URL}/api/posts/${$postId}/publish`;

const options = {
    method: 'PATCH',
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
        return `Error: Post with ID ${$postId} not found.`;
    }

    if (!response.ok) {
        return `Error: Unable to toggle publish status. Status: ${response.status} - ${response.statusText}`;
    }

    const data = await response.json();

    // Format success message
    const status = data.is_published ? 'published' : 'unpublished';
    const message = `Success: Post "${data.title}" has been ${status}.`;

    return `${message}\n\nUpdated Post Details:\n${JSON.stringify(data, null, 2)}`;

} catch (error) {
    console.error('Error toggling publish status:', error);
    return `Error: ${error.message}`;
}
