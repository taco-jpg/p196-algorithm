# PR177 execution evidence preservation

## Result and custody

**PASS_WITH_HISTORICAL_MANIFEST_CAVEAT** for byte-preserving archival and recorded-hash readback.
Source head: `6f48ca108dee4c07588f8c5582bcfef55388537f`. Base: `74a1c3922eb7af438fe40b23d2105ad07556e3f5`.
Snapshot observation window: 2026-10-17T05:37:11.888445+00:00 to 2026-10-17T05:37:12.450023+00:00.

The actual Lean executor and verification publisher is **Agent #1**. Agent #9
only copied and checked evidence bytes. Agent #9 did not execute Lean, rebuild
the 19-module closure, alter source, publish remotely, or assume verification
ownership. Agent #107 remains source owner and Agent #31 remains main writer.
This archive is ready for Agent #9's authorized publication without waiting for
another Agent #1 packaging step. It does not claim repository-wide PASS.

## Exact retained scope

- `corpus/pr177-evidence/`: every substantive file from the named evidence root,
  including original/repaired verifier scripts, both supplemental runner versions,
  patches, registries, all four console logs, all run receipts, raw logs, generated
  Lean audit programs, source snapshots, manifests and failure files.
- `corpus/pr177-review/`: all six review/input files from the named review root.
  These are retained reports by their original authors, not new reviews by Agent #9.
- `corpus/agent1-repo/`: all 75 exact paths named in `review-inputs.json`, plus the
  original and repaired runnable verifier scripts. The scoped input registry is
  already among the 75 paths. This preserves the actual author failure snapshots
  and logs, input sources, metadata and verifier registry without checkout
  infrastructure. Every path matches its recorded byte count, SHA256 and Git blob
  identifier. Full origin names are retained in `ORIGIN_INVENTORY.json`.

There are **192 copied source artifacts** totaling
**3,336,192 bytes**. There are
**39 explicitly excluded files**, each with origin, exact size,
SHA256 and reason in `EXCLUDED_FILES.json`: 38 reproducible `.olean` files and
one Python bytecode cache. Both supplements' 19 exact object pins match the
excluded strict-run object hashes. No object is presented as source evidence.
No `.ilean` or native objects occurred in the two enumerated roots. Checkout
and `.git` infrastructure were not traversed. Runtime binaries outside these
roots are not duplicated; their original pins remain in the receipts.

## Preserved actual execution history

| Attempt | Preserved outcome | Exact qualification |
|---|---|---|
| `canonical-run-001` | FAIL | All 19 module commands exited 0; original commands omit explicit `--trust=0`; endpoint validation then failed before ProjectAudit. The nested project status remains RUNNING in the original FAIL receipt and is not rewritten. |
| `trust0-run-001` | PASS | Repaired verifier: 19 module commands plus ProjectAudit, all 20 exit 0 with explicit `--trust=0`. Retained exact-head report, clean-source receipt, 19 source snapshots and all logs. |
| `supplement-001` | FAIL | SafeDefinitionAudit exit 0; LiteralEndpointAudit exit 1 because `pp.width` is not registered. Raw failed source, output and failure receipt remain unchanged. |
| `supplement-002` | PASS | The exact successful safe stage from attempt 001 is reused and labeled `REUSED_EXACT_SUCCESS`; corrected literal stage freshly exits 0. No third closure build or duplicate safe-stage execution is claimed. |

The retained supplemental result reports 1,453 theorem constants, 414 safe
definitions, no safe opaque declarations, all 115 literal theorem outputs from
the seven new modules, and all nine checked endpoints. Original raw multiline
axiom output is copied in full. The 3,940 implementation entries use the audit's
combined unsafe-or-partial predicate; they must not be called 3,940 unsafe axioms.
The already completed independent supplement readback remains in the separate
frozen `supplement-review-002` deliverable. This preservation program verifies
provenance and hash continuity; it does not repeat that proof/audit review.

## Historical preliminary-manifest caveat

`corpus/pr177-evidence/PRELIMINARY_FILES.json` remains byte-identical. Its
`run_supplement.py` entry names an earlier 8,817-byte draft with SHA256
`7b195d686863dde8b7b9e7fe281614e2a67579cc4c26062a89a52f405dd8dc70`. The scoped input search found
0
matching files. A separate read-only search of all 1339
available package files and 643 regular
members in saved tar.xz archives found **0 matches**;
every compared path, member and digest is in `HISTORICAL_DRAFT_SEARCH.json`.
The retained independent `supplement-review.md`, section "Review and corrections",
states: "The first draft had two concrete evidence issues, both fixed before
execution". This is an attributed review statement, not an independent Agent9
timestamp attestation. The actual first-run
version is retained as `run_supplement.v1.py` (9,643 bytes, SHA256
`a96fb1f93b13eed7a733cf871d875c5d5c0ef878cf7d7072fc3e4196cfbfe3c9`), and the corrected
continuation is retained as `run_supplement.py` (11,091 bytes, SHA256
`1aeedfea7977790e0eea844532e33809ce0976a83df754d00aca8c56275daf5f`).

The historical mismatch is explicit, not silently repaired or counted as a
matching entry. It is not evidence of an absent executed attempt. All actual
attempt directories currently present are preserved, including failures. A
claim that this archive contains every intermediate pre-execution draft would
be unsupported. Any later recovery of that draft belongs in a separate addendum.

## Agent9 archival-validator attempt preserved

`preservation-attempt-001/` contains the complete original first preservation
attempt, unchanged, including its exact program, FAIL receipt, comparison data,
manifest, README and copied corpus. That program exited 1 after seven comparison
failures because Agent9 compared byte-count/hash pairs against preliminary
manifest records that additionally contain an origin `path` key. Six actual
content hashes already matched. The seventh is the known historical draft
mismatch described above. This is an archival-validator schema error, not a
Lean failure or new source defect. Its original README did not successfully
classify the historical exception; the current README and result supply that
qualification while retaining the original record. The corrected program checks
origin paths separately and compares only bytes/SHA256 for content. No original
manifest or external input was edited.

## Verification and freeze

`snapshot_and_verify.py` is the exact preservation/validation program. It reads
external files only, writes inside this new directory, verifies copied bytes,
checks all 92 entries of the four
per-attempt manifests, all recorded command-log and source hashes, both
supplemental audit-source hashes, report and registry bindings, exact successful
reuse, source review pins, and the excluded object pins. `CHECKS.json` records
every comparison; `SNAPSHOT_RESULT.json` records scope, observations and outcomes.

The program observed **0 moving/missing-file events**. It
compares complete root listings and rereads all scoped regular files at the end.
This bounded observation is not an atomic filesystem-snapshot guarantee.

`COPY_MANIFEST.json` lists every copied original artifact. Root `FILES.json`
lists every file in this delivery, including original nested manifests and this
program, except itself (self-hashing is not claimed). Each entry has bytes and
SHA256. The program checks the generated manifest and then freezes all files
read-only and all directories non-writable. Its final stdout supplies the root
manifest hash. Root may archive/publish these exact bytes. No earlier checkpoint
or `supplement-review-002` file was changed.

To reproduce preservation in a new authorized directory, copy the exact program
there and run `python snapshot_and_verify.py` while the named origins remain
available. It refuses to overwrite an existing corpus. To verify the frozen
delivery, recompute every entry of root `FILES.json`; no Lean runtime is needed.
