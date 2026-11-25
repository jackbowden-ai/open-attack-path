# Internal pipeline

The stages inside open-attack-path, from Trivy JSON in to report out, with the data passed between them. Based on decisions up to D-013. Stage order shows data dependencies only; how the stages are built is not decided.

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

    s3["3. Enrich findings (D-009)<br/>CVE to CWE, EPSS score, KEV status<br/>queried live every run (D-010)<br/>OPEN: when to call NVD (Q-002)<br/>OPEN: findings without a CVE ID (Q-007)"]
    ext[("NVD API, optional key (D-012)<br/>FIRST EPSS API<br/>CISA KEV feed")]
    d3a[/"Enriched findings"/]
    d3b[/"Data gaps: sources that failed (D-011)"/]

    s4["4. Infer app exposure from dependencies (D-008)<br/>labelled as inferred<br/>OPEN: user override (Q-001)<br/>OPEN: effect of dev dependencies (Q-003)"]
    d4[/"Inferred exposure profile"/]

    s5["5. Build chains: OPEN<br/>what a chain is: D-005<br/>how findings link, CWE level: Q-008<br/>attacker model: not yet discussed"]
    d5[/"Candidate chains"/]

    s6["6. Score and rank chains: OPEN (Q-004)"]
    d6[/"Ranked chains"/]

    s7["7. Write the report: OPEN<br/>format and audience not yet discussed<br/>already required: secrets redacted (D-013),<br/>data gaps listed (D-011), exposure marked as inferred (D-008)"]
    out[/"Attack-path report"/]

    in --> s1 --> s2
    s2 --> d2a
    s2 --> d2b
    d2a --> s3
    s3 <-->|"live queries"| ext
    s3 --> d3a
    s3 --> d3b
    d2b --> s4 --> d4
    d3a --> s5
    d4 --> s5
    s5 --> d5 --> s6 --> d6 --> s7
    d3b --> s7
    s7 --> out

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
    class s2,k1 decided
    class s1,s3,s4,k2 partial
    class s5,s6,s7,k3 open
    class in,d2a,d2b,d3a,d3b,d4,d5,d6,out,k4 data
    class ext,k5 external
```
