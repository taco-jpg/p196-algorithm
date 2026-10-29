# All-base reachable SCC classification for the period-six word 101100

## Precise statements

**COMPUTED** (exhaustive, no state cap reached). Fix temporal overflow
`g=101100` or one of its six cyclic rotations. The exact reachable-state
automaton of `bauto3.cpp`, starting at the **canonical root**
`(L,H,Y)=(0,g,1)` and requiring a strictly positive first spatial
coefficient, has these directed-graph statistics:

| base | reachable vertices | distinct edges | cyclic SCCs | minimum BFS depths of cyclic SCCs |
|---|---:|---:|---:|---|
| 4 | 957 | 1012 | 4 (each a self-loop) | 9, 13, 14, 18 |
| 5 | 5 | 4 | 0 | none |
| 6 | 5 | 4 | 0 | none |

These numbers hold **separately for all six rotations**, not just for one
phase. Every state is expanded and every closed temporal trajectory and
edge is enumerated. There was no runtime, memory, state, or edge cap in
these 18 runs; all completed. Every edge and vertex was compared with a
separately implemented Python exhaustive carry-vector engine. In base 4,
the four reachable self-loop states and exact period-six coefficient/carry
words are in `agent16_b4_loops.json`; the independent checker verifies the
complete transition for every witness and its recorded BFS depth.

**PAPER PROOF** (the unbounded base extension). The previously committed
`results/Agent16F2Base4RootClassification.md` proves that for every
integer base `b>=2` and every rotation of `g=101100`, the first-position
root transition exists exactly when `b` is 4, 5, or 6. To recall the
algebra for the rooted word, with guessed output carries `c_t∈{0,1}` and
pair coefficients `x_t`, root closure gives
`floor((x_t+c_t)/b)=g_t`,
`x_(t+1)=(x_t mod b)+(g_t ? 1 : (x_t+c_t) mod b)`, `x_6=x_0`.
The adjacent 1s at t=2,3 force `x_2=b-1`, `x_3=b`, `x_4=1`;
the 1 at t=0 followed by a 0 forces `x_0>=b` and
`x_1=x_0-b+1`. The two zero-block equations then force
`3b=11+4c_4+2c_5+c_1`, hence `b∈{4,5,6}`. Conversely each
of those bases realizes four complete root carry vectors. Temporal
rotation is a bijection of rooted closed trajectories since coefficients
at overflow positions are positive. Therefore every other base has no
outgoing edge at the canonical root, and so cannot have a *reachable*
cyclic SCC. Combining with the complete b=4,5,6 graphs proves that
**only base 4** has a reachable cyclic SCC for the fixed overflow necklace.
This is **not** a claim about arbitrary overflow schedules or disconnected
bulk cycles, and does not imply a base-10 Lychrel result.

## Exact position-automaton equations

At time position `t`, current cut state `L[t], H[t]∈{0,1}` and `Y[t]`
for `g[t]=1` gives a candidate coefficient `x_t∈[0,2b-2]` and output
upper carry `c_t∈{0,1}`. It must satisfy:

`floor((x_t+c_t)/b)=H[t]`

`x_(t+1)=((x_t+L[t]) mod b) + (g[t] ? Y[t] : (x_t+c_t) mod b)`.

Closure means `x_p=x_0`. The successor state is
`L'[t]=floor((x_t+L[t])/b)`, `H'[t]=c_t`, and
`Y'[t]=(x_t+c_t) mod b` at the overflow times. The first coordinate
additionally requires `1<=x_0<=2b-2`. These are exactly the search
relations; no palindrome conclusion follows from an SCC alone.

## Reproduction from repository alone

One complete result, all source and compact data in this commit:

- `calculation/decimal_frontier/lattice_formats/code/agent16_root_graph.cpp`:
  forward enumerator, closed time paths, complete reachable BFS and
  iterative Kosaraju SCC decomposition; `--dump` emits the exact directed graph.
- `calculation/decimal_frontier/lattice_formats/code/agent16_root_independent.py`:
  independent enumeration over all `2^6` carry bit vectors, exact
  graph-state and adjacency comparison for 18 combinations, rotation
  controls, and exact replay of compact cycle witnesses.
- `calculation/decimal_frontier/lattice_formats/code/agent16_b4_loops.json`:
  all four self-loop states, minimum root depths and pair-coefficient
  temporal/carry words (small complete data).
- `calculation/decimal_frontier/lattice_formats/code/agent16_fullroot_run.sh`:
  compile, run all tests, and run mandatory b9/b13 positive controls.

From the repository root, execute:

```bash
bash calculation/decimal_frontier/lattice_formats/code/agent16_fullroot_run.sh /tmp/agent16-fullroot
```

The script compiles the C++17 program with `-O3`, limits its virtual
address space to 8 GB and uses `nice -n 15` for the large controls.
The Python independent checker runs all six rotations for each of bases
4, 5 and 6 and also confirms exact first-column counts for bases
2..100. It validates all four saved base-4 fixed-point witnesses.
The complete output ends with `ALL GRAPH/CONTROL CHECKS PASSED`.

**Mandatory control outputs, reproduced by the SAME C++ engine:**

- `b=9, g=1100011000`: exactly **956310 states, 1005301 edges,
  7 cyclic SCCs**. Two size-4 SCCs occur at minimum BFS depth 61,
  matching `m=4, |B|=61`.
- `b=13, g=1010010000`: exactly **250302 states, 254201 edges,
  5 cyclic SCCs**. Self-loops at depths 55 and 75 reproduce the
  `|B|=55,75` reference cases.

The controls are exact uncapped graph enumerations, not just first-column
checks. The result neither proves that the base-4 cycles have absorbing
self-mirror lattices nor establishes a new Lychrel certificate; the known
base-4 positive control already exists. No Lean files were added.
