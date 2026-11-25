"""Planning aid for open-attack-path: summarise a Trivy JSON report.

Standard library only. Usage: python -I inspect_trivy.py path/to/report.json
Never prints secret Match/Code content or free-text descriptions from the report.
"""
import json
import sys
from collections import Counter


def top(counter, n=10):
    return ", ".join(f"{k} ({v})" for k, v in counter.most_common(n)) or "none"


def main():
    if len(sys.argv) != 2:
        sys.exit("usage: inspect_trivy.py report.json")
    with open(sys.argv[1], encoding="utf-8-sig") as fh:
        rep = json.load(fh)

    results = rep.get("Results") or []
    print("== Report")
    print(f"SchemaVersion: {rep.get('SchemaVersion')}  Trivy: {(rep.get('Trivy') or {}).get('Version', 'not recorded')}")
    print(f"ArtifactType: {rep.get('ArtifactType')}  CreatedAt: {rep.get('CreatedAt')}")
    classes = Counter(r.get("Class", "missing") for r in results)
    print(f"Results by Class: {top(classes)}")

    vulns = [(r, v) for r in results for v in r.get("Vulnerabilities") or []]
    pkgs = [p for r in results for p in r.get("Packages") or []]
    mis = [m for r in results for m in r.get("Misconfigurations") or []]
    secs = [(r, s) for r in results for s in r.get("Secrets") or []]

    print(f"\n== Vulnerabilities: {len(vulns)} ({len({v.get('VulnerabilityID') for _, v in vulns})} unique IDs)")
    if vulns:
        print(f"By class: {top(Counter(r.get('Class') for r, _ in vulns))}")
        print(f"By severity: {top(Counter(v.get('Severity') for _, v in vulns))}")
        with_cwe = sum(1 for _, v in vulns if v.get("CweIDs"))
        print(f"With CweIDs: {with_cwe}/{len(vulns)}")
        print(f"Top CWEs: {top(Counter(c for _, v in vulns for c in v.get('CweIDs') or []))}")
        src = Counter(s for _, v in vulns for s in (v.get("CVSS") or {}))
        print(f"CVSS sources: {top(src)}")
        vec = sum(1 for _, v in vulns if any(c.get("V3Vector") or c.get("V40Vector")
                                              for c in (v.get("CVSS") or {}).values()))
        print(f"With a CVSS v3/v4 vector: {vec}/{len(vulns)}")
        print(f"With FixedVersion: {sum(1 for _, v in vulns if v.get('FixedVersion'))}/{len(vulns)}")
        print(f"ID prefixes: {top(Counter(str(v.get('VulnerabilityID', '')).split('-')[0] for _, v in vulns))}")

    print(f"\n== Packages listed: {len(pkgs)}")
    if pkgs:
        print(f"Relationship: {top(Counter(p.get('Relationship', 'absent') for p in pkgs))}")
        print(f"With DependsOn: {sum(1 for p in pkgs if p.get('DependsOn'))}  Dev=true: {sum(1 for p in pkgs if p.get('Dev'))}")

    print(f"\n== Misconfigurations: {len(mis)}")
    if mis:
        print(f"By status: {top(Counter(m.get('Status') for m in mis))}")
        print(f"By type: {top(Counter(m.get('Type') for m in mis))}")
        print(f"By severity: {top(Counter(m.get('Severity') for m in mis))}")
        print(f"Top check IDs: {top(Counter(m.get('AVDID') or m.get('ID') for m in mis))}")

    print(f"\n== Secrets: {len(secs)} (values never shown)")
    for r, s in secs[:20]:
        print(f"- {s.get('RuleID')} [{s.get('Category')}, {s.get('Severity')}] {r.get('Target')}:{s.get('StartLine')}")
    if len(secs) > 20:
        print(f"... and {len(secs) - 20} more")

    print("\n== Checks against planning decisions")
    if rep.get("ArtifactType") not in ("filesystem", "repository"):
        print(f"- ArtifactType is {rep.get('ArtifactType')}; D-002 expects a repo filesystem scan.")
    if classes.get("os-pkgs"):
        print("- os-pkgs results present; D-003 excludes OS packages.")
    if not classes.get("config") and not mis:
        print("- No config results: misconfig scanner probably not enabled (it is off by default), or no config files.")
    if classes.get("lang-pkgs") and pkgs and not any(p.get("Dev") for p in pkgs):
        print("- No Dev=true packages: --include-dev-deps may not have been used (D-004), or the ecosystem has no dev distinction.")
    if classes.get("lang-pkgs") and not pkgs:
        print("- No Packages listed: dependency graph unavailable (--list-all-pkgs off?).")


if __name__ == "__main__":
    main()
