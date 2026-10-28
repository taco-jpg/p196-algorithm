# Exact all-base canonical-root F1 classification for `101100`

**PAPER PROOF.** This concerns *only* a possible first spatial-column transition
from `bauto3.cpp`'s canonical root `L=0, H=g, Y=1`, with a closed
period-six time trajectory. It does not assert a reachable exterior cycle.
All coefficients below are pair sums (`0 <= x_t <= 2b-2`), not ordinary digits.

For `g=(1,0,1,1,0,0)`, let `c_t` denote the guessed outgoing upper carry.
The exact root constraints are `(x_t+c_t)//b=g_t`, `c_t in {0,1}`, and
`x_(t+1)=(x_t mod b)+(1 if g_t=1 else (x_t+c_t) mod b)`, with `x_6=x_0`.
We also require `1 <= x_0 <= 2b-2` (the engine's first-column restriction).

**Necessity.** Since `g_2=g_3=1`, `x_3=(x_2 mod b)+1` lies between
`b-1` and `b`: otherwise `x_3+c_3 < b`. If `x_3=b-1`, then
`c_3=1` and `x_4=b`, contradicting `g_4=0`. Hence `x_3=b` and
`x_2 mod b=b-1`. Since `x_2 <= 2b-2` and `g_2=1`, this forces
`x_2=b-1`, `c_2=1`, and `x_4=1`.
Because `g_0=1` but `g_1=0`, `x_0=b-1` is impossible (it would make
`x_1=b`); therefore `x_0>=b` and `x_1=x_0-b+1`.
At the three zero-carry times,
`x_2=2x_1+c_1=b-1`, `x_5=2+c_4`, and
`x_0=2x_5+c_5=4+2c_4+c_5`.
Eliminating `x_0,x_1` yields `3b=11+4c_4+2c_5+c_1`.
Because the three carries are bits, the RHS lies in `[11,18]`,
so `b in {4,5,6}`. The only carry triples `(c_1,c_4,c_5)` are
`(1,0,0)` for b=4, `(0,1,0)` for b=5, `(1,1,1)` for b=6.

**Sufficiency and count.** Substitution gives the three trajectories
`b=4: (4,1,3,4,1,2)`, `b=5: (6,2,4,5,1,3)`,
`b=6: (7,2,5,6,1,3)`. Each satisfies every root constraint.
The bit `c_2=1` is forced. The bits `c_0` and `c_3` are each free
because `x_0>=b` and `x_3=b`; all other carries are uniquely fixed.
Thus each base has exactly 4 full time-closed root paths.

**Time rotation.** Each coefficient in all three trajectories is positive;
rotating a trajectory and its carry bits yields a legal canonical-root
trajectory for each of the other five cyclic shifts of `101100`.
Conversely every rotated solution can be rotated back: the coefficient
at any time whose overflow bit is 1 is at least `b-1>=1`, so the
engine's first-column positivity restriction remains satisfied.
Hence the classification applies to all six time rotations.

**Independent check (COMPUTED control, not exhaustive evidence for the theorem).**
`python3 calculation/decimal_frontier/lattice_formats/code/agent16_base4_f1.py`
enumerates each initial coefficient and all 64 carry patterns for every
base 2..200 and all six time rotations. It checks exactly 4 paths at
b=4,5,6 and 0 at every other tested base, matching the proof.
The theoretical base range is *unbounded* and uses no search cap.
No other overflow word, spatial coordinate, SCC, or Lychrel outcome is claimed.
