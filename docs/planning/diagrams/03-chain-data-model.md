# Chain data model

The things the chain engine works with and how they relate: findings, their weighted CWEs, the capabilities they require and give, the links between findings, the chains made from links, and the starting positions chains begin from. Based on decisions up to D-045.

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
        goal or not
    }
    class StartingPosition {
        remote with no account
        logged-in user
        local on the host
        upstream package
        available: inferred or overridden
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
        start available or not
        likelihood
        impact
        score
    }

    Finding "1" --> "0..*" CWE : vulnerabilities have, each weighted D-022
    CWE --> Capability : consequences give D-020
    Finding --> Capability : requires and gives
    StartingPosition --> Capability : gives before the first step D-032
    Link --> Finding : from and to D-016
    Chain "1" *-- "1..*" Link : made of D-016, D-017
    Chain --> StartingPosition : first step needs D-033
    Chain --> Capability : must end in a goal D-025

    note for Finding "Vulnerabilities: requires and gives from CVSS and CWE (D-020)<br/>physical-access CVEs are never steps (D-039)<br/>Misconfigurations and secrets: curated table,<br/>generic fallback at lower confidence (D-021),<br/>can join either kind of chain (D-045)<br/>Likelihood: EPSS, raised to a floor if on CISA KEV,<br/>otherwise fixed per category (D-027),<br/>reduced if victim interaction is needed (D-040)"
    note for Capability "Short project-specific list (D-023)<br/>Goals: code execution, read or change data, service down,<br/>privilege escalation, credential theft (D-030, D-031)<br/>Build-time goals add code on a dev/CI machine,<br/>build secret theft, tampered output (D-038)<br/>Impact in a fixed order (D-041, D-042)<br/>OPEN: the list itself (Q-010)"
    note for StartingPosition "Inferred from runtime dependencies (D-036)<br/>or set by the override: app type, then per position (D-037)<br/>logged-in available whenever remote is (D-035)<br/>local only when inferred or overridden (D-034)<br/>CVSS network or adjacent = remote, local = local (D-039)<br/>upstream starts either kind of chain (D-044)<br/>OPEN: Trivy flagging malicious packages (Q-016)"
    note for Chain "Score = likelihood × impact (D-026)<br/>likelihood = product of step likelihoods<br/>impact from the final goal<br/>start not available: sorted below all others (D-033)<br/>no repeated findings, reorderings collapsed (D-029)<br/>runtime and build-time kept separate (D-028)<br/>OPEN: numeric values (Q-011)"
    note for Link "A links to B when A gives what B requires (D-016)<br/>Confidence from CWE weights,<br/>shown separately from the score (D-022, D-026)"
```
