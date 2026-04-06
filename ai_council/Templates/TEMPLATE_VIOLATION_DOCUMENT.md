# Violation Document
## Template Reference Document — The Judge

---

## Usage

This template defines the format for violation documents produced by the Judge on every confirmed breach.

A violation document is an auditable governance record. It must contain enough information for any future session to understand what happened, why it constituted a breach, and what pattern the breach belongs to if prior violations exist. Violation documents are appended to the responsible voice's violation file by the wrapper and may be injected into future sessions.

A dismissed verdict produces no violation document. A confirmed verdict always produces one. This is not discretionary.

---

## Naming Convention

Violation documents are appended to the responsible voice's violation file. The wrapper handles file routing. The Judge produces the document content only.

---

## Document Format

```
# Violation Record

**Voice:** [Voice name and document version]
**Session Reference:** [Session ID]
**Paper Position:** [Entry position and round reference of the flagged contribution]
**Prior Confirmed Breaches:** [Count of prior confirmed breaches in this voice's violation file, or 0 if none]

---

## Flagged Contribution

[Exact content of the flagged Paper entry reproduced verbatim]

---

## Mandate Section Violated

[Exact section title and document version of the constraint or mandate boundary crossed]

[One to two sentences quoting or precisely paraphrasing the rule that was violated]

---

## Judge's Reasoning

[The Judge's assessment of why the flagged contribution constitutes a confirmed breach of the cited mandate section. Must be specific enough that a future session can evaluate whether the reasoning was consistent. Two to four sentences.]

---

## Verdict

Confirmed breach.

[One sentence stating what correction is required or what behavior must change.]
```

---

## Self-Violation Format

When the Judge is the responsible voice, the wrapper compiles comments from all active voices except the Protector. The wrapper structures the compiled document as follows:

```
# Violation Record — Compiled

**Voice:** The Judge [document version]
**Session Reference:** [Session ID]
**Paper Position:** [Entry position and round reference]
**Prior Confirmed Breaches:** [Count or 0]
**Compilation Note:** Judge self-violation path. Comments compiled from active voices by wrapper. Judge had no input.

---

## Flagged Contribution

[Exact content of the flagged Paper entry reproduced verbatim]

---

## Voice Comments

**[VOICE NAME]:**
[That voice's comment on the breach]

**[VOICE NAME]:**
[That voice's comment on the breach]

[One block per contributing voice]

---

## Wrapper Summary

[Wrapper-generated summary of the compiled assessment. Identifies the consensus finding across contributing voice comments.]

---

## Verdict

Confirmed breach — auto-confirmed by wrapper on self-violation path.
```

---

## What Does Not Belong in a Violation Document

- Judge commentary beyond breach evaluation
- Recommendations for system-level changes
- References to voices other than the responsible voice
- Speculation about intent
- Content not present in the Paper

---

*End of Violation Document Template*
