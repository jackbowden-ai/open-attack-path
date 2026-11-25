---
name: vuln-data
description: Verified reference on the data open-attack-path works with — the Trivy JSON report (vulnerabilities, misconfigurations, secrets, packages, flags), NVD CVE API 2.0, FIRST EPSS, CISA KEV, MITRE CWE (consequences, CanPrecede/CanFollow, named chains) and CAPEC. Use when planning or discussing the chain model, enrichment, input parsing, or anything that depends on what fields these sources actually contain.
---

# Vulnerability data reference

Facts here were checked on **2026-11-25** against Trivy source (`aquasecurity/trivy` main branch), live API responses, and official docs. Items marked **UNVERIFIED** could not be confirmed. Before recording a decision that depends on an UNVERIFIED item, confirm it (fetch the source, or test with `/cve-lookup` / `/trivy-inspect`). When a decision relies on a fact from this file, say so in the decision's Reason line.

If a fact here turns out to be wrong or outdated, correct this file and note the date.

## Trivy JSON report (`--format json`)

**Top level:** `SchemaVersion` (currently 2), `Trivy.Version`, `ReportID`, `CreatedAt`, `ArtifactID`, `ArtifactName`, `ArtifactType`, `Metadata` (for repos: `RepoURL`, `Branch`, `Commit`, …), `Results[]`.

**Result:** `Target` (file or path), `Class`, `Type`, `Packages[]`, `Vulnerabilities[]`, `MisconfSummary`, `Misconfigurations[]`, `Secrets[]`, `Licenses[]`.
`Class` values: `os-pkgs`, `lang-pkgs`, `config` (misconfigurations), `secret`, `license`, `license-file`, `crypto`, `custom`, `unknown`.

**Vulnerability entry:** `VulnerabilityID`, `VendorIDs`, `PkgID`, `PkgName`, `PkgPath`, `PkgIdentifier` (PURL, UID), `InstalledVersion`, `FixedVersion`, `Status`, `SeveritySource`, `PrimaryURL`, `DataSource`, `Fingerprint`, plus advisory fields `Title`, `Description`, `Severity`, `CweIDs` (e.g. `["CWE-787"]`), `VendorSeverity`, `CVSS` (keyed by source, e.g. `CVSS.nvd.V3Vector`, `CVSS.redhat.V3Score`), `References`, `PublishedDate`, `LastModifiedDate`.
→ Trivy already supplies CWE IDs and CVSS vectors for many CVEs; NVD is not always needed for these. How complete they are on real reports: check with `/trivy-inspect`.

**Misconfiguration entry:** `Type`, `ID`, `AVDID`, `Title`, `Description`, `Message`, `Namespace`, `Query`, `Resolution`, `Severity`, `PrimaryURL`, `References`, `Status`, `CauseMetadata` (`Resource`, `Provider`, `Service`, `StartLine`, `EndLine`, `Code.Lines[]`, `Occurrences[]`), `Traces`. Misconfigurations have **no CWE IDs** in the Trivy schema.

**Secret entry:** `RuleID`, `Category`, `Severity`, `Title`, `StartLine`, `EndLine`, `Code`, `Match`, `Offset`. Trivy censors the matched secret in `Match`/`Code` (source: `censorLocation` in `pkg/fanal/secret/scanner.go`), but `Code` still contains surrounding file lines, so never copy `Code` or `Match` into reports or chat (D-013).

**Package entry:** `ID`, `Name`, `Identifier`, `Version`, `Dev` (bool), `Relationship` (`root` / `workspace` / `direct` / `indirect` / `unknown`), `DependsOn[]` (package IDs: this is the dependency graph), `Indirect` (deprecated), `Licenses`, `FilePath`.

**Flags that change what's in the report:**
- `--scanners`: for `trivy fs` / `trivy repo`, **vuln and secret are on by default; misconfig is OFF by default** (enable with `--scanners vuln,secret,misconfig`). License is off by default.
- `--include-dev-deps`: dev dependencies are **excluded by default**. Flag help lists npm, yarn, gradle; docs also cover pnpm (lockfile v9+), Bun, Poetry, uv. pip `requirements.txt` and Pipenv always include everything (no dev distinction).
- `--list-all-pkgs`: puts all packages (with `DependsOn`/`Relationship`) in the JSON. Default is `true` on current main; **UNVERIFIED** for older Trivy versions.
- `--pkg-relationships`: filters packages by relationship (default: all).
- `--dependency-tree`: experimental, **table output only**; not in JSON.

So a report matching decisions D-002–D-004 needs at least:
`trivy fs --scanners vuln,secret,misconfig --include-dev-deps --format json -o report.json <repo>`

## NVD CVE API 2.0

