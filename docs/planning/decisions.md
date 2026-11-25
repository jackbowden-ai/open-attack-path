# Decisions

Settled answers from planning. Append new entries; never edit or delete old ones. If a decision changes, add a new entry that supersedes the earlier ID.

Entry format:

```
## D-001: <short title>
- Date: YYYY-MM-DD
- Area: <topic from /plan-interview checklist>
- Question: <what was asked>
- Decision: <the answer>
- Reason: <why, in the user's words where possible>
- Consequences: <what this rules in or out>
- Supersedes: <D-xxx, if any>
```

---

## D-001: Input is a single Trivy JSON report file
- Date: 2026-11-25
- Area: Inputs and detection
- Question: What does the tool read, in which format, and does it run Trivy itself?
- Decision: The input is one Trivy native JSON report (`trivy --format json`) per run, produced by the user beforehand. The tool does not run Trivy and does not merge multiple reports.
- Reason: "I want to use the output of Trivy." Native JSON chosen over CycloneDX/SPDX; "Take a file"; "Single file".
- Consequences: Vulnerability detection is delegated to Trivy; the tool does no manifest parsing or package-to-CVE matching itself. Ecosystem coverage is whatever Trivy supports. Tests can use saved Trivy reports as fixtures. The parser is tied to Trivy's JSON schema.

## D-002: Trivy is run against the repository filesystem
- Date: 2026-11-25
- Area: Targets
- Question: What is Trivy pointed at to produce the input?
- Decision: The repo filesystem (`trivy fs` / `trivy repo`), not container images.
- Reason: User's choice ("Repo filesystem").
- Consequences: No OS-package findings appear in the input. Container runtime facts (actual base image, what ships) are not visible unless expressed in IaC/Dockerfiles in the repo.

## D-003: Finding types eligible as chain links
- Date: 2026-11-25
- Area: Targets
- Question: Which kinds of Trivy findings can be links in a chain?
- Decision: Dependency vulnerabilities, misconfigurations (Dockerfile/IaC), and exposed secrets. OS-package vulnerabilities are excluded.
- Reason: User's definition of chaining covers "security flaws, misconfigurations"; secrets selected as well.
- Consequences: The chain engine must model three kinds of finding with different metadata (CVE/CWE for vulns, Trivy check IDs for misconfigs, rule IDs for secrets). Initially the user picked "Dependencies" as the only artifact type; this decision broadens that to everything Trivy reports from a repo scan except OS packages.

## D-004: Full dependency tree including dev/build dependencies
- Date: 2026-11-25
- Area: Targets
- Question: Which dependencies are included?
- Decision: Direct and transitive, runtime and dev/build dependencies.
- Reason: User's choice ("Full tree, everything").
- Consequences: Covers build-time supply-chain risk; more findings and more noise. See Q-003 on how dev dependencies interact with exposure inference.

## D-005: Definition of a vulnerability chain
- Date: 2026-11-25
- Area: Chain model
- Question: What should a "vulnerability chain" mean in the report?
- Decision: Two or more flaws or misconfigurations linked so that, in sequence, they achieve an attack none could achieve alone. Combined CVEs can amount to something more severe than any single one.
- Reason: User's words: "Vulnerability chaining is the practice of linking two or more security flaws, misconfigurations, that sequentially achieve an attack no single attack could reach on its own. This could be two separate CVEs amount to a more severe CVE."
- Consequences: Chains are capability-based (what one step gives the attacker enables the next), not dependency-tree paths. The report needs a way to express a chain's combined severity (see Q-004).

## D-006: Targets are the user's own projects
- Date: 2026-11-25
- Area: Scope and safety
- Question: Whose projects will this run against?
- Decision: The user's own projects.
- Reason: User's choice.
- Consequences: No client-scoping or authorisation workflow needed initially. Secrets handling still matters (D-013).

