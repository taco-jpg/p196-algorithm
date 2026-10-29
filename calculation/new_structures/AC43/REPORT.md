# AC43 phase-10 carry-root correction

**Label: PAPER PROOF**, with a deterministic finite 130-step carry trace; not Lean-verified. No decimal Lychrel certificate or complete endpoint return.

The phase-10 p12/m9 lattice has zero-based W[10] = (0,9,11,1,10,8,5,9,16), whereas W[9] = (10,4,5,10,14,13,12,9,7). Mixing B[10] with W[9] produces a false coefficient-10 mismatch. A physical phase-10 state reached from phase 0 can also have different physical digits than a freshly greedy-realized B[10]/W[10] pairword.

**Universal carry-cap lemma:** For all q >= 14 and any legal inner junction, U and centre, starting from the canonical greedy phase-0 exterior B[0] ++ W[0]^q, the first 34 pair coefficients at physical steps 10 and 130 equal B[10]. Overflows over steps 10 through 129 are (001000100010)^10.

**Proof:** The outer 160 digits at each end are independent of the unknown centre. At each decimal addition, the low-cap carry starts at zero; the carry entering the high cap is one of precisely 0 or 1. Normalize both high cases and retain the common exterior prefix, requiring equal overflow. Induction makes these caps exact for every possible inner state. A 130-step finite arithmetic trace retains 152 positions per side at t=10 and 62 at t=130, enough to establish the 34-coefficient equality. It uses neither strict phasewise W9 pruning nor odd-centre mod-11 gates.

**Independent COMPUTED checks:** Ten true-Python-integer 130-step replays at q/k=(14,100),(20,80),(40,160),(80,320),(160,640), both C parities. A separate digit-array engine checked each cap over 130 steps for 24 randomized trials. All agree.

Run `python3 calculation/new_structures/AC43/phase10_outer_caps.py` and `python3 calculation/new_structures/AC43/verify_rooted_bigint.py` from the repository root.

**Scope:** This corrects a physical-root premise, not a 120-step seam return, not an exhaustive J6 census and not an infinite nonpalindrome proof. The all-time T* lemma still requires complete W9/J/U/C and physical carry closure plus a nonpalindrome guard. Earlier index-10 obstruction samples must be independently reconciled with zero-based row indexing before promotion.
