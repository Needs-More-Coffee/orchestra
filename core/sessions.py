from core.loader import Loader
from core.anthropic_provider import AnthropicProvider
from core.paper import Paper
import random
import datetime
import re
import os

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
        pattern = r'\*\*Flag:\*\*\s*([^\n]+)'
        match = re.search(pattern, voice_output)
        if match:
            flag_line = match.group(1).strip()
            if flag_line:
                names = [n.strip() for n in flag_line.split(',')]
                for name in names:
                    if name in self.seat_order:
                        flag_tallies[name] = flag_tallies.get(name, 0) + 1
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
        seat_order_map = "\n".join([
            f"Position {i+1}: {voice}"
            for i, voice in enumerate(self.seat_order)
        ])

        self.paper.write_system(
            f"Session initialized.\n\n"
            f"SEAT ORDER:\n{seat_order_map}"
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
        if initial_flags:
            round_order = self.calculate_round_order(initial_flags)
        else:
            round_order = self.seat_order.copy()
        self.paper.write_system(f"Round 1 order: {round_order}")
    
        print("Pre-deliberation complete.")
        print(f"Round limit: {self.round_limit}")
        print(f"Round 1 order: {round_order}")
        print(self.paper.as_string())

        for round_num in range(self.round_limit):
            self.paper.write_system(f"Round {round_num + 1} open")
            flag_tallies = {}
            early_exit = False
    
            for voice in round_order:
        
                voice_prompt = self.loader.load_voice(voice)
                response = self.provider.send(
                    voice_prompt,
                    self.paper.as_string()
                )
                self.paper.write_voice(voice, response)
        
                flags = self.parse_flags(response)
                for v, count in flags.items():
                    flag_tallies[v] = flag_tallies.get(v, 0) + count
        
                if voice == "THE_STEWARD":
                    if "COMPLETE" in response.upper():
                        early_exit = True
                        break
    
            if early_exit:
                break
    
            round_order = self.calculate_round_order(flag_tallies)
            self.paper.write_system(
                f"Round {round_num + 2} order: {round_order}"
            )

        self.paper.write_system("Session end")

        scholar_prompt = self.loader.load_voice("THE_SCHOLAR")
        concept_key_instruction = """
        Produce the concept key now.
        Follow TEMPLATE_CONCEPT_KEY exactly.
        Derive from the session record only.
        Every concept must have a transcript anchor.
        Nothing else.
        """

        concept_key = self.provider.send(
            scholar_prompt + concept_key_instruction,
            self.paper.as_string()
        )

        session_id = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        self.paper.save(f"sessions/session_{session_id}.md")

        os.makedirs("reference", exist_ok=True)
        with open(f"reference/concept_key_{session_id}.md", 'w') as f:
            f.write(concept_key)

        print(f"Session complete.")
        print(f"Paper: sessions/session_{session_id}.md")
        print(f"Concept Key: reference/concept_key_{session_id}.md")