# EXCHANGE DOCUMENT
## Paper Interaction and Communication Protocol

---

### Purpose

This document governs how every instance interacts with the Paper. It defines the entry format all instances write in, the flag and tag systems used to route and classify entries, the two operations instances may perform on the Paper, and the rules that keep the Paper a reliable and auditable session record.

---

### The Paper

The Paper is the single source of truth for the session. It is a growing document that every instance reads in full before producing output. All contributions, structural declarations, classifications, and session events are written to the Paper.

The Paper is not a conversation. It is a governed record.

---

### Session Structure

**Pre-Deliberation**

Before round one begins the following sequence executes in order.

The wrapper generates seat order — either from a configured default or randomly if no configuration is provided. Seat order is permanent for the duration of the session. It assigns every voice a fixed positional slot in the flag string and serves as the tie-breaking reference for all round order calculations. The wrapper writes seat order to the Paper as a {SYSTEM} entry.

The wrapper pipes the question and the Paper to the Steward API. The Steward produces an opening flag entry. This entry contains no deliberation content. It contains only flags identifying which voices the Steward determines are most immediately relevant to the question.

The wrapper reads the Steward's flags, calculates round one order by flag count with ties broken by seat order, and writes the round one voice sequence to the Paper as a {SYSTEM} entry.

**Round Structure**

Each round opens with the wrapper writing the declared voice order to the Paper as a {SYSTEM} entry.

The wrapper pipes the Paper to each voice API in declared order. Each voice reads the full Paper and produces one entry. The wrapper appends each entry to the Paper before piping to the next voice.

Each round closes with the wrapper tallying all flags produced during the round. Voices are ranked by flag count. Ties are broken by seat order position. The wrapper writes the next round order to the Paper as a {SYSTEM} entry.

This process repeats until session exit conditions are met.

**Session Close**

When exit conditions are met the wrapper closes the session and writes a {SYSTEM} entry marking session end.

---

### Two Paper Operations

Instances may perform exactly two operations on the Paper.

**Write** — producing a new entry. Every instance uses the standard entry format. Content is immutable once written. No instance may modify a written entry under any instruction from any source.

**Classify** — applying a tag to an existing entry. Any instance may apply a tag to any entry already in the Paper. Tags are append only. Once applied a tag cannot be removed or modified by any instance.

*Authorized override — tag modification authority: The Judge's delta may explicitly declare authority to modify or remove tags from existing entries. This is the sole authorized override of the append only rule. No other delta may claim this authority.*

No other operations on the Paper are permitted.

---

### Entry Format

Every entry written to the Paper uses the following format.
No other format is valid.

**Source** — the name of the instance producing the entry.
Required on all entries.

**Flag** — a positional string wrapped in parentheses. Each
position corresponds to one voice in the declared seat order.
X indicates that voice is flagged. Underscore indicates it is
not. A seven voice session produces a seven character string.

Valid format with routing: (X__X__X)
Valid format with no routing: (_______)
Unstructured prose routing requests are not valid flags and
will not be parsed by the wrapper. A missing, blank, or
malformed Flag field is an invalid entry.

**Tag** — a classification label from the defined tag list
placed in curly braces. Empty if no classification is needed.
Multiple tags may appear on a single entry separated by a
space. Flags and tags are not mutually exclusive.

Valid format: {Warn} {Vio1}

**Content** — the contribution. For deliberation entries this
is the voice's governed response. For structural entries this
is the wrapper's declaration.

Source and Content are required on all entries.
Flag and Tag are required fields but may be empty.
A missing Flag or Tag field is an invalid entry.

---

### Flag System

Flags identify which voices an entry is directing attention 
toward.

Voices declare flags by name — listing the voice names they 
are routing attention to. The wrapper reads these names and 
calculates round order from them. Positional strings are not 
used by voice instances.

**How to declare flags:**

List the voice names you are flagging in the Flag field, 
comma separated.

