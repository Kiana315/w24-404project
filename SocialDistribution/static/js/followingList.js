document.addEventListener('DOMContentLoaded', () => {
    const username = _getURLUsername();
    fetch(`profile/${username}/following/`)  
    .then(response => {
        if (response.status === 200) {
            return response.json();
        } else {
            alert("Something went wrong when fetching followings: " + response.status);
        }
    })
    .then(data => {
        var followingList = document.getElementById("following-list");  
        followingList.innerHTML = "";

        data.forEach(following => {  
            followingList.innerHTML += "<li class='person'><img class='person-photo' src='person1.jpg' alt='Profile Picture'></img><p class='person-name'>" + following.username + "</p></li>";
        });
    });
});

function _getURLUsername() {
    const pathSections = window.location.pathname.split('/');
    return pathSections[2];
}
