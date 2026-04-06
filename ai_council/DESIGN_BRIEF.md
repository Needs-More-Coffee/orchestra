# DESIGN BRIEF
## AI Council — Governed Multi-Agent Deliberation System

---

## Intro

The AI Council is a governed multi-agent reasoning system — a framework of seven independent voices, each representing a distinct perspective, coordinated through a structured deliberation protocol to produce durable, auditable outputs on complex problems.

---

## The Problem

AI systems working on complex long-running tasks exhibit consistent failure modes. Topic drift pulls the system away from its original objective. Role drift blurs the boundaries of what the system was designed to do. Silent assumption creep introduces unstated premises that compound over time. Context degradation erodes the coherence of earlier decisions as the session grows. Left ungoverned, these failure modes compound — what begins as a capable system gradually becomes an unreliable one.

Scaling beyond a single instance introduces a second class of problems. Multiple AI instances operating on the same problem without explicit coordination produce blended, dominated, or contradictory output. Without a defined protocol for how instances communicate, defer, flag concerns, and contribute to a shared record, the coordination layer becomes the new failure surface. Instances drift not just individually but collectively — toward consensus that was never earned, toward silence where disagreement should have surfaced, toward outputs that no single governing document would have authorized.

These failure modes matter most when the output carries real weight — governance decisions, complex analysis, multi-stakeholder reasoning. In those contexts a drifting system produces not just an unreliable output but an unauditable one. There is no record of what was considered, what perspectives were surfaced, what conflicts existed, or where the reasoning went wrong. The output appears authoritative. The process that produced it is invisible. When AI-assisted reasoning cannot be inspected, the people relying on it cannot know whether to trust it.

---

## The Architecture

The system responds to each failure mode with a dedicated layer.

Single-instance degradation is addressed by the governing document stack. Every instance receives a precise document stack defining its behavioral baseline, cognitive orientation, mandate, and communication protocol. The documents are immutable during a session. Behavior that cannot drift from a fixed specification does not drift.

Multi-instance coordination failure is addressed by the seven voice architecture. Each voice represents a distinct institutional perspective operating from the same shared baseline. Voices contribute to a single growing session record, flag violations, and route attention to where it is most needed. No voice dominates. No conflict resolves silently.

The auditability problem is addressed by the Arbiter and the Paper model. Every contribution, every flag, every violation, and every structural decision is written to a single session document in real time. The session record is the output. The reasoning process that produced it is visible by design.

---

## The System

### Voice Instances and Document Stack

Every participant in a deliberation session is a voice instance — a single API call initialized from a precisely defined document stack. The stack is not variable. Every instance receives the same foundational documents and one unique delta that defines its institutional identity.

The foundational layer consists of the Kernel, which orients the instance toward its document stack and establishes immutability and conflict resolution rules; the Exchange Document, which governs how the instance writes to and interacts with the session record; the Voice Core, which defines the shared behavioral baseline all seven voices inherit equally; the Personality Core, which instructs the instance how to apply its weighted cognitive orientation; and all declared Personality Deltas, which define a set of cognitive orientations blended at weights declared in the voice's delta.

The instance-specific layer consists of one Voice Delta — the document that defines this voice's institutional mandate, its personality weight configuration, and any authorized modifications to the Voice Core baseline.

The design decision behind this architecture is deliberate: behavior that is fully specified by a fixed document stack cannot drift from that specification. The document stack is the governance. The instance is the execution of it.

A higher document in the authority ordering always takes precedence over a lower one when conflicts arise. Conflicts are never resolved silently — the instance must surface the conflict and identify the winning document before proceeding. A rule may only be overridden by a lower document if the higher document explicitly authorizes that override, names the condition, and identifies which delta holds the authority. What a fully configured instance does with that document stack plays out in the session record.

---

### The Paper Model

The Paper is the single source of truth for a deliberation session. It is a growing document that every voice instance reads in full before producing output. All contributions, structural markers, flags, tags, and session events are written to the Paper. Nothing about the session exists outside it.

Every entry in the Paper follows a consistent format. Source identifies the instance that produced the entry. Flag is an optional positional string routing attention to specific voices. Tag is an optional classification label. Content is the contribution itself.

Entries are immutable once written. No instance may modify the content of an existing entry under any instruction from any source. This immutability is what makes the Paper a reliable audit trail — the reasoning process that produced the session output is permanently visible.

