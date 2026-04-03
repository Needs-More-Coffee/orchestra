# Orchestra
### Python Wrapper for the AI Council Deliberation System

---

## What This Is

Orchestra is the execution layer for the [AI Council](https://github.com/Needs-More-Coffee/ai_council) — a governed multi-agent deliberation system. It loads governance documents, manages session lifecycle, routes API calls to seven independent voice instances, and produces auditable session records.

The governing documents are the system. Orchestra runs them.

---

## How It Works

A deliberation session takes a single question as input and returns two outputs — a complete session record and a concept key derived from it.

At session open the wrapper generates a random seat order and pipes the question to The Steward, which declares which voices are most relevant and how many rounds the deliberation warrants. The wrapper reads these declarations and sets round one order.

Each round iterates through the active voice sequence. Every voice reads the full session record before producing output. Voices route attention to each other by name — the wrapper tallies flags received by each voice across the round and routes accordingly in the following round. A voice that receives no flags abstains entirely.

The session exits when The Steward declares SESSION: COMPLETE or the round ceiling is reached. At close The Scholar produces a concept key from the session record. Both documents are written to disk.

---

## Repository Structure

```
main.py                     — Entry point
core/
    provider.py             — Provider base class
    anthropic_provider.py   — Anthropic API implementation
    loader.py               — Loads governance documents from ai_council/
    paper.py                — Session record, append-only
    sessions.py             — Arbiter — session lifecycle and round execution
ai_council/                 — Governance documents (gitignored, clone separately)
sessions/                   — Session records output (gitignored)
reference/                  — Scholar-produced concept keys (gitignored)
```

---

## Setup

**Clone both repositories:**

```bash
git clone https://github.com/Needs-More-Coffee/orchestra
cd orchestra
git clone https://github.com/Needs-More-Coffee/ai_council
```

**Create and activate virtual environment:**

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -e .
```

**Add API key:**

Create a `.env` file in the orchestra root:

```
ANTHROPIC_API_KEY=your_key_here
```

**Run:**

```bash
python main.py
```

Enter a question at the prompt. Session record and concept key will be written to `sessions/` and `reference/` on completion.

---

## Output

Each session produces two files.

**sessions/session_[timestamp].md** — The complete Paper. Every voice entry, every system marker, every flag declaration, in the exact order it was written. The reasoning process that produced the output is permanently visible.

**reference/concept_key_[timestamp].md** — Scholar-produced derivation of the session. Named and numbered concepts, each anchored to a specific point in the transcript, with explicit reasoning for why each concept matters. Designed for injection into future sessions as compressed prior context.

---

## Current Status

| Component | Status |
|---|---|
| Document loader | Complete |
| Paper model | Complete |
| Provider abstraction | Complete — Anthropic implemented |
| Session runner | Operational |
| Flag-based routing | Operational |
| Steward early exit | Operational |
| Scholar concept key | Operational |
| Vio2 interrupt handling | TODO |
| Halt interrupt handling | TODO |
| Provider selection at runtime | Planned |
| Session config at prompt submission | Planned |

---

## What This Is Not

- A conversational assistant
- An autonomous decision-maker
- A consensus engine — unresolved conflict in the output is a feature, not a failure
- A finished product — the architecture is validated and running, not production-ready

---

## Related

- [ai_council](https://github.com/Needs-More-Coffee/ai_council) — Governance documents this wrapper executes
- [wrapper_test](https://github.com/Needs-More-Coffee/wrapper_test) — Earlier adversarial dialogue prototype that validated the stateless exchange pattern

---

*Architecture validated. Wrapper operational. Interrupt handling and provider selection are the open build items.*
