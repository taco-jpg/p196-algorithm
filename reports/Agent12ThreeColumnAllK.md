# All-repetition three-column decimal exterior rigidity

**PAPER PROOF** (conditional only on the elementary position-column recurrence stated below), with **COMPUTED** exhaustive finite transfer tables. This does **not** give a base-10 reverse-and-add certificate.

## Exact question

Fix an arbitrary integer `k >= 1`, base `b=10`, and **time-rooted** overflow word `g=(11000)^k` of length `p=5k`. Begin the `bauto3` positional automaton in the canonical state `L_t=0, H_t=g_t, Y_t=1` at the overflow times. Follow exactly three adjacent spatial-column edges. Each edge consists of a coefficient history `x_t` (between 0 and 18), a chosen carry history `c_t ∈ {0,1}`, and the closure condition `x_p=x_0`; only the very first spatial coefficient has `x_0>=1`. At a column, `L_t,H_t∈{0,1}` and `Y_t` is the previous lower partner digit when `g_t=1`. The complete one-time transition is

```
 floor((x_t+c_t)/10) = H_t
 x_(t+1) = ((x_t+L_t) mod 10)
             + (Y_t if g_t=1 else ((x_t+c_t) mod 10))
 L_next[t] = floor((x_t+L_t)/10)
 H_next[t] = c_t
 Y_next[t] = ((x_t+c_t) mod 10), at times g_t=1.
```

These formulas are exactly the `transitions` equations of `calculation/decimal_frontier/lattice_formats/code/bauto3.cpp`; all coefficients generated in the checked tables lie in `[0,18]`.

## Exhaustive five-time-step transfer enumeration (finite lemma)

Write `z=x_(5i)` and `z'=x_(5i+5)`. For fixed five-bit input streams `(L,H,Y)`, enumerate all 19 starts `z=0..18` (or 18 positive starts in the first column) and the `2^5` possible carries, rejecting choices immediately if the quotient constraint fails. The complete relations, including multiplicity of carry histories per ordered edge, are:

1. First column: `L=00000, H=11000, Y=(1,1)`. **8 edges, each multiplicity 2**: `9 -> 8,9,10,11,12,13,14,15`. The unique directed cycle is the loop `9->9`, with `x=(9,10,1,2,4)` and `c=(1,u,0,0,1)` for `u∈{0,1}`. No other start has an outgoing five-step edge. In particular, any time-closed `p=5k` path must choose this loop every block.
2. For `u=1` there are **no** second-column five-step edges (inputs `L=01000, H=11001, Y=(0,1)`). Therefore every block has `u=0`. Now `L=01000, H=10001, Y=(0,0)`. The complete second-column graph has **19 edges, each multiplicity 4**: `11 -> {0,1,2,3,9}`; `12 -> {4,5,6,7,8,9,10,11}`; `13 -> {12,13,14,15,16,17}`. Its unique directed cycle is `13->13`; the coefficient block is `x=(13,3,4,8,16)` and the four output-carry blocks are `c=(a,b,0,0,1)` for independently arbitrary `a,b∈{0,1}`.
3. The third column then has `L=10001, H=(a,b,0,0,1), Y=(3+a,3+b)`. For `(a,b)=(0,0)` and `(1,0)`, there are **no** five-step edges. For `(0,1)` there are exactly six edges `6 -> {13,14,15,16,17,18}`; for `(1,1)` there are exactly six edges `15 -> {13,14,15,16,17,18}`. Every edge has **four** carry-history realizations. The only directed cycle of this entire labeled graph is `15 -> 15` labeled `(1,1)`. On it `x=(15,10,4,8,17)` and the four outgoing carry histories are `(a',b',0,1,0)`, `a',b'∈{0,1}`.

The exact finite enumeration, graph equality (no omitted edges), multiplicities and coefficient/carry labels are asserted by `block_graph.py` with no third-party dependency. This finite check is small enough to inspect directly or translate to a Lean `decide` proof, but **no Lean claim is made**.

## All-k deduction (paper proof)

A time-closed `p=5k` coefficient history induces a **closed directed walk of length k** on the appropriate finite five-step transfer relation. Every vertex on a closed directed walk belongs to a directed cycle. The first graph has only `9->9`, so its temporal coefficient block is forced for each of the k repetitions. If it selected `u=1` in any block, the second graph would have no edge; hence `u=0` everywhere. The second graph has only `13->13`, forcing its coefficient blocks, but leaving four choices per block for the outgoing `(a,b)` bits. In the third graph, the only closed-walk cycle is `15->15` and it requires `(a,b)=(1,1)` **at every block**, fixing those second-column choices. At each of the k third-column self-loop traversals there are exactly four possible outgoing carry assignments, independently of the others. Thus the complete time-closed three-column histories have the forced three coefficient words and exactly `4^k` distinct histories for **every positive k**, with no upper time-period cutoff.

This does **not** imply those three-column prefixes extend to a fourth column, reach any absorbing/neutral accepting state, admit a periodic centre, or produce an ordinary integer Lychrel orbit. The coefficient words have temporal period 5; the freely chosen third-column outgoing carries can have larger periods.

## Reproduce from this commit alone

From the repository root:

```
python3 calculation/decimal_frontier/threecol_allk/block_graph.py
c++ -O2 -std=c++17 calculation/decimal_frontier/threecol_allk/independent_whole_period.cpp -o /tmp/p196_threecol_independent
/tmp/p196_threecol_independent 8
c++ -O2 -std=c++17 calculation/decimal_frontier/threecol_allk/full_scc_controls.cpp -o /tmp/p196_threecol_full_controls
/tmp/p196_threecol_full_controls
```

The independent C++ checker **does not use five-step graphs**. It enumerates all time-closed root and second-column trajectories for `k=1..8`, then performs a separate full-`5k`-time integer-arithmetic DP for the third coefficient, with explicit off-pattern detection, no state cap. Control counts, listed as `(k, root histories, second histories, third histories)`, are `(1,2,4,4)`, `(2,4,16,16)`, `(3,8,64,64)`, `(4,16,256,256)`, `(5,32,1024,1024)`, `(6,64,4096,4096)`, `(7,128,16384,16384)`, `(8,256,65536,65536)`. The standalone full-automaton C++ controls independently reproduce:

- base 9, `1100011000`: 956310 reachable states, 1005301 edges, 7 nontrivial SCCs, 4-cycles at depth 61;
- base 13, `1010010000`: 250302 reachable states, 254201 edges, 5 nontrivial SCCs, fixed points at depths 55 and 75;
- base 17, `1100011000`: one root state, zero outgoing edges, zero SCCs.

Control programs compile with standard C++17, each uses one core and under 0.2 GB peak memory in the author's run. Exact search values do not depend on random seeds or solver caps. `python3 tools/verify.py --changed` is **not claimed** here: the local environment cannot clone GitHub via DNS and does not contain Lean 4.19.0, so no Lean files are modified.
