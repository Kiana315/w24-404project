document.addEventListener('DOMContentLoaded', function() {
    const editButton = document.getElementById('edit-btn'); // 确保这个 ID 与 HTML 中的按钮 ID 匹配
    const editModal = document.getElementById('editPostModal');
    const closeButton = document.querySelector('.modal .close'); // 确保选择器正确

    // 当点击编辑按钮时
    editButton.addEventListener('click', function() {
        // 显示编辑模态框
        editModal.style.display = 'block';

        // TODO: 从后端获取帖子标题和内容
        // 假设这里是 AJAX 请求或其他方式获取的数据
        const currentPostTitle = '从后端获取的标题';
        const currentPostContent = '从后端获取的内容';

        // 加载当前帖子的数据到表单中
        document.getElementById('titleInput').value = currentPostTitle;
        document.getElementById('contentInput').value = currentPostContent;
    });

    // 点击关闭按钮时隐藏弹出框
    closeButton.addEventListener('click', function() {
        editModal.style.display = 'none';
    });

    // 处理编辑表单的提交
    const editForm = document.getElementById('editPostForm');
    editForm.addEventListener('submit', function(event) {
        event.preventDefault();
        // 获取表单中的数据
        const updatedTitle = document.getElementById('titleInput').value;
        const updatedContent = document.getElementById('contentInput').value;

        // TODO: 发送这些数据到服务器进行更新
        console.log('Updated Title:', updatedTitle);
        console.log('Updated Content:', updatedContent);

        // 关闭模态框
        editModal.style.display = 'none';
    });
});
