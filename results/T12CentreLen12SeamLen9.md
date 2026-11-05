# T12CentreLen12SeamLen9

**Claim (COMPUTED, plus one PAPER PROOF; 2026-11-04).** In the T12 route (Phi^120(P(14,100)) = P(14,105), phase 0, B34/W9, U3),
every witness needs |C| >= 13 and |J| >= 10.
- Centre: |C| = 7..12 excluded for all 30 U and every J (2,273,552,730 cases, 0 survivors; two-inlet cone of AC46). With AC46
  (|C| <= 6): every |C| <= 12 fails.
- Independence (PAPER PROOF): the centre cone (<= 122) and junction cone (<= 152) never meet inside the U band, so the return splits
  into a centre condition independent of J and a seam condition independent of C.
- Seam: |J| = 0, 1 by direct census (cross-checked against big-integer replay); |J| = 7, 8, 9 by an exact two-carry SAT encoding,
  30 U x 3 lengths = 90/90 UNSAT (cadical); J ++ U^m gives the same seam, so this covers every |J| <= 9. Positive and negative
  controls pass.
**Method.** `calculation/decimal_frontier/round11/t12_seam/FINAL.md`.
**Not claimed:** |C| >= 13 or |J| >= 10; the T12 return itself (UNDECIDED).
