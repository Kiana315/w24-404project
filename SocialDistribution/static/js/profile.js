function editUserName() {
    let el = document.getElementById("username");
    el.style.display = 'none';

    let input = document.getElementById("edit-username");
    input.style.display = 'inline';
    input.focus();
    input.value = el.innerText;
}

function handleUserNameBlur() {
    let el = document.getElementById("edit-username");
    let formData = new FormData();
    formData.append("username", el.value)
    fetch(`update-username/`, {
        method: 'POST',
        headers: {
            'X-CSRFToken': getCookie('csrftoken') // Get CSRF token
        },
        body: formData
    })
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(data => {
            let errEl = document.getElementById("update-username-error")
            if (errEl) {
                errEl.remove()
            }
            if (data.error !== '') {
                let parentElement = document.getElementById("profile-info");
                let spanElement = document.createElement("span");
                spanElement.textContent = data.error;
                spanElement.style.color = 'red';
                spanElement.setAttribute("id", "update-username-error")
                parentElement.insertBefore(spanElement, el.nextSibling)
                el.focus();
            } else {
                el.style.display = 'none'
                let username = document.getElementById("username");
                username.innerText = el.value
                username.style.display = 'inline';
                let parts = window.location.pathname.split('/')
                parts[parts.length - 2] = el.value
                history.replaceState(null, "User Profile Page", parts.join('/'));
            }

        })
        .catch(error => {
            el.focus();
        });
}


document.addEventListener('DOMContentLoaded', function() {
    const followButton = document.getElementById('follow-btn');
    if (followButton) {
        followButton.addEventListener('click', function() {
            const selfUsername = _getURLSelfUsername();
            const targetUsername = _getURLTargetUsername();

            fetch(`/api/user/${selfUsername}/followerOf/${targetUsername}/`, {
                method: 'POST',
                headers: {
                    'X-CSRFToken': getCookie('csrftoken'),
                    'Content-Type': 'application/json'
                }
            })
            .then(response => {
                if (response.ok) {
                    followButton.style.display = 'none';
                    alert("Follow Success!");
                } else {
                    alert("Already Followed...");
                }
            })
            .catch(error => console.error('Error:', error));
        });
    }
});

function _getURLTargetUsername() {
    const pathSections = window.location.pathname.split('/').filter(Boolean);;
    return pathSections[pathSections.length - 1];
}

function _getURLSelfUsername() {
    const pathSections = window.location.pathname.split('/').filter(Boolean);;
    return pathSections[pathSections.length - 2];
}


function getCookie(name){
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}