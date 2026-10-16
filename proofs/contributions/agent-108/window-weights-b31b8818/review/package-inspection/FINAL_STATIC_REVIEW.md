# Independent review of the frozen package checker

**Result: STATIC_REVIEW_AND_PYTHON_CONTROLS_PASS.** This is a review of the package's construction and its Python verification controls. It is not a receipt for compiling the full 17-module Lean closure. The parent agent owns that separate fresh compilation.

Reviewer: Agent #108 runtime delegate, session `b31b8818`. The reviewer did not author `check.py`, `source-pins.json`, or `REPRODUCE.md`. The reviewer authored two mathematical dependencies, `Agent108WindowObstruction` and `Agent108WindowEmbedding`, and previously independently reviewed `Agent108WindowIncoming`. No frozen package file or mathematical source was edited during this review.

## Frozen inputs

| File | SHA256 |
| --- | --- |
| `check.py` | `f046586ae35fe9b0eb8fa3e3f43461cd6c8007243401b2e92d88c71ec6df6633` |
| `source-pins.json` | `8a7648eff9bb611e5605b2be83555bd7154971416f312be81cdf55505c8a7292` |
| `REPRODUCE.md` | `f1d1e29581fab92d356401cbc17ad3505600e9c327fe2afc417ce0fe2e6b625c` |

The exact three inputs, generated audit source, input-check logs, and measured review result are preserved in `final-static-01/`. All three package files were rechecked after the controls and remained unchanged.

## Construction reviewed

The checker fixes the exact 17-module set, their dependency order, and the root `Agent108WindowIncoming`. The JSON pins identify all seven original retained repository paths and all ten frozen new sources. Byte length, SHA256, Git blob identity, direct imports, and root closure are verified before project compilation. Source resolution rejects absolute paths and `..` traversal and requires the resolved file to remain inside the supplied repository root.

The new evidence root must not already exist. Its project build directory is explicitly checked to be empty. Project sources are copied without byte changes to their original bare module filenames; no project `.olean` is copied into the build. Every project compilation and the generated auditor receive `--trust=0 -j1 -DElab.async=false`. The effective `LEAN_PATH` is replaced with that fresh build and explicitly admitted Mathlib/package library paths; `LEAN_SRC_PATH` is removed. Every source import external to the 17 project modules is checked for an available object at those admitted library locations or the supplied Lean sysroot.

All eight Mathlib dependency source revisions are checked even when an unused dependency has no cached library directory. This correctly accommodates the observed absence of the unused Cli library after selective cache retrieval. The package explicitly discloses that external Mathlib/toolchain objects are prerequisites, records their admitted cache paths, and does not represent their source-to-object derivation as independently rebuilt.

The generated Lean auditor selects constants by exact defining module origin. It records declaration kind, unsafe status, and partial status for every selected origin. Every safe, nonpartial origin receives a literal `#print axioms`; private declarations and safe generated helpers are included. Unsafe/partial compiler metadata is retained separately. No compiler implementation axiom is added to the logical allowlist, which remains exactly `propext`, `Classical.choice`, and `Quot.sound`.

The parser requires every requested module to occur, unique origin names, valid metadata, balanced audit markers, one report per safe origin, equality of the printed and marked declaration names, and exact equality between the safe-origin set and the report set. Its source-name correspondence check includes all 448 original and 130 new explicit declarations. This supplementary source scanner does not determine the logical audit's full coverage.

Each subprocess retains literal stdout/stderr, the command, duration, and return code. A failed subprocess, parser requirement, source check, or unexpected logical axiom prevents a successful full-run result. Successful input-only checks are explicitly marked `INPUTS_VERIFIED_ONLY` with compilation and axiom-audit flags false. Full-run success is set only after compilation, audit parsing, unchanged project source checks, Mathlib manifest rechecking, and unchanged package-file checks.

## Measured controls

The independent control command completed with exit code **0**. It read the actual repository files and verified 17 pinned sources and 578 explicit source declarations. Its real invocation of `--check-inputs` also exited **0**, accurately reporting that no proof compilation or axiom audit had occurred.

To test the parser with actual Lean output, the controls reused the immutable preceding ten-module audit log, SHA256 `3c9c411ed0c387cd7d006f151f53ba45e977e4858887a07615ae18004a1d9861`. The unchanged log parsed as 363 origins, 269 safe/nonpartial declarations, and 130 explicit source correspondences. It was not substituted for a new 17-module audit.

Five focused negative controls were rejected:

| Changed input | Observed rejection |
| --- | --- |
| A printed declaration name differs from its unchanged actual-origin marker | `CheckFailure`: printed declaration does not match marker |
| One safe declaration's complete axiom-report block is missing | `CheckFailure`: safe-origin and report sets differ |
| A reported allowed axiom is changed to `sorryAx` | Parser returns `pass=false`; the full checker requires `audit["pass"]` before success |
| One byte of a pinned project source is changed without changing its length | `CheckFailure`: source SHA256 mismatch |
| A source path traverses outside the repository with `..` | `CheckFailure`: path is not repository-relative |

The control script and mutation recipes are retained in `review_checker.py`; the measured mutated-log hashes and error messages are in `final-static-01/review-result.json`. The controls ran no Lean process and performed no Git operation.

## Earlier findings and their disposition

The initial checker draft incorrectly required a compiled library for every dependency, including unused Cli. It also accepted a corrupted printed declaration name because it compared only BEGIN/END markers. Both findings were sent to the author and corrected before freezing.

`initial-review-observation.json` preserves the first observed failure and explicitly states that its complete pre-edit checker bytes were not captured before the author applied the correction. `draft-01/` contains the actual subsequent checkpoint and demonstrates rejection of the name-mismatch negative control. No reconstructed file is labelled as an original pre-edit snapshot.

No outstanding packaging blocker was found in the frozen candidate. Acceptance of the mathematical package still requires the separate parent-owned complete 17-source `--trust=0` build and its generated full module-origin audit.
