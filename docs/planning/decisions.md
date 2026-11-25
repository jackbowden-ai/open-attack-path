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

## D-016: Links are decided by capability matching, with CWE relationships as evidence
- Date: 2026-11-25
- Area: Chain model
- Question: How does the engine decide that finding A can lead to finding B?
- Decision: Each finding has "requires" and "gives" capabilities. A links to B when A gives what B requires. MITRE CWE relationships (CanPrecede/CanFollow, named chains) are shown as supporting evidence for a link but don't create links on their own.
- Reason: User chose the recommended option: deterministic, explainable results (D-015) without relying on CWE links, which are too sparse to find most chains alone.
- Consequences: Every finding type needs a requires/gives mapping (D-020, D-021). Links can be explained step by step in the report. AI-judged linking is not used for this.

## D-017: Chains contain only findings from the report
- Date: 2026-11-25
- Area: Chain model
- Question: Can a chain include steps that aren't findings (e.g. "attacker logs into the cloud account")?
- Decision: No. Every step in a chain is a finding from the Trivy report.
- Reason: User's choice ("Findings only").
- Consequences: Every chain is fully evidenced. Chains that need an unreported attacker action in the middle won't be found; the next step after a secret must itself be a finding that requires credentials.

## D-018: Maximum chain length is configurable, default 3
- Date: 2026-11-25
- Area: Chain model
- Question: How long can a chain be?
- Decision: A configurable maximum, defaulting to 3 steps.
- Reason: User's choice. Targets are small single services (D-007).
- Consequences: The setting must be documented and tested. Longer runs and larger reports when users raise it.

## D-019: Only chains of two or more findings are reported
- Date: 2026-11-25
- Area: Chain model
- Question: Should a single finding that achieves a serious outcome alone appear in the report?
- Decision: No. Only chains of 2+ findings are reported; single critical findings are left to Trivy's own output.
- Reason: User's choice ("Chains only"), consistent with the chain definition (D-005).
- Consequences: The report is strictly about chaining. A single finding can still appear as a step inside chains.

## D-020: Vulnerability capabilities are derived automatically from CVSS and CWE
- Date: 2026-11-25
- Area: Chain model
- Question: Where do a dependency vulnerability's "requires" and "gives" come from?
- Decision: Derived automatically: "requires" from the CVSS vector (attack vector, privileges required, user interaction); "gives" from the CWE common consequences plus CVSS impact. No hand-curated per-CWE overrides.
- Reason: User's choice ("Auto from CVSS+CWE").
- Consequences: No per-CWE table to maintain; inherits CWE vagueness (e.g. "Varies by Context"), which the capability translation (D-023) must handle. Applies to any vulnerability with CVSS/CWE data, including non-CVE advisories such as GHSA (part of Q-007).

## D-021: Misconfiguration and secret capabilities come from a curated table with a generic fallback
- Date: 2026-11-25
- Area: Chain model
- Question: How are "requires" and "gives" defined for misconfigurations and secrets, which have no CVE or CWE (Q-007)?
- Decision: A curated table keyed by Trivy check ID and secret rule category. Where no entry exists, a generic rule for the finding's category applies, labelled lower confidence.
- Reason: User's choice ("Curated + generic fallback").
- Consequences: A curated table must be created and maintained in the repo. The same table holds these findings' fixed likelihoods (D-027). Together with D-020 and D-027 this resolves Q-007.

## D-022: All of a CVE's CWEs are kept, each weighted by how well it matches
- Date: 2026-11-25
- Area: Chain model
- Question: A CVE often has several CWEs at different levels and from different sources. Which drive capabilities (Q-008)?
- Decision: All CWEs attached to a CVE count, each with a weight for how strongly it matches the CVE. The weight comes from specificity (Variant/Base over Class/Pillar), source (e.g. NVD Primary over Secondary, vendor vs Trivy), and MITRE mapping guidance (Discouraged/Prohibited CWEs weigh little). The weight sets link confidence only: no CWE is dropped.
- Reason: User's own answer: "CWEs should be attached with weights to the strength matching the CVE." Weight factors and their use chosen in follow-up questions; agreement between sources was not chosen as a factor.
- Consequences: Resolves Q-008. Link confidence is shown in the report and kept separate from likelihood (D-026). Because nothing is dropped, broad CWEs can create many low-confidence links, so ranking carries the weight of keeping the report readable. Weight values are still to be set (Q-011).

