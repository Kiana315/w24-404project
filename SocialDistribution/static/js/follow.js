function loadFollowers(username) {
    fetch(`/profile/${username}/followers/`)
        .then(response => response.json())
        .then(data => {
            // 使用 data 来更新页面
        });
}

function loadFollowing(username) {
    fetch(`/profile/${username}/following/`)
        .then(response => response.json())
        .then(data => {
            // 使用 data 来更新页面
        });
}
