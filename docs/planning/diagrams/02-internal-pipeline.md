# Internal pipeline

The stages inside open-attack-path, from Trivy JSON in to report out, with the data passed between them. Based on decisions up to D-045. Stage order shows data dependencies only; how the stages are built is not decided.

```mermaid
---
config:
  flowchart:
    wrappingWidth: 600
---
flowchart TB
    in[/"Trivy JSON report (D-001)"/]

    s1["1. Load and check the report<br/>OPEN: supported Trivy versions (Q-005)<br/>OPEN: report made with wrong flags (Q-006)"]
    s2["2. Extract findings (D-003)<br/>dependency vulnerabilities, misconfigurations, secrets<br/>OS packages excluded<br/>secret values never kept (D-013)"]
    d2a[/"Findings: 3 kinds"/]
    d2b[/"Package list, incl. dev dependencies (D-004)"/]

    s3["3. Enrich findings (D-009)<br/>CWEs, EPSS score, KEV status, queried live every run (D-010)<br/>NVD only to fill gaps, or for every CVE when an API key is set (D-024)"]
    ext[("NVD API, optional key (D-012)<br/>FIRST EPSS API<br/>CISA KEV feed")]
    d3a[/"Enriched findings"/]
    d3b[/"Data gaps: sources that failed (D-011)<br/>NVD mode used (D-024)"/]

    s4["4. Work out which starting positions are available (D-032)<br/>remote with no account, logged-in user, local on the host, upstream package<br/>inferred from runtime dependencies only (D-036)<br/>override beats inference: app type, then per-position on/off (D-037)<br/>logged-in user available whenever remote is (D-035)<br/>local on the host only when inferred or overridden (D-034)<br/>OPEN: inference rules and app-type table, drafted from real data (D-043, Q-010)"]
    ovr[/"Optional exposure override in config (D-037)"/]
    d4[/"Available starting positions,<br/>each marked inferred or overridden (D-036)"/]

    s5["5. Assign capabilities to each finding<br/>vulnerabilities: requires from CVSS,<br/>gives from CWE consequences and CVSS impact (D-020)<br/>misconfigurations and secrets: curated table,<br/>generic fallback at lower confidence (D-021)<br/>every CWE kept, weighted by specificity,<br/>source and MITRE guidance (D-022)<br/>OPEN: the capability list (Q-010)"]
    cwe[("MITRE CWE data<br/>consequences, relationships, mapping guidance<br/>OPEN: how it is obtained (Q-014)")]
    tbl[/"Curated table: misconfiguration and secret<br/>capabilities and likelihoods (D-021, D-027)<br/>OPEN: contents (Q-010, Q-011)"/]
    d5[/"Findings with requires and gives,<br/>plus link confidence"/]

    s6["6. Build chains (D-016)<br/>A links to B when A gives what B requires<br/>CWE links shown as evidence<br/>report findings only (D-017)<br/>2 to 3 findings by default, configurable (D-018, D-019)<br/>no repeated findings, reorderings collapsed (D-029)<br/>runtime and build-time chains kept separate (D-028)<br/>misconfigurations and secrets can join either kind (D-045)<br/>CVEs needing physical access are never steps (D-039)<br/>first step needs a starting position; upstream can start either kind (D-032, D-044)<br/>must end in an attacker goal (D-025): code execution, read or change data,<br/>service down, privilege escalation, credential theft (D-030, D-031)<br/>build-time also: code on dev/CI machine, build secrets, tampered output (D-038)<br/>OPEN: does Trivy flag malicious packages, for upstream starts (Q-016)"]
    d6[/"Candidate chains: runtime and build-time"/]

    s7["7. Score and rank chains (D-026)<br/>score = likelihood × impact, likelihood = product of step likelihoods<br/>step likelihood: EPSS, KEV raised to a floor, otherwise fixed per category (D-027)<br/>steps needing victim interaction: likelihood reduced (D-040)<br/>impact from the final goal, in a fixed order (D-041, D-042)<br/>chains whose start isn't available sorted below all others (D-033)<br/>link confidence shown separately<br/>OPEN: numeric values (Q-011)"]
    d7[/"Ranked chains"/]

    s8["8. Write the report: OPEN<br/>format and layout not yet discussed<br/>already required:<br/>secrets redacted (D-013)<br/>data gaps and NVD mode stated (D-011, D-024)<br/>each position marked inferred or overridden (D-036)<br/>starting position each chain needs shown (D-033)<br/>link confidence shown (D-022)<br/>readable by technical and non-specialist readers (D-015)<br/>OPEN: how build-time chains are laid out (Q-013)"]
    out[/"Attack-path report"/]

    in --> s1 --> s2
    s2 --> d2a
    s2 --> d2b
    d2a --> s3
    s3 <-->|"live queries"| ext
    s3 --> d3a
    s3 --> d3b
    d2b -->|"runtime only (D-036)"| s4
    ovr -.-> s4
    s4 --> d4
    d3a --> s5
    cwe --> s5
    tbl --> s5
    s5 --> d5 --> s6
    d2b -->|"dev or runtime (D-028)"| s6
    d4 -->|"is each chain's start available (D-033)"| s7
    s6 --> d6 --> s7
    tbl --> s7
    s7 --> d7 --> s8
    d4 --> s8
    d3b --> s8
    s8 --> out

    subgraph legend["Key"]
        direction LR
        k1["Decided"]
        k2["Decided, with open parts"]
        k3["Not decided yet"]
        k4[/"Data"/]
        k5[("External source")]
    end

    classDef decided fill:#e8f1fb,stroke:#2563eb,color:#111
    classDef partial fill:#e8f1fb,stroke:#d97706,stroke-width:2px,color:#111
    classDef open fill:#fff4e5,stroke:#d97706,stroke-dasharray:5 5,color:#111
    classDef data fill:#f3f4f6,stroke:#6b7280,color:#111
    classDef external fill:#ecfdf5,stroke:#059669,color:#111
    class s2,s3,k1 decided
    class s1,s4,s5,s6,s7,k2 partial
    class s8,k3 open
    class in,d2a,d2b,d3a,d3b,d4,d5,d6,d7,out,tbl,ovr,k4 data
    class ext,cwe,k5 external
```
