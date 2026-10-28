# A mod-3 obstruction for the two-step neutral exterior

**PAPER PROOF** (not Lean-verified). For every integer base `b>=2` satisfying
`b ≡ 1 (mod 3)`, the exact period-two position automaton for cyclic overflow
word `g=01` has no neutral-band accepting cut state reachable from the
canonical root, at any B-width. This includes all even bases `b≡4 (mod 6)`;
the prior odd-base exclusion was independent of this congruence. Combining
the two theorems, a **necessary** condition for this g=01 neutral exterior
is `b≡0 or 2 (mod 6)`. It is not sufficient; no Lychrel conclusion follows.

## Exact arithmetic

Write the cut-state bits as `(l0,l1),(h0,h1)` and digit `y` (0<=y<b).
For a legal column let `x0,x1` be the temporal pair coefficients,
`c0,c1` the freely chosen high carries, and `a,e` the new low carries:

    x1 = (x0+l0) mod b + (x0+c0) mod b
    x0 = (x1+l1) mod b + y
    h0 = floor((x0+c0)/b), h1=floor((x1+c1)/b)
    a  = floor((x0+l0)/b), e=floor((x1+l1)/b)
    (l'0,l'1)=(a,e), (h'0,h'1)=(c0,c1), y'=(x1+c1) mod b.

The proven one-carry invariant for this g=01 system implies `a+e=1`
for the root transition and every subsequently reachable column.
Direct substitution (without modular assumptions) gives

    y' = b*(a+h0+2*e-h1) -l0 -2*l1 -c0+c1 -2*y.

When `b≡1 (mod3)`, using `-2≡1`, `a+e=1`, and
`K=l0+l1`, this is equivalent modulo 3 to

    y' - y ≡ (1-K)+(e-l1)+(h0-h1)-(c0-c1).

Define the scalar cut-state charge

    I(L,H,y) = y - l1 + h0 - h1   (mod 3).

Then every legal reachable transition satisfies
`I(next)-I(current) ≡ 1-K (mod3)`. The root has
`(L,H,y)=((0,0),(0,1),1)`, hence `I(root)=0` and `K=0`.
Its first successor has `I=1`. At every later state `K=1` by the
one-carry invariant, so **all positive-depth reachable states have I=1**.

Acceptance requires `l0+h0=l1+h1=1` and `y=(b-1)*l1`.
The only candidates with one low carry are

* `A`: L=(0,1), H=(1,0), y=b-1; its charge is `I=0` because
  `b-1≡0 (mod3)`.
* `B`: L=(1,0), H=(0,1), y=0; its charge is `I=-1≡2`.

Neither candidate has charge 1, and the root is not accepting.
Therefore no accepting state is reachable at any width. Cyclic
rotation of the temporal overflow word gives the equivalent `g=10` result.

## Exact finite checks (not the proof)

Run `python3 calculation/decimal_frontier/lattice_formats/code/agent10_g01_mod3_check.py`.
The independent digit-level enumerator checks every legal transition
from every one-carry cut state (plus the root) for bases
`b=4,7,...,100`: 13,860 edge checks, no violation, and the two
acceptance charges are rejected. Before the census the generic program
reproduced the mandatory b9 period-10 m=4 control at depth 61 and
b13 period-10 fixed-point controls at depths 55 and 75.