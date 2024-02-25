document.addEventListener('DOMContentLoaded', function() {
    const postContainer = document.querySelector('.post-container');
    const postId = postContainer.getAttribute('data-post-id');
    const editButton = document.getElementById('edit-btn'); 
    const editModal = document.getElementById('editModal');
    const options= document.getElementById('options-container');

    editButton.addEventListener('click', function() {
        editModal.style.display = 'block';  // Show up edit modal
        options.style.display = 'none';     // Hide menu

        fetch(`/api/posts/${postId}/`)
            .then(response => {
                if (!response.ok) {
                    throw new Error('Network response was not ok');
                }
                return response.json();
            })
            .then(data => {
                // Load the obtained data into the form
                document.getElementById('titleInput').value = data.title;
                document.getElementById('contentInput').value = data.content;
            })
            .catch(error => {
                console.error('Error fetching post data:', error);
        });
        
    });

    // Close modal when clicking outside
    window.onclick = function(event) {
        if (event.target === editModal) {
            editModal.style.display = "none";
        }
    }

    // Handling edit form submissions
    const editForm = document.getElementById('editForm');
    editForm.addEventListener('submit', function(event) {
        event.preventDefault();
        // Get new data from form
        const updatedTitle = document.getElementById('titleInput').value;
        const updatedContent = document.getElementById('contentInput').value;
        
        fetch(`/api/posts/${postId}/update/`, {
            method: 'PUT',  
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken')  
            },
            body: JSON.stringify({ title: updatedTitle, content: updatedContent })
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(data => {
            
            console.log('Post updated:', data);
            editModal.style.display = 'none'; // Close modal after submit
            window.location.reload();
        })
        .catch(error => {
            console.error('Error:', error);
        });

        
    });
});

function closeModal() {
    editModal.style.display = 'none';
}