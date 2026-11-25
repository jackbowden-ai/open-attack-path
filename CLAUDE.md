# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this project is

open-attack-path analyses a target software project to find **vulnerability chains**: sequences of weaknesses that are individually limited but, combined, give an attacker a meaningful capability (e.g. SSRF → cloud metadata credentials → storage access). The output is a **report** describing each possible attack path.

## Current phase: planning — no code yet

The user wants extensive planning before anything is built.

- Do not write implementation code, scaffold projects, add dependencies, or pick a language/stack until `docs/planning/plan.md` exists and the user has explicitly approved it (recorded in `docs/planning/decisions.md`). Write a throwaway spike only if the user asks for one, and label it as such.
- When something is ambiguous, ask; don't assume. If an assumption is unavoidable to make progress, write it down in `docs/planning/open-questions.md` as an unconfirmed assumption.
- Use the project skills:
  - `/plan-interview` — structured question rounds before deciding anything about an area (scope, chain model, report format, etc.). Use it whenever a new topic comes up, not only when asked.
  - `/plan-challenge` — adversarial review of a draft plan or design before the user approves it.
  - `/vuln-data` — verified reference on Trivy JSON, NVD, EPSS, KEV, CWE and CAPEC. Use it instead of memory when a decision depends on what these sources contain.
  - `/cve-lookup <CVE-ID>` — live NVD/EPSS/KEV/CWE data for one CVE, to test chain-model ideas on real vulnerabilities.
  - `/trivy-inspect <report.json>` — summarises a real Trivy report (coverage, gaps, mismatches with decisions) without showing secret values.
  The Python scripts inside `.claude/skills/` are planning tools (standard library only, run with `python -I`), not part of the product.
- The `claude-security` plugin (Anthropic) is installed at project scope. It can triage other scanners' results and build threat models; useful for cross-checking findings on the user's own repos.

## Planning records

- `docs/planning/decisions.md` — settled answers; the source of truth. Read it before asking questions so nothing settled is re-asked. If a new answer contradicts an entry, point out the conflict and add a superseding entry rather than editing the old one.
- `docs/planning/open-questions.md` — unresolved questions and unconfirmed assumptions, each noting what it blocks.
- `docs/planning/plan.md` — the plan itself, written once enough decisions exist. Its status line says whether it is draft or approved.

When code exists, re-run `/init` to add build/test commands and architecture notes here.