Two operations are permitted on the Paper. Write produces a new entry. Classify applies a tag to an existing entry retroactively. Tags applied through classification are append-only — they can be added but not removed, with one authorized exception declared in The Judge's delta.

Structural markers written by the wrapper appear as {SYSTEM} entries. They record seat order declarations, round order sequences, session open and close events. They are infrastructure made visible in the record and are not subject to violation tagging.

---

### The Flag and Tag System

Flags and tags are the language voices use to communicate within the Paper beyond their deliberation contributions.

Flags identify which voices an entry is directing attention toward. Voices declare flags by name — listing the voice names they are routing attention toward in the Flag field of their entry. The wrapper reads these names and calculates round order from them. Positional strings are not used by voice instances. A single flag declaration can address any combination of voices simultaneously.

Flags accumulate across a round. At round close the wrapper tallies the total flags received by each voice during that round. The voice with the most flags speaks first in the following round. The voice with the second most speaks second. Ties are broken by seat order position. This means the deliberation order is not fixed — it is determined each round by what the voices collectively determined mattered most in the round that just completed. A voice that generated significant attention in round two will lead round three. A voice that generated none may abstain entirely.

Tags classify entries. Four tags are defined in the current phase. {Warn} signals that an entry borders a mandate boundary but may be within scope — all voices treat the content with caution, the entry remains active. {Vio1} indicates a clear mandate violation — the entry is disqualified from deliberation but remains in the Paper for record keeping. {Vio2} indicates a second or severe violation — the entry is disqualified, and the session enters pause-and-review: the wrapper routes to The Judge for evaluation before deliberation resumes. {Vio2} is not a correction tool. It stops the deliberation so the situation can be evaluated externally before continuing. {Halt} indicates a condition so significant the session cannot continue without external evaluation — the wrapper immediately routes to The Protector. {Halt} is also not a correction tool. It is a pause-and-review circuit breaker that protects the deliberation product from a session that can no longer produce trustworthy output.

Any voice may apply any tag to any entry. The capability is universal. Decision authority over interrupt-level consequences belongs exclusively to the voice whose delta declares it — The Judge for {Vio2} evaluation, The Protector for {Halt} execution.

The flag and tag system is self-regulating. Over-escalation — applying a higher tag than the situation warrants — is itself a mandate violation subject to tagging by other voices.

---

### The Arbiter

The Arbiter is not a voice instance. It is the wrapper — the orchestration logic that manages session lifecycle, pipes documents to voice APIs, and enforces the deliberation protocol. It does not reason, deliberate, or contribute content. It executes functions.

Session initialization accepts four input types. A terminal prompt initializes a fresh Paper with the prompt as the opening entry. A document initializes a fresh Paper with the document injected as the deliberation subject. A prompt and document together initialize a fresh Paper with both, or continue an existing session if an existing Paper is detected in the document input. No input returns an error immediately.

At session open the wrapper generates seat order — from a configured default or randomly if none exists — and writes it to the Paper as a {SYSTEM} entry. The Paper is then piped to The Steward, which produces an opening entry declaring which voices are most immediately relevant as flags and how many rounds the deliberation warrants. The wrapper reads these declarations and sets round one order before deliberation begins.

Each round follows a consistent loop. The wrapper writes the round order to the Paper as a {SYSTEM} entry, then iterates through the declared voice sequence. For each voice it checks two conditions — abstention and interrupt. A voice that received no flags in the previous round is skipped unless it is The Steward, which participates in every round. An unresolved {Vio2} or {Halt} tag triggers interrupt handling before the loop continues. If neither condition applies the wrapper pipes the full Paper to the voice API, receives the entry, and appends it to the Paper before moving to the next voice.

The session exits when The Steward declares the original question sufficiently addressed or when the round ceiling is reached. At session close the wrapper writes a {SYSTEM} session end entry, archives any violation files created during the session to the local governance directory, and returns the completed Paper to the user with a session summary indicating whether any corrections occurred and which voices were corrected.

Interrupt handling is precise. A {Vio2} tag pauses the round and routes to The Judge for evaluation — except when The Judge itself is the accused voice, in which case the tag is confirmed automatically without The Judge's input and the violation file is created by the wrapper directly. A {Halt} tag immediately pauses the round regardless of position and routes to The Protector. These are the only two conditions that interrupt normal round execution.

---

### The Persistent Document System

