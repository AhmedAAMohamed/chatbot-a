// DOM Elements
const chatLog = document.getElementById('chatLog');
const chatInput = document.getElementById('chatInput');
const sendBtn = document.getElementById('sendBtn');

// API Configuration - use relative URL for deployment
const API_URL = '';  // Changed from '/api' to empty string

// Track conversation history
let messageHistory = [];

// Function to call the backend API
async function callChatAPI(userMessage) {
  try {
    // Add user message to history
    messageHistory.push({
      role: "user",
      content: userMessage
    });
    
    console.log("Sending request to API:", messageHistory);
    
    const response = await fetch(`${API_URL}/api/chat`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        messages: messageHistory,
        temperature: 0.7
      })
    });
    
    const data = await response.json();
    
    if (!response.ok) {
      console.error("API Error Response:", data);
      throw new Error(`API error: ${data.detail || response.status}`);
    }
    
    console.log("API Response:", data);
    
    // Add assistant response to history
    messageHistory.push({
      role: "assistant",
      content: data.message
    });
    
    return data.message;
  } catch (error) {
    console.error('Error calling chat API:', error);
    return `Sorry, I encountered an error: ${error.message}. Please try again.`;
  }
}

// Function to add a message to the chat log
function appendMessage(message, sender) {
  const msgDiv = document.createElement('div');
  msgDiv.classList.add('chat-message', sender === 'user' ? 'user-message' : 'bot-message');
  msgDiv.textContent = message;
  chatLog.appendChild(msgDiv);
  chatLog.scrollTop = chatLog.scrollHeight; // Auto-scroll to latest message
}

// Function to add a loading indicator
function showLoadingIndicator() {
  const loadingDiv = document.createElement('div');
  loadingDiv.classList.add('chat-message', 'bot-message', 'loading-message');
  
  const loadingIndicator = document.createElement('div');
  loadingIndicator.classList.add('loading');
  loadingIndicator.innerHTML = '<span></span><span></span><span></span>';
  
  loadingDiv.appendChild(loadingIndicator);
  chatLog.appendChild(loadingDiv);
  chatLog.scrollTop = chatLog.scrollHeight;
  
  return loadingDiv;
}

// Function to send a message
async function sendMessage() {
  const userMessage = chatInput.value.trim();
  if (!userMessage) return; // Do not send empty messages

  // Display user message
  appendMessage(userMessage, 'user');

  // Clear input
  chatInput.value = '';

  // Show loading indicator
  const loadingDiv = showLoadingIndicator();

  // Call the API
  const botResponse = await callChatAPI(userMessage);
  
  // Remove loading indicator and show response
  chatLog.removeChild(loadingDiv);
  appendMessage(botResponse, 'bot');
}

// Event Listeners
sendBtn.addEventListener('click', sendMessage);

chatInput.addEventListener('keyup', (event) => {
  if (event.key === 'Enter') {
    sendMessage();
  }
});

// Initialize chat interface
function initChat() {
  chatInput.focus();
}

// Start the app
initChat(); 