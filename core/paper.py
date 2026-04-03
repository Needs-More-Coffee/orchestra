import os

class Paper:
    def __init__(self):
        self.entries = []
    
    def write_system(self, content):
        self.entries.append({
            "source": "{SYSTEM}",
            "content": content
        })
    
    def write_voice(self, voice_name, content):
        self.entries.append({
            "source": voice_name,
            "content": content
        })
    
    def as_string(self):
        result = ""
        for entry in self.entries:
            result += f"-{entry['source']}-\n"
            result += f"{entry['content']}\n"
            result += "---\n"
        return result
    
    def save(self, filepath):
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        with open(filepath, 'w') as f:
            f.write(self.as_string())