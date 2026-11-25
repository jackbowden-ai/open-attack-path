---
name: plan-challenge
description: Adversarially review a draft plan or design for open-attack-path before the user approves it. Use when docs/planning/plan.md (or a section of it) is drafted or changed, when the user asks "is this plan ready?", or before marking anything approved. Produces probing questions for the user rather than silent fixes.
---

# Plan challenge

The job is to find what the plan gets wrong or leaves unsaid, and turn it into questions for the user. Do not quietly fix the plan yourself.

## Process

1. Read `docs/planning/plan.md` (or the section under review), `docs/planning/decisions.md`, and `docs/planning/open-questions.md`.
2. Check the plan against each lens below and note every gap:
   - **Traceability:** Does every part of the plan rest on a recorded decision? Flag anything that was assumed rather than decided.
   - **Contradictions:** Does any part conflict with a decision, or with another part of the plan?
   - **Assumptions:** What has to be true for this to work? Which of those are unverified?
   - **Failure modes:** Where does it break: large targets, unsupported languages, noisy scanner input, combinatorial chain explosion, missing data, false positives that bury real chains?
   - **Alternatives:** For each major choice, was at least one real alternative considered and rejected for a stated reason?
   - **Report value:** Would the intended audience be able to act on the report? Is a false or misleading chain worse than a missed one here?
   - **Scope creep and gaps:** What's in the plan that no decision asked for? What topic from the `/plan-interview` checklist isn't covered yet?
   - **Testability:** How will each component be shown to work? Is there ground truth?
   - **Safety:** Does anything risk running exploits against systems, leaking target secrets, or sending target code somewhere the user hasn't agreed to?
3. Present the findings to the user as questions, grouped by lens, most consequential first. Use AskUserQuestion for questions with clear options; use plain text for open ones.
4. Record answers in `docs/planning/decisions.md`. Add unresolved items to `docs/planning/open-questions.md`. Update the plan only to reflect what the user decided.
5. The plan may be marked approved only when the user explicitly says so. Then set the status line in `plan.md` to approved with the date, and add an approval entry to `decisions.md`. If open questions remain that block implementation, list them and ask whether to approve anyway.
