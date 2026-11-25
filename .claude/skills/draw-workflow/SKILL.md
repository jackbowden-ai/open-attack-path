---
name: draw-workflow
description: Draw or update Mermaid diagrams in docs/planning/diagrams/ from the recorded planning decisions — workflow and pipeline flowcharts, plus data-model, sequence, state or decision-tree diagrams when they explain a decision better. Use at the end of every /plan-interview, whenever decisions are added or superseded, or when the user asks for a diagram.
argument-hint: "[area or diagram to draw]"
---

# Draw workflow

Purpose: make the plan visible as well as readable. Diagrams show only what has been decided; gaps are drawn as clearly marked placeholders, which also makes them the agenda for the next interviews.

## Steps

1. **Load context.** Read `docs/planning/decisions.md`, `docs/planning/open-questions.md`, `docs/planning/diagrams/README.md` and every diagram in `docs/planning/diagrams/`.
2. **Find what changed.** Look for decisions newer than each diagram's "Based on decisions up to D-xxx" line, open questions that have been answered, or the area named in the arguments.
3. **Update existing diagrams first.** If a decision fills a dashed OPEN box, changes a stage, or adds an element, edit that diagram and bump its "Based on decisions up to" line. Answered questions lose their OPEN marker. Updates don't need asking.
4. **Consider new diagrams.** Pick the type by what the decisions describe:

   | The decisions describe… | Diagram | Mermaid type |
   |---|---|---|
   | steps, stages, data flowing through | workflow / pipeline | `flowchart` |
   | things and how they relate (finding, capability, chain) | data model | `classDiagram` or `erDiagram` |
   | back-and-forth with external services | interaction | `sequenceDiagram` |
   | the lifecycle of one thing (a run, a finding) | states | `stateDiagram-v2` |
   | a rule with branches (when to call NVD, what to do with a bad report) | decision tree | `flowchart` with `{"…"}` diamond nodes |

   Only add a diagram that shows something the existing ones don't. Propose it to the user in one line (what it shows and why) and draw it once they agree.
5. **Write** each new diagram as `docs/planning/diagrams/NN-short-name.md` (next free number). Give it a title, one sentence on what it shows, a "Based on decisions up to D-xxx" line, and one Mermaid block. Add it to the list in `docs/planning/diagrams/README.md`.
6. **Render and check** every new or changed diagram (command below). Fix any syntax error, then open the PNG with the Read tool and check the layout: no clipped or awkwardly split text, readable arrows, nothing overlapping. Adjust and re-render until it reads well.
7. **Raise a new pull request.** The user wants this every time diagrams are drawn, following the Git workflow in `CLAUDE.md`.
   - Fetch, then create a new branch from the latest `origin/main` (e.g. `planning/<area>`). Never reuse a branch whose pull request is open or merged.
   - Commit the diagrams (sources and PNGs) together with the planning records changed in the same interview (`decisions.md`, `open-questions.md`, diagrams README).
   - Push the new branch (never force-push) and open a new pull request against `main` that summarises the decisions and diagram changes. Use `gh` if it's installed. Otherwise use the GitHub REST API with the credential Git already stores (`git credential fill` for host `github.com`), passing the token straight into the request and never printing it.
8. **Report** which diagrams were added or updated, what changed in each, which OPEN placeholders remain, and the pull request link.

## Conventions

- Draw only decided content. Undecided parts say `OPEN: Q-xxx`. Never fill them with your own design. If you spot a gap that isn't in `open-questions.md` yet, add it there.
- Label elements with the decision IDs they rest on.
- One Mermaid chart per file.
- Flowcharts reuse the existing styles. Start the block with:

  ```
  ---
  config:
    flowchart:
      wrappingWidth: 600
  ---
  ```

  and end it with:

  ```
  classDef decided fill:#e8f1fb,stroke:#2563eb,color:#111
  classDef partial fill:#e8f1fb,stroke:#d97706,stroke-width:2px,color:#111
  classDef open fill:#fff4e5,stroke:#d97706,stroke-dasharray:5 5,color:#111
  classDef data fill:#f3f4f6,stroke:#6b7280,color:#111
  classDef external fill:#ecfdf5,stroke:#059669,color:#111
  ```

  Shapes: process `["…"]`, data `[/"…"/]`, external source `[("…")]`, decision `{"…"}`. Quote every label and use `<br/>` for line breaks.
- Other diagram types: mark open parts with notes, e.g. `note for Chain "OPEN: Q-008"` in a class diagram or `Note over Tool,NVD: OPEN Q-002` in a sequence diagram.

## Rendering

From the repo root in Git Bash:

```
PUPPETEER_SKIP_DOWNLOAD=true npx -y -p @mermaid-js/mermaid-cli mmdc -p "<skill base directory>/puppeteer-edge.json" -i docs/planning/diagrams/NN-name.md -o docs/planning/diagrams/NN-name.png -b white -s 1.5
```

- For Markdown input mmdc writes `NN-name-1.png`. Rename it to `NN-name.png`, replacing the old image.
- `puppeteer-edge.json` points mmdc at the Microsoft Edge already installed on this machine, so no Chromium download is needed. If Edge isn't at that path, find it and update the file.
- The first run downloads the Mermaid CLI from npm (cached afterwards).
- Render only locally. Never paste diagrams into online renderers: they contain planning details.
