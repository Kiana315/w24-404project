document.addEventListener('DOMContentLoaded', function() {
    const followButton = document.getElementById('follow-btn');
    if (followButton) {
        followButton.addEventListener('click', function() {
            const username = this.getAttribute('data-username');
            fetch(`/follow/${username}/`, {
                method: 'POST',
                headers: {
                    'X-CSRFToken': getCookie('csrftoken'),
                    'Content-Type': 'application/json'
                }
            })
            .then(response => {
                if (response.ok) {
                    followButton.style.display = 'none'; // 隐藏按钮
                    // 可选：更新正在关注列表
                } else {
                    alert("Something went wrong.");
                }
            })
            .catch(error => console.error('Error:', error));
        });
    }
});
