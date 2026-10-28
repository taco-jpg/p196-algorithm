# Parametric root-column closure for a family of overflow schedules

**PAPER PROOF.** Let `r>=1`, `a=2^r`, `p=2r+4`, and
`g_r=1 0^r 11 0^(r+1)`, indexed from t=0. We classify **only** a
closed first-coordinate transition of the `bauto3` canonical root
`L=0, H=g, Y=1` for bases b>=2, not a reachable SCC or a Lychrel orbit.

Pair coefficients `x_t in [0,2b-2]` satisfy `x_p=x_0`, first coefficient
`x_0>=1`, and bits `c_t in {0,1}` satisfy the exact root equations
`floor((x_t+c_t)/b)=g_t` and
`x_(t+1)=x_t%b+(1 if g_t=1 else (x_t+c_t)%b)`.

**Forced middle.** The consecutive 1s at t=r+1,r+2 followed by 0 force
`x_(r+1)=b-1`, `c_(r+1)=1`, `x_(r+2)=b`, `x_(r+3)=1`:
indeed `x_(r+2)=(x_(r+1)%b)+1` is at most b and must be at least b-1.
If it were b-1 then `c_(r+2)=1` would make the next coefficient b,
contradicting the following zero. Thus it equals b, and the preceding
coefficient must be b-1 (not 2b-1, beyond the pair-sum range).
The first 1 followed by 0 similarly forces `x_0>=b` and
`x_1=x_0-b+1` (otherwise x_1=b, contradicting the next zero).

**Zero blocks.** Let `U` be the integer encoded by the r carry bits
`c_1,...,c_r` (most-significant bit first), so `0<=U<a` and
`b-1=x_(r+1)=a*x_1+U`.
Let `V` be the integer encoded by the r+1 carry bits
`c_(r+3),...,c_(p-1)`, so `0<=V<2a` and
`x_0=x_p=2a+V`.
Eliminating x_0 and x_1 gives
`(a+1)b = 2a^2+aV+a+1+U`, equivalently
`b = 2a+V-1+(U-V+2)/(a+1)`.
Thus `U-V+2` must be a multiple of `a+1`.
Its range is `[3-2a,a+1]`, so only the values `+(a+1)`, 0,
`-(a+1)` are possible.

**All admissible cases.** Exactly one of the following holds:
- `U=a-1, V=0`: `b=2a`, `x_0=b`.
- `U=u, V=u+2`, `0<=u<a`: `b=2a+u+1`, `x_0=b+1`.
- `U=u, V=u+a+3`, `0<=u<=a-4`: `b=3a+u+1`, `x_0=b+2`.
The last case exists iff a>=4. For a=2 (r=1) these give b=4,5,6;
for a>=4 they give every integer b in `[2a,4a-3]`.
All cases have b>=4 and `b<=x_0<=b+2<=2b-2`.
Reversing the formulas for x_1, the two zero blocks and the forced
middle shows all required zero-overflow carry inequalities hold:
each block doubles nonnegative coefficients with bits, terminating at
b-1 (first block) or x_0<=2b-2 (second block).
Hence all three cases are sufficient, not merely necessary.

**Multiplicity and rotations.** U and V uniquely fix all carries except
`c_0` and `c_(r+2)`; those two are arbitrary because their coefficient
is at least b. Thus there are exactly four carry assignments per base.
Every coefficient in a valid trajectory is positive. Therefore cyclic
rotation gives solutions for every time rotation, and any solution of a
rotated word rotates back to the fixed word (the first bit is 1, so its
coefficient is at least b-1). The same classification applies to all p rotations.

**Independent controls.** `python3 calculation/decimal_frontier/lattice_formats/code/agent16_param_f1.py`
uses bit-by-bit dynamic programming, not this congruence proof, to count
all canonical-root paths for r=1..7, every base b=2..2^(r+2)+3,
and every rotation. All tests passed with four or zero paths as stated.
The process uses a resumable local checkpoint (default `/tmp/`), not
repository evidence. The proof covers *all* r and bases with no state cap.
No other schedule, exterior B-cycle, certificate, or decimal result is claimed.
