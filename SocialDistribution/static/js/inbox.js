'use strict';


document.addEventListener('DOMContentLoaded', function() {
let messages = document.querySelectorAll('.inbox-messages .message');

messages.forEach(function(message) {
    message.querySelector('.message-header').addEventListener('click', function() {
        message.classList.toggle('unfolded');
    });
});
});