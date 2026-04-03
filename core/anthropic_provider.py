from anthropic import Anthropic
from core.provider import Provider
from dotenv import load_dotenv

load_dotenv()

class AnthropicProvider(Provider):
    def __init__(self):
        self.client = Anthropic()
    
    def send(self, system_prompt, user_message):
        response = self.client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=4096,
            system=system_prompt,
            messages=[
                {"role": "user", "content": user_message}
            ]
        )
        return response.content[0].text