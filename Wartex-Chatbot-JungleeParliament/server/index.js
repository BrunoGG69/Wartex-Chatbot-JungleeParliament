const express = require('express');
const path = require('path');
const dotenv = require('dotenv');
const ChatBot = require('./chatbot');

// Load environment variables
dotenv.config();

// Initialize Express app
const app = express();
const PORT = process.env.PORT || 5000;

// Middleware
app.use(express.json());
app.use(express.static(path.join(__dirname, '../client/dist')));

// Initialize ChatBot
const apiKey = process.env.GOOGLE_API_KEY;
const chatbot = new ChatBot(apiKey);

// In-memory chat history
const chatHistory = [];

// Helper function to get current time
const getTime = () => {
  const currentTime = new Date();
  const roundedTime = currentTime.getMilliseconds() >= 500
    ? new Date(currentTime.getTime() + 1000)
    : currentTime;
  roundedTime.setMilliseconds(0);
  return roundedTime.toISOString();
};

// API endpoint to handle chat messages
app.post('/api/send_message', async (req, res) => {
  const { message } = req.body;

  if (!message) {
    return res.status(400).json({ error: 'Message is required.' });
  }

  if (message.toLowerCase() === 'exit') {
    return res.json({ response: 'Goodbye!' });
  } else if (message.toLowerCase() === 'history') {
    return res.json({ response: chatHistory });
  }

  try {
    const response = await chatbot.sendPrompt(message);
    const time = getTime();
    const chatEntry = { time, prompt: message, response };
    chatHistory.push(chatEntry);
    res.json({ response });
  } catch (error) {
    console.error('Error:', error.message);
    res.status(500).json({ error: error.message });
  }
});

// API endpoint to get chat history
app.get('/api/chat_history', (req, res) => {
  res.json(chatHistory);
});

// Serve React app
app.get('*', (req, res) => {
  res.sendFile(path.resolve(__dirname, '../client/dist/index.html'));
});

// Start the server
app.listen(PORT, () => {
  console.log(`Server running on port ${PORT}`);
});
