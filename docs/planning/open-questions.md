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

## Q-002: When should the engine consult NVD?
- Area: Inputs and detection
- Type: question
- Blocks: Enrichment design and run time (NVD is rate-limited, D-012).
- Notes: D-009 says "pull any detail from NVD if we think it will help". Depends on what the chain model needs that Trivy's JSON lacks. Trivy vulnerability entries already carry `CweIDs` and per-source CVSS vectors (vuln-data skill), so NVD may only be needed where those are missing. Measure on a real report with `/trivy-inspect`. Decide during the chain model area.

## Q-003: How should dev/build dependencies affect exposure inference and chain reachability?
- Area: Chain model / Attacker model
- Type: question
- Blocks: Exposure inference (D-008) and chain construction.
- Notes: D-004 includes dev dependencies, so a test-only HTTP server package could wrongly suggest the app is network-facing, and a dev-only CVE may not be reachable in production. Possible answers: exclude dev deps from exposure inference, label chains that pass through dev deps, or treat them as build-time/supply-chain chains only. Fact (vuln-data skill): Trivy marks packages `Dev: true` only for some ecosystems (npm, yarn, pnpm v9+, Bun, Poetry, uv, gradle). pip `requirements.txt` and Pipenv have no dev distinction, so for those the tool can't tell dev from runtime at all.

## Q-004: How is a chain's combined severity calculated?
- Area: Chain model / Report
- Type: question
- Blocks: Chain ranking and report layout.
- Notes: D-005: "two separate CVEs amount to a more severe CVE". Candidates include severity of the final capability gained, a composite of step CVSS/EPSS/KEV, or a qualitative rating.

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

## Q-007: How are findings without a CVE ID handled?
- Area: Inputs and detection
- Type: question (needs confirming on a real report)
- Blocks: Enrichment (D-009): EPSS, KEV and NVD are all keyed by CVE ID.
- Notes: Trivy can report advisories by other IDs (e.g. GHSA-…) when no CVE exists. Misconfigurations and secrets never have CVEs or CWEs. These need their own way of saying what they require and give an attacker.

## Q-008: Which CWE level should chaining reason at?
- Area: Chain model
- Type: question
- Blocks: How links between findings are decided (D-005, D-009).
- Notes: Real data shows CVEs mapped to several CWEs at different levels. Log4Shell has CWE-20 (broad, Class level, CanPrecede 5 other weaknesses, very general consequences) plus CWE-917 (specific, "Execute Unauthorized Code or Commands"). Linking on broad CWEs could connect almost anything. Options include preferring the most specific CWE, combining all, or weighting by abstraction level. To be covered in the chain model area.

## Q-009: Is open-attack-path static-only, or will it ever validate chains against running systems?
- Area: Scope and safety
- Type: question
- Blocks: Scope statement in the README, the confidence design, and safety rules.
- Notes: The original README describes "static vulnerability analysis", and all decisions so far reason over a Trivy report only. On 2026-11-25 the user chose to leave this out of the README mission statement until the scope and safety interview.