## D-023: Capabilities use a short project-specific list, drafted from real data
- Date: 2026-11-25
- Area: Chain model
- Question: What list of attacker capabilities do "requires" and "gives" use, and how is it created?
- Decision: A short project-specific list, with a fixed translation from CWE technical impacts and CVSS. It is drafted only after looking at a real Trivy report (via /trivy-inspect and /cve-lookup).
- Reason: User's choices ("Own short list"; "From real data first").
- Consequences: Cleaner chains and plainer reports than raw CWE impacts. Blocked on a real Trivy report from one of the user's projects (Q-010).

## D-024: NVD fills gaps by default, and is fetched for every CVE when a key is set
- Date: 2026-11-25
- Area: Inputs and detection
- Question: When should the engine call NVD (Q-002)?
- Decision: By default, only when Trivy's entry lacks CWEs or a CVSS vector. When an NVD API key is configured, fetch every CVE so source weighting (D-022) has full data. Results may differ between the two modes; the report states which mode was used.
- Reason: User's choices ("Gaps, or with a key"; "Yes, state it").
- Consequences: Resolves Q-002. Refines D-009 ("NVD where it helps"). Runs are fast by default and fuller with a key.

## D-025: A reported chain must end in an attacker goal
- Date: 2026-11-25
- Area: Chain model
- Question: What makes a linked sequence of findings worth reporting?
- Decision: The last step must give a capability that counts as an attacker goal. Which goals count is decided in the attacker model.
- Reason: User's choice ("Must end in a goal"). The stricter option requiring a plausible starting position was not chosen.
- Consequences: Chains that lead nowhere serious are dropped. Depends on the attacker model's list of goals (Q-012).

## D-026: Chains are scored by likelihood × impact
- Date: 2026-11-25
- Area: Chain model
- Question: How is a whole chain scored for ranking (Q-004)?
- Decision: Score = likelihood × impact. Likelihood is the product of the steps' likelihoods (every step must succeed). Impact comes from the final capability gained. Link confidence (D-022) is shown separately and is not part of the score.
- Reason: User chose the recommended option: it separates "how likely" from "how bad" for prioritising fixes and explaining risk (D-015). Multiplying chosen over weakest-link or average.
- Consequences: Resolves Q-004. Longer chains score lower even when each step is easy. Impact values per capability are still to be set (Q-011).

## D-027: Where step likelihoods come from
- Date: 2026-11-25
- Area: Chain model
- Question: What likelihood does each step get, including findings with no EPSS score?
- Decision: CVE steps use their EPSS score. CVEs on the CISA KEV list are raised to a high minimum likelihood, whatever EPSS says. Misconfigurations, secrets and non-CVE advisories get a fixed likelihood per category, kept in the curated table (D-021).
- Reason: User's choices ("Raise to a floor"; "Fixed by category").
- Consequences: Completes the answer to Q-007. The KEV floor and category values are judgement calls still to be set (Q-011).

## D-028: Runtime and build-time chains are separate
- Date: 2026-11-25
- Area: Chain model
- Question: How do dev and build dependencies affect chains (Q-003)?
- Decision: Runtime chains never include dev dependencies. Dev dependencies form their own build-time (supply-chain) chains. Where Trivy can't tell dev from runtime (pip requirements.txt, Pipenv), packages are assumed to be runtime.
- Reason: User's choices ("Separate build chains"; "Assume runtime").
- Consequences: Resolves the chain part of Q-003; its effect on exposure inference remains open (Q-003, narrowed). Unknown packages err towards reporting a runtime chain that may not exist in production. What goals build-time chains end in is open (Q-013).

## D-029: No repeated findings, and reordered duplicates are collapsed
- Date: 2026-11-25
- Area: Chain model
- Question: How are repeated and near-duplicate chains handled?
- Decision: A finding appears at most once per chain. Chains using the same set of findings in a different order are collapsed to the highest-scoring order.
- Reason: User's choice ("No repeats, collapse sets").
- Consequences: No cycles. The report shows each set of findings once.
