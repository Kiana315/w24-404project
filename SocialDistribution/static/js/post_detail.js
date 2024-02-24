'use strict';

document.addEventListener('DOMContentLoaded', function() {
    const moreOptionsButton = document.getElementById('more-options-button');
    const optionsContainer = document.getElementById('options-container');
    const postContainer = document.querySelector('.post-container');
    const postId = postContainer.getAttribute('data-post-id');
    const likeButton = document.getElementById('like-button');
    const likeCountElement = document.getElementById('like-count');
    const commentButton = document.getElementById('comment-button');
    const commentForm = document.getElementById('comment-form');
    const submitCommentButton = document.getElementById('submit-comment');
    const commentInput = document.getElementById('comment-input');

    moreOptionsButton.addEventListener('click', function() {
        if (optionsContainer.style.display === 'none') {
            optionsContainer.style.display = 'block';
        } else {
            optionsContainer.style.display = 'none';
        }
    });

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
                    throw new Error(`HTTP error! status: ${response.status}, statusText: ${response.statusText}`);
                }
            })
            .then(() => {
                fetchComments();
                commentInput.value = ''; // Clear the input field
                commentForm.style.display = 'none'; // Hide the comment form again
            })
            .catch(error => {
                console.error('Error:', error);
                console.log('Error message:', error.message);
                alert(error.message);
            });
        });
    }
});

function fetchComments() {
    const postId = document.querySelector('.post-container').getAttribute('data-post-id');
    fetch(`/api/posts/${postId}/comments/`)
        .then(response => {
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}, statusText: ${response.statusText}`);
            }
            return response.json();
        })
        .then(data => {
            renderComments(data);
        })
        .catch(error => {
            console.error('Error:', error);
            console.log('Error message:', error.message);
            alert(error.message);
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

function getPostIdFromUrl() {
    const path = window.location.pathname;
    const pathParts = path.split('/');  // split the url
    const postId = pathParts[pathParts.length - 2];  // get the post ID from url
    return postId;
}

function deletePost() {
    const postId = getPostIdFromUrl();
    if (confirm("Are you sure you want to delete this post?")) {
        fetch(`/posts/${postId}/delete/`, {
            method: 'DELETE',
            headers: {
                'X-CSRFToken': getCookie('csrftoken')
            }
        }).then(response => {
            if (response.status === 204) {
                window.location.href = '/';
            } else {
                alert("Something went wrong.");
            }
        }).catch(error => console.error('Error:', error));
    }
}

document.addEventListener('DOMContentLoaded', function() {
    // 获取弹出框和关闭按钮
    var modal = document.getElementById("editModal");
    var closeButton = document.querySelector(".close");

    // 获取 "Edit" 按钮并添加点击事件监听器
    var editButton = document.getElementById("edit-button");
    editButton.addEventListener('click', function() {
        modal.style.display = "block";
        // 填充表单数据
        // var currentData = ...; 获取当前需要编辑的数据
        // document.getElementById("editContent").value = currentData;
    });

    // 点击关闭按钮时隐藏弹出框
    closeButton.addEventListener('click', function() {
        modal.style.display = "none";
    });

    // 提交表单的逻辑
    var form = document.getElementById("editForm");
    form.addEventListener('submit', function(event) {
        event.preventDefault();
        // 提交数据到服务器
        // var updatedData = document.getElementById("editContent").value;
        // ... 发送 AJAX 请求等操作
    });

    // 点击弹出框外部时也隐藏弹出框
    window.onclick = function(event) {
        if (event.target == modal) {
            modal.style.display = "none";
        }
    };
});

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
