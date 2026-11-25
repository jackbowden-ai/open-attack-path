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

## Q-001: Will users later be able to override or supply the inferred exposure profile?
- Area: Attacker model
- Type: question
- Blocks: Attacker model design (starting positions), and how confidently the report can state an attacker's entry point.
- Notes: D-008 says exposure is inferred from dependencies "initially". Options discussed: user-supplied profile, infer + user override.

## Q-003: Should dev/build dependencies count when inferring the app's exposure?
- Area: Attacker model
- Type: question
- Blocks: Exposure inference (D-008).
- Notes: The chain part was resolved by D-028 (runtime and build-time chains are separate; unknown packages assumed runtime). Still open: a test-only HTTP server package could wrongly suggest the app is network-facing. Likely follows D-028 (infer from runtime dependencies only), but not yet asked.

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
- Notes: D-023 says to draft it from real data. Needs a Trivy report from one of the user's projects: `trivy fs --scanners vuln,secret,misconfig --include-dev-deps --format json -o report.json <repo>`, then `/trivy-inspect` and `/cve-lookup` on its CVEs. Trivy isn't installed on this machine yet.

## Q-011: What are the numeric values in scoring?
- Area: Chain model
- Type: question
- Blocks: Link confidence (D-022) and chain scores (D-026, D-027).
- Notes: Still to set: CWE weights for specificity, source and MITRE guidance; the KEV minimum likelihood; fixed likelihoods per misconfiguration/secret category; impact value per capability. Best set after Q-010 and checked against test targets with known chains (testing area).

## Q-012: Which capabilities count as attacker goals, and where can an attacker start?
- Area: Attacker model
- Type: question
- Blocks: Which chains are reported (D-025), and what the first step of a chain may require.
- Notes: Chains must end in a goal (D-025), but the goal list isn't defined. A starting position wasn't required for a chain to be reported, but the first step's "requires" (e.g. network access) must still be met by something; how that's satisfied belongs with the attacker model and exposure inference (D-008).

## Q-013: What goals do build-time chains end in, and how are they reported?
- Area: Attacker model / Report
- Type: question
- Blocks: Build-time chains (D-028).
- Notes: Build-time (supply-chain) chains through dev dependencies are separate from runtime chains. Their goals (e.g. compromising the build or developer machines) and how they appear in the report aren't decided.

## Q-014: How is MITRE CWE data obtained?
- Area: Inputs and detection / Operation
- Type: question
- Blocks: Capability derivation (D-020), CWE weighting (D-022) and CWE relationship evidence (D-016).
- Notes: Found while drawing the pipeline diagram. CWE consequences, relationships, abstraction level and mapping guidance all come from MITRE, but D-010 ("fetched live every run") only covers NVD, EPSS and KEV. Options include the CWE REST API per run (no key needed), or the downloadable CWE catalogue (`cwec_latest.xml.zip`) refreshed on a schedule. See the vuln-data skill.

## Q-015: Can misconfigurations and secrets be steps in runtime chains, build-time chains, or both?
- Area: Chain model
- Type: question
- Blocks: Chain building (D-028) for non-dependency findings.
- Notes: Found while drawing the step decision tree. D-028 sorts dependencies into runtime or build-time chains, but misconfigurations and secrets aren't packages. A secret in a CI config or a Dockerfile build stage might belong in build-time chains, while one in application config belongs in runtime chains. Options include both, by file location, or by category in the curated table (D-021).
