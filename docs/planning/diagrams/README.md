# Workflow diagrams

Agreed 2026-11-25. Diagrams are written in **Mermaid** inside Markdown, so they display on GitHub, in VS Code (with a Mermaid preview extension) and at mermaid.live. Excalidraw was dropped because its hosted service needs a paid workspace.

- [01-end-to-end.md](01-end-to-end.md): what the user does before and after the tool, with the tool as one block.
- [02-internal-pipeline.md](02-internal-pipeline.md): the tool's stages from Trivy JSON in to report out, with the data passed between them and external sources.

Each has a rendered image alongside it ([01-end-to-end.png](01-end-to-end.png), [02-internal-pipeline.png](02-internal-pipeline.png)) for viewing without a Mermaid renderer. The `.md` file is the source; the PNG is a snapshot of it.

## Rules

- Draw only what's decided. Undecided stages are dashed boxes marked "OPEN" with their question ID (e.g. Q-008). Don't fill them with a proposed design.
- Label each element with the decision IDs it rests on.
- When a decision is added or superseded, or an open question is answered, update the affected diagram in the same change, and re-render its PNG so the image never lags the source. Render with the Mermaid CLI, e.g. `npx -p @mermaid-js/mermaid-cli mmdc -i 01-end-to-end.md -o 01-end-to-end.png -b white -s 1.5`. mmdc appends `-1` to the output name for Markdown input, so rename the result. On this machine, point it at Edge with `-p` and a puppeteer config containing `{"executablePath":"C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe"}` to avoid downloading Chromium.
