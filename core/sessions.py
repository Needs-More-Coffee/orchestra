from core.loader import Loader
from core.anthropic_provider import AnthropicProvider
from core.paper import Paper
import random
import datetime

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
        pass
    
    def parse_flags(self, voice_output):
        pass
    
    def parse_round_limit(self, steward_output):
        pass
    
    def calculate_round_order(self, flag_tallies):
        pass
    
    def run(self, question):
        pass