$(document).ready(function() {
    // Scroll to the latest message on document ready
    function scrollToLatestMessage() {
        const chatBox = document.querySelector('.chat-box');
        chatBox.scrollTop = chatBox.scrollHeight;
    }

    scrollToLatestMessage();

    // Function to reset the chat by making an AJAX request to the reset endpoint
    function resetChat() {
        fetch('/reset_chat', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            }
        })
        .then(response => response.json())
        .then(data => {
            if (data.status === "Chat history reset.") {
                // Clear chat UI
                const chatBox = document.querySelector('.chat-box');
                chatBox.innerHTML = '';
            }
        });
    }

    // Add event listeners when the DOM is completely loaded
    const userInput = document.getElementById('user_input');
    const form = userInput.closest('form');

    // Focus the input field when the page loads
    userInput.focus();

    // Listen for 'Enter' keypress to submit the form
    userInput.addEventListener('keypress', function(event) {
        if (event.key === 'Enter' && !event.shiftKey) {
            event.preventDefault();
            form.submit();
        }
    });

    // Scroll to the latest message after each form submission
    form.addEventListener('submit', function() {
        setTimeout(scrollToLatestMessage, 100); // Delay to ensure the new message is loaded
    });

    // Event listener for reset button
    const resetButton = document.getElementById('reset-button');
    if (resetButton) {
        resetButton.addEventListener('click', resetChat);
    }
});