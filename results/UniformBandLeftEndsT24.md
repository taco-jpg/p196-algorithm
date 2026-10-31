# UniformBandLeftEndsT24

**Claim (COMPUTED).** For every binary overflow clock and every left-end period T <= 24 (1,465,899 (T, clock) pairs, one
clock per rotation class), except (T=24, clock 0001) and (T=24, clock 01), no periodic decimal left end of ANY height can
carry a uniform absorbing band ({0}, {18}, {6,12} or the 6-cycle 2,4,8,16,14,10, any phase). So "left end + uniform band
+ mirror" -- the format of the base-4 (Seal) and base-13 certificates -- has no decimal instance in this range.
This decides 10 of the 12 tasks capped in `calculation/decimal_frontier/lattice_formats/FORMATS.md` section 6, including
"(10)^8" (clock 01, T=16: 257,093,986 shift-orbits, frontier empty at height 592). The only 9-wire streams are those of
the census (p11 at T=11, 22; p12 at T=12).
**Method.** Exact BFS over left-end interfaces (frontier empty = all heights checked), optional quotient by the clock
shift; validated by recovering the base-4 and base-13 certificates (big-integer replay) and the p11/p12 census streams.
**Not claimed:** the two T=24 tasks above (stopped at 137M / 118M orbits); periods > 24; non-uniform bands or centres.
**Code/data:** `calculation/decimal_frontier/uniform_bands/` (README, `calib.sh`, `sweep.py`, `data/`).
Details: `reports/UniformBandLeftEndsT24.md`.
