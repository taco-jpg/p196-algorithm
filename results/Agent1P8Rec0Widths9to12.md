# Agent1P8Rec0Widths9to12

**COMPUTED.** For decimal `g=10101010`, p=8, the reachable `rec0`
spatial-period-20 lattice has no indefinitely surviving centre with
lower-half free-window width 9, 10, 11 or 12, in any `n0=400+o` class (`o=0..3`).
The exact horizon-SAT instances were UNSAT, without state caps, at (`o=0..3`):
- w=9: (37,39,33,43); the corresponding H-1 horizons were SAT.
- w=10: (41,43,41,48).
- w=11: (56,48,46,53).
- w=12: (64,55,60,60). These H for w>=10 are sufficient, not minimal.
A periodic centre would survive all horizons, so all temporal periods are excluded.
Reproduce: using the published `agent303_w8_exclusion.py` `write_lat0`
function, generate `/tmp/lat0.txt`, then for each triple above run
`python3 calculation/decimal_frontier/lattice_kinks/code/sat_kink.py /tmp/lat0.txt W O hor H` (python-sat/CaDiCaL).
Not claimed: width >=13, other lattices, any decimal Lychrel certificate or 196.
