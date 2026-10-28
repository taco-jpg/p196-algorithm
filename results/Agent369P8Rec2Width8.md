# Agent369P8Rec2Width8

**COMPUTED.** The decimal period-8, spatial-period-48 lattice (`rec2`) has no time-periodic centre with lower-half free-window width at most 8.

Scope: all four initial length residues `o = 0,1,2,3`; any temporal period. This is not an all-width result and says nothing about 196.

The exact horizon-SAT maximum survival lengths are respectively 28, 27, 27, and 37; UNSAT at 29, 28, 28, and 38 excludes every periodic centre in each class.

Reproduce (with `python-sat` / CaDiCaL):
`for o in 0 1 2 3; do python3 calculation/decimal_frontier/lattice_kinks/code/lifet.py calculation/decimal_frontier/lattice_kinks/data/lat2.txt 8 $o 16; done`

Data: `calculation/decimal_frontier/lattice_kinks/data/lat2.txt`, derived from `lattice_formats/p8_scc.txt`; solver: `code/sat_kink.py`.
