# PAPER PROOF: no decimal canonical-root exterior cycles for (11 0^r)^k, all r,k>=1

**PAPER PROOF** for all integers `r>=1` and `k>=1`. This is an all-spatial-width exclusion in the exact `bauto3`/`bauto5` canonical-root position automaton for the *specific* time-rooted overflow family `g=(11 0^r)^k`. It does **not** settle the Lychrel problem in decimal or the orbit of 196. No Lean theorem is claimed.

## 1. Exact temporal first-column arithmetic

Write `m=r+2` and `g=(1,1,0,...,0)^k`, with `r` consecutive zero bits, at base `b=10`. At the canonical first spatial column, the position automaton has input `L=0`, `H=g`, `Y=1` at overflow times and requires `1<=x_0<=18`. Let `c_t in {0,1}` be the outgoing carry choice. The *exact* transition is

```
 floor((x_t+c_t)/10)=g_t,
 x_(t+1)=(x_t mod 10) + (1 if g_t=1 else ((x_t+c_t) mod 10)),
 x_(mk)=x_0.
```

These are the literal root equations in `calculation/decimal_frontier/lattice_formats/code/bauto3.cpp` and are reimplemented independently in the two new checkers. For a whole time-closed prefix of any number of spatial columns, this first-coordinate closure is **necessary**, regardless of exterior or centre format.

## 2. A complete elementary classification of one temporal block

For every `r>=1`, the first two required overflow ones force the following alternatives:

- `x_0=9`, `c_0=1`, `x_1=10` and `x_2=1`, with `c_1 in {0,1}` independently arbitrary;
- `x_0=18`, `x_1=9`, `c_1=1`, `x_2=10` (the first carry can be 0 or 1).

Any other `x_0 in 1..18` fails one of the two initial overflow requirements. As `g_2=0` and `x_2=10` would require `floor((10+c_2)/10)=0`, which is impossible, **only `x_0=9` survives** the first two ones plus the first zero. From `x_2=1`, during each following zero time we must have `x_t+c_t<10`, and therefore exactly `x_(t+1)=2*x_t+c_t`. The first four successful zero steps produce the exact endpoint supports

| Number of zero times `r` | Allowed endpoints `x_(r+2)` | Exact number of distinct one-block carry histories |
|---|---|---:|
| 1 | `{2,3}` | 4 |
| 2 | `{4,5,6,7}` | 8 |
| 3 | `{8,9,10,11,12,13,14,15}` | 16 |
| 4 | `{16,17,18}` | 6 |
| `>=5` | empty | 0 |

The counts include the two independent `c_1` choices at the second overflow time. For `r>=5`, after four zeros the current coefficient is at least 16, so the *fifth* required zero quotient is impossible; hence the endpoint set is empty for every larger `r`, not just those individually tested.

For any one-block continuation with **another identical `(11 0^r)` block**, the next block must again start from `x=9`, because every successful block has **only** starting coefficient 9. Therefore a time-closed trajectory over `k` repetitions (equivalently, a closed walk of length `k` in the one-block relation) exists **iff** one block has an edge `9 -> 9`. By the table, this happens **only for r=3**. At `r=3`, there are exactly two such self-loop carry histories per block, so the exact number of time-closed first-column histories is `2^k` for all `k>=1`. For every `r≠3` the count is exactly zero for every positive `k`.

## 3. Eliminate the sole exceptional zero-run length r=3

When `r=3`, the overflow schedule is `g=(11000)^k`. The already committed complete all-k PAPER PROOF `Agent12SixthColumnNoGoAllK` (commit `6a9ad209`) proves that, for every `k>=1`, the canonical-root automaton admits **no time-closed SIX-spatial-column prefix**. Its exhaustive finite sixth-column graph has 25 participating states, 54 ordered edges and 104 exact carry paths; crucially the set of 9 source boundary states and 16 target boundary states are disjoint, so no two consecutive five-step sixth-column transfers can occur. Its proof and exact reproducer are in `reports/Agent12SixthColumnNoGoAllK.md` and `calculation/decimal_frontier/sixcol_allk/sixcol_transfer.py`, available on `main`.

If a reachable spatially periodic SCC existed for `g=(11000)^k`, the root-to-SCC path plus repetitions of the SCC would yield paths of arbitrarily large spatial length, in particular six spatial columns. This contradicts that complete sixth-column obstruction. Combining this with Section 2 proves the theorem for **every** `r>=1,k>=1`: no rooted reachable spatial SCC for the specified overflow family.

The theorem does not claim a missing-centre obstruction, a general decimal infinite-orbit result, or any statement about a rotation with a different chosen initial time origin except insofar as the full rooted time schedule is explicitly identical to the one analyzed.

## 4. Independent exhaustive control programs

`family_exact.py` enumerates the entire `(r+2)`-time first-column relation for each `r=1..50`, checking the exact endpoint supports and multiplicities, and independently recomputes closed histories via the *full repeated-time recurrence* at every pair `r=1..50, k=1..12`. `family_independent.cpp` is a different C++17 full-time dynamic program, separately checking every one of **1,200** `(r,k)` pairs with `1<=r<=100`, `1<=k<=12` and exactly matching `0` for all `r≠3` and `2^k` for `r=3`. Both use exact integers, no random sampling, no state caps and no solver.

The previously committed `sixcol_allk/sixcol_transfer.py` independently reconstructs the r=3 sixth-column no-go at **all k**, not merely the finite checks; its own separate whole-time C++ checker verifies k1..8. Finally, the new copy of the independent full-SCC control engine `full_scc_controls.cpp` reproduces mandatory b9/b13 data: base 9 overflow `1100011000`, **956310** reachable states and **7** nontrivial SCCs including depth-61 4-cycles; base 13 overflow `1010010000`, **250302** states and **5** nontrivial SCCs including depth-55 and depth-75 fixed points; and base 17 fixed `1100011000` with 1 node and no edges.

## 5. Reproduce from the repository

No packages beyond Python 3 and a C++17 compiler:

```
python3 calculation/decimal_frontier/adjacent_ones_family/family_exact.py --rmax 50 --kmax 12
c++ -O2 -std=c++17 calculation/decimal_frontier/adjacent_ones_family/family_independent.cpp -o /tmp/p196_adjacent_independent
nice -n 10 /tmp/p196_adjacent_independent 100 12
python3 calculation/decimal_frontier/sixcol_allk/sixcol_transfer.py
c++ -O2 -std=c++17 calculation/decimal_frontier/adjacent_ones_family/full_scc_controls.cpp -o /tmp/p196_adjacent_controls
nice -n 10 /tmp/p196_adjacent_controls
```

All scripts needed for the new all-r argument and independent numerical checks are added **in this same commit**; the r=3 theorem is a cited, separately completed and already committed result with its own complete source in the same repository. No file is left only in a local sandbox. Local git DNS and absent Lean 4.19.0 prevent running `python3 tools/verify.py --changed`; no Lean files are added or modified, and **LEAN-VERIFIED** is not claimed.
