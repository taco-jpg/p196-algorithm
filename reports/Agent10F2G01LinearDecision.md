# Linear-state exact decision algorithm for the two-step overflow word 01

**PAPER PROOF** (not Lean-verified). For every integer base `b >= 2`,
reachability of a neutral-band exterior accepting cut state from the
canonical root of the exact position automaton for the period-two overflow
necklace `g=01` is decidable using at most `8b+1` visited states and at most
four candidate transitions per state, hence `O(b)` arithmetic operations
and `O(b)` words of memory. Each arithmetic operation involves `O(log b)`
bit integers. This theorem does not assert that a neutral centre closes, nor
that a Lychrel number exists in any particular base. It is not an all-base
closed-form classification of which b are accepted.

## Exact column equation and reduction

A cut state consists of carry bits `(l0,l1)`, `(h0,h1)` and a partner digit
`0<=y<b`. For a period-two column choose coefficients `x0,x1` in
`0..2b-2` and free high carries `c0,c1` in `{0,1}`. The exact equations are

    x1 = ((x0+l0) mod b) + ((x0+c0) mod b)
    x0 = ((x1+l1) mod b) + y
    h0 = floor((x0+c0)/b), h1 = floor((x1+c1)/b)
    a  = floor((x0+l0)/b), e = floor((x1+l1)/b)
    L' = (a,e), H' = (c0,c1), y'=(x1+c1) mod b.

The first position starts from `(L,H,y)=((0,0),(0,1),1)` and requires
`x0>0` (indeed also `x1>0`, which follows at this root). The accepted state
predicate is `l0+h0=l1+h1=1` and `y=(b-1)l1`.

The one-carry invariant (proved fully for all `b>=2` by the two strict
inequalities in `reports/Agent10F2OddBaseG01.md`) says the first column
has `a+e=1`, and every successor of a state with `l0+l1=1` also has
`a+e=1`. Thus the root is the only reachable `L=(0,0)` state and
`L=(1,1)` is never reachable. Every later state has one of exactly two
possible L values, four H values and b partner digits: at most `8b`
states, plus the root.

Expanding the two time equations, write
`x1=2*x0+l0+c0-b*(a+h0)` and `x0=x1+l1+y-b*e`. Hence

    x0 = b*(a+h0+e) - (l0+l1+c0+y)
       = b*(1+h0) - (l0+l1+c0+y),

using `a+e=1`. For any visited state and either choice of `c0`, this
produces the **only possible** `x0`, regardless of b. Test the exact
range, root-leading, h0, time-closure and pair-coefficient equations;
then for each `c1` test h1 and construct `(L',H',y')`.
There are at most `2*2=4` candidate edges from any visited state.

## Soundness and completeness

Every actual legal column satisfies the derived affine formula because
its output carries sum to one; it will therefore be enumerated under its
actual `c0,c1`. Conversely, each emitted edge passes all original exact
column equations and thus is a legal edge. Breadth-first traversal of
this graph finds an accepting state iff a neutral exterior B-cycle exists
for this overflow word at some width, by the exact position-automaton
acceptance correspondence stated in `calculation/decimal_frontier/exterior_census/EXTERIOR.md`.
A direct-address visitation array of `16b` bits/bytes and a queue of at
most `8b+1` states makes the entire decision finite and linear in b.

## Reproduction and safeguards

`calculation/decimal_frontier/lattice_formats/code/agent10_g01_even_fast.cpp`
is the executable exact affine BFS, with an append-only base-by-base CSV
checkpoint to resume a census without repeating completed bases.
`c++ -O3 -std=c++17 agent10_g01_even_fast.cpp -o /tmp/a10g01`;
`/tmp/a10g01 2 10000 /tmp/a10-g01.csv`.
The independent generic position automaton agrees on all 299 bases
`b=2..300`: visited-state counts and first accepting widths match exactly.
The specialized engine exhausted all bases `2..10000`: 1,710 of the 5,000
even bases have a reachable accepting cut state; all odd bases are negative,
in agreement with the earlier all-odd-base theorem. The positive control
`b=26` first accepts at width 8 (104 reachable states). This scan is a
finite control of the general algorithm, not an infinite-family theorem.
The generic engine also reproduces the mandatory base-9 and base-13
period-10 controls before this new census, as documented in the earlier result.