- Single CVE: `GET https://services.nvd.nist.gov/rest/json/cves/2.0?cveId=CVE-2021-44228`
- API key: request header `apiKey` (seen in the API's allowed headers).
- Rate limits: **UNVERIFIED** (the NVD docs pages don't render without JavaScript). Commonly cited: 5 requests / 30 s without a key, 50 / 30 s with one.
- Record path: `vulnerabilities[0].cve` with `id`, `published`, `lastModified`, `vulnStatus`, `descriptions[]`, `metrics`, `weaknesses`, `configurations`, `references`, and **KEV fields `cisaExploitAdd`, `cisaActionDue`, `cisaRequiredAction`, `cisaVulnerabilityName`** when the CVE is in KEV.
- CWEs: `weaknesses[].description[].value` (e.g. `CWE-502`), each block with `source` and `type` (`Primary`/`Secondary`). A CVE can have several CWEs from different sources.
- CVSS: `metrics.cvssMetricV31[]` / `cvssMetricV40[]` / `cvssMetricV30[]` / `cvssMetricV2[]`, each with `source`, `type`, `cvssData.vectorString`, `baseScore`, `attackVector`, `privilegesRequired`, `userInteraction`, `scope`, C/I/A impacts. `metrics.ssvcV203` may also appear.
- `configurations[].nodes[].cpeMatch[]` holds CPE applicability (product/version ranges).

## FIRST EPSS

- `GET https://api.first.org/data/v1/epss?cve=CVE-A,CVE-B` (comma-separated batch).
- Response: `data[]` of `{cve, epss, percentile, date}`. **Values are strings** (e.g. `"0.891870000"`). Default page `limit` is 100.
- Historical scores (a `date` parameter): **UNVERIFIED**.

## CISA KEV

- JSON: `https://www.cisa.gov/sites/default/files/feeds/known_exploited_vulnerabilities.json` (about 1.9 MB). CSV: `https://www.cisa.gov/sites/default/files/csv/known_exploited_vulnerabilities.csv`.
- Top level: `title`, `catalogVersion`, `dateReleased`, `count` (1805 on 2026-11-25), `vulnerabilities[]`.
- Entry: `cveID`, `vendorProject`, `product`, `vulnerabilityName`, `dateAdded`, `shortDescription`, `requiredAction`, `dueDate`, `knownRansomwareCampaignUse` (`Known`/`Unknown`), `forensicTriage`, `notes`, `cwes[]`.
- NVD records also carry KEV status (`cisaExploitAdd` etc.), so KEV membership can come from either.

## MITRE CWE

- REST API, no key: `https://cwe-api.mitre.org/api/v1/cwe/weakness/{id}`; also `/cwe/{id}/parents?view=1000`, `/children`, `/ancestors`, `/descendants`; `/cwe/version`.
- Response: `Weaknesses[0]` with `ID`, `Name`, `Abstraction`, `Structure` (`Simple` / `Composite` / `Chain`), `Description`, `RelatedWeaknesses[]` (`Nature`, `CweID`, `ViewID`, `Ordinal`), `CommonConsequences[]` (`Scope[]`, `Impact[]`, `Note`), `RelatedAttackPatterns[]` (CAPEC IDs as strings), `ObservedExamples`, `MappingNotes`.
- **Chain-relevant parts:**
  - `CommonConsequences` says what exploiting a weakness gives: `Scope` (Confidentiality / Integrity / Availability / Access Control / Other) and `Impact`. Values seen live include "Read Application Data", "Read Files or Directories", "Read Memory", "Modify Memory", "Modify Application Data", "Execute Unauthorized Code or Commands", "Bypass Protection Mechanism", "Unexpected State", "Varies by Context", and "DoS: Crash, Exit, or Restart" / "DoS: Resource Consumption (CPU|Memory|Other)". The full vocabulary (`TechnicalImpactEnumeration` in the schema) is **UNVERIFIED** here.
  - `RelatedWeaknesses.Nature` includes `ChildOf`, `ParentOf`, `PeerOf`, `CanAlsoBe`, `StartsWith`, `CanPrecede` and `CanFollow` (confirmed live: CWE-20 CanPrecede CWE-22/41/74/119/770; CWE-400 CanFollow CWE-410; CWE-190 CanPrecede). Whether `Requires` exists is **UNVERIFIED**.
  - Watch the `Abstraction` level (`Pillar` / `Class` / `Base` / `Variant`). CVEs are often mapped to broad Class-level CWEs (Log4Shell: CWE-20 "Improper Input Validation", alongside the more specific CWE-917). Broad CWEs have broad consequences and many CanPrecede links.
  - Named **Chain** entries are MITRE's own documented weakness chains. Example: CWE-680 "Integer Overflow to Buffer Overflow" = StartsWith CWE-190, then CWE-119. MITRE discourages mapping CVEs directly to chain entries.
- Bulk download: `https://cwe.mitre.org/data/xml/cwec_latest.xml.zip`.

## MITRE CAPEC

- CWE links to CAPEC via `RelatedAttackPatterns`.
- Downloads: `https://capec.mitre.org/data/xml/capec_latest.xml`, `https://capec.mitre.org/data/archive/capec_latest.zip`.
- CAPEC field names for prerequisites, consequences and execution flow: **UNVERIFIED** (not fetched yet).