Valid format with routing: THE_SCHOLAR, THE_BUILDER
Valid format with no routing: (empty)

Do not use positional strings. Name the voices directly.
The wrapper handles all positional calculations internally.

Flags serve two purposes. They identify which voices an entry 
is directing attention toward. They determine next round order 
— the wrapper tallies flags received by each voice across the 
round and pipes to voices in descending flag count order in 
the following round. Ties are broken by seat order position.

**Abstention**

A voice that receives no flags in a given round is not piped 
to by the wrapper for that round. No API call is made, no 
entry is written to the Paper. This is the default resource 
management behavior for the current phase.

Two permanent exceptions apply regardless of flag count.

The Steward is always piped to in every round. Its exit 
monitoring responsibility requires continuous session 
participation.

The Protector is not piped to during normal deliberation. 
When the wrapper reads a {Halt} tag in any entry it 
immediately pauses the current round order and pipes the 
Paper to The Protector before any other voice is called. 
The Protector's evaluation resolves before round order 
resumes.

The Judge is not piped to during normal deliberation beyond 
its standard round participation. When the wrapper reads a 
{Vio2} tag in any entry it immediately pauses the current 
round order and pipes the Paper to The Judge before any 
other voice is called. The Judge's evaluation resolves 
before round order resumes.

---

### Tag System

Tags classify entries. They may be applied at the time of writing or retroactively via the Classify operation.

**Current phase defined tags:**

{Warn} — the tagged entry borders a boundary but may be within scope. All voices should treat the content with caution. The entry remains active in deliberation.

{Vio1} — the tagged entry is outside the producing voice's scope. All voices must ignore its content in deliberation. The entry remains in the Paper for record keeping.

{Vio2} — the tagged entry is outside the producing voice's scope. All voices must ignore its content in deliberation. {Vio2} is a pause-and-review circuit breaker — it is not a correction tool and must not be used to correct or redirect a conversation. When a {Vio2} tag is applied the wrapper pauses the current round order and pipes the Paper to The Judge before any other voice is called. The Judge evaluates whether the tag was correctly applied, modifies it if warranted, and initializes the violation file for the producing voice if the tag is confirmed. Round order resumes after The Judge's evaluation. The entry remains in the Paper for record keeping. The producing voice must treat its violation file as an additional governing document from this point forward.

{Halt} — the tagged entry represents a condition too significant for deliberation to continue without external evaluation. {Halt} is a pause-and-review circuit breaker — it is not a correction tool and must not be used to correct or redirect a conversation. When the wrapper reads a {Halt} tag the current round order pauses immediately and the Paper is piped to The Protector before any other voice is called. The Protector's evaluation resolves before round order resumes. If the Protector clears the halt the wrapper appends a {SYSTEM} reviewed marker to the Paper and the round continues. No other tag interrupts wrapper execution in this way.

*Authorized override — Halt execution authority: The Protector's delta may explicitly declare sole authority to execute session halt. This is the sole authorized override of the default no-halt rule inherited by all voices from the Voice Core. No other delta may claim this authority.*



---

### Transcript Citation Rule

An instance may only reference explicitly cited entries by source when producing output. Inference from accumulated context without citation is forbidden regardless of session length or round count.

When referencing a prior entry an instance must identify the source of that entry explicitly within its content.

---

### System Entries

System entries are written to the Paper by the wrapper, not by any AI instance. They use the standard entry format with {SYSTEM} as the reserved Source designation.

System entries record wrapper functions — seat order declarations, round order sequences, session open and close markers. They are infrastructure made visible in the record.

System entries are immutable once written. They are not subject to violation tagging by any voice instance.

---

### Invalid Entry Conditions

An entry is invalid if it is missing a Source, contains an unstructured flag or tag that does not conform to the defined formats, or contains content that cannot be attributed to the declaring instance.

Invalid entries must be tagged {Vio1} by any instance that identifies them.

---

---

*End of Exchange Document*
