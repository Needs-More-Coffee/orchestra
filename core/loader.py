import os

class Loader:
    def __init__(self, base_path):
        self.base_path = base_path
    
    def load_file(self, relative_path):
        full_path = os.path.join(self.base_path, relative_path)
        with open(full_path, 'r') as f:
            return f.read()
    
    def load_voice(self, voice_name):
        pass

if __name__ == "__main__":
    loader = Loader("ai_council")
    print(loader.load_file("KERNEL.md"))