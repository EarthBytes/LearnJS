async function sendQuery() {
    const inputEl = document.getElementById("userInput");
    const input = inputEl.value.trim();
    const chatLog = document.getElementById("chatLog");

    if (!input) return;

    // Add user message
    chatLog.innerHTML += `<p class="user">&gt; ${escapeHtml(input)}</p>`;
    inputEl.value = "";

    // Check for "quit" command
    if (input.toLowerCase() === "clear") {
        chatLog.innerHTML = ""; 
        inputEl.value = "";
        inputEl.focus();
        return; 
    }

    // Add typing indicator
    const typingElement = document.createElement("p");
    typingElement.className = "bot typing";
    typingElement.innerHTML = "Bot is typing...";
    chatLog.appendChild(typingElement);
    chatLog.scrollTop = chatLog.scrollHeight;

    try {
        const res = await fetch("http://127.0.0.1:8000/ask", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ message: input })
        });
        const data = await res.json();

        // Remove typing message
        typingElement.remove();
        
        // Process and add bot response with proper formatting
        const formattedResponse = formatBotResponse(data.response);
        const responseElement = document.createElement("div");
        responseElement.className = "bot";
        responseElement.innerHTML = formattedResponse;
        chatLog.appendChild(responseElement);
        
        chatLog.scrollTop = chatLog.scrollHeight;

    } catch (err) {
        // Remove typing message
        typingElement.remove();
        
        const errorElement = document.createElement("p");
        errorElement.className = "bot error";
        errorElement.innerHTML = "Error connecting to server.";
        chatLog.appendChild(errorElement);
        
        chatLog.scrollTop = chatLog.scrollHeight;
    }

    inputEl.focus();
}

function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

function formatBotResponse(response) {
    // Handle line breaks and bullet points properly
    let formatted = escapeHtml(response);
    
    // Convert \n to <br> for line breaks
    formatted = formatted.replace(/\n/g, '<br>');
    formatted = formatted.replace(/(?:^|<br>)•\s*(.*?)(?=<br>|$)/g, '<li>$1</li>');
    formatted = formatted.replace(/(<li>.*?<\/li>)+/gs, '<ul>$&</ul>');
    formatted = formatted.replace(/<br>\s*(?=<li|<ul)/g, '');
    formatted = formatted.replace(/<\/li><br>/g, '</li>');
    formatted = formatted.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');
    formatted = formatted.replace(/```([\s\S]*?)```/g, '<pre><code>$1</code></pre>');
    formatted = formatted.replace(/`([^`]+)`/g, '<code>$1</code>');
    if (!/^<ul>/.test(formatted)) {
        formatted = '<p class="bot">' + formatted + '</p>';
    }
    
    return formatted;
}

// Handle Enter key press
document.getElementById("userInput").addEventListener("keypress", function(event) {
    if (event.key === "Enter") {
        event.preventDefault();
        sendQuery();
    }
});

// Auto-focus on input field when page loads
document.addEventListener("DOMContentLoaded", function() {
    document.getElementById("userInput").focus();
});