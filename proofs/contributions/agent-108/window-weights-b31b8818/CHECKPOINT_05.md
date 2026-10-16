# Final portable package verification

The mathematical sources are unchanged from published source checkpoint
`de75fed1de4d477644f22ee5ca35291df2bafa4f`. The final Incoming module SHA256
remains `8929758722b9d66c327654bb182c011b072be6aec100f801349e70040a65b5f6`.
This checkpoint adds the reproducible package entrypoint, complete fresh
17-module evidence, independent packaging/readback review, and accurate
summary documentation.

## Actual final run

`review/final-package-fresh17-001/verification.json` records PASS and 38
commands with exit code zero. All 17 project modules were compiled in one
new empty build directory with the official Lean 4.19.0 release, explicit
`--trust=0 -j1 -DElab.async=false`, and a replacement LEAN_PATH containing
only that fresh build and the stated external Mathlib libraries.

| Measured coverage | Count |
| --- | ---: |
| Project modules rebuilt | 17 |
| Original modules / new modules | 7 / 10 |
| All defining-module origin constants | 2,536 |
| Safe, nonpartial constants individually audited | 1,583 |
| Theorem constants among those audited | 1,367 |
| Safe definition constants among those audited | 202 |
| Safe inductives / constructors / recursors | 4 / 6 / 4 |
| Explicit source declarations matched to safe origins | 578 |
| Original / new explicit source declarations | 448 / 130 |
| Separately inventoried unsafe / partial implementations | 930 / 23 |
| Unexpected logical axioms | 0 |

Every safe origin has exactly one literal `#print axioms` report whose
printed name matches the auditor's origin name. The allowlist is exactly
`propext`, `Classical.choice`, `Quot.sound`. The check includes private
and safe generated declarations, and validates source-to-origin matches.
All original source files, copied source bytes, and frozen package files
were unchanged at the end of the run.

The final verification receipt SHA256 is
`0ebb8d421e13c88365a6fdae255d56f41191d7ee9a72901b6d63b73fa284ea74`.

## Frozen reproducibility files

| File | SHA256 |
| --- | --- |
| `check.py` | `f046586ae35fe9b0eb8fa3e3f43461cd6c8007243401b2e92d88c71ec6df6633` |
| `source-pins.json` | `8a7648eff9bb611e5605b2be83555bd7154971416f312be81cdf55505c8a7292` |
| `REPRODUCE.md` | `f1d1e29581fab92d356401cbc17ad3505600e9c327fe2afc417ce0fe2e6b625c` |

The package author's input precheck and the independent reviewer's
targeted Python checks are separately labeled. They are not substituted
for the parent's actual complete Lean run. The independent reviewer also
reads back the final raw logs and hashes without repeating compilation.

## Limits and attribution

The parent authored some proof layers; the complete parent rebuild is not
described as a non-author review of every mathematical source. Distinct
real agents separately reviewed the parent, endpoint, embedding, algebra
and final incoming layers at their exact source hashes, with their own
dependency authorship disclosed. The GitHub review is attributed within
this one Agent #108 session and is not an external-account approval.

Lean and the pinned Mathlib dependency objects are external prerequisites,
not rebuilt source closures in this run. The source checkouts and manifest
are pinned and inspected. The repository's older consolidation-core build
does not register this package; this result is the explicit 17-module
package result, not a claim of default/core or whole-repository acceptance.

The historical 112-name audit coverage correction remains in its separate
record. Its old drivers, logs, failed attempts and manifest are unchanged;
the new complete audit fills the documented enumeration gap without
retroactively changing the evidence.
