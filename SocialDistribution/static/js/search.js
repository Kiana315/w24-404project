// document.getElementById('search-form').addEventListener('submit', function(e) {
//     e.preventDefault();
//     const query = this.q.value;  // Get the entered search content
//     fetch(`/search/?q=${encodeURIComponent(query)}`)
//         .then(response => {
//             if (response.ok) {
//                 return response.json();
//             } else {
//                 throw new Error('User not found');
//             }
//         })
//         .then(data => {
//             window.location.href = data.url;  // Direct to user's profile page
//         })
//         .catch(error => {
//             alert(error.message);  // Pop-up window displays the user not found
//         });
// });

document.addEventListener('DOMContentLoaded', function() {
    const searchForm = document.getElementById('search-form');
    if (!searchForm) {
        console.error('Search form not found');
        return;
    }

    searchForm.addEventListener('submit', function(event) {
        event.preventDefault();

        // 确保在这里正确获取输入框的值
        const currentUserInput = searchForm.querySelector('input[name="user1_id"]');
        const searchQueryInput = searchForm.querySelector('input[name="user2_id"]');

        if (!currentUserInput || !searchQueryInput) {
            console.error('Input fields not found');
            return;
        }

        const currentUser = currentUserInput.value;
        const searchQuery = searchQueryInput.value;

        // 构造新的 URL 并重定向
        window.location.href = `/api/user/${currentUser}/${searchQuery}/`;
    });
});
