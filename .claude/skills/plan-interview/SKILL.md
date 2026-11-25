---
name: plan-interview
description: Interview the user with structured question rounds before any design or implementation decision in open-attack-path. Use when starting a new topic or area, when a requirement is vague, before drafting or extending the plan, and before writing any code. Records answers in docs/planning/decisions.md and unresolved items in docs/planning/open-questions.md.
---

# Plan interview

The goal is to surface every decision that would change the design, and get the user's answer to it, before anything is built. Err on the side of asking more.

## Process

1. **Load context.** Read `docs/planning/decisions.md` and `docs/planning/open-questions.md`. Never re-ask something already decided; build on it instead.
2. **Name the area** being planned (from the user's request, or the topic list below). Tell the user which area this round covers.
3. **Ask in rounds** with the AskUserQuestion tool (up to 4 questions per call, 2–4 options each):
   - Each question must stand on its own: say why it matters in one clause.
   - Give concrete options with their trade-offs in the description. Mark one "(Recommended)" only when there is a real reason, and say the reason.
   - Use `multiSelect` when choices aren't mutually exclusive.
   - Use plain text questions instead when the answer is open-ended (e.g. "describe a chain you'd want this to catch").
4. **Follow up.** After each round, look at what the answers imply and ask about new branches they open ("you chose X; does that mean Y, or Z?"). Keep going until no remaining question in the area would change the design.
5. **Close the area** by asking: "Is there anything about <area> I haven't asked that you have opinions on?"
6. **Record.**
   - Each answer → a new entry in `docs/planning/decisions.md` using the format in that file.
   - Each unanswered question, "not sure yet", or assumption → `docs/planning/open-questions.md`, noting what it blocks.
7. **Play it back.** Summarise the decisions from this session in a few bullets and ask the user to confirm or correct them.
8. **Draw.** Once the user has confirmed, run `/draw-workflow` for the area just covered, so the diagrams in `docs/planning/diagrams/` reflect the new decisions.

## Rules

- Do not write code, choose a stack, or fill gaps with your own assumptions during an interview.
- Don't bundle a decision into a question's wording ("Should the Python CLI output Markdown?" presumes Python and CLI).
- If the user says "you decide", give your recommendation with reasons, ask them to confirm it, and record it as a decision made on Claude's recommendation.

## Topic checklist for this project

Pick the areas relevant to the current request; cover all of them before the plan is approved.

- **Targets:** What is analysed: source repos, dependency manifests, container images, IaC, live deployments? Which languages and frameworks? Expected size?
- **Inputs and detection:** Consume findings from existing scanners (e.g. SARIF from Semgrep/CodeQL, Trivy, dependency audits), do our own detection, or both? Which vulnerability data sources (NVD, OSV, GHSA, CWE)?
- **Chain model:** How is a single weakness represented (preconditions, capability gained, attacker position)? What links one step to the next: data flow, privilege, network reachability, trust boundaries, shared secrets? Maximum chain length? How are combinatorial explosion and cycles handled?
- **Attacker model:** Starting positions (unauthenticated remote, authenticated user, insider, local, supply chain) and goals (RCE, data exfiltration, privilege escalation, persistence).
- **Confidence:** How certain must a chain be before it's reported? Static reasoning only, or some form of validation? Acceptable false-positive vs false-negative balance?
- **Report:** Audience (developers, security team, management)? Format (Markdown, HTML, PDF, SARIF, JSON)? What each chain shows: steps, evidence with file:line, severity scoring method, remediation, the cheapest link to break? How are chains ranked and de-duplicated?
- **Scope and safety:** Limited to projects the operator owns or is authorised to assess? Any live exploitation at all? How are secrets found in the target handled in the report?
- **LLM use:** Is Claude or another model part of the analysis? Where, and with what cost or privacy limits (sending target code to an API)?
- **Operation:** CLI, CI integration, service? Runtime and resource limits? Must it work offline?
- **Technology:** Language/stack preferences, packaging, how it's distributed.
- **Testing and success:** How will we know it works? Ground-truth targets with known chains (deliberately vulnerable apps, hand-built fixtures)? What metrics?
