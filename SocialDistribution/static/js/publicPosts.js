'use strict';


function createPost(userPost) {
    let div_post = document.createElement("div");
    let div_userInfo = document.createElement("div");
    let img_avatar = document.createElement("img");
    let div_userName = document.createElement("div");
    let div_content = document.createElement("div");
    let p_content = document.createElement("p");

    div_post.classList.add("post");
    div_post.appendChild(div_userInfo);
    div_post.appendChild(div_content);

    div_userInfo.classList.add("user-info");
    div_userInfo.appendChild(img_avatar);
    div_userInfo.appendChild(div_userName);
    img_avatar.classList.add("avatar");
    img_avatar.src = "";
    img_avatar.alt = "User Avatar";
    div_userName.classList.add("username");
    div_userName.textContent = userPost.username;

    div_content.classList.add("content");
    div_content.appendChild(p_content);
    p_content.textContent = userPost.content;

    return div_post;
}

function fetchPublicPosts() {
    let request = new Request(`/api/pps/`);
    fetch(request)
        .then(response => {
            if (!response.ok) throw new Error("Invalid Request Response");
            return response.json();
        })
        .then(userPosts => {
            let div_postContainer = document.getElementById("post-container");
            for (let userPost in userPosts) {
                let div_post = createPost(userPost);
                div_postContainer.appendChild(div_post);
            }
        })
        .catch(error => {
            console.error('Fetching Error', error);
        });
}


window.addEventListener("load", fetchPublicPosts)




