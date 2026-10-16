# Publication scope and omissions

The objective is to publish **all research findings**, including failed constructions and unresolved attempts, in a reviewable source release. It is not to copy every temporary byte produced while searching. [FINDINGS.md](FINDINGS.md) covers each substantive result family; [REPORTS.md](REPORTS.md) lists every written research report and manuscript source; [INVENTORY.tsv](INVENTORY.tsv) accounts for every source-snapshot file individually.

The release preserves all original `.lean`, `.py`, `.cpp`, `.md`, `.tex`, and written report files outside disposable build/test scratch, without changing their contents. Every local Lean source dependency is present. All substantive compact result records are retained, including negative outcomes and UNKNOWN. Selected larger files are preserved when they enable important direct replays: the source safe-ancestry NFA and all terminal witnesses, boundary rank certificates and small graph chains, arbitrary-group certificates, exact rational/graph certificates, and the conditional-parity CNF/LRAT pair.

The following generated categories are omitted deliberately:

| Category | Reason and retained replacement |
|---|---|
| Compiled binaries, `.olean`, Python caches, copied build directories | Rebuildable products, not proof source; original sources, dependencies, version pins, build records and commands are retained. |
| CPU integration scratch directories | Generated per-case input/output/log trees; deterministic harnesses, exact compact result matrix, provenance, findings, and minimal structural counterexamples are retained. |
| Large raw graph, kernel, bulk-mixture and search-state outputs | The original proof/status report, generator, parameters, compact final/independent-audit record, and source-file hash are retained. Regenerate the full table before replaying a checker that reads it. |
| Raw solver/progress logs and incomplete serialized states | Their scoped result, timeout/cap status, discovery source and any substantive proof note are retained. Incomplete runs remain UNKNOWN. |
| Generated solver inputs | Generators and outcome records are retained. The completed conditional-parity CNF and LRAT trace are retained in full for direct proof replay. |
| Rendered manuscript PDFs | Complete LaTeX manuscript sources are retained; the rendered PDFs repeat that material. |
| Earlier whole-workspace hash lists | The release inventory records every source-snapshot file's original hash, while MANIFEST.sha256 verifies the exact published files. |

Each `INVENTORY.json` record gives the original relative path, original byte count and SHA-256, retention decision, reason and primary report mapping. Retained records also identify their published path. `OMITTED_OUTPUT_SUMMARIES.json` is explicitly metadata-only: it reports top-level scalars and collection sizes for omitted JSON, not mathematical certificates.

The source tree is historical research evidence. Earlier statements about publication or formalization status may have been superseded by a later named pass. This release's README and findings matrix state the current interpretation and trust boundaries. No earlier UNKNOWN is relabeled as an exclusion merely because a different later ansatz was excluded.

The repository review is pinned to upstream commit `8219522a02d46fbb72a6ee38819e5723b8c8fc9f`. Upstream source archives already present in that repository are referenced, not duplicated under `proofs/`. No production checkpoint or unrelated repository file is altered by this release.

Exact counts and byte totals appear in [release_stats.json](release_stats.json); the final list of published paths is [FILES.md](FILES.md). The release does not claim a main existence proof, a verified decimal Lychrel witness, novelty, or external peer review.
