import google.generativeai as genai

class GeniAIExeption(Exception):
    """Base class for exceptions in this module."""

class ChatBot:
    CHATBOT_NAME = "Chatbot 69"
    
    def __init__(self, api_key):
        self.genai = genai
        self.genai.configure(api_key=api_key)
        self.model = self.genai.GenerativeModel(model_name="tunedModels/jungleeparliament-8blqszw8n5vh")
        self.conversation = None
        self._conversation_history = []
        
        self.preload_conversation()
        self.start_conversation()  # Automatically start a conversation

        
    def send_prompt(self, prompt, temperature = 1):
        if temperature < 0.1 or temperature > 1:
            raise GeniAIExeption("Temperature must be greater than 0.1")
        if not prompt:
            raise GeniAIExeption("Prompt cannot be empty")
        try :
            response = self.conversation.send_message(
                content = prompt, 
                generation_config = self._generate_config(temperature),
            )
            # response.resolve()
            return f'{response.text}\n'
        except Exception as e:
            raise GeniAIExeption(str(e))
        
    @property
    def history(self):
        conversation_history = [
            {'role': message.role, 'text' : message.parts[0].text} for message in self.conversation.history
        ]
        return  conversation_history
        
        
    def clear_conversation(self):    
        self.conversation = self.model.start_chat(history = [])
        
    def start_conversation(self):
        self.conversation = self.model.start_chat(history=self._conversation_history)
    
    def _generate_config(self, temperature):
        return genai.types.GenerationConfig(
            temperature=temperature,
        )
        
    def _construct_message(self, text, role = 'user'):
        return {
            'role': role,
            'parts': [text]
        }
    
    def preload_conversation(self, conversation_history = None):
        if isinstance(conversation_history, list):
            self._conversation_history = conversation_history
        else:
            self._conversation_history = [
                self._construct_message("This is a jungle, in which there is the Junglee Parliament. The members of the parliament are represented by different animals, for example lion as prime minister, an elephant as president, an Owl as vice president, etc. They are here to solve the problems regarding the jungle just like the members of the Indian Parliament discuss and solve the problems together."),
            ]

