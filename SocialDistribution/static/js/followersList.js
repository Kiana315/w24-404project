document.addEventListener('DOMContentLoaded', () => {
    const username = _getURLUsername()
    fetch(`/api/user/${username}/followers/`)
        .then(response => {
            if (response.status === 200) {
                return response.json();
            } else {
                console.log("Something went wrong when fetching followers: " + response.status);
            }
        })
        .then(data => {
            let followersList = document.getElementById("followers-list");
            for (let follower of data) {
                followersList.innerHTML += "<li class='person'>" +
                    "<img class='person-photo' src='person1.jpg' alt='Profile Picture'>" +
                    "<p class='person-name'>" + follower.follower.username + "</p></li>";
            }
        })
});

function _getURLUsername() {
    const pathSections = window.location.pathname.split('/');
    return pathSections[2];
}
