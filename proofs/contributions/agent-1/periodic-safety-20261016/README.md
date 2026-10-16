# Exact periodic state safety — Agent #1

Status: **LEAN-CHECKED full source; fresh combined review pending**. First boundary source compiles under official Lean4.19.0 with kernel reduction and literal axiom reports. The universal positive-repeat Bool/BadWord and maximal-strip equivalence proofs are in progress. The parent is sole Git writer; isolated claim `53448de233d15fdddcc992e4440961f4e3a80f55` owns only the exact periodic test and its strip invariance, with optional explicit finite boundary witnesses. This does not claim successor safety or repeated safe transitions.

The original universal arithmetic palindrome criterion is reused, not re-proved. `SOURCE_SCOPE.md` pins the existing statements and defines precise next-output semantics. Mathematical files not yet frozen or accepted are outside a new registry until their compilation completes. Author increments may reuse pinned reviewed prerequisite objects; fresh combined verification and independent review remain required.

The first closed witness has B=H=[], w=[10,10,10,10], k=3. Kernel reduction confirms normalized digits `0::replicate24 1`, exact raw blocks `[1,2,2,2]`, nine2s, `[2,2,2,2]`, actual carry1, and maximal quotient center `[2]` with strip counts0,1. It lies in unchanged ValidPeriodic. Its safety assertions will be added only after the exact Boolean definition compiles. No ordinary infinite orbit or P196 conclusion follows.


All four new modules now compile. The literal Boolean is equivalent to original BadWord complement at every k>0 with nonempty period, and maximal stripping preserves it. The Numeric endpoint applies the unchanged original arithmetic criterion to every Canonical/hrep realization. No generic arithmetic bridge is re-proved. The Boundary root now kernel-checks safety=true of the valid tens input and safety=false of its exact quotient; it also shows that dropping the positive-exponent premise fails. These are finite counterexamples to two overstrong extensions, not infinite-time obstructions. Exact source pins and all21 modules are in `proofs/Agent1PeriodicSafety.registry.json`.

Historical first checkpoint text above records what was complete then; its pending-safety statements are superseded by this paragraph and the new frozen source. Final acceptance still requires the separately running clean reviews.
