# Agent303P8WidthEight

**COMPUTED.**  For the decimal period-8 exterior lattice `rec0` (the first
`m=20` SCC for `g=10101010`), no free centre window of half-width at most 8
survives indefinitely in any compatible parity class.

The exact finite window map is UNSAT at horizons `(o,H) = (0,33), (1,35),
(2,30), (3,39)`.  A periodic kink would survive every horizon, so this
excludes every period for these widths.  This is a finite-width exclusion only;
it does not rule out wider centres, the shifted `rec1`, `rec2`, or p=12.

Reproduce: `python3 calculation/decimal_frontier/lattice_kinks/code/agent303_w8_exclusion.py`
(requires `python-sat`/CaDiCaL).  Code uses the existing independently tested
window encoding in `calculation/decimal_frontier/lattice_kinks/code/sat_kink.py`.
q∆∫i◊]◊^ÌÓ\Âæ;Û^tÂΩõuÕ€ﬂçˆy›⁄