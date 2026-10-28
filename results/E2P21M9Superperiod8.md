# E2P21M9Superperiod8

**COMPUTED.** Complete exact base-10 absorbing-lattice bulk row-map census for overflow word `g=001001010101001010101` (p=21), primitive reflective spatial period `m=9`, and minimal temporal return periods `21k` for every `1 <= k <= 8`.

Every one of the nine reflection axes and `19^5=2,476,099` palindromic length-9 coefficient rows per axis was tested: **22,284,891** axis-labelled initial rows, no state cap. Exactly 630 returned after at most 8 blocks; **378** have primitive spatial period 9.

Primitive exact temporal periods: `k=2: 90` rows, `k=4: 216`, `k=8: 72`; `k=1,3,5,6,7: 0`. Grouping by spatial rotations and whole-21-step temporal phase gives **12 families**: 5 at temporal period 42, 6 at 84, and 1 at 168.

The native row update passed 200,000 deterministic comparisons against an independent cyclic-carry fixed-point implementation, and every primitive returning row was independently replayed through its entire 42/84/168-step period with the moving reflection axis checked on every step. Base-9 and base-13 position-automaton controls (m=4/depth61; singleton depths55,75) had been reproduced before the census.

Reproduce: compile `calculation/decimal_frontier/lattice_formats/code/census_p21_m9_superperiod8.cpp` with `g++ -O3 -std=c++17`; run the executable with `--selftest`, then `STATE_FILE CANDIDATES_FILE`. Count families with `python3 calculation/decimal_frontier/lattice_formats/code/cluster_p21_m9_superperiod8.py CANDIDATES_FILE`. State/data files stay local, not in the repository.

**Not claimed:** a reachable periodic exterior, real integer reverse-and-add replay, any bounded centre, a decimal Lychrel number, or absence of cycles with minimal temporal period `k>8`. Those remain **UNDECIDED**.
