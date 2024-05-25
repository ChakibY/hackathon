document.getElementById('send-button').addEventListener('click', async () => {
    const input = document.getElementById('chat-input').value;
    const chatWindow = document.getElementById('chat-window');

    if (!input.trim()) {
        return; // Don't send empty messages
    }

    // Display user message
    const userMessage = document.createElement('div');
    userMessage.className = 'user-message';
    userMessage.textContent = input;
    chatWindow.appendChild(userMessage);

    // Clear input
    document.getElementById('chat-input').value = '';

    // Add a delay to pace requests
    await new Promise(resolve => setTimeout(resolve, 1000)); // 1000 ms delay

    // Send message to the server
    try {
        const response = await fetch('/chat', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ message: input }),
        });

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        const data = await response.json();
        console.log("Server response:", data);  // Log the server response

        // Display bot response
        const botMessage = document.createElement('div');
        botMessage.className = 'bot-message';
        botMessage.textContent = data.message;
        chatWindow.appendChild(botMessage);
    } catch (error) {
        console.error('Error:', error);  // Log any errors
        const errorMessage = document.createElement('div');
        errorMessage.className = 'error-message';
        errorMessage.textContent = `Error: ${error.message}`;
        chatWindow.appendChild(errorMessage);
    }
});
