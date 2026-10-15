# No-overflow births audit

Accepted module: `../../NoOverflowBirths.lean`.
Namespace: `Agent106.NoOverflowBirths`.
Dependency: unmodified `LychrelDigitSums` (Lean 4.19.0, Std only).

## Proof status

All 13 exported theorems compiled together successfully on the first full-module attempt.
`ModuleAttempt01.log` records the complete `#print axioms` output. Every theorem
uses only a subset of `propext`, `Classical.choice`, and `Quot.sound`.
There are no `sorry`, `admit`, `native_decide`, or new axioms.
`LocalAttempt01.lean` and its log record the earlier standalone arithmetic check.
`ModuleAttempt01.lean` is the exact source snapshot of the first full check.
There were no failed Lean source attempts in this module.

## Semantic bridge

The word-level classification theorems assume the existing `Admissible L q`,
`i < L`, and the actual final carry `DecimalDigits.carry q L = 0`. They rewrite
`FoldedDecimal.nextColumns` via the existing `folded_emission_no_overflow`
theorem. The incoming carries are exactly

- `carry q i`, the incoming low-direction carry;
- `carry q (L - 1 - i)`, the incoming reflected carry, or beta_(i+1).

Their bounds by one are proved using `carry_bounded` and the bound field of
`Admissible`; no guessed carry assignment or target emission is assumed.
The local arithmetic equivalences retain the old coefficient bound by 18.

The accepted module supplies both carry-sum and individual-bit versions of
both section-4 equivalences. `fresh_eighteen_iff` and `fresh_zero_iff` remove
the unchanged old-target cases. The full old-9 emission classification
proves the low-low/mixed/high-high outcomes 18/9/0 respectively.
The old-8/18 and old-0/10 exact emission formulas are also exported.
At a self-reflected center the old-9 birth option is excluded by the actual
center parity field of `Admissible`, yielding the last two center theorems.

## Scope boundary

These are local, all-width equivalences on the actual folded transition.
No restriction to orbit samples or a finite word length is used.
They make no maximal-run ancestry, lifetime, no-merging, or infinite-safe-orbit
claim. Those questions are separate from the birth classification.
The parametric example in section 4 is not part of this module.
No remaining proof obligation exists for the two requested equivalences.

## Reproduction

From the contribution repository root, with the independently compiled
unmodified base module in `/workspace/scratch/50e90e07524e/build106`:

```sh
LD_PRELOAD=/workspace/scratch/50e90e07524e/runtime/readlink_self.so \
LEAN_PATH=/workspace/scratch/50e90e07524e/build106 \
/workspace/scratch/50e90e07524e/runtime/lean-4.19.0-linux/bin/lean \
  proofs/contributions/agent-106/run-births/NoOverflowBirths.lean
```
