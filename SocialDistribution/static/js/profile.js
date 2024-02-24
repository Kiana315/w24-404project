function editUserName() {
    var el = document.getElementById("username");
    el.style.display = 'none';

    var input = document.getElementById("edit-username");
    input.style.display = 'inline';
    input.focus();
    input.value = el.innerText;
}

function handleUserNameBlur() {
    var el = document.getElementById("edit-username");

    var formData = new FormData();
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
            var errEl = document.getElementById("update-username-error")
            if (errEl) {
                errEl.remove()
            }
            if (data.error !== '') {
                var parentElement = document.getElementById("profile-info");
                var spanElement = document.createElement("span");
                spanElement.textContent = data.error;
                spanElement.style.color = 'red';
                spanElement.setAttribute("id", "update-username-error")
                parentElement.insertBefore(spanElement, el.nextSibling)
                el.focus();
            } else {
                el.style.display = 'none'
                var username = document.getElementById("username");
                username.innerText = el.value
                username.style.display = 'inline';
                var parts = window.location.pathname.split('/')
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
            const selfUsername = this.getAttribute('data-username');
            const targetUsername = _getURLTagetUsername()
            fetch(`api/user/${selfUsername}/followerOf/${targetUsername}}/`, {
                method: 'POST',
                headers: {
                    'X-CSRFToken': getCookie('csrftoken'),
                    'Content-Type': 'application/json'
                }
            })
            .then(response => {
                if (response.ok) {
                    followButton.style.display = 'none';
                } else {
                    alert("Something went wrong.");
                }
            })
            .catch(error => console.error('Error:', error));
        });
    }
});


function _getURLTagetUsername() {
    const pathSections = window.location.pathname.split('/');
    return pathSections[-1];
}