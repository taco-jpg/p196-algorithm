# P8Rec1FixedCentreLen16

**Claim (COMPUTED, with PAPER PROOF reductions; 2026-11-04).** In the p8 lattice rec1 (m = 20, g = 10101010), the family
P(q,C) = B0 W0^q C rev(W0)^q rev(B0) has no fixed-centre exact return T^80(P(q,C)) = P(q+1,C) for any legal palindromic centre with
|C| <= 16 and any q >= 5. L13..16: 27,286,610,980 centres, every centre enumerated in exact integer arithmetic (no pruning), 0 returns,
max matched prefix 147 < 159. Together with P8FixedCentreLen12 this covers |C| = 4..16.
- Periods 160 / 240: shield thresholds q0 = 8 / 11 for rec0 and rec1 (PAPER PROOF reduction to q0, kernel 640/640); at the threshold
  rec1 |C| <= 14 (K = 2) and |C| <= 13 (K = 3), rec0 |C| <= 12, 0 returns. Below the threshold, direct exhaustion for |C| <= 10, 0 returns.
- Stack S(s) W20^r C ... of HYBRID §7b (PRO-R03-e): for s <= 16 and r >= r0 = 5 / 8 / 11 the stack returns iff rec1 P(r0, C) does
  (PAPER PROOF, finite kernel); small r for s = 1..3 exhausted, 0 returns.
**Method.** `calculation/decimal_frontier/round11/p8_stack_centres/FINAL.md` (cen2.cpp SIMD with scalar fallback; three independent cross-checks; big-integer replay
of the max-prefix centres over several periods: no palindrome, no return).
**Not claimed:** |C| >= 17; period >= 320; moving centres; stack s >= 17; rec0 at |C| = 15, 16.