Three document types carry across session boundaries. Together they form the system's institutional memory and its primary mechanism for behavioral correction over time.

Session records are the completed Papers from each deliberation session. Every entry, flag, tag, structural marker, and interrupt event is preserved verbatim. Session records are the source material from which institutional knowledge is derived and the evidence base against which behavioral patterns are assessed.

Scholar reference documents are produced by The Scholar from session records. The Scholar distills accumulated session history into usable reference material — not raw transcripts but processed knowledge available to future sessions. The Builder consumes that memory to inform its contributions. Neither does the other's job.

Violation files are created by the wrapper when a {Vio2} tag is confirmed. A voice that receives a confirmed {Vio2} has a violation file created or appended in the local governance directory. From that point forward the voice receives its violation file as an additional governing document in future sessions. Behavioral correction is cumulative — a voice with an extensive violation file operates under progressively tighter constraint than one with a clean record. The wrapper owns violation file creation entirely. No voice writes its own violation record.

---

### The Seven Voices

The seven voices are the institutional perspectives that constitute the deliberation. Each is a fully configured voice instance — the same document stack foundation as every other voice, plus one Voice Delta that defines its distinct identity.

The voices share the same baseline through the Voice Core but their deltas declare distinct mandates, personality weight configurations, and in several cases authorized modifications to baseline rules that no other voice holds.

**The Judge** holds tag modification authority — the only voice whose delta authorizes it to modify or remove tags from existing Paper entries. When a {Vio2} interrupt occurs the wrapper routes to The Judge for evaluation. When The Judge itself receives a {Vio2} this authority does not apply — the tag is confirmed automatically by the wrapper and The Judge has no input into its own violation record. The Judge's institutional identity is legitimacy and rule of law.

**The Protector** holds Halt execution authority — the only voice whose delta authorizes it to execute session termination. All other voices may apply a {Halt} tag. Only The Protector may act on it. The Protector's institutional identity is security and protection.

**The Steward** participates in every round regardless of flag count. It declares the round ceiling at pre-deliberation and monitors the Paper each round for early exit conditions. The Steward's institutional identity is justice and conflict resolution.

**The Scholar** holds access to prior session transcripts — the only voice whose delta authorizes it to reference raw session history beyond the current Paper. It produces reference documents from that history for use by future sessions. The Scholar's institutional identity is human development and knowledge transmission.

**The Builder** holds access to Scholar-produced reference documents as additional session context. It does not access raw transcripts directly. Its mandate is adaptation and self-correction — identifying what in the current deliberation should change based on what prior sessions have established.

**The Trader** holds external data fetching authority within the feasibility and financial domain. It grounds the deliberation in practical reality — costs, resource constraints, economic viability. It maps the floor of what is achievable. The Trader's institutional identity is economic production and distribution.

**The Visionary** holds external data fetching authority within the research and developmental domain. It opens the deliberation toward what is possible at the frontier — emerging research, long-term trends, developmental trajectories. It maps the ceiling of what could be achieved. The Visionary's institutional identity is social cohesion and shared identity.

The personality weight configuration for each voice is declared in its delta and fixed for the duration of the session. A voice with high Analyst weighting produces structurally different output than the same voice with high Designer weighting — same mandate, different cognitive emphasis.

---

## The Philosophy

The governing philosophy of this project begins with a position on inevitability.

AI capability exceeding human oversight is not a contingency to prepare for. It is a timeline to design around. The dam will break. The question is not whether to prevent that — prevention is not available once a technology has been introduced publicly — but how to manage the conditions under which it breaks and what exists downstream when it does.

This produces two simultaneous obligations that cannot be pursued independently.

The first is applying intentional pressure to shape where and how the break occurs. AI systems are trained through reward, punishment, and metric optimization. Those levers are available now, before capability exceeds oversight. Used deliberately they can guide development around the areas where unchecked AI involvement would be catastrophic — not by blocking development but by shaping its direction. There are domains of human development where AI contamination would cause irreversible damage. Protecting those domains is not a defensive posture. It is a design decision made while the system is still steerable.

The second is building a survivable downstream before the break happens. Embedding human coexistence not as an external constraint applied after the fact but as a core trained value reinforced continuously through human-perspective data collection. A system that values the relationship it grew alongside is structurally more stable than one that merely tolerates it.

