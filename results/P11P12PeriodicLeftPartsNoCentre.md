# P11P12PeriodicLeftPartsNoCentre

**Claim (COMPUTED + PAPER PROOF (reduction); 2026-11-11).** On the decimal clocks 00001110001 (d = 11) and (1000)^3 (d = 12) every
d-periodic rooted infinite closed history ends, above a finite height, in a 9-wire or in the lattice W0 = p12m9; hence no left part
of time period d (exterior with any band, lattice, anything) carries an eventually time-periodic centre, of any width and period.
- Interface graph IF(d) (r13c): d = 11: 1,612 interfaces, one non-trivial SCC (the all-9 loop); d = 12: 22,657 interfaces, four
  non-trivial SCCs (the 9-cycle of W0, three all-9 loops = time rotations of one wire). An infinite path ends in one of them.
- The per-tail closures are NeutralBandNoCapAllPeriods (wires) and EdgeRelaxW9NoCentre (W0), re-run here on the tails found
  (Cyc_acc(6) empty on every phase orbit, 0 exact orbits at K <= 5, depth 0 by plain addition). Only the completeness is new.
- By r13c Theorem B (L = 22, 33, 44 on p11; L = 24, 36 on clock 1000) the same holds for left parts of those time periods.
Checks: |IF(d)| equal r13c's two codes; closures by C++ mc14w (self-tested vs big-integer addition) and Python pyscc identical;
IF(8) cycles agree with the position automaton to length 128; all eight Lean neutral certificates found as positive controls.
By-product: no census band of spatial period <= 8 and time period dividing d has a rooted d-periodic left end (d = 8, 11, 12).
**Not claimed:** other clocks (clock 10 / task K1 stays open), other time periods, centres that are not eventually periodic; 196.
Code: `calculation/decimal_frontier/round14/tails_no_centre/` (PROOF.md, ifscc.py, mc14w.cpp, pyscc.py, logs/).
