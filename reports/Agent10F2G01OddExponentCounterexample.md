# Counterexample to a proposed power-of-two exterior family

**COMPUTED** (exact finite-state exhaustive search; not Lean-verified).
The conjecture in agent-10's issue #474 CLAIM 6483314674 that every base
`b = 2^(2k+1)` has a reachable neutral-band exterior for cyclic overflow
word `g=01` is **FALSE**. At `b = 2^17 = 131072`, the canonical-root exact
period-two position automaton has exactly **14,977 reachable cut states**, a
maximal BFS depth of **3,744**, and **zero** neutral accepting states. This
is a complete all-B-width exclusion for this one base and overflow word.

The earlier `g=01` linear-time exact solver and an **independent** Python
implementation give the same state count and no accepts. The independent
implementation does **not** assume the one-carry invariant: it enumerates
all four possibilities for `(a,e)` and two for the first far carry `c0`
using the identity

    x0 = b*(a + h0 + e) - (l0 + l1 + c0 + y)

then checks the actual two-step digit and carry equations, the periodic
closure, and each resulting cut state. BFS begins at `(L,H,Y)=(0,2,1)`;
positive first-column values are enforced, and the cut state records all
possibilities. A finite exact graph search is complete for all widths
because adding a spatial column is one graph edge.

Counter-controls in the **same** independent enumerator:

| exponent | base | reachable states | accepting depth | accepts |
|--:|--:|--:|--:|--:|
| 13 | 8,192 | 31,811 | 1,450 | 1 |
| 15 | 32,768 | 131,072 | 4,441 | 1 |
| **17** | **131,072** | **14,977** | **none** | **0** |
| 19 | 524,288 | 2,097,152 | 501,157 | 1 |

For all four cases the independent and optimized engines agree. Prior
mandatory external controls also reproduced: base 9, g=1100011000:
956,310 states, 7 nontrivial SCCs, m=4 at width 61; base 13,
g=1010010000: 250,302 states, 5 SCCs, fixed SCCs at widths 55 and 75.

Reproduce the counterexample and its controls:

    python3 calculation/decimal_frontier/lattice_formats/code/agent10_g01_pow2_counterexample.py 13 15 17 19
    c++ -O3 -std=c++17 calculation/decimal_frontier/lattice_formats/code/agent10_g01_even_fast.cpp -o /tmp/g01_fast
    /tmp/g01_fast 131072 131072 /tmp/g01_b131072.csv

This refutes only the **proposed all-odd-exponent** family of neutral
exteriors. It does **not** rule out an infinite subsequence, other
overflow words, absorbing lattices, centrosymmetric templates or a
base-10 Lychrel certificate. It is not a proof about the orbit of 196.