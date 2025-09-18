async function sendQuery() {
    const input = document.getElementById("userInput").value;
    const chatLog = document.getElementById("chatLog");

    if (!input.trim()) return;

    // Add user message
    chatLog.innerHTML += `<p class="user">&gt; ${input}</p>`;
    document.getElementById("userInput").value = "";
    chatLog.innerHTML += `<p class="bot">Bot is typing...</p>`;
    chatLog.scrollTop = chatLog.scrollHeight;

    try {
        const res = await fetch("http://127.0.0.1:8000/ask", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ message: input })
        });
        const data = await res.json();

        // Remove typing message and show response
        chatLog.lastChild.remove();
        chatLog.innerHTML += `<p class="bot">${data.response}</p>`;
        chatLog.scrollTop = chatLog.scrollHeight;

    } catch (err) {
        chatLog.lastChild.remove();
        chatLog.innerHTML += `<p class="bot">Error connecting to server.</p>`;
    }
}
