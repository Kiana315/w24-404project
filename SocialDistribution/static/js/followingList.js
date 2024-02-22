// TODO
document.addEventListener('DOMContentLoaded', function() {
    const username = '当前用户名';  // 获取当前用户名
    loadFollowing(username);
});

function updateFollowingList(data) {
    const followingList = document.getElementById('following-list');
    followingList.innerHTML = '';  // 清空现有内容
    data.forEach(user => {
        // 创建新的元素来展示每个用户
        const userElement = document.createElement('div');
        userElement.textContent = user.username;
        followingList.appendChild(userElement);
    });
}