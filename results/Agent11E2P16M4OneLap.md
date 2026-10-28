# Agent11E2P16M4OneLap

**COMPUTED.** Base 10, `g=(01)^8` (period 16, overflow count 8), spatial period
exactly `m=4`: among self-mirror non-neutral absorbing cyclic row patterns
returning after **one 16-step temporal period**, none is reachable from the
canonical position-automaton start state, at any exterior width.
Exact enumeration over all 4 reflection axes gives 48 primitive-spatial
period-4 row cycles (distinct indexed starting rows), compressing to 8
canonical accepting cut targets; 3,072 independent column-transition checks pass.
The complete 8-fold cyclic-time quotient BFS visits 257,093,987 states,
exhausts at depth 592, and visits none of those 8 targets.
This does NOT decide temporal periods 32, 48, ...; other spatial periods,
neutral exteriors, other overflow streams, centres or decimal Lychrel numbers.
Reproduce with mandatory b9/b13 positive controls (C++17, <4 GiB):
`bash calculation/decimal_frontier/lattice_formats/code/agent11_p16_m4_reproduce.sh /tmp/a11-m4`.
