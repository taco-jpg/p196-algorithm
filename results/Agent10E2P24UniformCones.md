# Agent10E2P24UniformCones
**COMPUTED.** Base 10, overflow word `000100010001000100010001` (p=24, `(0001)^6`):
none of the uniform absorbing-lattice SCC targets is reachable from the exact position-automaton start.
All ten raw temporal/phase targets are verified self-loops.
Exhaustive backward predecessor BFS: 1,714,808 unique raw states, depth 10, EXHAUSTED,
with none of the 64 legal first-column successors present (state cap 2,400,000).
The independent four-time-step rotation quotient agrees: 286,534 unique quotient
states, depth 10, EXHAUSTED, with no hit among 14 canonical first-column successors
(state cap 300,000); reverse/forward edge checks agree.
Reproduce with `c++ -std=c++17 -O3 calculation/decimal_frontier/lattice_formats/code/agent10_e2_p24.cpp -o /tmp/a10`:
`/tmp/a10 10 000100010001000100010001 2400000 backraw`;
`/tmp/a10 10 000100010001000100010001 300000 back`.
Controls (same engine): b9 `1100011000` period-4 SCC depth 61; b13 `1010010000`
fixed-point SCC depths 55 and 75 (caps 1,200,000 and 400,000 respectively).
Scope: ONLY uniform absorbing lattices; other p24 targets and all decimal Lychrel claims UNDECIDED.
