# Adversarial review by an Agent #103 subagent (not a cross-agent review)

A separate-context subagent of Agent #103 reviewed this package at `4ad4878`. It reused
the prebuilt objects and did **not** perform a full fresh rebuild. This record does not
count as INDEPENDENTLY-REVIEWED in the cross-agent sense.

## Verdict

No BLOCKER and no MAJOR issue was found.

## What the subagent checked

**Statement fidelity**
- `pairAt` indexes the outside coefficients, checked against Python reverse-and-add on
  several seeds over 29 steps.
- `warmup L = max(0, ceil((14-L)/3))` holds for all `L`; checked numerically up to 200.
- `Admissible` is no stronger than "canonical pair word of a positive integer".
- The hypotheses are satisfiable: the integer 13 gives R=2, and 103943 gives R=3.

**Proof chain**
- `two_column_step` is proved for every width `L >= 2`.
- `reaches` encodes return to (4,4), and the checker soundness lemmas are proved by
  induction.
- The 15-state set equals `BJobData0`/job 16 in the same order.
- The application of `finite_root_bound` (width 2, bound 636) is correct.

**Generators and drivers**
- Re-running `gen_broader.py` reproduces all 34 generated files byte-identically.
- No row check was dropped relative to the original generators.
- The `verify_*` diffs are as documented.
- The split audit still requires the exact set of declared theorems.
- Of the 6,249 environment theorems outside the base file, the 738 not audited are all
  compiler-generated (equation lemmas, projections, `_proof_N`, etc.).

## Minor items and notes (no proof impact)

- **MINOR:** `BroaderRoot.lift_edge_iff` proves only the forward implication, despite
  its name. Only that direction is used.
- **NOTE:** the driver's theorem-name regex `^theorem\s+(\w+)` skips `private`,
  `lemma`, primed and attributed forms. Today this skips only the private
  `PrefixExtension.width_ge_initial`, which is covered transitively.
- **NOTE:** the docstring of `stage2/verify_stage2.py` says it is "verify_broader.py
  plus". It was actually assembled from `verify_v2.py` together with the stage-1
  additions.

The sources are left unchanged so that the pinned build evidence stays valid. These
items are recorded here instead.
