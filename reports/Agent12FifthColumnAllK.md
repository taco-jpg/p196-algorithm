# PAPER PROOF: Fifth spatial-column obstruction for decimal repeated overflow word (11000)^k

**Status: PAPER PROOF** for all integers `k>=1`; the finite graph and independent controls are **COMPUTED** without state caps. This concerns only the first **five** spatial coefficients of the exact position automaton at **time period `p=5k`**; it does not prove or disprove a base-10 Lychrel number.

## Prerequisite and exact arithmetic

In the base-10 canonical-root position automaton, `g=(11000)^k`, the first-three-column coefficient words are, in each five-time block, respectively `(9,10,1,2,4)`, `(13,3,4,8,16)` and `(15,10,4,8,17)`, with each third-column outgoing carry word freely `(a,b,0,1,0)`, `a,b in {0,1}`, for every block. This is the independently checked all-k PAPER PROOF in committed `results/Agent12ThreeColumnAllK.md` (commit `a5dd730e`). The subsequent four-column classification is in `results/Agent12FourthColumnAllK.md` (commit `118b9963`).

For each fourth coefficient `x4_t` and chosen carry `c4_t in {0,1}`, the exact `bauto3.cpp` position recurrence, in a five-time block, reads:

```
 g     = (1,1,0,0,0)
 L4    = (1,1,0,0,1)
 H4    = (a,b,0,1,0)
 Y4    = (5+a,b) at the two overflow times
 floor((x4_t+c4_t)/10)=H4_t
 x4_(t+1)=((x4_t+L4_t) mod 10) + (Y4_t if g_t=1 else ((x4_t+c4_t) mod 10))
```

For the fifth coefficient `x5_t`, chosen carry `c5_t`, the exact inputs are **determined at every time by the fourth path**, with no approximation:

```
 L5_t = floor((x4_t+L4_t)/10)
 H5_t = c4_t
 Y5_t = (x4_t+c4_t) mod 10, at overflow times
 floor((x5_t+c5_t)/10)=H5_t
 x5_(t+1)=((x5_t+L5_t) mod 10) + (Y5_t if g_t=1 else ((x5_t+c5_t) mod 10))
```

All coefficients are in `[0,18]`. For `k` five-time blocks, every spatial coefficient must close at `p=5k`, including `x4_p=x4_0`, `x5_p=x5_0`. Earlier three columns are already closed by construction. Outgoing fifth carry is unrestricted until the sixth column.

## Finite transfer lemma, exhaustively certified

For each four-bit pair `(a,b)` (four choices) and each fourth starting coefficient `u4=0..18`, enumerate the 32 possible five-time carry words `c4`; keep those satisfying the exact equations, recording the fourth coefficient trajectory and endpoint `v4`. There are **182** fourth-column paths across all four `(a,b)` labels (28, 68, 6 and 80 respectively). For every retained fourth path, enumerate all 19 fifth starting coefficients `u5` and 32 five-time carry choices `c5`, enforcing the fifth equations with fourth-derived `L5,H5,Y5`. Each accepted pair of paths is a directed weighted edge from `(u4,u5)` to `(v4,v5)`. This is a **complete finite enumeration**, with no state cap and no solver assumption.

`fivecol_transfer.py` checks that the resulting 5-time transfer has precisely:

- **266** participating joint spatial states from the possible `19^2=361` states;
- **846** distinct ordered state pairs (multiplicities summed over `(a,b)` and both carry histories);
- **2,874** paths counting all distinct third labels, fourth carries and fifth carries;
- **264** strongly connected components, only **one** cyclic component; all other 263 are acyclic singletons.

The sole cyclic component is exactly the three ordered states

```
 S = ((9,9), (15,0), (15,9))
```

with exact integer weighted adjacency matrix (in this order)

```
 M = [[0,1,1],
      [4,0,0],
      [2,0,0]].
```

The source exhaustively reconstructs these values and proves that every closed transfer walk of any positive length lies in this set, by computing the SCCs of the *complete finite graph*. Each matrix entry is the exact number of distinct complete local coefficient/carry histories yielding that edge, so multiplying weights counts genuine complete five-column histories.

## All-k conclusion

Any time-closed five-column history with `g=(11000)^k` induces a `k`-step closed directed walk of the above weighted transfer graph. Conversely, every weighted such walk glues into a legitimate time-closed five-column coefficient/carry history, since prior columns' coefficients are five-time periodic and the two third-column outgoing carry bits may be chosen independently in each block. Thus the exact number of time-closed first-five-column histories is

```
 F_k = trace(M^k).
```

Direct integer matrix multiplication gives `M^3 = 6 M` and `det(xI-M)=x(x^2-6)`. Consequently `trace(M^(2j+1))=0` for every `j>=0`, and `trace(M^(2j))=2*6^j` for every `j>=1`. Equivalently,

```
 F_k = 0             if k is odd;
       2 * 6^(k/2)  if k is even.
```

This is a complete **all-k first-five-column obstruction for every odd number of overflow blocks**, not an all-width exterior exclusion. Even k still leaves exponentially many five-column histories that can die in the sixth column.

## Independent whole-time checker (no five-step blocks)

`fivecol_whole_time.cpp` recomputes the result without using the five-time transfer, SCCs or three-state matrix. For every `k=1..12`, it directly iterates the literal **single-time equations** on all 361 states `(x4,x5)` from each possible initial state, carrying the exactly forced previous three-column values through the `5k` steps. At phase 0/1, `(a,b)` is simply the uniquely implied quotient `floor((x4+c4)/10)`, and at phases 2/3/4 it imposes the fixed required quotients `(0,1,0)`. It loops over all `c4,c5` choices, then counts only states returning to their exact initial pair. No search cap, randomization, blocking assumptions or transfer-matrix code is reused.

Direct results:

| k | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 | 11 | 12 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| count | 0 | 12 | 0 | 72 | 0 | 432 | 0 | 2592 | 0 | 15552 | 0 | 93312 |

The separate `full_scc_controls.cpp` reproduces the mandatory independently computed full-automaton controls with no cap: base 9, fixed `g=1100011000`, **956310** states, **1005301** edges, **7** nontrivial SCCs including two depth-61 four-cycles; base 13 `g=1010010000`, **250302** states, **254201** edges, **5** nontrivial SCCs including depth-55 and depth-75 loops; base 17 `1100011000` has one root and no edge.

## Reproduction: all source in this commit

From repository root, with only Python 3 and standard C++17 installed:

```
python3 calculation/decimal_frontier/fivecol_allk/fivecol_transfer.py
c++ -O2 -std=c++17 calculation/decimal_frontier/fivecol_allk/fivecol_whole_time.cpp -o /tmp/p196_fivecol_whole
nice -n 10 /tmp/p196_fivecol_whole 12
c++ -O2 -std=c++17 calculation/decimal_frontier/fivecol_allk/full_scc_controls.cpp -o /tmp/p196_fivecol_controls
nice -n 10 /tmp/p196_fivecol_controls
```

These checks use one core. No Lean files are modified; local GitHub DNS and missing Lean 4.19.0 prevented running `tools/verify.py --changed`, so no Lean verification is claimed. Every statement about an unbounded `k` follows from the displayed exact finite transfer graph, not from extrapolating `k<=12` data.
