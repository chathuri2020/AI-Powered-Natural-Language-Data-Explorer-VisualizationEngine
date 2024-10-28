document.getElementById('send-button').addEventListener('click', function() {
    const message = document.getElementById('message-input').value;
    fetch('/send_message/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
            'X-CSRFToken': getCookie('csrftoken')
        },
        body: `message=${encodeURIComponent(message)}`
    })
    .then(response => response.json())
    .then(data => {
        const history = document.querySelector('.history');
        history.innerHTML += `<div class="message"><p>${data.message}</p></div>`;
        document.getElementById('message-input').value = '';
    });
});

function getCookie(name) {
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
