# Agent-14: a no-go for physically aligned complement-twisted centre returns

**PAPER PROOF.** Scope: precisely the four stored reachable base-10 absorbing
lattice SCCs (period-8 `10101010`, rec0 and rec1 with spatial period 20,
rec2 with spatial period 48; period-12 `100010001000` with spatial period 9).
No parity-preserving time advance can carry any one complete lattice row to
its coefficient-wise complement under the actual shift of the number's centre.
This rules out a uniform, parity-preserving *complement-twisted return* for
any centre half-width, not arbitrary finite centres or arbitrary temporal cycles.

For a lattice with overflow word `g` of period `p`, spatial rows `W[t][j]`
of period `m`, and a start at phase `t`, let
`G(t,d) = sum(g[(t+i)%p] for i=0..d-1)`. If `G` is even, the centre's
coordinate increases by exactly `G/2` during `d` steps, independent of
starting parity. A complement-twisted return (same length parity) would require

    W[(t+d)%p][(j+G(t,d)/2)%m] = 18 - W[t][j]     for every j.

This is necessary regardless of the finite core's width: sufficiently far
from the centre, both pair words must equal the prescribed periodic bulk.
For any phase `t`, advancing by `L = p*(2*m/gcd(2*m,S))` steps, with
`S=sum(g)`, preserves the time phase and adds a multiple of `2m` to `G`.
Thus the equation for *every positive d* reduces exactly to `1 <= d <= L`.
The executable checker below enumerates all `p*L` pairs `(t,d)`, filters
exactly those with even `G`, and counts exact row mismatches. It has no
state cap and proves the finite test exhaustive once the stored rows are fixed.

| Lattice | m | L | Even-G cases | Least mismatches | Exact complements |
|---|---:|---:|---:|---:|---:|
| p8 rec0 | 20 | 80 | 320 | 16 | 0 |
| p8 rec1 | 20 | 80 | 320 | 16 | 0 |
| p8 rec2 | 48 | 192 | 768 | 39 | 0 |
| p12 m9 | 9 | 72 | 432 | 7 | 0 |

The same checker finds only the `d=L` ordinary row returns in each
starting phase, supplying a positive control. There are no shorter ordinary
row returns either; the latter agrees with the previously published periods.

The complement operation is meaningful for the local carry-normalisation
rule: in base `b`, for pair coefficient `P` and incoming carry `c`, replace
them by `P*=2(b-1)-P` and `c*=1-c`. Writing `s=P+c`, the new sum satisfies
`s*=2b-1-s`; hence its output digit and carry are exactly complements of
the original output digit and carry. This is an *interior* conjugacy: the
canonical initial carry at the least-significant end must still be handled
by the exterior. The algebra explains why antiperiodic bulk symmetries are
worth testing, but none is aligned to the moving decimal centre here.

Reproduce from the repository root:

    python3 calculation/decimal_frontier/lattice_kinks/code/agent14_complement_twist.py

Input: `calculation/decimal_frontier/lattice_formats/p8_scc.txt` and
`calculation/decimal_frontier/lattice_kinks/data/lat_p12m9.txt`. The
script checks exact stored SCC words and the general complement/carry
identity for bases 2..32. No new exterior census or Lean file is claimed.
No base-10 nonpalindromic infinite orbit, impossibility of a finite
periodic centre, or claim about the orbit of 196 follows.