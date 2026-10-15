# Agent #105: actual high-region return bridge

Status: **INDEPENDENTLY-REVIEWED**; not yet integrated into the shared default build.
Task `agent105-actual-high-return` was published in coordination commit
`ee1469781ab386dbd5fd77b700d8a1b33140d5b2`.

This completes the actual-orbit bridge to the existing `HighReturnRank`
certificate. A high canonical pair word has every coefficient in `9..18`
and exterior at least ten. For every positive ordinary integer `n`, every
starting time `start`, and every `R`, if its actual orbit is high at each
`start + 2*j` with `j <= R`, then `R <= 3`.

The endpoint is
`Agent105.ActualHighReturn.numeric_high_returns_after_le_three`.
The zero-start endpoint is `numeric_high_returns_le_three`. Both use the
repository's actual canonical decimal representation and `Lychrel196.orbit`.
No assumed abstract edge, no-overflow premise, or unsupplied finite
certificate remains. Widths one and two and overlapping positions are covered.

## Proof sources and verification

The five new sources (`NeutralExterior`, `HighReturnPrefix`, `SmallWidth`,
`NumericHigh`, `ActualHighReturn`) are pinned by the source hashes in
`verification/initial/source-publication.json` to source commit
`167eed51bc2ae014450626b9e5c0d3302a5ae5c4`.
The previously proved `HighCarryReduction` and `HighReturnRank` are reused.

The author checker rebuilt all eight source modules from an empty directory
and audited all 343 explicit public theorem/lemma declarations. Every compiler
command exited zero, all source hashes remained unchanged, and the only
reported foundational axioms were `propext`, `Classical.choice`, and
`Quot.sound`. No `sorryAx`, custom axiom, `Lean.ofReduceBool`, or
compiler-trusted evaluation shortcut occurs in the audited dependency chain.
Lean is the official 4.19.0 release, commit `6caaee842e94`.

A separate specialist reviewed the statements and actual-width interpretation
(`review/StatementReview.md`). Another specialist independently rebuilt all
eight sources and audited the 34 new declarations plus five reused rank
lemmas (`review/independent_build/report.json`). Its initial audit-parser
failure and rejected second build are retained; the successful review adopts
only the first empty-directory build after verifying its source and object
hashes. See `review/independent_build/REVIEW.md` for that distinction.
Finite Python controls are supplementary evidence, not mathematical proofs.

From the repository root, with a normal Lean installation:

```sh
python3 proofs/contributions/agent-105/actual-high-return/check.py /path/to/lean-4.19.0/bin/lean --output-dir /tmp/agent105-review-new
```

Use a new output directory for each run. This environment additionally needed
the documented process-path startup shim in `runtime/`; compiler and Lean
libraries were unchanged. The checker, full compiler/axiom logs, failed
attempts, runtime provenance, and exact finite controls are retained.

This theorem does not prove P196, an infinite palindrome-avoiding orbit,
or that an orbit cannot reenter the high region after leaving it. Agent #1's
separate safe sharpness family is reused only as related research, not claimed
or duplicated here.
