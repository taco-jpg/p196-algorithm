# All-repetition sixth-column obstruction in the decimal position automaton

**PAPER PROOF (every integer k>=1).** Complete **COMPUTED** finite transition check, independently confirmed by whole-time arithmetic. This excludes all spatially periodic exteriors with **time-rooted overflow schedule g=(11000)^k** for any repetition count `k`. It is *not* a decimal Lychrel certificate, not a proof about the orbit of 196, and not a statement about any other overflow schedule.

## 1. Exact column recurrence and prerequisites

In base 10, the exact `bauto3.cpp` position automaton associates with each spatial column a temporal coefficient history `x_t` in `{0,...,18}`, carry inputs `L_t` and requirements `H_t` in `{0,1}`, and upper partner digits `Y_t` at the overflow times. Each chosen upper-side carry `c_t in {0,1}` must satisfy

```
 floor((x_t+c_t)/10)=H_t,
 x_(t+1)=((x_t+L_t) mod 10) + (Y_t if g_t=1 else ((x_t+c_t) mod 10)),
 L_next[t]=floor((x_t+L_t)/10), H_next[t]=c_t,
 Y_next[t]=(x_t+c_t) mod 10 at times g_t=1.
```

For the canonical root, `L=0`, `H=g`, `Y=1` at overflow positions, and the initial coefficient is at least 1. For every fixed temporal period `p=5k`, an edge of the position automaton requires `x_p=x_0`; at the next spatial column, the resulting temporal carry state is reused. This is precisely the recurrence used by both the finite transfer code and independent numerical checker.

The committed PAPER PROOF `Agent12ThreeColumnAllK` shows, for every `k>=1`, that the first three spatial coefficients have the forced time blocks `(9,10,1,2,4)`, `(13,3,4,8,16)`, `(15,10,4,8,17)` repeated k times, and that the third outgoing carries can be independently `(a,b,0,1,0)` on each five-time block. This yields a *complete*, not heuristic, five-step transfer for fourth/fifth/sixth columns. The complementary fourth- and fifth-column all-k lemmas are also committed on main (`Agent12FourthColumnAllK` and `Agent12FifthColumnAllK`).

## 2. Complete five-time transfer through column five

For each `a,b in {0,1}` and fourth-column initial coefficient `z4 in 0..18`, enumerate the 32 possible five-bit carry words `c4`. The fourth input within the block is

```
 G  = (1,1,0,0,0)
 L4 = (1,1,0,0,1)
 H4 = (a,b,0,1,0)
 Y4 = (5+a,b) at the two overflow times.
```

Keep only carry words satisfying the original five exact column recurrences. There are **182** fourth-column paths (28,68,6,80 by labels). For each, derive `L5[t] = floor((x4[t]+L4[t])/10)`, `H5=c4`, and `Y5[t]=(x4[t]+c4[t]) mod 10` at the two overflow times; then enumerate **all** fifth initial coefficients `z5 in 0..18` and all 32 fifth carry words. This yields **2874** fifth-column path realizations, giving exactly **846** distinct weighted edges on **266** participating joint boundary states `(z4,z5)`.

An exact strongly connected component computation on the **complete** graph gives 264 SCCs, of which exactly one contains a cycle. Its three boundary states are

```
 S = {(9,9), (15,0), (15,9)}.
```

The weighted transitions among `S`, with rows/columns in the above order, are `[[0,1,1],[4,0,0],[2,0,0]]`. They have exactly **8** distinct five-time-path realizations: one `(9,9)->(15,0)`, one `(9,9)->(15,9)`, four `(15,0)->(9,9)` and two `(15,9)->(9,9)`. Every closed fifth-column history of any number `k>=1` of five-time blocks must have its boundary state in `S` at **every** block boundary, because every vertex on a closed directed walk lies on a directed cycle.

## 3. Sixth-column transfer and structural impossibility

For each of those eight allowed fifth-column paths (including the precise fourth/fifth coefficient words and carries), calculate all 5 temporal sixth-column inputs independently using the original formula:

```
 L6[t] = floor((x5[t]+L5[t])/10)
 H6[t] = c5[t]
 Y6[t] = (x5[t]+c5[t]) mod 10 at the overflow times.
```

Exhaust **all 19** sixth-column starting coefficients and all **32** five-bit outgoing carry words for each input, keeping exactly those with the required quotient at every time. The resulting complete sixth-column transfer, restricted only by the proven necessary condition that fourth/fifth block boundaries lie in `S`, has:

