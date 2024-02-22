document.getElementById('search-form').addEventListener('submit', function(e) {
    e.preventDefault();
    const query = this.q.value;  // Get the entered search content
    fetch(`/search/?q=${encodeURIComponent(query)}`)
        .then(response => {
            if (response.ok) {
                return response.json();
            } else {
                throw new Error('User not found');
            }
        })
        .then(data => {
            window.location.href = data.url;  // Direct to user's profile page
        })
        .catch(error => {
            alert(error.message);  // Pop-up window displays the user not found
        });
});