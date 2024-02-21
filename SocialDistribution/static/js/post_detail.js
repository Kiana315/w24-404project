document.addEventListener('DOMContentLoaded', function() {
    const postID = _getURLPostID();

    const likeButton = document.getElementById('post-like');
    const commentButton = document.getElementById('post-comment');
    const commentSubmitButton = document.getElementById('submit-comment');
    const shareButton = document.getElementById('post-share');
    const commentFormContainer = document.getElementById('comment-form-container');

    if (likeButton) {
        function handleLike() {
            const likeAPI = `/api/posts/${postID}/likes/`;
            fetch(likeAPI, {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({})
            })
                .then(response => response.json())
                .then(data => {
                    console.log('>> Like Sent Successfully: ', data);
                    // todo - UI update
                })
                .catch((error) => {
                    console.error('>> Like Sent Unsuccessfully: ', error);
                });
        }
        likeButton.addEventListener('click', handleLike);
    }

    if (commentButton) {
        function toggleCommentForm() {
            // If the form is hidden, show it, otherwise hide it
            if (commentFormContainer.style.display === 'none') {
                commentFormContainer.style.display = 'block';
            } else {
                commentFormContainer.style.display = 'none';
            }
        }

        commentButton.addEventListener('click', toggleCommentForm);
        if (commentSubmitButton) {
            function handleComment() {
                const commentText = document.getElementById('comment-text').value;
                const commentAPI = `/api/posts/${postID}/comments/`;

                fetch(commentAPI, {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({text: commentText})
                })
                    .then(response => {
                        if (!response.ok) {
                            throw new Error('Network response was not ok');
                        }
                        return response.json();
                    })
                    .then(data => {
                        console.log('>> Comment Sent Successfully: ', data);
                        // TODO - UI update
                        commentFormContainer.style.display = 'none';
                        document.getElementById('comment-text').value = '';
                    })
                    .catch((error) => {
                        console.error('>> Comment Sent Unsuccessfully: ', error);
                    });
            }
            commentSubmitButton.addEventListener('click', handleComment);
        }
    }

    if (shareButton) {
        function handleShare() {
            console.log('Share button clicked');
            // todo
        }
        shareButton.addEventListener('click', handleShare);
    }

});

function _getURLPostID() {
    const pathSections = window.location.pathname.split('/');
    return pathSections[2];
}
