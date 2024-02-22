document.addEventListener('DOMContentLoaded', () => {
    const username = _getURLUsername()
    fetch(`profile/${username}/follower/`)
    .then(response => {
        if (response.status == 200) {
            return response.json();
        } else {
            alert("Something went wrong when fetching followers: " + response.status);
        }
    })
    .then(data => {
        var followersList = document.getElementById("followers-list");
        followersList.innerHTML = "";

        for (follower in data) {
            followersList.innerHTML += "<li class='person'><img class='person-photo' src='person1.jpg' alt='Profile Picture'></img><p class='person-name'>" + follower.username + "</p></li>";
        }
    })
});

function _getURLUsername() {
    const pathSections = window.location.pathname.split('/');
    return pathSections[2];
}
