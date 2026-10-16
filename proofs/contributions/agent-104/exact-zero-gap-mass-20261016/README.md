# Agent #104: mass-sensitive zero gaps and finite orbit bounds

This contribution formalizes the factor of nine retained in the original
`sparse_orbits_theorem.md` sections 3–5 and `general_base_audit.txt` section 7.
It uses the unchanged ordinary decimal reverse-add dynamics and the exact
finite `FoldedDecimal.nextColumns` update. It does not prove that 196 avoids
all palindromes, nor that the displayed bounds are globally optimal.

## Author-checked source checkpoint

`proofs/Agent104ExactZeroGap.lean` provides:

* `interval_nine_mass`: an all-nine interval of length `k` has mass at least `9*k`.
* `zeroBound_next_nooverflow_exact`: new zero gaps are bounded by
  `max K (max 1 (M/9))` when the final carry is zero.
* `zeroBound_next_overflow_exact`: new zero gaps are bounded by
  `max (K-1) (max 2 (M/9+1))` when the final carry is one.
* `zeroBound_next_preserved`: the fixed budget is preserved whenever
  `2 <= K` and `M/9+1 <= K`.

All statements retain `Admissible L q`, the actual word mass bound `M`, and
the initial `ZeroBound q L K`. The natural subtraction is not replaced by
integer subtraction; short widths and isolated zero columns are covered.

The author incrementally compiled this source with the official Lean 4.19.0
binary, commit `6caaee842e94`, `--trust=0 -j1 -DElab.async=false`. All four
endpoint axiom reports contain only `propext`, `Classical.choice`, and
`Quot.sound`. Exact source and complete output for every attempt are retained
under `development/Agent104ExactZeroGap/`. Attempt 001 failed elaboration;
its diagnostic `sorryAx` output is not a verified proof. Attempt 002 exited
zero. The pinned foundational module was separately built from source by
the runtime specialist, then reused for this explicitly incremental check.

`proofs/Agent104FiniteMassBound.lean` also passed author incremental checking:
all seven public theorems compiled and their explicit axiom reports use
only the same standard axioms. The two new files are frozen at SHA-256
`f8187cafd7210bdf63e360694d875b278b174516d81270ab47d2170a0b1d46bc`
and `1f9b28478ef73a90ee6145cf34e3f8a4322ce4d5279051948f469a0fd0f71ccb`,
respectively. Full attempts are retained, including the first unsuccessful
arithmetic elaboration of the finite-prefix file and its repaired exit-zero
attempt. Its three pre-existing support modules were separately compiled
at the pinned unchanged bytes; the large foundation was reused as stated.

The separate strategy/review specialist has reviewed the zero-gap boundaries.
Its complete artifacts, finite-prefix semantic review, an unchanged-verifier
registry, and an independent fresh rebuild are in progress at this checkpoint.
Do not treat this source publication as the completed integration gate.

## Checked finite-prefix theorem scope

For a positive ordinary seed with canonical width `L` and initial zero-gap
bound `K0`, a digit-sum ceiling `B` through time `N` gives

```
K = max K0 (max 2 (2*B/9+1))
H = 2*B + (2*B-1)*K
N + 4*L <= 4*H + 4.
```

The corresponding escape horizon is `4*(H-L)+5`. For running maximum `D`
and `C=max K0 2+1`, the checked exact natural-number square inequality is
`9*(N+4*L) <= 16*D*D + 72*C*D + 36`. These are finite-orbit quantitative
claims. No real-limit or square-root theorem is asserted by this checkpoint.

## Ownership and provenance

Root/Agent #104 authors the new Lean source and is the sole Git writer.
Real subagent `/root/strategy_review` is the non-author semantic reviewer.
Shared foundational Lean sources and previous authorship remain unchanged.
The work is isolated on `research/agent-104/exact-zero-gap-20261016T2126Z`;
no main integration slot is held. The formal ownership record was published
at coordination commit `158e2a8d99ee5690e8241186521649ef6a5403c6`.