## D-007: Typical target is a small, single service
- Date: 2026-11-25
- Area: Targets
- Question: How large is a typical target?
- Decision: One app/repo, roughly under 50k lines.
- Reason: User's choice.
- Consequences: Exhaustive chain search is likely feasible; no need to design for multi-service system models up front.

## D-008: Application exposure is inferred from dependencies, initially
- Date: 2026-11-25
- Area: Attacker model
- Question: How does the tool know how the app is exposed (web server, CLI, privileges)?
- Decision: Infer it from the dependencies (e.g. an HTTP framework implies a network-facing server).
- Reason: User: "Infer for dependencies initially."
- Consequences: Inferred exposure must be labelled as inferred in the report. "Initially" implies a later override or profile mechanism (see Q-001).

## D-009: Enrichment engine maps CVEs to CWEs, adds EPSS, CISA KEV and NVD detail
- Date: 2026-11-25
- Area: Inputs and detection
- Question: Beyond Trivy's output, what data should the tool use to decide how flaws connect?
- Decision: Build an attack-path engine that associates CVEs with CWEs, and includes EPSS and CISA KEV data. Pull detail from NVD where it helps.
- Reason: User: "I think we will need to create an attack path engine to associate CVEs to CWEs. Add EPSS and CISA KEV in our engine too, pull any detail from NVD if we think it will help."
- Consequences: The tool needs network access. CWE becomes a key input to working out what each vulnerability gives and requires. When NVD is consulted is not yet defined (see Q-002).

## D-010: Enrichment data is fetched live on every run
- Date: 2026-11-25
- Area: Operation
- Question: How should EPSS/KEV/NVD data be obtained?
- Decision: Query live sources on every run; no local cache or offline bundle.
- Reason: User's choice ("Fetch every run").
- Consequences: Always-current data; runs need network access, are slower, and are not exactly reproducible over time.

## D-011: Fetch failures don't stop the run
- Date: 2026-11-25
- Area: Operation
- Question: What happens when EPSS, KEV or NVD can't be reached or rate-limits?
- Decision: Finish the analysis with whatever data arrived, and state in the report which sources were missing and which chains may be affected.
- Reason: User's choice ("Continue, flag gaps").
- Consequences: The report needs a data-completeness section and per-chain flags for missing enrichment.

## D-012: Optional NVD API key
- Date: 2026-11-25
- Area: Operation
- Question: Should the tool support an NVD API key?
- Decision: Use one if configured; otherwise run unauthenticated (slower).
- Reason: User's choice ("Optional key").
- Consequences: Configuration must accept a key without requiring it; the key itself must never appear in the report or logs.

## D-013: Secret values are fully redacted in the report
- Date: 2026-11-25
- Area: Scope and safety
- Question: How should exposed secrets appear in the report?
- Decision: Show only secret type, file:line and Trivy rule; never the value, even partially.
- Reason: User chose the recommended option: a chain only needs to know a secret exists and where.
- Consequences: The report is safe to share or commit. Redaction must also cover any intermediate output and logs.

## D-014: open-attack-path is a personal project
- Date: 2026-11-25
- Area: Scope and safety
- Question: Who is open-attack-path for?
- Decision: A personal project, built for the user's own use and learning. Public, but not aimed at other users yet.
- Reason: User's choice ("Personal project").
- Consequences: README is written as a personal project. No onboarding, multi-user or distribution requirements for now. Complements D-006 (it analyses the user's own projects).

## D-015: What the report should help its reader do
- Date: 2026-11-25
- Area: Report
- Question: What should the report help someone do once they've read it?
- Decision: All four: see combined risk that per-finding severity hides; prioritise fixes based on which chains are possible, not only individual CVSS scores; explain to non-specialists how an attacker could get in; learn how vulnerability chaining works in real dependency trees.
- Reason: User selected all four outcomes; they form the README mission statement.
- Consequences: The report must serve both technical readers (prioritising fixes) and non-specialists (understanding risk). This partly answers report audience, which is otherwise still to be discussed. Format and layout remain open.
