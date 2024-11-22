const { GenerativeAI } = require('gemini-api'); // Hypothetical library (replace with actual)

class ChatBot {
  constructor(apiKey) {
    if (!apiKey) {
      throw new Error('API key is required.');
    }

    this.genAI = new GenerativeAI({ apiKey });
    this.model = this.genAI.createModel('tunedModels/jungleeparliament-diaqdo66oviu');
    this.conversation = null;
    this.conversationHistory = [];
    this.preloadConversation();
    this.startConversation();
  }

  preloadConversation() {
    this.conversationHistory = [
      {
        role: 'system',
        parts: [
          "This is a jungle, in which there is the Junglee Parliament. The members of the parliament are represented by different animals..."
        ],
      },
    ];
  }

  startConversation() {
    this.conversation = this.model.startChat({
      history: this.conversationHistory,
    });
  }

  async sendPrompt(prompt, temperature = 1) {
    if (!prompt) throw new Error('Prompt cannot be empty.');
    if (temperature < 0.1 || temperature > 1) throw new Error('Temperature must be between 0.1 and 1.');

    try {
      const response = await this.conversation.sendMessage(prompt, {
        temperature,
      });
      return response.text;
    } catch (error) {
      throw new Error(error.message);
    }
  }

  clearConversation() {
    this.conversation = this.model.startChat({ history: [] });
  }
}

module.exports = ChatBot;
