document.addEventListener('DOMContentLoaded', function() {
    const editButton = document.getElementById('edit-btn');
    const editModal = document.getElementById('editPostModal');
    const titleInput = document.getElementById('titleInput');
    const contentInput = document.getElementById('contentInput');
    const closeButton = document.querySelector('.modal .close');

    // 假设这些是从后端获取的当前帖子的数据

    titleInput.value = currentPostTitle;
    contentInput.value = currentPostContent;

    // 当点击编辑按钮时
    editButton.addEventListener('click', function() {
        // 显示编辑模态框
        editModal.style.display = 'block';
        console.log("btn clicked");
        // 加载当前帖子的数据到表单中
        titleInput.value = currentPostTitle;
        contentInput.value = currentPostContent;
    });

    // Click the x to close the pop-up window
    document.getElementsByClassName("close")[0].onclick = function() {
        modal.style.display = "none";
    }

    // 处理编辑表单的提交
    const editForm = document.getElementById('editPostForm');
    editForm.addEventListener('submit', function(event) {
        event.preventDefault();

        // 获取表单中的数据
        const updatedTitle = titleInput.value;
        const updatedContent = contentInput.value;

        // TODO: 发送这些数据到服务器进行更新
        console.log('Updated Title:', updatedTitle);
        console.log('Updated Content:', updatedContent);

        // 关闭模态框
        editModal.style.display = 'none';
    });
});
