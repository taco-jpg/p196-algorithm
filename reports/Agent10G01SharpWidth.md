# Sharp universal exterior-width bound for the period-two overflow word 01

**PAPER PROOF** (not Lean-verified). For every integer base `b >= 2`, suppose
an exact canonical-root neutral-band exterior position automaton with cyclic
overflow word `g=(0,1)` reaches an accepting cut in `m >= 2` spatial columns.
Then

    b <= B(m) := 3*2^(m-1)-4.

This is **sharp for every m >= 2**: at base `b=B(m)` the first accepting
cut is reached at **exactly** width `m`. Thus the infinite exterior family
`b_k=3*2^k-4` of commit `bcb3be6` has provably minimum width `k+1`, not
merely the previously known attainable width. Cyclic rotation of g is time
reindexing. This is about exterior B-cycles, **not** centres or Lychrel
numbers; in particular nothing here proves that 196 is Lychrel.

## 1. Complete two-time column equations

A cut state `(L,H,y)` has low/high carry bits `l_t=(L>>t)&1`,
`h_t=(H>>t)&1` for `t=0,1` and one overflow partner digit `0<=y<b`.
The canonical root is `(L,H,y)=(0,2,1)`. For a column of coefficients
`0<=x0,x1<=2b-2` and free upper carries `c0,c1 in {0,1}`:

    h0 = (x0+c0)//b,                 h1 = (x1+c1)//b,
    x1 = (x0+l0)%b + (x0+c0)%b,    x0 = (x1+l1)%b + y,
    a = (x0+l0)//b,                 e = (x1+l1)//b,
    (L',H',y') = (a+2e,c0+2c1,(x1+c1)%b).

At the first column `x0>=1`. An accepting cut has
`l0+h0=l1+h1=1` and `y=(b-1)*l1`. Since every positive-depth
reachable L is one-hot (proved next), the only accepting states are

    T0=(1,2,0),      T1=(2,1,b-1).

**One-carry lemma, including the root.** Put `s=l0+l1`, which is 0 at
the root (where `y=1`) or 1 after it. The two displayed coefficient
equations imply

    x0 = b*(a+h0+e) - (s+c0+y).

As `x0+l0` and `x1+l1` are below `2b`, each of `a,e` is 0 or 1.
If `a+e=0` and `h0=0`, this gives `x0<=0`, contrary to `s=1`
or to the first-column positivity at the root. If `a+e=0,h0=1`,
then `x0+c0=b-(s+y)<b`, contradicting `h0=1`.
If `a+e=2,h0=1`, `x0=3b-(s+c0+y)>=2b-1>2b-2`.
If `a+e=2,h0=0`, `x0+c0=2b-(s+y)>=b`, contradicting `h0=0`.
Therefore `a+e=1` always: `L'=1` or `2`, and each reachable cut after
the root is indeed one-hot. The exact necessary `x0` formula is

    x0=b*(1+h0)-(s+c0+y).

Both reproduction programs separately check the unshortened equations.

## 2. Four-state corridor lemma (all integer bases)

Write `f=(1,0,2,1)` and `q=(-2,-3,-1,-2)` indexed by `h=0,1,2,3`.
For `A>=3`, define the complete four-state sets

    O_A = {(2,h,b-A+f[h]) : h=0,1,2,3},
    E_A = {(1,h,A+q[h])   : h=0,1,2,3}.

When `b>=4A-4`, all states have legal `0<=y<b` and the EXACT
non-first-column successor sets are

    Succ(O_A) = E_(2A),    Succ(E_A) = O_(2A).

These are equalities, not subset or overapproximation statements.
To check them, substitute each of the four values of `h` and both
values of `c0` into the necessary `x0` formula, then test the four
original carry/equality equations and `c1=0,1`. The only productive
source in `O_A` is `h=1`; its `c0=0,1`, `c1=0,1` successors have
`L'=1`, `H'=c0+2c1` and respective
`y'=2A-2,2A-3,2A-1,2A-2` (ordered by H'=0,1,2,3).
The only productive source in `E_A` is `h=2`; its four successors
have `L'=2`, `H'=c0+2c1` and respective
`y'=b-2A+1,b-2A,b-2A+2,b-2A+1`.
All other sources fail either the required `h_t` or the one-carry
lemma. Every listed edge satisfies the original equations: for the
productive `O_A` source the two `x1` choices are `2A-2,2A-3`;
for the productive `E_A` source they are `2b-2A+1,2b-2A`.
The inequality `b>=4A-4` ensures every carry and bound used here.

At the canonical root, for every `b>=3`, exact first-column enumeration
gives `Succ(root)=O_3` (and for `b=2` it gives two members of `O_3`).
Thus as long as the size inequality holds, spatial layers alternate:

    layer j (j odd):  O_(3*2^(j-1)),
    layer j (j even): E_(3*2^(j-1)).

No state in these sets is accepting (`O` has the required H=1 only
at `y=b-A != b-1`; `E` has the required H=2 only at
`y=A-1 != 0`).

## 3. Terminal predecessor lemma (sharp cutoff)

For `A>=3`, among the four states `O_A`, a transition into either
accepted state `T0,T1` is possible at `b>=2A-4` **only when**
`b=2A-4`, from `(2,0,b-A+1)` to `T1`. In fact `T0` is impossible
since its outgoing `e=0` conflicts with `x1=b-1,l1=1`; for `T1`
we have `c0=1,c1=0`, and `y'=b-1` forces `x1=b-1`.
Then the carry equations require input `H=0`, giving
`x0=A-3`, `x1=2A-5` and hence `b=2A-4`.

Among the four states `E_A`, an accepting transition is possible
at `b>=2A-4` only at `b=2A-4`, from `(1,3,A-2)` to `T0`.
`T1` is impossible because `x1=b-1,l1=0` forces `e=0`, not 1.
For `T0`, `c0=0,c1=1` and `y'=0` force `x1=b-1`;
`H=3` and the coefficient equations give `x1=2b-2A+3`,
so `b=2A-4`. The alternative `H=1` has `h1=0`, incompatible
with `x1+c1=b`. This covers every accepting transition with the
original exact carry equations; no assumption about later states.

## 4. All-base sharpness, including small widths

Fix any `m>=3` and suppose `b>B(m)=3*2^(m-1)-4`.
At every prior corridor step `j=1,...,m-2`, its parameter is
`A=3*2^(j-1)` and the required inequality
`b>=4A-4` holds, because the largest right-hand side is `B(m)`.
The complete layer at depth `m-1` is therefore `O_A` or `E_A`
with `A=3*2^(m-2)`, and no earlier layer accepts.
The terminal lemma rules out acceptance at depth `m`, since
`b>2A-4=B(m)`. Hence acceptance at width <=m implies `b<=B(m)`.
The case `m=2` follows directly from the root `O_3` and terminal
lemma: only `b=2` can accept at width 2.

For `b=B(m)` with `m>=3`, exactly the same corridor equality holds
through depth `m-1`, and the terminal lemma gives the single final
accepting transition. Thus its FIRST accepted width is exactly m.
For `m=2,b=2`, the exact two-column control is

    (0,2,1) -> (2,0,0) -> (2,1,1).

This establishes the global all-base bound AND its equality case
for every `m>=2`, not merely a finite computation.

## 5. Full reproduction, independent checker, and positive controls

From the repository root:

    python3 calculation/decimal_frontier/lattice_formats/code/agent10_g01_sharp_width.py --prove 512
    python3 calculation/decimal_frontier/lattice_formats/code/agent10_g01_sharp_width_independent.py
    python3 calculation/decimal_frontier/lattice_formats/code/agent10_g01_sharp_width.py --controls

The first executable evaluates every symbolic corridor/terminal column
via exact integers at m=2..512, with large-base adjacent exclusions and
generic A,b inequality controls. The INDEPENDENT verifier enumerates
all actual coefficient `x0` and carries (`c0,c1`) with NO one-carry
lemma, affine shortcut, or imported primary function: fully checks
b=2..256 through width 8, the equality and next-base exclusions
m=2..10 and the positive base-26 g=01 depth-8 exterior.
`--controls` compiles the already-tracked `bauto3.cpp` and independently
reproduces mandatory base 9 `g=1100011000` spatial period 4 at depth 61,
and base 13 `g=1010010000` singleton SCC depths 55 and 75. The theorem
is proved algebraically; test ranges are regressions, not the source
of the all-m conclusion.

Scope: canonical-root, period-two g=01, the neutral exterior only.
No statement about nonneutral bands, centres, arbitrary overflow words,
base-10 Lychrel numbers, or Lean verification.
