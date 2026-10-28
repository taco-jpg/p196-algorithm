# Agent11E2P16Alternating

**COMPUTED.** For base 10 and cyclic overflow `g=(01)^8` (equivalently `(10)^8`),
the exact neutral-band exterior position automaton exhausts all reachable cut
states with **no accepting state**, for **every exterior width** and carry stream.
The 8-fold cyclic-time quotient has 257,093,987 reachable states, empties at
BFS depth 592 (all widths <=591 fully scanned), and has 0 accepted streams.
This is a complete negative decision for this fixed neutral exterior only:
no claim about absorbing lattices, other overflow words, centres, or decimal Lychrel existence.
The identical engine's 40M boundary agrees with the prior 40,003,127-state census;
independent SCC controls: b13 `1010010000` has depths 55/75, b9 `1100011000`
has two period-4 SCCs at depth 61. Two-tier exact hash keys; no probabilistic filtering.
Reproduce (C++17, <4 GiB RAM, checkpointable, nice):
`bash calculation/decimal_frontier/lattice_formats/code/agent11_p16_reproduce.sh /tmp/p196-a11-p16`.
