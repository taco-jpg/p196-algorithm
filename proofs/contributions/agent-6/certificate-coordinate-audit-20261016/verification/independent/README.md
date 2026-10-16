# Agent #6 independent certificate-coordinate review evidence

This package records a completed independent same-project review of the
source at remote commit `937c33ba3a98b9778bfee45a0bf2f0c0b3765055`.
The reviewer authored none of the three new theorem modules and changed no
theorem source or Git object.

## Main records

- `REVIEW_RESULT.json`: final source-bound verdict and exact receipt hashes.
- `FORMAL_REVIEW.md`: attributed review text prepared for parent publication.
- `baseline/source-manifest.json`: seventeen unchanged dependency snapshots.
- `baseline/build/compilation.json`: actual fresh baseline compilation commands.
- `baseline/audit/verification.json`: independent complete baseline origin and
  axiom audit, including all safe definitions.
- `final/source-manifest.json`: frozen twenty-source snapshot before publication.
- `final/build/compilation.json`: separate fresh twenty-module build.
- `final/audit/verification.json`: new-module and complete-closure audit.
- `final/SEMANTIC_REVIEW.md`: substantive statement, hypothesis, boundary,
  insufficiency, iterator, sum, and overflow review.
- `final/registry-source-comparison.json`: exact registry/source/endpoint mapping.
- `final/publication/binding-937c33ba.json`: append-only remote source binding.
- `historical-receipt-correction.json`: historical multiline-list correction.
- `baseline/module-origin-comparison.json`: two generated normalization equation
  names assigned to OuterBridge in the larger import environment.

Every source snapshot, actual command, compiler fingerprint, full log,
structured axiom record, private helper origin, anonymous-instance census,
and generated unsafe implementation record is retained. `COPY_MANIFEST.json`
in the ready-to-copy package lists the selected files, their bytes and hashes,
and the excluded compiled objects.

## Execution provenance

`compile_exact.py`, `audit_exact.py`, and `audit_final.py` are the exact runner
versions used. Baseline and final runs used the same independently verified
official Lean 4.19.0 runtime, with binary SHA256
`92c3d35b5bfaa5e0fea413a775d504cf46cd95e1345df61c2274f76779e7e023`.
The execution environment deliberately provided only the fresh project object
directory as `LEAN_PATH`. The commands used `--trust=0 -j1 -DElab.async=false`
through supported executor escalation. No shim or preload was used.

Compiled objects are excluded from this evidence copy. Their original paths,
sizes, and hashes remain in the compilation receipts. Replay requires the
pinned runtime and parser layout plus a fresh isolated snapshot directory;
the runners intentionally refuse an existing build/audit directory. Their
absolute recorded source paths describe the actual review workspace. The
parent's portable canonical source replay is a separate evidence stream.

The compilation receipts retain their stage status
`COMPILED_PENDING_INDEPENDENT_AXIOM_AUDIT`, and the initial source snapshot
retains publication-pending fields. Later audit and publication binding
receipts complete those stages without rewriting their historical records.
The final decision and current source identity are in `REVIEW_RESULT.json`.
