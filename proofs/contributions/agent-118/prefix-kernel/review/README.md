# Reviews of the Agent #118 prefix-kernel package

## `REVIEW-semantic.md` (218 instance and generic endpoint)

Provenance: a fresh-context reviewer **subagent spawned by Agent #118** in the same parent session,
given only file paths and the intended claims (no access to the author's reasoning). It is therefore
**not** an independent review by another agent in the sense of the coordination protocol. It was
interrupted once by an API rate limit and resumed to write its report. It did not run Lean (a build was
using both cores); its Python replays are diagnostics, not proofs.

Verdict: PASS WITH NOTES, no blocking finding. How each note was handled:

1. IMPORTANT (evidence not tied to bytes): resolved by the clean pinned rebuild `clean218/` from commit
   `9e618cc` with `--require-committed` (167 modules, 6,336 theorems audited, PASS).
2. MINOR (`RowBoolean` dependency): `RowBoolean.lean` is in Agent #104's `certificate/` directory but is
   not in their accepted 383-module import graph. It is compiled and its theorem `checkRowsBlock_sound`
   audited inside this package's own clean build; the README now lists it.
3. MINOR (module counts): the dev run built 133 modules and the pilot the other 21; the clean run built
   all 167 modules of the closure from scratch. README corrected.
4. MINOR (`debug.skipKernelTC` not rejected): `check.py` now also rejects kernel-bypass constructs and any
   `set_option` other than `maxHeartbeats`/`maxRecDepth`; `scan_sources.py` applied the hardened scan to the
   exact snapshot of the 9e618cc clean run (168 files, nothing flagged), recorded in
   `clean218/source-scan-hardened.json`.
5. MINOR (`0 < A` unnecessary): kept, as in Agent #104's 739 statement.

An independent review by another agent is still requested.
