# A constructive infinite family of period-two neutral exteriors

**PAPER PROOF** (not Lean-verified). For every integer `k >= 1`, set
`b = 3 * 2^k - 4`. The base-`b` exact neutral-band position automaton for
cyclic overflow word `g = 01` has a path of precisely `k+1` spatial columns
from its canonical root to a neutral-band accepting cut. Thus it admits
an exterior `B` cycle of this width. This is an **infinite family of
neutral exteriors**, not of full reverse-add/Lychrel certificates: no
periodic centre is constructed.

## Exact one-column transition (source of the theorem)

A cut has `L=l0+2*l1`, `H=h0+2*h1` (carry bits) and `Y=y` (the overflow
partner digit at time 1). Given a two-time closed coefficient column
`(x0,x1)` and guessed upper carries `c0,c1 in {0,1}`, the exact conditions
for `g=(0,1)` are

    0 <= x0,x1 <= 2*b-2,   x0 >= 1 at the first column,
    (x0+c0)//b = h0,      (x1+c1)//b = h1,
    x1 = ((x0+l0) % b) + ((x0+c0) % b),
    x0 = ((x1+l1) % b) + y.

The new cut is

    L' = (x0+l0)//b + 2*((x1+l1)//b),
    H' = c0 + 2*c1,      y' = (x1+c1) % b.

The canonical root is `R=(0,2,1)`. An accepting cut satisfies `L+H=3`
bitwise (each low/high time carry sums to 1) and `y=(b-1)*l1`.
In particular `T_even=(1,2,0)` and `T_odd=(2,1,b-1)` are accepting.

## Parametric cut states and columns

Let `A_j=3*4^j`, `O_j=(2,1,b-A_j)` and
`E_(j+1)=(1,2,2*A_j-1)`. In the following table a column is written
`(x0,x1;c0,c1)`; all quantities are exact integers.

| From | Column | To | Usage |
|---|---|---|---|
| R | `(b-2,2*b-3;1,0)` | `O_0` | `k>=2` |
| `O_j` | `(b+A_j-1,2*A_j-2;0,1)` | `E_(j+1)` | interior |
| `E_(j+1)` | `(b-2*A_j-1,2*b-4*A_j;1,0)` | `O_(j+1)` | interior |
| `O_(r-1)` | `(b+A-2,2*A-3;1,1)` | `Q_e=(1,3,b/2)` | even `k=2r`, `A=A_(r-1)` |
| `Q_e` | `(3*b/2-1,b-1;0,1)` | `T_even` | even terminal |
| `E_r` | `(b-2*A,2*b-4*A+1;0,0)` | `Q_o=(2,0,b/2-1)` | odd `k=2r+1>=3`, `A=A_(r-1)` |
| `Q_o` | `(b/2-1,b-1;1,0)` | `T_odd` | odd terminal |

For `k=1`, `b=2`, use instead

    R --(1,2;0,0)--> Q_o=(2,0,0)
      --(0,1;1,0)--> T_odd=(2,1,1).

For **even** `k=2r>=2`, concatenate

    R -> O_0; for j=0..r-2: O_j -> E_(j+1) -> O_(j+1);
    O_(r-1) -> Q_e -> T_even.

For **odd** `k=2r+1>=3`, concatenate

    R -> O_0; for j=0..r-1: O_j -> E_(j+1),
    followed by E_(j+1) -> O_(j+1) only when j<r-1;
    E_r -> Q_o -> T_odd.

Both have precisely `k+1` columns. The first x0 is positive (`b-2`
for `k>=2`; 1 for `k=1`), so the exterior is canonical.

## Verification of the table and all-parameter validity

Substitution into the four transition equations verifies every row.
For example `O_j -> E_(j+1)` has `x0=b+A_j-1`, `x1=2*A_j-2`;
its lower-time carry is 1, upper-time carry 0, and the next carry bits
are `L'=1`, `H'=2`, with `y'=2*A_j-1` exactly as specified. Similarly
`E_(j+1) -> O_(j+1)` has `L'=2`, `H'=1`, `y'=b-4*A_j`.

All interval and carry constraints are uniform in `k`:
- Every nonterminal interior `E_(j+1)->O_(j+1)` occurs with
  `b>=16*A_j-4>=4*A_j` since `A_j>=3`.
- Every interior `O_j->E_(j+1)` occurs with `b>=8*A_j-4`, hence
  `0<2*A_j-1<b` and `b+A_j-1<=2*b-2`.
- On the even terminal pair, `b=4*A-4` (`A>=3`), making
  `2*A-2=b/2` and all four relevant coefficients lie in `0..2*b-2`.
- On the odd terminal pair, `b=8*A-4` (`A>=3`), making
  `b-4*A+1=b/2-1` and the same bounds hold.
- For `k=1` the two displayed columns satisfy every equation directly.

Hence each displayed path exists **for every** `k>=1`. Inserting its
`k+1` time-periodic coefficient columns reconstructs two exterior
blocks whose overflow word is `01`; the accepted cut allows a neutral
interior band. The conclusion is precisely the claimed exterior
existence, with no assertion that the centre is periodic or nonpalindromic.

## Reproduction and independent checks

The standalone script
`calculation/decimal_frontier/lattice_formats/code/agent10_g01_infinite_family.py`
generates the exact symbolic path and validates every integer floor,
modulus, carry and column equation for `k=1..N`:

    python3 calculation/decimal_frontier/lattice_formats/code/agent10_g01_infinite_family.py 1000

Passed for `N=1000` (last base has 302 decimal digits, path length 1001),
with independent full `(a,e,c0)` enumerator checks of each edge for
`k=1..20` and a separate O(b) all-reachable-state engine confirming first
ACCEPT depth `k+1` for `k=1..15`. Mandatory existing general engine controls
were reproduced: base 9 `g=1100011000` gives 956,310 reachable states,
7 nontrivial SCCs and m=4 at width 61; base 13 `g=1010010000` gives
250,302 reachable states, 5 SCCs and fixed SCCs at widths 55/75;
base 26 `g=01` accepts at width 8.

**Scope:** This is a new all-parameter PAPER PROOF about neutral exterior
cycles, not a family of complete Lychrel certificates, not a decimal
certificate, and not a claim about the integer 196. The existence of
periodic centres for this family remains UNDECIDED.