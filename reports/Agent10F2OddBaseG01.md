# Odd-base obstruction for the two-step overflow stream 01

**PAPER PROOF** (not Lean-verified). For every odd integer base `b >= 3`, the exact
position automaton for the two-step overflow word `g = 01` has no path from
its canonical root to a neutral-band accepting cut state, at any B-width.
The cyclic rotation `10` is covered by time reindexing. This excludes this
particular two-step neutral exterior, not other words, absorbing-lattice
bands, arbitrary formats, or Lychrel numbers.

## Column equations

Write the cut state `(L,H,y)` with bits `l0,l1` and `h0,h1` and one overflow
partner digit `0 <= y < b`. A position chooses pair coefficients
`0 <= x0,x1 <= 2b-2` and next high carries `c0,c1` in `{0,1}`. The exact
period-two column transition is

    x1 = ((x0+l0) mod b) + ((x0+c0) mod b),
    x0 = ((x1+l1) mod b) + y,
    ht = floor((xt+ct)/b),
    l't = floor((xt+lt)/b),  h't = ct,
    y' = (x1+c1) mod b.

The root is `(L,H,y)=(00,01,1)` (bits listed in temporal order), and the
first column has `x0 > 0`. Acceptance requires `l't+h't=1` for both times,
and `y'=(b-1)l'1`.

## The one-carry invariant

If `l0+l1=1`, then **every** legal successor also has `l'0+l'1=1`:

* If both new carries are zero, `x1 >= x0+l0`, whence
  `x1+l1 >= x0+1`. But the second equation has
  `x0=x1+l1+y >= x1+l1`, a contradiction.
* If both are one, `x1 <= x0+l0-1`, whence `x1+l1 <= x0`.
  The second equation then has `x0=x1+l1-b+y <= x1+l1-1`,
  again a contradiction.

At the root, `h0=0,l0=l1=0,y=1`. Two new carries of one are impossible
because `x0>=b` would contradict `h0=0`. Two zero carries would give
`x1=2x0+c0` and `x0=x1+1`, impossible for `x0>0`.
Consequently every positive-depth reachable state has **exactly one**
low carry: `L=01` or `L=10`; `L=00` occurs only at the root and `L=11`
never occurs.

## The only two possible accepting states

The complement condition leaves `A=(L=01,H=10,y=b-1)` and
`B=(L=10,H=01,y=0)` (bits in order `t=0,1`). The other two acceptance
patterns have `L=00` or `11`, already excluded.

For an incoming edge to `A`, the target requires
`l'0=0,l'1=1,c0=1,c1=0,y'=b-1`. Therefore `x1=b-1`,
`l1=1` and `x0=y`.

* If `x0=b-1`, then `l0=0`, and the predecessor is exactly `A`:
  its `H=10` and `y=b-1`, with a self-loop.
* Otherwise `x0<=b-2`, so `b-1=x1=2y+l0+1` and
  `2y+l0=b-2`. For odd `b`, `l0=1`; together with `l1=1`
  this would require an unreachable predecessor `L=11`.

For an incoming edge to `B`, the target requires
`l'0=1,l'1=0,c0=0,c1=1,y'=0`. Hence `x1=b-1`,
`l1=0`, and `x0=b-1+y`.

* If `y=0`, then `l0=1`; the predecessor is precisely `B`,
  which has a self-loop.
* Otherwise `x0>=b`, giving `b-1=x1=2y-2+l0` or
  `2y+l0=b+1`. For odd `b`, `l0=0`; hence the predecessor
  has `L=00` and must be the root. But it requires
  `y=(b+1)/2>=2`, whereas the root has `y=1`.

Thus neither `A` nor `B` has an incoming path from the root. The root
itself is not accepting. This proves the stated all-width obstruction.

## Computational controls

`calculation/decimal_frontier/lattice_formats/code/agent10_g01_odd_check.py`
independently enumerates every reachable cut state for odd bases
`3,5,...,301`, checks the one-carry invariant for every outgoing edge
from `L=01/10` for odd bases `3..51`, and reproduces the positive
base-26 `g=01` control (first ACCEPT at B-width 8, 104 states).
The generic exact SCC code also reproduced the independent mandatory
base-9 `1100011000` control (956310 states, 7 cyclic SCCs, m=4 at depth 61)
and base-13 `1010010000` (250302 states, 5 cyclic SCCs, fixed points at
widths 55 and 75) before this census. Finite tests are not the proof.