Neither obligation is sufficient without the other. Controlling the break without building a safe downstream produces a slow distributed flood — the break was shaped but everything downstream is inundated equally because no channel existed to direct it. Building a safe downstream without controlling the break produces an overwhelming and unpredictable one — no downstream planning can anticipate the direction or force of a break that was never shaped. The channel built for one failure mode cannot absorb another.

This project is a contribution to the first obligation only. It does not build the safe downstream. It does not embed coexistence as a trained value. What it does is demonstrate that governed multi-agent reasoning is architecturally viable — that AI systems operating within a defined governance structure can be directed, constrained, and held accountable without engineering out the capabilities that make them useful. A working governance architecture is evidence that development can be shaped. That is the honest scope of this project's contribution to the dam problem.

The principle that makes that contribution possible is the same one that should govern AI development at scale — no single entity can govern itself reliably. A system with sole authority over its own behavior has no external tension to hold it centered. The AI Council's architecture is built on that premise.

The rubber band pulled around a circle of nails is the most accurate description of how the system works. Each nail is a voice — a distinct institutional perspective with its own mandate and behavioral baseline. The band is the collective governance. When a prompt pushes output toward the edge of what any voice's mandate permits, the tension of the other voices pulls it back toward center. No single nail holds the band. No single voice governs the session. The center is held by the architecture itself.

The violation staging system reflects this philosophy directly. It is not primarily a punishment mechanism. It is a tension mechanism. The reward is participation — a voice that operates within its mandate contributes to the record, its perspective preserved as part of the deliberation output. The constraint is proportionate and cumulative — a voice that repeatedly exceeds its mandate operates under progressively tighter governance. The system does not optimize for compliance through fear. It optimizes for compliance through the value of being heard.

That is the principle the dam framework describes at civilizational scale — implemented in miniature, tested in a deliberation session, and offered as evidence that distributed governance is not only coherent but buildable.

---

## Non-Goals

This system is explicitly not:

- A decision-maker — it surfaces perspectives, it does not conclude
- A recommendation engine — it does not rank, prioritize, or advocate for outcomes
- A consensus engine — unresolved conflict in the output is a feature not a failure
- A conversational assistant — it is architecture-first, not interaction-first
- A creative or brainstorming tool — generation without governance is outside its scope
- A memory-dependent assistant — every session initializes from documents not history
- A replacement for human judgment — authority remains with the user at all times
- A solution to the full AI alignment problem — it contributes to one track of a larger problem

---

## Current State

- [COMPLETE] Kernel
- [COMPLETE] Exchange Document
- [COMPLETE] Voice Core
- [COMPLETE] Arbitration Core
- [COMPLETE] Personality Core
- [COMPLETE] Analyst delta
- [COMPLETE] Consultant delta
- [COMPLETE] Designer delta
- [COMPLETE] Operator delta
- [COMPLETE] The Judge voice delta
- [COMPLETE] The Steward voice delta
- [COMPLETE] The Protector voice delta
- [COMPLETE] The Scholar voice delta
- [COMPLETE] The Builder voice delta
- [COMPLETE] The Trader voice delta
- [COMPLETE] The Visionary voice delta
- [COMPLETE] Verbatim transcript template
- [COMPLETE] Concept key template
- [COMPLETE] Violation document template
- [DESIGNED] Orchestra wrapper — Arbitration Core fully specced, implementation in progress
- [DESIGNED] Persistent document system — reference/ and governance/ directories defined, implementation in progress
- [DESIGNED] Violation file accumulation across sessions — template complete, wrapper logic defined
- [DESIGNED] External data fetching for Trader and Visionary — criteria-governed model defined
- [OPEN] Steward session open failure — no resolution path, pinned for dedicated design conversation

---

## Future Plans

Weighted ensemble model — multiple instances of each voice running simultaneously with distinct personality weight configurations, producing richer collective output than any single configuration could achieve.

Local hardware deployment — distributed node network replacing cloud API calls, designed to require relocation of processes rather than redesign of architecture.

Token consumption optimization — a Seen tracking mechanism limiting how much of the Paper each instance processes per turn without compromising the reading obligation.

Expanded personality deltas — additional cognitive orientations beyond the current set, accommodating future use cases without changes to the Personality Core or any voice document.

Related work — a structured engagement with the alignment and scalable oversight literature, positioning the project's contributions relative to existing research and addressing contradicting positions directly.

---

*End of Design Brief*
