'use strict';

document.addEventListener('DOMContentLoaded', function() {
    const postContainer = document.querySelector('.post-container');
    const postId = postContainer.getAttribute('data-post-id');
    const likeButton = document.getElementById('like-button');
    const likeCountElement = document.getElementById('like-count');
    const commentButton = document.getElementById('comment-button');
    const commentForm = document.getElementById('comment-form');
    const submitCommentButton = document.getElementById('submit-comment');
    const commentInput = document.getElementById('comment-input');

    fetchComments();

    if (likeButton) {
        likeButton.addEventListener('click', function() {
            const likeCount = parseInt(likeCountElement.textContent, 10);

            console.log('Like button clicked for post:', postId);

            fetch(`/api/posts/${postId}/likes/`, {
                method: 'POST',
                headers: {
                    'X-CSRFToken': getCookie('csrftoken') // Get CSRF token
                },
            })
            .then(response => {
                if (!response.ok) {
                    throw new Error('Network response was not ok');
                }
                return response.json(); 
            })
            .then(data => {
                likeCountElement.textContent = data.likes_count; 
                likeButton.classList.add('liked');
            })
            .catch(error => {
                console.error('There was a problem with the fetch operation:', error);
            });
        });
    }

    if (commentButton) {
        commentButton.addEventListener('click', function() {
            commentForm.style.display = 'block'; // Show the comment form
        });

        // Event listener for submitting a comment
        submitCommentButton.addEventListener('click', function() {
            const commentText = commentInput.value.trim();

            if (commentText === '') {
                alert('Please enter a comment.');
                return;
            }

            // Proceed with submitting the comment
            fetch(`/api/posts/${postId}/comments/`, {
                method: 'POST',
                headers: {
                    'X-CSRFToken': getCookie('csrftoken'),
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ comment_text: commentText })
            })
            .then(response => {
                if (!response.ok) {
                    throw new Error('Network response was not ok');
                }
            })
            .then(() => {
                fetchComments();
                commentInput.value = ''; // Clear the input field
                commentForm.style.display = 'none'; // Hide the comment form again
            })
            .catch(error => {
                console.error('Error:', error);
            });
        });
    }
});

function fetchComments() {
    const postId = document.querySelector('.post-container').getAttribute('data-post-id');
    fetch(`/api/posts/${postId}/comments/`)
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(data => {
            renderComments(data);
        })
        .catch(error => {
            console.error('Error:', error);
        });
}

function renderComments(comments) {
    const commentsContainer = document.getElementById('comments-container');
    commentsContainer.innerHTML = ''; 

    comments.forEach(comment => {
        // Create Content Container
        const commentElement = document.createElement('div');
        commentElement.classList.add('comment');

        const avatarElement = document.createElement('img');
        avatarElement.src = comment.commenter_avatar_url; 
        avatarElement.alt = 'User Avatar';
        avatarElement.classList.add('comment-avatar'); 

        // add username
        const commenterNameElement = document.createElement('h5');
        commenterNameElement.textContent = comment.commenter_username;
        commenterNameElement.classList.add('commenter-name');
        
        // add comment text
        const commentTextElement = document.createElement('p');
        commentTextElement.textContent = comment.comment_text;
        commentTextElement.classList.add('comment-text');

        // append username, comment text, and
        commentElement.appendChild(avatarElement);
        commentElement.appendChild(commenterNameElement);
        commentElement.appendChild(commentTextElement);

        commentsContainer.appendChild(commentElement);
    });
}

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

            