'use strict';


function clickableListItem() {
    document.addEventListener('DOMContentLoaded', function() {
        let messages = document.querySelectorAll('.inbox-messages .message');
        messages.forEach(function(message) {
            message.querySelector('.message-header').addEventListener('click', function() {
                message.classList.toggle('unfolded');
            });
        });
    });
}


function clickableFilterMessages() {
    document.addEventListener('DOMContentLoaded', function() {
        let filterForm = document.getElementById('filter-form');
        let messageContainer = document.querySelector('.inbox-container');
        filterForm.addEventListener('submit', function(event) {
            event.preventDefault();
            let filterValue = document.getElementById('filter').value;
            filterMessages(filterValue);
        });
    });
}

function filterMessages(filter) {
    let messages = messageContainer.querySelectorAll('.message');
    messages.forEach(function(message) {
        switch (filter) {
            case 'all':
                message.style.display = '';
                break;
            case 'unread':
                if (message.classList.contains('unread')) {
                    message.style.display = '';
                } else {
                    message.style.display = 'none';
                }
                break;
            case 'read':
                if (!message.classList.contains('unread')) {
                    message.style.display = '';
                } else {
                    message.style.display = 'none';
                }
                break;
        }
    });
}


function createMessage(msg, isNewMsg=true) {
    let li_message = document.createElement("li");
    li_message.classList.add("message");
    if (isNewMsg) li_message.classList.add("unread");

    let div_messageHeader = document.createElement("div")
    div_messageHeader.classList.add("message-header")
    let span_statusDot = document.createElement("span")
    let span_sender = document.createElement("span")
    let span_subject = document.createElement("span")

    span_statusDot.classList.add("status-dot")
    span_sender.classList.add("sender")
    span_sender.textContent = msg.sender;
    span_subject.classList.add("subject")
    span_subject.textContent = msg.subject;
    div_messageHeader.appendChild(span_statusDot)
    div_messageHeader.appendChild(span_sender)
    div_messageHeader.appendChild(span_subject)

    let div_messageBody = document.createElement("div")
    div_messageBody.classList.add("message-body")
    let p_text = document.createElement("p")
    p_text.textContent = msg.text;
    p_text.classList.add("message-text")
    let button_delete = document.createElement("button")
    button_delete.classList.add("inbox-delete-btn")
    button_delete.textContent = "Delete"
    let button_star = document.createElement("button")
    button_star.classList.add("inbox-star-btn")
    button_star.textContent = "Star"

    div_messageBody.appendChild(p_text)
    div_messageBody.appendChild(button_delete)
    div_messageBody.appendChild(button_star)
    li_message.appendChild(div_messageHeader)
    li_message.appendChild(div_messageBody)
    return li_message
}


function fetchInboxMessage(username) {
    let request = new Request(`api/msgs/${username}/`);
    fetch(request)
        .then(response => {
            if (!response.ok) throw new Error("Invalid Request Response");
            return response.json();
        })
        .then(userPosts => {
            let ul_inboxMsgContainer = document.getElementById("inbox-messages-container");
            for (let userPost in userPosts) {
                let li_message = createMessage(username);
                ul_inboxMsgContainer.appendChild(li_message);
            }
        })
        .catch(error => {
            console.error('Fetching Error', error);
        });
}



/*
var messageList = document.querySelector('ul'); // Replace 'ul' with the appropriate selector for your list
var newMessage = createMessage({
    header: '', // Assuming header should be empty for a status dot
    sender: 'Eden',
    subject: 'Hey, did you get my last message?',
    text: 'Hey, just checking to see if you received my last message. Let me know if you have any questions about the project.'
}, true);
messageList.appendChild(newMessage);
*/


// todo - How to acquire the username?
// todo - How to change the msg status?

clickableListItem();
clickableFilterMessages();
fetchInboxMessage(username="Eden");
