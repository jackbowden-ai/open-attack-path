# Workflow diagrams

Agreed 2026-11-25. Diagrams are written in **Mermaid** inside Markdown, so they display on GitHub, in VS Code (with a Mermaid preview extension) and at mermaid.live. Excalidraw was dropped because its hosted service needs a paid workspace.

- [01-end-to-end.md](01-end-to-end.md): what the user does before and after the tool, with the tool as one block.
- [02-internal-pipeline.md](02-internal-pipeline.md): the tool's stages from Trivy JSON in to report out, with the data passed between them and external sources.
- [03-chain-data-model.md](03-chain-data-model.md): findings, weighted CWEs, capabilities, starting positions, links and chains, and how they relate.
- [04-step-decision-tree.md](04-step-decision-tree.md): how one finding becomes a chain step: which rule sets its capabilities, its likelihood, and which chains it can join.

Each has a rendered PNG alongside it with the same name for viewing without a Mermaid renderer. The `.md` file is the source; the PNG is a snapshot of it.

## Rules

- Draw only what's decided. Undecided stages are dashed boxes marked "OPEN" with their question ID (e.g. Q-008). Don't fill them with a proposed design.
- Label each element with the decision IDs it rests on.
- When a decision is added or superseded, or an open question is answered, update the affected diagram in the same change, and re-render its PNG so the image never lags the source. The `/draw-workflow` skill does this (it runs at the end of every `/plan-interview`) and holds the rendering command and style conventions.
