# open-attack-path

Find the attack paths hiding between a project's vulnerabilities.

## Mission

Vulnerability scanners report findings one at a time, each with its own severity. Attackers don't work that way: they chain weaknesses together.

**Vulnerability chaining** is linking two or more security flaws or misconfigurations so that, in sequence, they achieve an attack none of them could achieve on its own. Two separate CVEs can amount to something far more severe than either one.

open-attack-path aims to take the weaknesses already found in a project and show how they could be linked into attack paths, so that combined risk, which no single severity score reveals, becomes visible and can be fixed.

## What it should help with

- **Seeing hidden combined risk:** attack paths that per-finding severity hides, such as two medium-severity issues that together give an attacker far more.
- **Prioritising fixes:** deciding what to fix first based on which chains are possible, not only on individual CVSS scores.
- **Explaining risk:** showing non-specialists, in plain terms, how an attacker could actually get in.
- **Learning:** exploring how vulnerability chaining works in real dependency trees.

## How it's planned to work

1. Scan a project with [Trivy](https://trivy.dev) and save the JSON report. The scan covers dependency vulnerabilities, misconfigurations (Dockerfiles, infrastructure as code) and exposed secrets.
2. open-attack-path reads the report and enriches each finding with its weakness type (CWE), how likely it is to be exploited (EPSS), whether it's known to be exploited in the wild (CISA KEV), and detail from NVD.
3. It works out which findings could be chained into attack paths.
4. It writes a report of the possible attack paths. Secret values are never shown in the report.

How chains are built, scored and presented is still being designed.

## Scope

- A personal project, for analysing my own projects.
- Starting with small, single-service projects.

## Status

**Planning.** No code yet: every design decision is made, recorded and reviewed before anything is built.

- Decisions: [`docs/planning/decisions.md`](docs/planning/decisions.md)
- Open questions: [`docs/planning/open-questions.md`](docs/planning/open-questions.md)
- Workflow diagrams: [`docs/planning/diagrams/`](docs/planning/diagrams/)
