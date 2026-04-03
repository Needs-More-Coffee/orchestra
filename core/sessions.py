from core.loader import Loader
from core.anthropic_provider import AnthropicProvider
from core.paper import Paper
import random
import datetime
import re

VOICES = [
    "THE_STEWARD",
    "THE_SCHOLAR",
    "THE_BUILDER",
    "THE_JUDGE",
    "THE_PROTECTOR",
    "THE_TRADER",
    "THE_VISIONARY"
]

class Session:
    def __init__(self):
        self.paper = Paper()
        self.provider = AnthropicProvider()
        self.loader = Loader("ai_council")
        self.seat_order = []
        self.round_limit = 1
    
    def generate_seat_order(self):
        self.seat_order = VOICES.copy()
        random.shuffle(self.seat_order)
        return self.seat_order
    
    def parse_flags(self, voice_output):
        flag_tallies = {}
        pattern = r'\(([X_]{7})\)'
        matches = re.findall(pattern, voice_output)
    
        for match in matches:
            for position, char in enumerate(match):
                if char == 'X':
                    voice = self.seat_order[position]
                    flag_tallies[voice] = flag_tallies.get(voice, 0) + 1
    
        return flag_tallies
    
    def parse_round_limit(self, steward_output):
        pattern = r'ROUNDS:\s*(\d+)'
        match = re.search(pattern, steward_output)
        if match:
            return int(match.group(1))
        return self.round_limit
    
    def calculate_round_order(self, flag_tallies):
        order = []

        flagged = sorted(
            flag_tallies.keys(),
            key=lambda v: (-flag_tallies[v], self.seat_order.index(v))
        )
    
        if "THE_STEWARD" not in flagged:
            flagged.append("THE_STEWARD")
    
        return flagged
    
    def run(self, question):
        self.generate_seat_order()
        self.paper.write_system(
            f"Session initialized. Seat order: {self.seat_order}"
        )

        self.paper.write_system(f"USER: {question}")

        steward_prompt = self.loader.load_voice("THE_STEWARD")
        steward_response = self.provider.send(
            steward_prompt,
            self.paper.as_string()
        )
        self.paper.write_voice("THE_STEWARD", steward_response)

        self.round_limit = self.parse_round_limit(steward_response)
        initial_flags = self.parse_flags(steward_response)
        round_order = self.calculate_round_order(initial_flags)
        self.paper.write_system(f"Round 1 order: {round_order}")
    
        print("Pre-deliberation complete.")
        print(f"Round limit: {self.round_limit}")
        print(f"Round 1 order: {round_order}")
        print(self.paper.as_string())