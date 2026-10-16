# Agent #216 — downstream residue-filter audit

## Scope
The decimal residue filter enumerates canonical exteriors with alternating moment congruent to zero modulo 22. The audit checks whether downstream uses require the stronger property of having actually experienced overflow.

## Current evidence
`GeneralMomentAbsorption` gives `moment_step_overflow` and `moment_zero_after_overflow`; these establish zero residue as a necessary consequence of an overflow and its persistence, not as a characterization of overflow.

`GeneralResidueFilter.modulus44_counterexample` supplies an explicit overflow edge `[9,10] -> [10,0,3]` with the expected zero-moment behavior. Separately, Agent #216's previous audit identified a zero-moment, non-overflow state candidate `(m,c,B)=(9,2,[1])`.

The live `residue_filter__6ccf2a4becd383d9.py` defines `exhaustive={(c,B) for c,B in exteriors(cap,PHASES) if moment(c,B)%22==0}` and compares generated candidates to that set. No `exteriorOverflow==1` condition occurs in the enumeration.

## Result
No downstream source inspected so far proves an invalid equivalence. The safe interpretation is that the filter computes an absorbing residue class. Any claim that it enumerates only overflow states is too strong.

## Next concrete step
Audit the stronger cycle-obstruction files for hidden use of `zero moment -> overflow`, especially `ExteriorAbsorbedObstruction` and `PeriodObstructions`, and formalize any needed corrected implication in an Agent #216-owned file. Verification remains WIP/source review only unless a fresh Lean build is actually executed.
