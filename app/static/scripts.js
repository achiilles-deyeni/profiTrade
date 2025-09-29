class ChatInterface {
  constructor() {
    this.messageInput = document.getElementById("messageInput");
    this.sendButton = document.getElementById("sendButton");
    this.chatMessages = document.getElementById("chatMessages");
    this.typingIndicator = document.getElementById("typingIndicator");

    this.init();
  }

  init() {
    // Event listeners
    this.sendButton.addEventListener("click", () => this.sendMessage());
    this.messageInput.addEventListener("keypress", (e) => {
      if (e.key === "Enter" && !e.shiftKey) {
        e.preventDefault();
        this.sendMessage();
      }
    });

    // Auto-resize textarea
    this.messageInput.addEventListener("input", () => this.autoResize());

    // Focus on input
    this.messageInput.focus();

    // Show welcome message
    this.showWelcomeMessage();
  }

  autoResize() {
    this.messageInput.style.height = "auto";
    this.messageInput.style.height =
      Math.min(this.messageInput.scrollHeight, 120) + "px";
  }

  showWelcomeMessage() {
    const welcomeDiv = document.createElement("div");
    welcomeDiv.className = "welcome-message";
    welcomeDiv.innerHTML = `
            <h3>👋 Welcome to ProfiTrade!</h3>
            <p>I'm your AI-powered financial sidekick. Ask me about:</p>
            <ul style="text-align: left; display: inline-block; margin-top: 1rem;">
                <li>📊 Market analysis and trends</li>
                <li>💰 Cryptocurrency insights</li>
                <li>📈 Trading strategies</li>
                <li>💡 Investment advice</li>
            </ul>
        `;
    this.chatMessages.appendChild(welcomeDiv);
  }

  async sendMessage() {
    const query = this.messageInput.value.trim();
    if (!query) return;

    // Disable input while processing
    this.setInputState(false);

    // Add user message
    this.addMessage(query, "user");

    // Clear input
    this.messageInput.value = "";
    this.autoResize();

    // Show typing indicator
    this.showTyping(true);

    try {
      // Send request to backend
      const response = await fetch("/chat/ask", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ query: query }),
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data = await response.json();

      // Simulate typing delay for better UX
      await this.delay(800 + Math.random() * 1000);

      // Hide typing and show response
      this.showTyping(false);
      this.addMessage(data.response, "bot");
    } catch (error) {
      console.error("Error:", error);
      this.showTyping(false);
      this.addMessage(
        "Sorry, I encountered an error. Please try again.",
        "bot",
        true
      );
    } finally {
      // Re-enable input
      this.setInputState(true);
      this.messageInput.focus();
    }
  }

  addMessage(content, type, isError = false) {
    const messageDiv = document.createElement("div");
    messageDiv.className = `message ${type}`;

    const avatar = document.createElement("div");
    avatar.className = "message-avatar";
    avatar.textContent = type === "user" ? "U" : "🤖";

    const messageContent = document.createElement("div");
    messageContent.className = "message-content";

    if (isError) {
      messageContent.style.background = "#dc3545";
      messageContent.style.color = "white";
    }

    // Handle line breaks and make links clickable
    const formattedContent = this.formatMessage(content);
    messageContent.innerHTML = formattedContent;

    if (type === "user") {
      messageDiv.appendChild(messageContent);
      messageDiv.appendChild(avatar);
    } else {
      messageDiv.appendChild(avatar);
      messageDiv.appendChild(messageContent);
    }

    this.chatMessages.appendChild(messageDiv);
    this.scrollToBottom();
  }

  formatMessage(content) {
    // Convert URLs to clickable links
    const urlRegex = /(https?:\/\/[^\s]+)/g;
    content = content.replace(urlRegex, '<a href="$1" target="_blank">$1</a>');

    // Convert line breaks
    content = content.replace(/\n/g, "<br>");

    return content;
  }

  showTyping(show) {
    if (show) {
      this.typingIndicator.style.display = "flex";
    } else {
      this.typingIndicator.style.display = "none";
    }
    this.scrollToBottom();
  }

  setInputState(enabled) {
    this.messageInput.disabled = !enabled;
    this.sendButton.disabled = !enabled;
  }

  scrollToBottom() {
    this.chatMessages.scrollTop = this.chatMessages.scrollHeight;
  }

  delay(ms) {
    return new Promise((resolve) => setTimeout(resolve, ms));
  }
}

// Initialize chat when DOM is loaded
document.addEventListener("DOMContentLoaded", () => {
  new ChatInterface();
});

// Add some utility functions
window.clearChat = function () {
  const chatMessages = document.getElementById("chatMessages");
  chatMessages.innerHTML = "";
  // Re-show welcome message
  const chat = new ChatInterface();
  chat.showWelcomeMessage();
};

// Add keyboard shortcuts
document.addEventListener("keydown", (e) => {
  // Ctrl/Cmd + K to clear chat
  if ((e.ctrlKey || e.metaKey) && e.key === "k") {
    e.preventDefault();
    clearChat();
  }
});
