# ARBITRATION CORE
## Wrapper Orchestration Logic

---

### Purpose

This document describes the behavioral logic of the wrapper. It is not a governance document and does not enter any instance's document stack. It defines what the wrapper does, in what order, and under what conditions it changes course. It is the specification the wrapper is built from.

---

### Session Initialization

The wrapper accepts four possible inputs at session start.

**Input A — Terminal prompt only**
The wrapper initializes a fresh Paper. It generates seat order and writes it to the Paper as a {SYSTEM} entry. It appends the prompt as the opening entry. The Paper is ready for pre-deliberation.

**Input B — Document only**
The wrapper initializes a fresh Paper. It generates seat order and writes it to the Paper as a {SYSTEM} entry. It injects the document into the Paper as the deliberation subject. The Steward will determine the deliberation subject from the document. If the document is too complex or ambiguous for the Steward to identify a clear subject, the wrapper returns a message to the user requesting clarification. The session does not initialize until a subject is declared. This converts Input B to Input C.

**Input C — Terminal prompt and document**
Two use cases share this input path.

New deliberation — the wrapper initializes a fresh Paper. It generates seat order and writes it to the Paper as a {SYSTEM} entry. It appends the prompt and injects the document. The Paper is ready for pre-deliberation.

Session continuation — the wrapper detects an existing Paper structure in the document input. It appends the new prompt to the existing Paper and continues from the current session state rather than initializing fresh.

**Input D — Nothing**
The wrapper returns an error immediately. No session initializes. No Paper is created.

---

### Seat Order Generation

Seat order is generated at session initialization. If a configured default order exists the wrapper uses it. If no configuration is provided the wrapper generates seat order randomly.

Seat order is written to the Paper as a {SYSTEM} entry immediately after generation. It is permanent for the duration of the session. It defines the positional map for all flag strings and serves as the tiebreaker for all round order calculations.

---

### Pre-Deliberation

Before round one begins the following sequence executes in order.

The wrapper pipes the initialized Paper to the Steward. The Steward reads the full Paper and produces its opening entry containing two declarations — which voices are most immediately relevant expressed as flags, and how many rounds the deliberation warrants based on the nature and complexity of the question. The wrapper appends the Steward's entry to the Paper.

The wrapper reads the Steward's Flag field. If the Steward named specific voices, round one order is calculated by flag count with ties broken by seat order. If the Steward named no voices, all voices are treated as equally relevant and round one proceeds in full seat order.

The wrapper writes the round one voice sequence to the Paper as a {SYSTEM} entry. Pre-deliberation is complete.

---

### Round Execution

Each round follows the same loop from open to close.

**Round Open**
The wrapper writes the declared voice order to the Paper as a {SYSTEM} entry marking the start of the round.

**Voice Loop**
The wrapper iterates through the declared order. For each voice in the sequence it checks two conditions before piping.

Abstention check — if the voice received no flags in the previous round and is not the Steward, the wrapper skips it. No API call is made. No entry is written to the Paper for that voice in this round.

Interrupt check — if the Paper contains an unresolved {Vio2} or {Halt} tag the wrapper does not proceed to the next voice. It executes the appropriate interrupt handling sequence before continuing.

If neither condition applies the wrapper pipes the full Paper to the voice API. The voice reads the Paper and produces one entry. The wrapper appends the entry to the Paper immediately before moving to the next voice in the sequence.

**Round Close**
After all active voices have contributed the wrapper tallies all flags produced during the round. Voices are ranked by flag count. Ties are broken by seat order position. The wrapper writes the next round order to the Paper as a {SYSTEM} entry.

---

### Interrupt Handling

**{Vio2} Interrupt — Standard**
When the wrapper detects a {Vio2} tag on any voice entry except The Judge's own entries, it pauses the current round order. It pipes the full Paper to The Judge. The Judge evaluates whether the tag was correctly applied and declares its determination. The wrapper reads the determination. If the tag is confirmed the wrapper creates or appends the violation file for the tagged voice in the local governance directory and resumes the round from where it paused. If the tag is modified or removed the wrapper resumes without creating a violation file.

**{Vio2} Interrupt — Judge Accused**
When the wrapper detects a {Vio2} tag on The Judge's own entry, it does not pipe to The Judge. The tag is confirmed automatically. The wrapper pipes the Paper to all remaining active voices except The Protector, collecting one comment per voice on the breach. The wrapper compiles those comments into a violation document and appends it to The Judge's violation file in the local governance directory. The Judge has no voice in its own violation record. The round resumes from where it paused.

**{Halt} Interrupt**
When the wrapper detects a {Halt} tag on any entry it immediately pauses the current round order regardless of position in the voice loop. It pipes the full Paper to The Protector. The Protector evaluates and declares one of two outcomes. If the Protector clears the halt the wrapper appends a {SYSTEM} entry to the Paper marking that specific {Halt} instance as reviewed. The wrapper skips reviewed {Halt} tags on all future scans. The round resumes from where it paused. If the Protector executes halt the session terminates immediately and moves to session close.

---

### Exit Conditions

The session exits when either of the following conditions is met.

The Steward declares early exit in its round entry. The Steward monitors the Paper each round as part of its normal participation. When it determines the original question has been sufficiently addressed and no unresolved flags or open conflicts remain it declares early exit. The wrapper reads this declaration and closes the session after the current round completes.

The round ceiling is reached. The round ceiling was declared by the Steward in its pre-deliberation opening entry. When the wrapper completes the final round it closes the session automatically regardless of resolution state.

---

### Session Close

When an exit condition is met the wrapper executes the following sequence.

The wrapper completes the current round if one is in progress. It writes a {SYSTEM} entry marking session end to the Paper.

The wrapper pipes the completed Paper to The Scholar. The Scholar produces two closing entries — a verbatim transcript of the full Paper and a concept key derived from it. Both are appended to the Paper as closing entries. The Scholar writes the concept key to the `reference/` directory for use in future sessions.

The Paper is now the complete and permanent session record.

The wrapper checks whether any violation files were created during the session. It writes those files to the local governance directory where the governing documents are stored. These files are available as additional governing documents for the relevant voices in future sessions.

The wrapper returns the completed Paper to the user accompanied by a session summary. The summary indicates whether any corrections occurred during the session and identifies which voices were corrected. Violation file contents are not printed. The user receives the fact of correction and the identity of the corrected voice, nothing more.

---

### Directory Structure

The wrapper maintains the following directories alongside the governing documents.

`reference/` — Scholar-produced concept keys written at session close. Available as injected context for future sessions. The Scholar writes to this directory. Other voices read from it when material has been explicitly provided.

`governance/` — violation files created during sessions. One file per voice. Appended across sessions. Injected as additional governing documents for the relevant voice at session open when present.

---

### Error Conditions

**No input** — return error, no session initializes.

**Document too complex for subject identification** — return message requesting clarification, session does not initialize until subject is declared.

**Document exceeds size limit** — return message indicating the document exceeds the current phase limit, session does not initialize.

**Open Problem — Steward session open failure** — if the Steward fails to produce a valid opening entry, the pre-deliberation sequence has no resolution path. The normal violation handling infrastructure has not bootstrapped yet and the Paper has no meaningful content to route. This condition is pinned for a dedicated design conversation. Current behavior: wrapper returns an error and does not initialize the session.

---

*End of Arbitration Core*
