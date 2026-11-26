# Open questions

Unresolved questions and unconfirmed assumptions. When one is answered, move it to `decisions.md` and delete it here.

Entry format:

```
## Q-001: <question>
- Area: <topic>
- Type: question | assumption
- Blocks: <what can't be decided or built until this is answered>
- Notes: <options discussed, partial answers>
```

---

## Q-005: Which Trivy versions / JSON schema versions must be supported?
- Area: Inputs and detection
- Type: question
- Blocks: Input parser and test fixtures.
- Notes: The parser is tied to Trivy's native JSON schema (D-001). Not urgent until implementation planning.

## Q-006: How does the tool handle a report produced with the wrong Trivy flags?
- Area: Inputs and detection
- Type: question
- Blocks: Input validation, and whether the report can claim to cover misconfigurations and dev dependencies.
- Notes: Trivy's defaults conflict with D-003/D-004. Misconfig scanning is off by default and dev dependencies are excluded by default. The needed command is `trivy fs --scanners vuln,secret,misconfig --include-dev-deps --format json -o report.json <repo>`. The JSON doesn't record which flags were used, so the tool can only infer (e.g. no `config` results, no `Dev: true` packages). Options: warn, refuse, or just document the required command.

## Q-009: Is open-attack-path static-only, or will it ever validate chains against running systems?
- Area: Scope and safety
- Type: question
- Blocks: Scope statement in the README, the confidence design, and safety rules.
- Notes: The original README describes "static vulnerability analysis", and all decisions so far reason over a Trivy report only. On 2026-11-25 the user chose to leave this out of the README mission statement until the scope and safety interview.

## Q-010: What is the capability list, and how do CWE impacts and CVSS translate into it?
- Area: Chain model
- Type: question
- Blocks: Capability matching (D-016, D-020, D-021), the curated misconfiguration/secret table, and impact values (Q-011).
- Notes: D-023 says to draft it from real data. Needs a Trivy report from one of the user's projects: `trivy fs --scanners vuln,secret,misconfig --include-dev-deps --format json -o report.json <repo>`, then `/trivy-inspect` and `/cve-lookup` on its CVEs. Trivy isn't installed on this machine yet. The same report is used to draft the exposure inference rules and the app-type → positions table (D-043, D-037).

## Q-011: What are the numeric values in scoring?
- Area: Chain model
- Type: question
- Blocks: Link confidence (D-022) and chain scores (D-026, D-027).
- Notes: Still to set: CWE weights for specificity, source and MITRE guidance; the KEV minimum likelihood; fixed likelihoods per misconfiguration/secret category; impact value per goal and capability, respecting the orders in D-041 and D-042; the likelihood reduction for steps needing victim interaction (D-040), and whether the KEV floor applies before or after it. Best set after Q-010 and checked against test targets with known chains (testing area).

## Q-013: How are build-time chains presented in the report?
- Area: Report
- Type: question
- Blocks: Report layout for build-time chains (D-028).
- Notes: Their goals are settled (D-038) and they share one impact scale with runtime chains (D-042), so they can be ranked together. Still open: one combined list, or separate runtime and build-time sections. Take up in the report interview, along with how the D-033 group boundary (chains whose start isn't available) is shown.

## Q-014: How is MITRE CWE data obtained?
- Area: Inputs and detection / Operation
- Type: question
- Blocks: Capability derivation (D-020), CWE weighting (D-022) and CWE relationship evidence (D-016).
- Notes: Found while drawing the pipeline diagram. CWE consequences, relationships, abstraction level and mapping guidance all come from MITRE, but D-010 ("fetched live every run") only covers NVD, EPSS and KEV. Options include the CWE REST API per run (no key needed), or the downloadable CWE catalogue (`cwec_latest.xml.zip`) refreshed on a schedule. See the vuln-data skill.

## Q-016: Does Trivy report malicious-package advisories for repo scans?
- Area: Inputs and detection
- Type: assumption
- Blocks: Runtime and build-time chains that start from the upstream-package position (D-044).
- Notes: Unconfirmed assumption behind D-044: that a Trivy filesystem scan flags known-malicious packages (e.g. OSV "MAL-" advisories), so an upstream start can be tied to a real finding as D-017 requires. If it doesn't, the upstream position can only be satisfied by the override (D-037) and needs another trigger. Check with `/vuln-data` and against a real report (Q-010).

## Q-017: When does the upstream-package position count as available?
- Area: Attacker model
- Type: question
- Blocks: Whether chains starting from the upstream position sort with the main list or below it (D-033).
- Notes: Found while drawing the attacker model diagram. Remote, logged-in and local each have an availability rule (D-034, D-035, D-036), but upstream doesn't. Options include: always available (any project can pull a hijacked package), only when the report contains a malicious-package finding (ties to Q-016), or only through the override (D-037).
