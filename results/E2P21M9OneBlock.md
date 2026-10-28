# E2P21M9OneBlock

**COMPUTED.** For base 10, overflow word `001001010101001010101` (21 steps; nine overflows), there is no primitive self-mirror absorbing lattice of spatial period `m=9` whose temporal row schedule returns after exactly one 21-step overflow block.

Scope: all nine spatial reflection axes; every palindromic 9-cell initial coefficient row over `0..18`; exact cyclic ascending/descending carry row map `Phi_g`. No state caps or extrapolation.

Enumeration: 19^5 = 2,476,099 rows per axis, 22,284,891 axis-labelled rows in all; each was evolved for 21 exact steps. Exactly 18 axis-labelled rows return: uniform `0^9` and `18^9` at each of the nine axes. **Zero** returning rows have primitive spatial period 9.

The native engine's exact cyclic-carry update passed **200,000** deterministic comparisons against an independent carry fixed-point solver. The mandatory exact position-automaton controls were reproduced separately: base 9 `g=1100011000` has a period-4 lattice at depth 61; base 13 `g=1010010000` has singleton SCCs at depths 55 and 75.

Reproduce: `g++ -O3 -std=c++17 calculation/decimal_frontier/lattice_formats/code/census_p21_m9_oneblock.cpp -o /tmp/p21_m9 && /tmp/p21_m9 --selftest && /tmp/p21_m9 /tmp/p21_m9.state /tmp/p21_m9.candidates`. The scanner checkpoints every 100,000 seed rows, uses one process, and resumes from its local state file.

**Not claimed:** all temporal periods (42/168-step bulk superperiods already exist for spatial period 3), root reachability, non-self-mirror lattices, centres, any decimal certificate, or any Lychrel theorem. Longer temporal periods at `m=9` remain **UNDECIDED**.
