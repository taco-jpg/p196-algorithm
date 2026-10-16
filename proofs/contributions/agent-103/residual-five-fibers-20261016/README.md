# Agent #103 — complete residual-five predecessor fibers

Tasks: `agent103-residual-five-fibers-20261016` and the separate continuing
`agent103-residual-five-residue-count-20261016`.

## Compiled source checkpoint

For every natural `r`, define `M_r = 33*10^(2*r+2)+22` and
`fiber r = Agent101.numericFiber (2 :: 12 :: List.replicate r 9) none`.
The original Agent #101 enumeration has been specialized without changing its
ordinary-decimal arithmetic or individual digit realization semantics.

`Agent103.ResidualFiveFibers.complete_predecessor_fiber` proves simultaneously:

- `(fiber r).Nodup`;
- `(fiber r).length = 14*10^r`;
- for every natural `n`, `n ∈ fiber r` iff `Lychrel196.step n = M_r`.

There is no source-width premise in this endpoint. It includes `r=0`, excludes
`n=0` by the original arithmetic, and counts ordinary integers, not abstract
coefficient words. Width elimination reuses the existing
`SevenColumnKernel.PalindromeBridge.no_overflow_of_target_leading_gt_one` and
original canonical uniqueness: `M_r` has leading digit three.

`occurrence_predecessor_mem` and `occurrence_predecessor_mod99` prove that an
occurrence `orbit 196 t = Agent119.EightFamilies.fam 5 r` forces
`orbit 196 (t-2) ∈ fiber r` and `orbit 196 (t-2) % 99 = 77`.
The time subtraction is justified by the already checked `100 < t` theorem.
This reduces a hypothetical predecessor to a complete finite list; it does not
exclude it or prove that 196 reaches a member.

Both new modules compile under Lean 4.19.0 with `--trust=0 -j1 -DElab.async=false`.
All explicit axiom prints use only the standard three allowed axioms. The root
conclusion has also passed a genuine non-author semantic review and independent
small-module rebuild by `scope_scan`. `runtime` is independently reviewing the
fiber source. Existing fifteen dependency modules have a complete 1,701-theorem
transitive audit. A full new-package clean build and portable registry are pending;
this checkpoint is not integrated or represented as the completed final gate.

The exact mod99-filtered cardinality remains WIP in a separate claimed task.
Finite diagnostic counts or a proposed recurrence do not establish its all-r
formula. The two completed modules do not assume such a formula.

## Dependency provenance

The four `vendor/Agent101*.lean` files are unchanged original modules from commit
`326645944168ad2b035a1e653b61527d79684156`. They were individually restored and
compiled successfully. The previously checked residual-five package at
`c5631c99a6d62d61ddf118ab8ff50a994eac722f` is in this branch's parent history.
Its verified `Lychrel196Research` import forwarder is shared with these modules:
the complete original foundation body is byte-identically contained in
`LychrelDigitSums`. The next registry checkpoint will record all source paths and
fixed SHA256 identities without duplicating arithmetic definitions.

Real failed development attempts, compiled sources, exact commands, and logs
are preserved under `attempts/` and `evidence/`. Compiled objects are omitted.
This branch does not change main or shared accepted-build indexes.
