# Four-column all-period transfer for the decimal time-rooted overflow schedule (11000)^k

**PAPER PROOF** (for *every* integer `k>=1`), with complete small **COMPUTED** transfer enumeration and independent whole-time checks. This is a classification of **time-closed first-four spatial columns in the exact `bauto3` position automaton**, not a decimal Lychrel number, centre certificate, or even an accepting exterior SCC.

## Exact recurrence and prerequisite

Base `b=10`, `p=5k`, overflow word `g=(11000)^k`, canonical initial spatial state `L_t=0`, `H_t=g_t`, `Y_t=1` for times where `g_t=1`. For one spatial-column coefficient history `x_t` and chosen outgoing carry `c_t in {0,1}`:

```
 floor((x_t+c_t)/10) = H_t,
 x_(t+1) = ((x_t+L_t) mod 10) + (Y_t if g_t=1 else ((x_t+c_t) mod 10)),
 L_next[t] = floor((x_t+L_t)/10), H_next[t]=c_t,
 Y_next[t] = (x_t+c_t) mod 10, at overflow times.
```

All coefficients are from `0..18`; at the canonical first spatial column `x_0>=1`. Every column must close after exactly `p` times, `x_p=x_0`. These are the unmodified `bauto3.cpp` equations and are independently reproduced by `fourcol_independent.cpp`.

The previously published `results/Agent12ThreeColumnAllK.md` (commit `a5dd730e`) proves, for **every** `k>=1`, that the unique coefficient histories at columns 1, 2, 3 are the five-time blocks `(9,10,1,2,4)`, `(13,3,4,8,16)`, `(15,10,4,8,17)` repeated `k` times. Exactly one third-column incoming carry schedule allows three-column time closure; its **outgoing carry** is freely `(a_i,b_i,0,1,0)` for each time block `i`, with `a_i,b_i independently in {0,1}`. Thus the fourth column receives on each five-time block:

```
 g = 1,1,0,0,0
 L = 1,1,0,0,1
 H = a,b,0,1,0
 Y at overflow times = (5+a,b).
```

## Exhaustive finite graph lemma

For each label `(a,b) in {0,1}^2`, enumerate all `z=x_(5i) in 0..18`, all `2^5` outgoing carry words, and the above five exact steps; keep the resulting `z'=x_(5i+5)` and multiplicities. The four labels produce respectively **28, 68, 6, 80** valid coefficient/carry paths. Their union has exactly **51 distinct labeled edges**, 50 distinct unlabeled (start,end) pairs, and aggregate multiplicity 182. The only directed SCC containing a cycle is the eight-state set

```
 S = (6,7,8,9,15,16,17,18).
```

Its weighted adjacency matrix (rows and columns indexed by `S`) is:

```
 0 0 0 4 0 0 0 0
 4 4 4 0 0 0 0 0
 0 0 0 4 4 4 0 0
 0 0 0 4 2 2 2 2
 0 0 0 4 0 0 0 0
 4 4 4 0 0 0 0 0
 0 0 0 4 4 4 0 0
 0 0 0 4 0 0 4 4
```

Every one of these entries is the number of (prior third-column carry-label, current fourth-column outgoing carry-history) pairs yielding that transition, so weights count **distinct complete four-column histories**, not merely coefficient cycles. The exact exhaustive transfer code `fourcol_block_graph.py` checks the complete original finite step relation, all multiplicities, unique cyclic SCC and matrix without a solver/state cap. This is a finite exhaustive lemma, not a statement that the fourth column ultimately extends to infinity in space.

## All-k paper deduction

A time-closed coefficient history of period `5k` induces a length-`k` closed walk in the five-time-step union transfer. Conversely every such closed walk, with its weighted edge realizations, glues to a valid entire `5k`-time four-column coefficient/carry history because the first three columns have the forced periodic coefficient blocks and independently free third outgoing carry bits on each block. Transient states cannot lie on a closed walk, so the exact count of complete four-column histories is

```
 F_k = trace(M^k), k>=1.
```

The exact integer Newton-trace characteristic-polynomial computation gives:

```
 det(xI-M) = x^5 (x-4) (x^2-8x-24).
```

Thus, using the identity that the trace of a matrix power equals the sum of its eigenvalues' kth powers counted with algebraic multiplicity,

```
 F_k = 4^k + (4+2 sqrt(10))^k + (4-2 sqrt(10))^k, for every k>=1.
```

This is an integer: letting `T_0=2`, `T_1=8`, `T_k=8 T_(k-1)+24 T_(k-2)` gives `F_k=4^k+T_k`. The first 12 exact counts are `12,128,1152,11648,118272,1215488,12521472,129179648,1333297152,13764067328,142101184512,1467105148928`.

## Completely independent whole-time arithmetic check

`fourcol_independent.cpp` does **not** call or read the five-step transfer or matrix. For each `k<=8`, it recursively enumerates all canonical time-closed root, second and third coefficient/carry histories via the literal `5k`-time equation; for each closed third-column history it counts fourth-column time-closed histories with a fresh 19-state coefficient DP. It also rejects any first-three-column coefficient history differing from the three forced blocks. No premature filtering by the fourth graph, no randomization and no state cap. It returns

```
 k:       1     2     3     4      5       6        7         8
 root:    2     4     8    16     32      64      128       256
 second:  4    16    64   256   1024    4096    16384     65536
 third:   4    16    64   256   1024    4096    16384     65536
 fourth: 12   128  1152 11648 118272 1215488 12521472 129179648
```

A third independent C++ full-SCC implementation reproduces the mandatory control runs base 9 `g=1100011000`: **956310** reachable states, **1005301** edges, **7** nontrivial SCCs (two 4-cycles at spatial depth 61), and base 13 `g=1010010000`: **250302** states, **254201** edges, **5** nontrivial SCCs (depth-55 and depth-75 self-loops); base 17 `g=1100011000`: 1 root, 0 edges.

## Reproduce from this one commit

From repository root, no package beyond Python 3 and a standard C++17 compiler is needed:

```
python3 calculation/decimal_frontier/fourcol_allk/fourcol_block_graph.py
c++ -O2 -std=c++17 calculation/decimal_frontier/fourcol_allk/fourcol_independent.cpp -o /tmp/p196_fourcol_independent
nice -n 10 /tmp/p196_fourcol_independent 8
c++ -O2 -std=c++17 calculation/decimal_frontier/fourcol_allk/full_scc_controls.cpp -o /tmp/p196_fourcol_scc_controls
nice -n 10 /tmp/p196_fourcol_scc_controls
```

All local controls passed using one core. The independent whole-time run used about 1.5 MB RSS and 1.63 s at `k=8`; full base9/base13 SCC controls used about 137 MB and 2.87 s. `python3 tools/verify.py --changed` was unavailable in the local container due shell GitHub DNS resolution and absent Lean 4.19.0, so this claim is explicitly **PAPER PROOF**, not **LEAN-VERIFIED**. No Lean or shared repository file is modified.
