# Exact integer-interval backward feasibility for the position automaton

**PAPER PROOF.** Fix an arbitrary base `b>=2`, binary temporal overflow word `g` of period `p>=1`, and any cut state `L_t,H_t in {0,1}` with partner coefficients `Y_t in [0,b−1]` at times `g_t=1`. A one-position temporal trajectory has `x_t in {0,...,2b−2}`, outgoing carry bits `c_t in {0,1}`, and is required to satisfy

`floor((x_t+c_t)/b)=H_t`,
`x_(t+1)=((x_t+L_t) mod b)+(Y_t if g_t=1 else ((x_t+c_t) mod b))`.

Unlike a position-automaton *edge*, the following feasibility problem does not impose `x_p=x_0`. If **even this relaxed full-word problem** is impossible, then the cut has no outgoing edge under any temporal closure condition.

## Exact preimage formula

Write `I` for any union of closed *integer* intervals within `[0,2b−2]`. Partition each candidate input coefficient into three disjoint regimes: `R0=[0,b−2]`, `R1={b−1}`, `R2=[b,2b−2]`. Fix `c in {0,1}`. Intersect regime `R` with the demanded-carry interval `[b*H−c, b*(H+1)−1−c]`. For this intersection the normalized output map is affine `y=m*x+k`, where `m=1` if `g=1`, `m=2` if `g=0`, and the exact intercepts are:

| regime | `g=1`: `k` | `g=0`: `k` |
|---|---|---|
| R0 | `L+Y` | `L+c` |
| R1 | `((b−1+L) mod b)+Y−(b−1)` | `((b−1+L) mod b)+((b−1+c) mod b)−2(b−1)` |
| R2 | `L+Y−b` | `L+c−2b` |

For each desired output interval `[a,z]` and each of the six (regime,carry) cases, the exact set of allowable input integers is the intersection of the regime/carry interval with

`[ceil((a−k)/m), floor((z−k)/m)]`.

Merge overlapping or adjacent integer intervals. This is **exact**, because every valid pair `(x,c)` belongs to exactly one of the cases, the formula is its exact normalized integer transition, and every integer in a selected preimage interval has an admissible carry and a corresponding output inside `I`. The algorithm neither rounds away holes in the input nor assumes real-valued carries. In particular, the integer division uses `ceil`, not real relaxation.

## Theorem and proof

Initialize `D_p=[0,2b−2]`. For `t=p−1,...,0`, set `D_t=Preimage_(L_t,H_t,g_t,Y_t)(D_(t+1))` by the formula above. By backward induction, **`D_t` is exactly the set of all admissible integer coefficients at time t that admit at least one full trajectory through times t,...,p−1 ending in the valid coefficient domain**. The base case `t=p` is immediate; the induction step follows directly from the six affine pieces and the exact union. Hence `D_0` is empty if and only if the relaxed full-time trajectory is impossible. In that case, no time-closed edge exists, with no state cap, arbitrary integer base, arbitrary temporal word, and any supplied cut. The method is not an algorithm for detecting cyclic SCCs: if `D_0` is nonempty, cyclic closure remains a separate condition.

The running time depends on the number of interval components during the backward sweep and on the bit length of b, not directly on enumerating every coefficient `0..2b−2`. Worst-case interval count is *not* claimed bounded independently of period p.

## Reproduction and exact finite scope

Run `bash calculation/decimal_frontier/lattice_formats/code/agent16_interval_run.sh /tmp/a16-interval` from the repository root. This calls the self-contained script `agent16_interval_preimage.py`, its independent `agent16_interval_independent.py` checker, and an included standalone C++ full-root graph-control engine. The independent implementation performs direct integer-state elimination at **every temporal suffix**, rather than calling the interval preimage formula, and matches 7000 seeded random `(b,p,L,H,Y)` cases with b2..21 and p1..10. An independent all-start temporal-carry DFS matches the interval-accelerated successor enumeration for all six boundary parents at r4..6.

**COMPUTED demonstration, finite scope only.** For the diagonal `b=2^(r+1)`, `g=1 0^r 11 0^(r+1)`, take six explicit boundary parents `S(r,s,j,u,v)` with parameters `(0,r−2,0,1)`, `(0,r−2,1,1)`, `(0,r−1,1,0)`, `(0,r−1,1,1)`, `(1,r−1,0,0)`, `(1,r−1,1,0)` as defined in the executable. The indicated candidate initial coefficients yield 4,4,8,8,4,4 successor states. For every `r=4..200` and separately `r=500,1000`, each of these 32 explicitly generated successors has `D_0=empty`, with no temporal closure assumption, and the backward sweep uses at most three intervals. The first-empty indices are 0 for 16 states, r+1 for 8, r+2 for 8. The candidate starting-coefficient catalogue is **not independently proved exhaustive for all r**, nor are the six parents proved to exhaust all root-reachable cuts. Consequently, this demonstration is **not** an all-r acyclicity proof; that F2 task remains UNDECIDED.

**Positive controls:** copied standalone `agent16_interval_controls.cpp` reproduces base9 `g=1100011000` (956310 vertices, two depth61 size4 SCCs) and base13 `g=1010010000` (250302 vertices, depth55 and depth75 singleton SCCs). The script checks exact output lines. Neither the theorem nor the finite controls prove any base10 Lychrel number or a 196 outcome.
