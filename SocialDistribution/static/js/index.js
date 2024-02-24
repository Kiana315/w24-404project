'use strict';


document.addEventListener('DOMContentLoaded', () => {
  

    fetch('/api/pps/')
        .then(response => response.json())
        .then(posts => {
            const postContainer = document.getElementById('post-container');
            posts.forEach(post => {
                const postElement = document.createElement('div');
                postElement.className = 'post';

                const postLink = document.createElement('a');
                postLink.href = `/posts/${post.id}`;
                postLink.className = 'post-link';

                const datePosted = new Date(post.date_posted);
                const formattedDate = `${datePosted.getFullYear()}-${datePosted.getMonth() + 1}-${datePosted.getDate()}`;

                const userInfoHTML = `
                    <div class="user-info">
                        <img src="${post.avatar}" alt="profile avatar" class="user-avatar">
                        <div class="username">${post.username || 'Unknown User'}</div>
                        <div class="post-time">${formattedDate}</div>
                    </div>
                `;

                const contentHTML = `
                    <div class="content">
                        <div class="title">${post.title}</div>
                        <p>${post.content}</p>
                    </div>
                `;

                const interactionHTML = `
                    <div class="interact-container">
                        <button id="share-button" type="button">
                            <ion-icon size="small" name="share-outline" style="margin-right: 8px;"></ion-icon>
                            Share
                        </button>
                        <button id="comment-button" type="button">
                            <ion-icon size="small" name="chatbox-ellipses-outline" style="margin-right: 8px;"></ion-icon>
                            Comment
                        </button>
                        <button id="like-button" type="button"> 
                            <ion-icon size="small" name="heart-outline" style="margin-right: 8px;"></ion-icon>
                            <span id="like-count">{{ likes_count }}</span>
                        </button>
                    </div>
                `;

                // Append userInfoHTML, contentHTML, and interactionHTML to postLink instead of postElement
                postLink.innerHTML = userInfoHTML + contentHTML;
                postElement.appendChild(postLink);
                postElement.innerHTML += interactionHTML;
                postContainer.appendChild(postElement);

                // Event listeners for like and comment buttons
                const likeButton = postElement.querySelector('.like-btn');
                const commentButton = postElement.querySelector('.comment-btn');
                const commentBox = document.createElement('div');
                commentBox.className = 'comment-box';
                commentBox.style.display = 'none';
                commentBox.innerHTML = `
                    <textarea class="comment-text" placeholder="Add a comment..."></textarea>
                    <button type="button" class="submit-comment">Post Comment</button>
                `;

                postElement.appendChild(commentBox);

                commentButton.addEventListener('click', (e) => {
                    e.stopPropagation();
                    commentBox.style.display = commentBox.style.display === 'none' ? 'block' : 'none';
                });
                likeButton.addEventListener('click', (e) => {
                    e.stopPropagation();
                    console.log('Like button clicked for post:', post.id);
                    fetch(`/api/posts/${post.id}/likes/`, {
                        method: 'POST',
                        headers: {'Content-Type': 'application/json'},
                        body: JSON.stringify({}),
                    })
                    .then(response => {
                        if (response.ok) {
                            console.log('>> Like Sent Successfully;');
                        } else {
                            console.log('>> Like Sent Unsuccessfully;');
                        }
                    })
                    .catch(error => console.error('Error:', error));
                });

                const submitCommentButton = commentBox.querySelector('.submit-comment');
                submitCommentButton.addEventListener('click', () => {
                    const commentText = commentBox.querySelector('.comment-text').value;
                    console.log('Comment submitted for post:', post.id, 'Comment:', commentText);
                    fetch(`/api/posts/${post.id}/comments/`, {
                        method: 'POST',
                        headers: {'Content-Type': 'application/json'},
                        body: JSON.stringify({ text: commentText }),
                    })
                    .then(response => {
                        if (response.ok) {
                            console.log('>> Comment Sent Successfully;');
                        } else {
                            console.log('>> Comment Sent Unsuccessfully;');
                        }
                    })
                    .catch(error => console.error('Error:', error));
                });
            });
        })
        .catch(error => console.error('Error:', error));
})

