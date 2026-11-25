# Chain data model

The things the chain engine works with and how they relate: findings, their weighted CWEs, the capabilities they require and give, the links between findings, and the chains made from links. Based on decisions up to D-029.

```mermaid
classDiagram
    direction TB

    class Finding {
        kind: vulnerability, misconfiguration or secret
        package: runtime or dev
        requires: capabilities
        gives: capabilities
        likelihood
    }
    class CWE {
        id
        abstraction level
        consequences
        weight for this CVE
    }
    class Capability {
        name
    }
    class Link {
        from finding
        to finding
        link confidence
        CWE relationship evidence
    }
    class Chain {
        2 to 3 findings by default, configurable
        runtime or build-time
        likelihood
        impact
        score
    }

    Finding "1" --> "0..*" CWE : vulnerabilities have, each weighted D-022
    CWE --> Capability : consequences give D-020
    Finding --> Capability : requires and gives
    Link --> Finding : from and to D-016
    Chain "1" *-- "1..*" Link : made of D-016, D-017
    Chain --> Capability : must end in a goal D-025

    note for Finding "Vulnerabilities: requires and gives from CVSS and CWE (D-020)<br/>Misconfigurations and secrets: curated table,<br/>generic fallback at lower confidence (D-021)<br/>Likelihood: EPSS, raised to a floor if on CISA KEV,<br/>otherwise fixed per category (D-027)<br/>OPEN: runtime or build-time for these (Q-015)"
    note for Capability "Short project-specific list (D-023)<br/>OPEN: the list itself (Q-010)<br/>OPEN: which are goals (Q-012)"
    note for Chain "Score = likelihood × impact (D-026)<br/>likelihood = product of step likelihoods<br/>impact from the final capability<br/>no repeated findings, reorderings collapsed (D-029)<br/>runtime and build-time kept separate (D-028)<br/>OPEN: numeric values (Q-011)"
    note for Link "A links to B when A gives what B requires (D-016)<br/>Confidence from CWE weights,<br/>shown separately from the score (D-022, D-026)"
```
