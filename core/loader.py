import os

CORE_DOCS = [
    "KERNEL.md",
    "EXCHANGE.md",
    "Voices/VOICE_CORE.md"
]

PERSONALITY_DELTAS = [
    "Personality/ANALYST.md",
    "Personality/CONSULTANT.md",
    "Personality/DESIGNER.md",
    "Personality/OPERATOR.md"
]

VOICE_TEMPLATES = {
    "THE_JUDGE": ["Templates/TEMPLATE_VIOLATION_DOCUMENT.md"],
    "THE_SCHOLAR": ["Templates/TEMPLATE_CONCEPT_KEY.md"]
}

class Loader:
    def __init__(self, base_path):
        self.base_path = base_path
    
    def load_file(self, relative_path):
        full_path = os.path.join(self.base_path, relative_path)
        with open(full_path, 'r') as f:
            return f.read()
    
    def load_voice(self, voice_name):
        prompt = ""
        for doc in CORE_DOCS:
            prompt += self.load_file(doc)
        prompt += self.load_file(f"Voices/{voice_name}.md")
        prompt += self.load_file("Personality/PERSONALITY_CORE.md")
        for delta in PERSONALITY_DELTAS:
            prompt += self.load_file(delta)
        if voice_name in VOICE_TEMPLATES:
            for template in VOICE_TEMPLATES[voice_name]:
                prompt += self.load_file(template)
        return prompt