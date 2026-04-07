import os

CORE_DOCS = [
    "KERNEL.md",
    "EXCHANGE.md",
    "Voices/VOICE_CORE.md",
    "VOICE_MANIFEST.md"
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
    
    def load_violations(self, voice_name):
        violations_path = os.path.join(self.base_path, "..", "violations")
        if not os.path.exists(violations_path):
            return ""
        result = ""
        prefix = f"violation_{voice_name}_"
        for filename in sorted(os.listdir(violations_path)):
            if filename.startswith(prefix) and filename.endswith(".md"):
                filepath = os.path.join(violations_path, filename)
                with open(filepath, 'r') as f:
                    result += f.read()
        return result

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
        violations = self.load_violations(voice_name)
        if violations:
            prompt += violations
        return prompt