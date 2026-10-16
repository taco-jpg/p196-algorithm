# Exact periodic state safety — Agent #1

Status: **WIP package**. First boundary source compiles under official Lean4.19.0 with kernel reduction and literal axiom reports. The universal positive-repeat Bool/BadWord and maximal-strip equivalence proofs are in progress. The parent is sole Git writer; isolated claim `53448de233d15fdddcc992e4440961f4e3a80f55` owns only the exact periodic test and its strip invariance, with optional explicit finite boundary witnesses. This does not claim successor safety or repeated safe transitions.

The original universal arithmetic palindrome criterion is reused, not re-proved. `SOURCE_SCOPE.md` pins the existing statements and defines precise next-output semantics. Mathematical files not yet frozen or accepted are outside a new registry until their compilation completes. Author increments may reuse pinned reviewed prerequisite objects; fresh combined verification and independent review remain required.

The first closed witness has B=H=[], w=[10,10,10,10], k=3. Kernel reduction confirms normalized digits `0::replicate24 1`, exact raw blocks `[1,2,2,2]`, nine2s, `[2,2,2,2]`, actual carry1, and maximal quotient center `[2]` with strip counts0,1. It lies in unchanged ValidPeriodic. Its safety assertions will be added only after the exact Boolean definition compiles. No ordinary infinite orbit or P196 conclusion follows.
