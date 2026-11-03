# P8FixedCentreLen12

**Claim (COMPUTED + PAPER PROOF reduction, 2026-11-02).** On the p = 8 lattices rec0 and rec1 (`lattice_formats/p8_scc.txt`, m = 20),
no legal palindromic centre C with 4 <= |C| <= 12 gives an exact 80-step return T^80(P(q,C)) = P(q+1,C), P(q,C) = B0 W0^q C rev(W0)^q
rev(B0), for any q >= 5.
- Reduction (#476 SWARM R03A1 for rec0; rechecked for rec1): the 80-step insertion is one literal 20-coefficient W block after the
  39-site cap (formal-centre kernel 640/640), the two-inlet shield holds for q >= 5 (q = 4 fails at t = 74 for rec1, t = 78 for rec0),
  so the return holds for all q >= 5 iff it holds at q = 5.
- Exhaustion at q = 5, exact C++ arithmetic: 75,795,921 centres per lattice (lengths 4..12), 0 returns, 0 clock deviations; maximum
  matching prefix 144 of 159. rec0 lengths 4..10 reproduce R03A1's counts and maximum prefixes exactly.
- Checks: 12,022 centres against `klib.pairword_step`, 0 mismatches; literal big-integer replays of the closest centres.
**Consequence.** The PRO-R03-e stacked exterior (rec2 over rec1, see HYBRID.md section 7b) needs a rec1-bulk centre; none of length
<= 12 exists in this fixed-centre, period-80 family. **Not claimed:** |C| >= 13, other return periods, moving centres, the stacked
exterior at small q. Files: `calculation/decimal_frontier/lattice_kinks/p8_centre_exhaust/`.
