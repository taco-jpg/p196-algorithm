# Decimal p=12 m=9 centre, half-width 8

**COMPUTED.**  For the decimal exterior with overflow word `100010001000`, the reachable non-uniform lattice of spatial period 9 admits no centre window of lower-half width 8 that survives indefinitely.

The exact SAT window map gives maximum survival horizons 33, 36, and 32 for the three residue classes `n mod 3 = 0, 1, 2`, respectively; horizons 34, 37, and 33 are UNSAT.

Thus every possible periodic kink of this stated width is excluded, irrespective of its temporal period.  This is not an exclusion at any other width and does not settle base 10 or 196.

Reproduce with `cd calculation/decimal_frontier/lattice_kinks/code` and `python3 lifet.py ../data/lat_p12m9.txt 8 O 16` for `O=0,1,2` (Python `python-sat`/CaDiCaL).  The stored lattice is the period-9 SCC from `bauto3 10 12 12 -g 100010001000`.

Paths: `calculation/decimal_frontier/lattice_kinks/data/lat_p12m9.txt`; `calculation/decimal_frontier/lattice_kinks/code/sat_kink.py`; `calculation/decimal_frontier/lattice_kinks/code/lifet.py`.
