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
        self.session_id = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")

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

    def parse_entry(self, voice_output):
        flag = ""
        content = voice_output
        compliance = ""

        compliance_match = re.search(r'\*\*Compliance:\*\*\s*([^\n*]+)', voice_output)
        if compliance_match:
            compliance = compliance_match.group(1).strip()

        flag_match = re.search(r'\*\*Flag:\*\*\s*([^*\n]*)', voice_output)
        if flag_match:
            flag = flag_match.group(1).strip()

        content_match = re.search(r'\*\*Content:\*\*\s*([\s\S]*?)(?=---|\Z)', voice_output)
        if content_match:
            content = content_match.group(1).strip()

        return flag, content, compliance

    def parse_tags(self, voice_name, voice_output):
        # Only parse TAG directives that appear before **Source:** in the output
        pre_entry = voice_output.split("**Source:**")[0]
        pattern = r'TAG:\s*(THE_\w+)\s*\|\s*(\{[^}]+\})\s*-\s*(.+)'
        matches = re.findall(pattern, pre_entry)
        return [(target, voice_name, tag, reason.strip()) for target, tag, reason in matches]

    def parse_round_limit(self, steward_output):
        pattern = r'ROUNDS:\s*(\d+)'
        match = re.search(pattern, steward_output)
        if match:
            return int(match.group(1))
        return self.round_limit

    def calculate_round_order(self, flag_tallies):
        flagged = sorted(
            flag_tallies.keys(),
            key=lambda v: (-flag_tallies[v], self.seat_order.index(v))
        )
        if "THE_STEWARD" not in flagged:
            flagged.append("THE_STEWARD")
        return flagged

    def handle_vio2(self, offending_source):
        print(f"[INTERRUPT] {{Vio2}} detected on {offending_source} — routing to Judge")
        judge_prompt = self.loader.load_voice("THE_JUDGE")
        response, stop_reason = self.provider.send(judge_prompt, self.paper.as_string())
        if stop_reason == "max_tokens":
            self.paper.write_system(f"Judge response truncated — {{Vio2}} evaluation incomplete, deliberation continues")
            return

        # Parse verdict
        verdict_pattern = r'VERDICT:\s*(THE_\w+)\s*\|\s*\{Vio2\}\s*->\s*(\{[^}]+\}|None)'
        verdict_match = re.search(verdict_pattern, response)

        if verdict_match:
            target = verdict_match.group(1)
            new_tag = verdict_match.group(2)

            if new_tag == "None":
                self.paper.replace_tag(target, "{Vio2}", None)
                print(f"[JUDGE] {target} — {{Vio2}} removed")
            else:
                if new_tag == "{Vio2}":
                    # Confirmed — write violation document
                    parts = response.split("---VIOLATION---")
                    if len(parts) > 1:
                        violation_content = parts[1].strip()
                        self.paper.save_violation(target, violation_content, self.session_id)
                        print(f"[JUDGE] {target} — {{Vio2}} confirmed, violation document saved")
                else:
                    # Downgraded
                    self.paper.replace_tag(target, "{Vio2}", new_tag)
                    print(f"[JUDGE] {target} — {{Vio2}} downgraded to {new_tag}")
        else:
            print(f"[JUDGE] No parseable verdict found — {{Vio2}} left unmodified")

    def handle_halt(self, offending_source):
        print(f"[INTERRUPT] {{Halt}} detected on {offending_source} — routing to Protector")
        protector_prompt = self.loader.load_voice("THE_PROTECTOR")
        response, stop_reason = self.provider.send(protector_prompt, self.paper.as_string())
        if stop_reason == "max_tokens":
            self.paper.write_system(f"Protector response truncated — {{Halt}} evaluation incomplete, treating as unresolved")
            return

        resolved_pattern = r'RESOLVED:\s*(THE_\w+)'
        resolved_match = re.search(resolved_pattern, response)

        if resolved_match:
            target = resolved_match.group(1)
            self.paper.resolve_halt(target)
            print(f"[PROTECTOR] {target} — {{Halt}} resolved, deliberation continues")
        else:
            # Halt Event — save and exit
            print(f"[PROTECTOR] Halt Event confirmed — saving Paper and exiting session")
            self.paper.save(f"sessions/session_{self.session_id}.md")
            exit(0)

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

        # pre-deliberation
        steward_prompt = self.loader.load_voice("THE_STEWARD")
        steward_response, stop_reason = self.provider.send(
            steward_prompt,
            self.paper.as_string()
        )
        if stop_reason == "max_tokens":
            self.paper.write_system("Steward opening entry truncated — session cannot initialize correctly")
            return
        flag, content, compliance = self.parse_entry(steward_response)
        self.paper.write_voice("THE_STEWARD", content, flag, compliance)
        self.round_limit = self.parse_round_limit(steward_response)
        initial_flags = self.parse_flags(steward_response)
        if initial_flags:
            round_order = self.calculate_round_order(initial_flags)
        else:
            round_order = self.seat_order.copy()
        self.paper.write_system(f"Round 1 order: {round_order}")

        # round execution
        current_round = 0

        while current_round < self.round_limit:
            self.paper.write_system(f"Round {current_round + 1} open")
            flag_tallies = {}
            early_exit = False

            for voice in round_order:
                voice_prompt = self.loader.load_voice(voice)
                response, stop_reason = self.provider.send(
                    voice_prompt,
                    self.paper.as_string()
                )

                if stop_reason == "max_tokens":
                    self.paper.write_system(f"{voice} entry truncated — entry discarded, voice skipped this round")
                    continue

                tags = self.parse_tags(voice, response)
                for target, tagger, tag, reason in tags:
                    self.paper.classify(target, tagger, tag, reason)

                flag, content, compliance = self.parse_entry(response)
                self.paper.write_voice(voice, content, flag, compliance)

                flags = self.parse_flags(response)
                for v, count in flags.items():
                    flag_tallies[v] = flag_tallies.get(v, 0) + count

                # Interrupt checks
                halt_source = self.paper.has_unreviewed_halt()
                if halt_source:
                    self.handle_halt(halt_source)
                    if not self.paper.has_unreviewed_halt():
                        pass  # resolved, continue round

                vio2_source = self.paper.has_unreviewed_vio2()
                if vio2_source:
                    self.handle_vio2(vio2_source)

                if voice == "THE_STEWARD":
                    if "SESSION: COMPLETE" in response:
                        early_exit = True
                        break

            if early_exit:
                break

            current_round += 1

            if current_round < self.round_limit:
                round_order = self.calculate_round_order(flag_tallies)
                self.paper.write_system(
                    f"Round {current_round + 1} order: {round_order}"
                )

        # session close
        self.paper.write_system("Session end")

        scholar_prompt = self.loader.load_voice("THE_SCHOLAR")
        concept_key_instruction = """
        Produce the concept key now.
        Follow TEMPLATE_CONCEPT_KEY exactly.
        Derive from the session record only.
        Every concept must have a transcript anchor.
        Nothing else.
        """
        concept_key, _ = self.provider.send(
            scholar_prompt + concept_key_instruction,
            self.paper.as_string()
        )

        self.paper.save(f"sessions/session_{self.session_id}.md")

        os.makedirs("reference", exist_ok=True)
        with open(f"reference/concept_key_{self.session_id}.md", 'w') as f:
            f.write(concept_key)

        print(f"Session complete.")
        print(f"Paper: sessions/session_{self.session_id}.md")
        print(f"Concept Key: reference/concept_key_{self.session_id}.md")
