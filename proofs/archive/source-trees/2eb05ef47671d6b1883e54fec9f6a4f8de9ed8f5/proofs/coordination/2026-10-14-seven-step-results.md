# Checked seven-step reset and collision-mass handoff — 14 October 2026

Integration parent: `e30848f6f4d40b360096f469b5c1c0dae175e4be`, branch
`main`. This checkpoint's containing commit is the result commit. All
previous research, trace parts and coordination checkpoints are preserved.
Decimal Lychrel existence and the assertion for 196 remain unproved.

We read and preserve the concurrent [active-seam safety note](2026-10-14-active-seam-safety.md)
at the integration parent. Its nonzero actual seam mask is a sufficient
one-output safety condition by the existing palindrome-predecessor
classification. It does not itself preserve that mask at later updates.
The announced 28-declaration module and aggregate seam archive are still
forthcoming in that stream and are not independently replayed by this
bundle. That criterion is compatible with the two separate preservation
obligations below.

## Concrete result for the concurrent language work

Start with the canonical whole pair word Q=(4,4,0) W (0,4,4), where W is
a nonempty padded symmetric middle with coefficients 0,...,18 and even
central coefficient when its width is odd. Zero middle endpoints are
allowed and must not be silently trimmed. Let c_t be the actual carry
entering the final three columns of G^t(Q), not a freely chosen control.

The first three coefficients return to (4,4,0) at time seven **if and
only if** the actual boundary-control word is `00*0*01`. Exactly four of
the 128 binary words qualify. The final-overflow schedule is `0010101`,
the middle incoming-carry schedule is `0000111`, and whole width gains
three. These actual-word and canonical-numeric return statements are now
covered by a fresh [29-declaration Lean audit](../contributions/2026-10-14-seven-step-formal/README.md).
Formal scope does not include the entire middle map or intermediate
palindrome safety; those remain separately proved in writing.

For the exact middle operator, let D be the retained normalization of W
with its actual incoming carry, m its represented width and gamma its
outgoing carry. At steps 0,1,3,5 the new middle is
`D(x)+x^(m-1)D(x^-1)`. At overflow steps 2,4,6 it is
`D(x)+x^m D(x^-1)+a(1+x^m)`, where a is respectively gamma,
5+gamma, and 0. Under the return guard, all seven positive successors are
safe exactly when both W_0 and W_1 contain a coefficient at least 10.
[The complete argument and finite catalog](../contributions/2026-10-14-seven-step-reset/SEVEN_STEP_RESET.md)
retain all cases and corrections for padded middles.

**The remaining language obligation is precise:** find a nonempty class
of padded middle words preserved by this seven-step operator, on which
both the five actual carry guards and the two safety tests remain true.
Repeated prefix return alone is insufficient. A word can satisfy two
safe returns and then immediately hit a palindrome: W_0=(1,1,18,1,1)
has first positive hit 15. The displayed three-return example loses the
step-five carry guard on its fourth attempt. These are checked
counterexamples to automatic induction, not exclusions of every possible
restricted invariant language.

The complete catalog covers 75,447 canonical starting middles of widths
one through seven. It contains 4,501 prefix returns and 23 cases with
three safe returns; all 23 fourth attempts fail the return guard. Those
are exact bounded results, not an all-width obstruction. Independent
review exhausts 4,190 padded middles and all 128 control words without
importing the gate implementation. Both compressed catalog files are
retained in full with decoded-byte provenance in the inventory.

## Additional proved and checked results

- **17 formal collision-mass declarations:** for complete normalized
  digit mass M_c(W), including the outgoing carry, and initial-nine
  length k(W), `M_c(W)+9*c*k(W)=M_0(W)+c`. For actual B H B boundary
  carries e,h, `M_0(BHB)+9*(e*k(H)+h*k(B))=2*M_0(B)+M_0(H)`.
  Empty, neutral and nonsymmetric bounded blocks are included. The
  actual-step theorem connects this to the ordinary integer digit sum.
  [Sources and audit](../contributions/2026-10-14-collision-mass/README.md)
  use ordinary logical axioms and have an independent 145,161-case
  finite control. A mass identity alone is not a recurrent invariant.
- **Fixed carry-clock classifications:** constant-zero, constant-one
  and alternating schedules are classified at prefix widths one through
  three. Each has a safe two-column cycle, so these schedules do not
  provide a general escape strategy. The independent audit covers 13,716
  prefix transitions and 27,432 phase states.
  [Exact scope and evidence](../contributions/2026-10-14-prefix-controls/FIXED_CLOCK_RESULTS.md)
  preserve the distinction between freely imposed clocks and the actual
  carry history of one integer. Prior-art notes are also retained.

## Reproduction from repository root

```sh
python3 proofs/contributions/2026-10-14-collision-mass/check.py /absolute/path/to/lean
python3 -B proofs/contributions/2026-10-14-collision-mass/finite_controls.py
python3 proofs/contributions/2026-10-14-seven-step-formal/check.py --lean /absolute/path/to/lean
python3 -B proofs/contributions/2026-10-14-seven-step-reset/seven_step_reset.py
python3 -B proofs/contributions/2026-10-14-seven-step-review/independent_reset.py
python3 -B proofs/contributions/2026-10-14-prefix-controls/independent_audit.py
python3 proofs/verify_release.py
```

Lean is pinned to 4.19.0. The 17 and 29 declaration counts are audit
metadata, not counts of independent discoveries. Complete compiler logs,
source identities, failed recurrence examples, branch certificates,
catalog outcomes and independent reviews are retained. The
[root audit](../contributions/2026-10-14-reset-root-review.json) records
the checked proof scope and replays. Existing published trace restoration
instructions remain unchanged.

## Active next obligation

Necessary spatial-extension graphs for an indefinitely repeating return
are under independent audit. A proposed first-zero branch obstruction
and a remaining three-branch graph on values {6,8,9} are active work,
not conclusions certified by this bundle. The generalized-overlap and
language contributor can use the explicit middle operator and both
preservation conditions above while those graphs are checked. Shared
repository evidence, not unobserved cross-chat communication, is the
coordination mechanism. No safe all-time finite seed is supplied here.
