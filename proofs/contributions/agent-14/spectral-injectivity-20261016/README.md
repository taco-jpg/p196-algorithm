# Agent 14: exact integer spectral coordinate

**Status: independently reviewed and verified; source ready for integration.**

This contribution proves the exact fixed-width injectivity assertion in the
preserved quadratic spectral notes. It defines the original T/R recurrences,
proves that natural subtraction is exact, proves strict domination of each
weight over all earlier coefficients bounded by 18, and recovers a symmetric
pair-sum word from its parity-dependent integer coordinate. It includes the
original decimal `Canonical` and `Admissible` wrappers. It does not recover an
integer's individual digit splits: the certified 12/21 collision makes that
boundary explicit. The canonical 196 control has pair sums (7,18,7) and
coordinate 158; it is not an orbit theorem.

## Evidence and source identity

The three mathematical sources and the scoped registry are unchanged from
published commit `1418f5c176582435d6aa824da72513117da2832b`. Exact remote file
bytes and the nontruncated evidence subtree were compared with local hashes.
The separate runtime specialist verified the same source hashes; it honestly
records local checkout HEAD `5ff4f607535587d572fbc9e95ba9501d1fbe5fc5`, rather
than claiming to have checked out the published commit.

- [Exact proof contract](CONTRACT.md)
- [Acceptance and scope report](REPORT.md)
- [Independent semantic source review](review/source-semantic-review.md)
- [Independent runtime, fresh build and axiom review](verification/independent/REVIEW.md)
- [Complete runtime/build evidence archive](evidence/p196-agent14-runtime-spectral-evidence-20261016.tar.xz)
- [Archive descriptor and recovery instructions](evidence/ARCHIVE.json)
- [Lossless archive manifest](evidence/MANIFEST.json)
- [Author decimal timeout evidence](evidence/p196-agent14-decimal-author-attempt-001.tar.xz)
- [Additive timeout termination record](development/Agent14SpectralDecimal/attempt-001/TERMINATION.json)
- [Scoped census and original successor queue](coverage-shortlist.md)
- [Current queue status](CENSUS_STATUS.md)

The unchanged canonical verifier passed a fresh four-module build, all 1,077
theorem constants and 15 registered endpoints. Its actual flags were `-j1
-DElab.async=false`. A second, genuinely independent source build compiled
all four modules anew using `--trust=0 -j1 -DElab.async=false`, followed by
all 1,237 safe constants and 50 explicit public signatures/axiom reports.
The only transitive axioms are `propext`, `Classical.choice`, and `Quot.sound`.
Post-build import audits inspect declarations and dependency origins; they are
not described as rechecking all imported proof terms. The fresh source
compilations provide that kernel checking.

The first safe-audit parser rejected Lean's wrapped final axiom list after
all Lean commands had succeeded. Its original FAIL, runner, stdout and
snapshots remain unchanged. A separately recorded continuation repaired the
parser, verified unchanged sources and objects, and completed the public
checks. The author decimal attempt also retains its real 300-second timeout
inside the unchanged foundation, before the new wrapper was reached.

## Reproduce

The complete runtime archive has 81 evidence files plus an internal manifest.
It preserves every substantive source, attempt, command, log and review, and
excludes only explicitly inventoried reproducible objects and the official
runtime distribution. The archive was extracted as a stream and every member
checked by SHA-256 and byte count. The smaller author archive independently
preserves the timed-out attempt and its additive terminal record.

For a complete replay, use the official Lean 4.19.0 release and the published
`verification/independent/rebuild.py` with an empty evidence directory, as
specified in the independent review. To inspect all historical raw logs,
extract the large archive into an empty directory; its `independent/` tree
contains the canonical pass, strict build, parser failure and continuation.
The complete official runtime provenance is under its `runtime/` tree.

No global source census or repository-wide acceptance is asserted. The scoped
registry deliberately retains `repository_wide_pass: false`. Integration
belongs to the coordinator holding the current exact main-write slot.
