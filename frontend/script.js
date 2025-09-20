async function sendQuery() {
    const input = document.getElementById("userInput").value;
    const chatLog = document.getElementById("chatLog");

    if (!input.trim()) return;

    // Add user message
    chatLog.innerHTML += `<p class="user">&gt; ${escapeHtml(input)}</p>`;
    document.getElementById("userInput").value = "";
    
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
    
    // Convert bullet points (• followed by text) to proper HTML
    formatted = formatted.replace(/•\s*([^<]*?)(?=<br>|$)/g, '<span class="bullet-point">• $1</span>');
    
    // Handle **bold** text (if any)
    formatted = formatted.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');
    
    // Handle code blocks (text within backticks)
    formatted = formatted.replace(/`([^`]+)`/g, '<code>$1</code>');
    
    // Handle multiple line breaks (convert double <br> to paragraph breaks)
    formatted = formatted.replace(/(<br>\s*){2,}/g, '</p><p class="bot">');
    
    // Wrap in paragraph if it doesn't already start with one
    if (!formatted.startsWith('<p')) {
        formatted = '<p class="bot">' + formatted + '</p>';
    } else if (!formatted.endsWith('</p>')) {
        formatted = formatted + '</p>';
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