function submitQuestion() {
  // Get the user's question
  var userInput = document.getElementById('userInput');
  var question = userInput.value;
  userInput.value = '';

  // Add the question to the chatbox
  addMessageToChatbox('User: ' + question, 'user-message');

  // Send the question to the server and get the answer
  fetch('/get_answer', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({question: question})
  })
  .then(response => response.json())
  .then(data => {
    // Add the answer to the chatbox
    addMessageToChatbox('PDF: ' + data.answer + ' (Page numbers: ' + data.page_numbers + ')', 'bot-message');

    // Scroll the chatbox to the bottom
    var chatbox = document.getElementById('chatbox');
    chatbox.scrollTop = chatbox.scrollHeight;
  });
}

function addMessageToChatbox(message, type) {
    let chatbox = document.getElementById('chatbox');
    let newMessage = document.createElement('div');
    newMessage.className = 'message ' + type;
    newMessage.innerText = message;
    chatbox.appendChild(newMessage);
}
