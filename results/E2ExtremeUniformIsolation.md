# E2ExtremeUniformIsolation

**PAPER PROOF.** For every base `b >= 2`, nonempty binary overflow word `g` of temporal length `p`, the uniform absorbing position-automaton cut states with constant coefficient `u=0` and `u=2b-2` each have exactly one predecessor: themselves.

Scope: all `b >= 2`, `p >= 1`, every `g`; no centre or nonuniform lattice is constrained, and no decimal Lychrel number is claimed.

At a predecessor column write `x_t` for its pair coefficient, `l_t` for its carry from below; `h'_t` is the carry demanded from above by the target. For `u=0`, the target has `L'=H'=0`, and overflow-time `Y'=0`. Thus `x_t+l_t < b`. At `g_t=0`, `x_{t+1}=2x_t+l_t >= x_t`, with equality only when `x_t=l_t=0`. At `g_t=1`, `(x_t+0)%b=0` and `x_t<b` force `x_t=0`; then `x_{t+1}=l_t+Y_t >= x_t`, with equality only when `l_t=Y_t=0`. The temporal trajectory is cyclic, so every inequality is equality; all `x,l,Y,H` are zero.

For `u=2b-2`, the target has `L'=H'=1` and overflow-time `Y'=b-1`, so `x_t+l_t >= b`, hence `x_t >= b-1`. At `g_t=1`, `(x_t+1)%b=b-1` forces `x_t=2b-2`; then `x_{t+1}=(b-2+l_t)+Y_t <= 2b-2=x_t`, equality iff `l_t=1,Y_t=b-1`. At `g_t=0`, if `x_t=b-1` then `l_t=1` and `x_{t+1}=0 < x_t`; otherwise `x_t>=b`, and `x_{t+1}=2x_t+l_t+1-2b <= x_t`, equality only when `x_t=2b-2,l_t=1`. Cyclicity again forces equality everywhere, hence only the constant upper extreme predecessor.

The position-0 root cannot reach either state at any positive spatial width: any incoming path must stay in that target forever, but the root is distinct (or, for all-zero `g`, its first transition forbids `x_0=0`). Thus the extreme uniform bands are unreachable in *every* base and temporal stream.

For base 10, all uniform absorbing coefficient cycles have lengths `1,1,2,6`: `{0}`, `{18}`, `{6,12}`, `{2,4,8,16,14,10}`. The still-capped primitive `p=21` word `001001010101001010101` can only admit uniform cycles with length dividing 21, namely `{0}` and `{18}`, and both are excluded without any state cap. **Nonuniform lattice SCCs, including spatial periods 3 and 9, remain UNDECIDED.**

Sanity check: `python3 calculation/decimal_frontier/lattice_formats/code/check_extreme_bands.py --small-controls` (6,604 exact target/word/base tests), alongside the mandatory pre-census base-9/base-13 controls of `bauto5`.
