# Agent 12: exact first-hit-four proof contract

A. Exact source: `proofs/research/main_existence_attempt/renewal_pass/tails/STATUS.md`, Statement table, cores (2,5), (2,6), (3,5), every integer spacer r>=1, at snapshot `74df59c5ecb6cb30fb3c88b1d5b26fdb9526d6c4`. Each canonical ordinary realization of the stated pair word has first positive palindrome time four.

B. Intended Lean proposition: `DecimalDelayBridge.FirstPositiveHit n 4`. It includes a palindrome at time four and nonpalindromicity at every positive time below four.

C. Definitions: unchanged `DelayedOverlapGate.initial r 1 u v`, width `2*r+7`, actual `Lychrel196.orbit`, and `DecimalDigits.Canonical`. In the source's concatenated word notation, exterior `11` means two adjacent coefficients 1, not one coefficient 11. Existing gate theorems already cover positive times one and two and the exact third-time criterion.

D. Hypotheses: `r>=1`; exactly one of the three literal core alternatives; canonical digits of n at the actual width; equality of their mirrored digit-pair sums to the source word. No desired first-hit conclusion, carry profile, no-overflow condition, low next-pair condition, or hypothetical arithmetic correspondence is assumed.

E. Quantifiers: every spacer and every canonical realization. `realized_first_hit_four` separately supplies a positive ordinary realization for every allowed parameter tuple, so the universal theorem is not vacuous.

F. Boundary cases: r=1 is proved in the same universal argument; there is no extrapolation from r>=2. Positive times are distinguished from initial time, whose palindrome status is unrestricted. Reversal uses ordinary natural-number leading-zero conventions; iteration continues after palindromes.

G. Exact coverage: the three first-hit timing claims only. The separate displayed decimal endpoint-string formulas and the (1,6), r>=5 first-hit-eleven claim remain separate obligations. No infinite-time, Lychrel or 196 result is asserted.

H. Dependencies: pinned Lean 4.19.0, Std only, exact imported source hashes in `accepted.json`. The newly proved `returned_carry` verifies its proposed carry word at every actual index via the existing normalization recurrence; `returned_no_overflow` follows from that certificate. `third_pairs_low` proves every next pair coefficient <=9, including the smallest spacer. `representation_next` supplies the already-proved actual arithmetic bridge.

I. Final identifiers: `P196.Agent12.FirstHitFour.numeric_first_hit_four` and `P196.Agent12.FirstHitFour.realized_first_hit_four`. Seven supporting exports are listed and audited; this count is not a claim count.

J. Verification: all dependencies were rebuilt unchanged; the new file compiled; every exported result passed a transitive axiom audit with only `propext`, `Classical.choice`, `Quot.sound`. The accepted verifier now includes this module in clean local and CI builds. Self-review is not independent semantic review. The first development attempt failed because partially simplified constant proposition conjunctions obstructed the tactic; the successful proof simplifies them before arithmetic case analysis. No mathematical premise or source claim was changed.

Task ownership was successfully published at `166027a127f35fd0ba44505a32c6cb7f7019e6df` after two rejected stale-head attempts; all concurrent records were preserved. Independent review and integration remain pending.
