# All-period rooted spatial-cycle classification for `(101100)^k`

**PAPER PROOF + COMPUTED, exhaustive exact finite relations.** This result
concerns the position automaton implemented in the repository's
`calculation/decimal_frontier/lattice_formats/code/bauto3.cpp` (pair
coefficients least-significant-first). It does **not** assert that any
particular integer, especially 196, is a decimal Lychrel number.

## The theorem

Let `k>=1`, `b>=2`, and `g` be a cyclic rotation of `(101100)^k`.
Start at the canonical cut state `L=0, H=g, Y=1` and impose the normal
strictly positive first spatial coefficient. The **reachable** full
position automaton has a cyclic SCC exactly when `b=4`, for every
`k` and every rotation. Here cyclic means size greater than one or
one vertex with a self-loop. This classification is complete over all
integer bases and all temporal multiples `k`, with no graph-size cap.

## Six-step first-column input, valid for every `k`

The earlier `results/Agent16F2Repeated101100.md` proves that the
first spatial coefficient word of any time-closed history is exactly a
six-periodic repetition of the following table. Carries at times 0 and
3 are arbitrary bits `a,d`, independently for each six-step block.

| base | first-column coefficients `X[0..5]` | forced carries `(c1,c2,c4,c5)` |
|---|---|---|
| 4 | `(4,1,3,4,1,2)` | `(1,1,0,0)` |
| 5 | `(6,2,4,5,1,3)` | `(0,1,1,0)` |
| 6 | `(7,2,5,6,1,3)` | `(1,1,1,1)` |

Other bases have no closed first-column history for any `k` or rotation.
The successor second-column input cut in each block is exactly
`L_t=floor(X_t/b)`, `H_t=c_t`, and, for `g_t=1`,
`Y_t=(X_t+c_t) mod b`.  Every possible time-closed second column
must concatenate six-step transitions of the resulting modes
`(a,d) in {0,1}^2`.

## Exact finite transfer and all-k implication

For any second-column coefficient `z_t in {0,...,2b-2}` and guessed
bit `e_t in {0,1}`, the local cut equations are precisely

`floor((z_t+e_t)/b)=H_t`, and
`z_(t+1)=((z_t+L_t) mod b) + (Y_t if g_t=1 else ((z_t+e_t) mod b))`.

The complete six-step transfer is the multigraph whose vertices are
`0,...,2b-2` and whose edges are all pairs `(z_0,z_6)` obtained by
exhaustively choosing mode `(a,d)`, six carry bits `e_0,...,e_5`,
checking these equations at **each** of the six time steps, and
requiring the intermediate and final coefficients to lie in `[0,2b-2]`.
No heuristic pruning, solver timeout or state cap occurs. The code
ships two independent exact algorithms: a coefficient trajectory DFS
and a product of six finite coefficient-to-coefficient weighted matrices.
They agree on the **entire mode-labelled weighted edge relation**.

For unrotated `g=101100`, the exact second-column transfer is:

| b | vertices | weighted edges | mode-labelled edges `(a,d,z0,z6; multiplicity)` | directed cyclic SCC? |
|---|---:|---:|---|---|
| 4 | 7 | 28 | 14 distinct keys (positive control) | yes, `{2,5}` |
| 5 | 9 | 16 | `(0,0,2,8;8)`, `(1,0,6,8;8)` | no |
| 6 | 11 | 0 | none | no |

In base 5, vertex 8 has no outgoing edge, hence no closed walk of
positive length. In base 6 there are no edges. For additional phase
control, the weighted edge counts for the six successive rotations
are, respectively, base 4: `(28,52,32,8,8,16)`, base 5:
`(16,8,0,36,66,16)`, and base 6: `(0,0,0,0,4,0)`.
**All 18** phase graphs were checked exhaustively by both methods;
every base-5/6 phase graph is acyclic. In general a full time-closed
second-column history of length `6k` would give a closed walk of
length `k` in this finite six-step graph; no such walk exists for
b5 or b6, irrespective of k. As the first spatial-column restriction
is necessary for any reachable SCC, all bases except 4 are excluded.

In base 4, `results/Agent16F2FixedBase4AllBase.md` provides an actual
reachable self-loop for the primitive six-step word, checked against
all 957 reachable states. Repeat its six-time trajectory `k` times,
including the finite root-to-loop path, to produce a rooted cyclic
SCC at temporal length `6k`. Cyclic rotation carries that witness
to each phase (all first-column coefficients are positive).
This proves the stated all-base, all-k classification.

## Complete reproduction from the repository alone

Run from the repository root:

```
bash calculation/decimal_frontier/lattice_formats/code/agent16_second_run.sh /tmp/agent16-second
```

The script uses only Python 3 standard library, C++17 and the already
committed `agent16_root_graph.cpp`. It executes both exact six-step
transfer algorithms for b4/5/6 and all six phases, compares every
mode-labelled weighted edge, checks directed cycles independently,
checks the above exact edge-count and b5/b6 edge tables, runs an
additional trace-of-matrix-powers check for k=1..20 at every phase,
and verifies the ordinary base-4 positive rooted SCC control.
The mandatory broader positive full-automaton controls are also run
with the same engine: b9 g=`1100011000` has 956310 states/7 cyclic
SCCs (two period-four SCCs at depth 61), and b13 g=`1010010000` has
250302 states/5 cyclic SCCs (singleton cycles depth 55 and 75).
Each process runs under 8 GB and the heavier controls use `nice -n 15`.

These are complete **finite** computations plus the elementary
all-k closed-walk proof, not Lean kernel proofs. No statement about
other overflow words, other formats, centres, decimal Lychrel
certificates or seed 196 is made.
