# Two spatial transitions for an infinite power-of-two schedule family

**PAPER PROOF.** Put `r>=1`, `b=2^(r+1)`, `p=2r+4`, and
`g=1 0^r 11 0^(r+1)`. We exhibit four exact *two-edge paths* from the
canonical root `(L,H,Y)=(0,g,1)` of the `bauto3` position automaton.
This is not a claim about SCCs, arbitrary spatial depth, or an infinite orbit.

At a position with state `(L,H,Y)` (L,H are time-indexed carry bits,
Y_t is defined only for g_t=1), the exact transition requirements are
`floor((x_t+c_t)/b)=H_t` and
`x_(t+1)=((x_t+L_t) mod b)+(Y_t if g_t else ((x_t+c_t) mod b))`,
where `c_t in {0,1}`, `x_p=x_0`, and `0<=x_t<=2b-2`.
The resulting state is `L'_t=floor((x_t+L_t)/b)`, `H'_t=c_t`, and
`Y'_t=(x_t+c_t) mod b` for g_t=1. The first edge requires x_0>=1.

**First edge (two choices).** For each `m in {0,1}`, use the same
pair-coefficient time trajectory
`x=[b] ++ [2^t-1: t=1..r+1] ++ [b] ++ [2^k: k=0..r]`
and carry list `c=[m] ++ [1]^(r+1) ++ [m] ++ [0]^(r+1)`.
Both satisfy the canonical-root transition equations and cyclic closure.
The successor state has L=1 exactly at times 0 and r+2,
H=c, and Y=(m,0,m) at the three overflow times 0,r+1,r+2.

**Second edge (two more choices for each m).** Fix `f in {0,1}`.
For m=0 set
`x=[b-2] ++ [b-1]^(r+2) ++ [0] ++ [2^k-1: k=1..r]`,
`c=[f] ++ [1]^(r+1) ++ [0] ++ [1]^r ++ [0]`.
For m=1 set
`x=[2b-3] ++ [b-1]^(r+2) ++ [2^(k+1)-1: k=0..r-1] ++ [b-2]`,
`c=[f] ++ [1]^(2r+1) ++ [0,1]`.
All lists have exactly p entries. Direct substitution into the two
transition equations gives the next listed x at every time and returns
to the first at time p. The carry constraints hold at every time:
on zero-overflow steps they are simple doubling identities, and at
three overflow steps the input Y values are respectively m,0,m.
All pair coefficients stay within [0,2b-2], for all r>=1.
The values of f give different second-edge H' words, and the values
of m give different first-edge H' words, hence four distinct two-edge paths.

**Independent check.** The standalone script
`python3 calculation/decimal_frontier/lattice_formats/code/agent16_two_column_family.py`
constructs all four paths directly and checks *every* exact transition
and coefficient bound for r=1..100 (all passed). This finite control
supports, but is not substituted for, the all-parameter algebra above.
Nothing here asserts a full spatial periodic cycle, decimal nonpalindromicity,
or a base-10 Lychrel number.
