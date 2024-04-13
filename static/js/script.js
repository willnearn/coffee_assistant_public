document.getElementById('send-btn').addEventListener('click', sendMessage);

document.getElementById('chat-input').addEventListener('keydown', function(event) {
    if (event.key === 'Enter') {
        event.preventDefault(); // Prevent the default action to avoid submitting the form or inserting a newline
        sendMessage();
    }
});

function sendMessage() {
    const input = document.getElementById('chat-input');
    const msg = input.value.trim();

    if (msg) {
        // Display the user's message
        displayMessage('You', msg);

        // Get a response from the chatbot backend
        postData('/', { input_string: msg })  //URL used to be https://umithecoffeecat.azurewebsites.net/api/endpoint
            .then(data => {
                // Display the response from the back-end
                displayMessage('Umi', data.output_string);
            })
            .catch(error => {
                console.error('Error:', error);
            });
    }

    input.value = ''; // Clear the input field
}

function displayMessage(sender, message) {
    const chatBody = document.getElementById('chat-body');
    const messageElement = document.createElement('div');
    if (sender === 'Umi') {
        messageElement.classList.add('umi-message');
        const img = document.createElement('img');
        img.src = '/static/images/pic5.jpeg';
        img.alt = 'Umi';
        img.style.width = '30px';
        img.style.height = '30px';
        img.style.marginRight = '4px';
        img.style.marginTop = '6px';

        const textSpan = document.createElement('span');
        const formattedMessage = marked.parse(message); // Convert markdown to HTML
        textSpan.innerHTML = DOMPurify.sanitize(formattedMessage); // Sanitize HTML content

        messageElement.appendChild(img);
        messageElement.appendChild(textSpan);
    } else {
        messageElement.classList.add('user-message');
        messageElement.textContent = `${sender}: ${message}`;
    }
    chatBody.appendChild(messageElement);

    chatBody.scrollTop = chatBody.scrollHeight;
}


// Communicate with back-end
function postData(url = '', data = {}) {
    // Default options are marked with *
    return fetch(url, {
      method: 'POST', // *GET, POST, PUT, DELETE, etc.
      mode: 'cors', // no-cors, *cors, same-origin
      cache: 'no-cache', // *default, no-cache, reload, force-cache, only-if-cached
      credentials: 'same-origin', // include, *same-origin, omit
      headers: {
        'Content-Type': 'application/json'
        // 'Content-Type': 'application/x-www-form-urlencoded',
      },
      redirect: 'follow', // manual, *follow, error
      referrerPolicy: 'no-referrer', // no-referrer, *no-referrer-when-downgrade, origin, origin-when-cross-origin, same-origin, strict-origin, strict-origin-when-cross-origin, unsafe-url
      body: JSON.stringify(data) // body data type must match "Content-Type" header
    })
    .then(response => response.json()); // parses JSON response into native JavaScript objects
  }


//Don't zoom in
const viewport = document.querySelector("meta[name=viewport]");

document.querySelectorAll("input, textarea").forEach(input => {
    input.addEventListener("focus", () => {
        viewport.setAttribute("content", "width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=0");
    });

    input.addEventListener("blur", () => {
        viewport.setAttribute("content", "width=device-width, initial-scale=1.0");
    });
});

function displayInitialMessage() {
    fetch('/initial_message')
        .then(response => response.json())
        .then(data => {
            const initialMessage = data.initialMessage;
            displayMessage('Umi', initialMessage);
        })
        .catch(error => console.error('Error fetching initial message:', error));
}


window.addEventListener('load', (event) => {
    displayInitialMessage();  // This will fetch and display the initial message after page load
});

