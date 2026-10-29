# An all-parameter no-edge theorem for an interior family of diagonal lattice cuts

**PAPER PROOF** (uncapped, all integer `r >= 4`). Fix `b=2^(r+1)`, `p=2r+4`, and the time-rooted overflow word
`g = 1 0^r 11 0^(r+1)`, with ones at times `0,r+1,r+2`. Pair coefficients
`x_t` are integers in `[0,2b-2]`; `c_t` is a bit. At a cut state `(L,H,Y)`,
its outgoing first-column transition would have to satisfy, for every `t mod p`,

    floor((x_t+c_t)/b)=H_t,
    x_(t+1)=((x_t+L_t) mod b) + (g_t ? Y_t : ((x_t+c_t) mod b)),
    x_p=x_0.

The exact state family `S(r,s,j,u,v)` has independent bits `s,u,v ∈ {0,1}` and integer `0<=j<=r-3`:

    L = 1^(r+2) 0 1^(j+1) 0^(r-j),
    H = (s ? 1^(j+1) : 0 1^j) 0^(r-j) u v 1^r 0,
    Y_(0)   = b-2+s,
    Y_(r+1) = b-2^(r-j)-1+u,
    Y_(r+2) = b-2^(r-j)-1+v.

All these vectors have length exactly `p`. There are `8(r-2)` such states. This theorem is a statement about the **explicit state family**, without an assumption or claim that the family exhausts the reachable automaton at all `r`.

## Exact argument

Set `a=2^(r-j)`, `T=r+3`, `m=j+1`; then `2^m a = b` and `2^m<=b/8`.
Throughout times `T,...,2r+2`, `H_t=1`. For times `T,...,T+m-1`, `L_t=1`; afterwards, through time `p-1`, `L_t=0`.

1. At the two preceding overflow times, the exact transition yields
   `x_T = (x_(r+2) mod b)+Y_(r+2) <= (b-1)+(b-a-1+v) <= 2b-a-1`.
   Thus the deficit `D_T=2b-x_T` is at least `a+1`.
2. For each of the next `m` zero-overflow steps, `H_t=H_(t+1)=L_t=1`.
   The edge case `x_t=b-1` would require `c_t=1` and make `x_(t+1)=0`,
   contradicting the next `H=1`. Therefore `x_t>=b`, and direct substitution gives
   `D_(t+1)=2D_t-1-c_t >= 2D_t-2`.
   Iterating all `m` steps proves
   `D_(T+m) >= 2^m(a-1)+2 = b-2^m+2 >= 7b/8+2`,
   hence `x_(T+m) <= 9b/8-2`.
3. Time `T+m` still has `H=1` but `L=0`, and the **following** time also has `H=1` because `j<=r-3`.
   If `x_(T+m)>=b`, the next step is at most
   `2(x_(T+m)-b)+1 <= b/4-3 < b-1`, impossible for the following `H=1`.
   The only remaining integer possibility consistent with `H=1` is
   `x_(T+m)=b-1`, where `c_(T+m)=1`.
4. At `x=b-1`, `H=1` and `L=0`, the next coefficient is again `b-1`.
   This repeats through time `2r+2` (all `H=1`), so the final input
   `x_(p-1)=b-1`. At time `p-1`, `H=L=0` forces `c_(p-1)=0`, and
   `x_p=2b-2`. Closure forces `x_0=2b-2`.
5. If `s=0`, then `H_0=0`, immediately contradicting `x_0>=b`.
   If `s=1`, then `H_0=L_0=1` and `Y_0=b-1`, so the first overflow step gives
   `x_1=((2b-2+1) mod b)+(b-1)=2b-2`. The first `j` zero steps
   have `H_t=L_t=1` for `t=1,...,j`, followed by `H_(j+1)=0`.
   Starting `D_1=2`, the recurrence there gives `D_(t+1)<=2D_t-1`,
   therefore `D_(j+1)<=2^j+1 <= b/16+1 < b` (also valid when `j=0`).
   Hence `x_(j+1)>b`, contradicting `H_(j+1)=0`.

Both cases contradict existence of an outgoing edge. Every inequality holds for **all** `r>=4`, with no finite-search cap. QED.

## Reproducing controls (COMPUTED, not a substitute for the proof)

From the repository root:

    bash calculation/decimal_frontier/lattice_formats/code/agent16_interior_run.sh /tmp/a16-interior

The script compiles the standalone exact C++ temporal-column DFS, tests all `8(r-2)` claimed no-edge states in **every r=4..12**, and checks the six positive boundary cases `j=r-2,r-1` (32 exact carry paths, not part of the negative theorem). A separate Python implementation exhaustively counts each input coefficient/carry history for `r=4..7` and checks the proof inequalities for sample `r` up to 1024. Finally it recompiles the earlier independent full-root C++ enumerator and reproduces the mandatory **base-9, `g=1100011000`** (956310 reachable states, seven cyclic SCCs, two depth-61 period-4 SCCs) and **base-13, `g=1010010000`** (250302 states, five cyclic SCCs, depths 55/75) controls.

All four test families are independent of any unproved claim that the depth-four templates exhaust every reachable cut. The `j=r-2,r-1` states, the 32 empirically observed deeper leaves, the whole rooted graph, other bases/schedules, and a decimal Lychrel certificate are **not** decided by this result.