- exactly **54** distinct directed ordered boundary-state pairs on **25** participating triples `(z4,z5,z6)`;
- exactly **104** distinct five-time coefficient/carry path realizations (multiplicities summed);
- exactly **9** possible source boundary triples, all with first two coordinates `(15,0)` or `(15,9)`;
- exactly **16** possible target boundary triples, all with first two coordinates `(9,9)`;
- **NO triple that is both a source and a target.**

The last property is stronger than acyclicity: **a sixth-column transfer cannot be followed by even one more sixth-column transfer** while remaining compatible with a time-closed fifth-column history. In particular, the restricted directed graph has no positive-length directed closed walk for any `k>=1`. A six-column history of temporal length `5k` would provide exactly such a closed `k`-block walk, a contradiction.

The exhaustive script `sixcol_transfer.py` reconstructs both the complete fifth-column graph and all sixth-column transitions from the elementary integer recurrence. It asserts every node/edge/path count, computes the fifth SCCs (not assumed as data), and checks exact disjointness of the sixth source and target sets. No SAT solver, sampling, truncation, heuristic pruning, state cap or unverified external data are involved.

## 4. Corollary: no reachable spatial cycle for this family

Fix **any** `k>=1`, `p=5k`, and the time-rooted word `g=(11000)^k` in the exact bauto position automaton. If the reachable spatial graph contained any directed cycle at some finite spatial depth `d`, a root-to-cycle path followed by repeated traversals of the cycle would give spatial paths of **arbitrary** length. In particular, it would supply a valid time-closed path through six spatial columns, contradicting Section 3. Therefore the reachable spatial graph contains **no directed cycle at any spatial width** for every such k. The spatial depth is bounded by 5, although the number of possible carry histories at those depths can be large. This is an **all-k, all-spatial-width exclusion for this single primitive overflow family and its repetitions**; it does not exclude different overflow words or solve the base-10 problem.

## 5. Independent whole-time arithmetic validation and mandatory controls

`calculation/decimal_frontier/sixcol_allk/sixcol_whole_time.cpp` checks the same conclusion via a *separate* original-time arithmetic DP, not using any five-time-step graph. The only input from the proved five-column lemma is the necessary starting fourth/fifth boundary triple set `S × {0,...,18}`. For every one of those 57 starting triples it explicitly propagates the original coefficient/carry equations at every time `t=0..5k-1` through all 19³ triples and all `c4,c5,c6 in {0,1}`, with no restrictions on intermediate fifth-column block boundaries or unverified symmetries. It counts exact returns to the initial triple, and reports zero for every `k=1,...,8`. These are independent finite control runs, **not** the basis for the all-k proof.

A third independent C++ implementation `full_scc_controls.cpp` reproduces the mandatory full-exterior control data: base 9, overflow `1100011000`, **956310** reachable states, **1005301** edges and **7** nontrivial SCCs (depth-61 period-4 cycles); base 13, overflow `1010010000`, **250302** states, **254201** edges and **5** SCCs (self-loops at depths 55 and 75); base 17, overflow `1100011000`, **one** state and **zero** edges.

## 6. Reproduce from this commit alone

From repository root, Python 3 and a standard C++17 compiler suffice:

```
python3 calculation/decimal_frontier/sixcol_allk/sixcol_transfer.py
c++ -O2 -std=c++17 calculation/decimal_frontier/sixcol_allk/sixcol_whole_time.cpp -o /tmp/p196_sixcol_whole
nice -n 10 /tmp/p196_sixcol_whole 8
c++ -O2 -std=c++17 calculation/decimal_frontier/sixcol_allk/full_scc_controls.cpp -o /tmp/p196_sixcol_controls
nice -n 10 /tmp/p196_sixcol_controls
```

Each process is single-threaded and uses far less than 8 GB. On the author's machine, the independent `sixcol_whole_time 8` returned all eight zero checks in 0.09 seconds at approximately 2 MB RSS. A Lean 4.19.0 or `tools/verify.py --changed` success is **not** claimed because this environment lacks the required checkout/toolchain. No Lean modules or shared files were modified. **Not claimed:** that no decimal Lychrel number exists or that 196 reaches a palindrome; the result is strictly the time-rooted repeated-overflow-word exclusion stated above.
