# U32: mod-9 cut-charge obstruction for p16 / m4 three-cycles

**Label:** PAPER PROOF for the charge lemma + COMPUTED exhaustive row-map application. Not Lean-verified. Not a decimal Lychrel witness.

**Redirect for the team:** do not spend more time trying to root the exact 48-periodic primitive `m=4`, `g=(01)^8` three-cycles; the invariant below rules out all 16. Move to other spatial periods, other clocks, or non-band mechanisms. This is deliberately narrower than a general no-zero-drift-band theorem.

## Algebraic lemma

Let `P` be divisible by 6, let `gamma_t` be any `P`-periodic overflow word, and consider a column trajectory `x_t` that is itself `P`-periodic (`x_P=x_0`). At a spatial cut, write the carry state as `S=(L,H,Y)`: `L_t` is the carry into the current coefficient from the low side, `H_t` is the carry passed from the current coefficient to the low side, and `Y_t` is the partner digit used at phases with `gamma_t=1`. Let `S'=(L',H',Y')` be the next cut state. For the coefficient `x_t` at the current column, put `c_t=H'_t`, `a_t=(x_t+L_t) mod 10`, and `b_t=(x_t+c_t) mod 10`. The exact relations are

- `x_t + L_t = a_t + 10 L'_t`;
- `x_t + H'_t = b_t + 10 H_t`;
- `x_{t+1} = a_t + gamma_t*Y_t + (1-gamma_t)*b_t`;
- when `gamma_t=1`, `Y'_t=b_t`.

Reducing modulo 9 (so `10 = 1 mod 9`) gives

`x_{t+1} = (2-gamma_t)*x_t + L_t-L'_t + gamma_t*Y_t + (1-gamma_t)*(H'_t-H_t) (mod 9)`,

and at overflow phases `Y'_t = x_t+H'_t-H_t (mod 9)`.

Set `lambda_t = 5^t mod 9`. Since `2*5=1 mod 9` and `P` is divisible by 6, `lambda_(t-1)=2*lambda_t` including the cyclic wrap at `t=0`. Multiply the first concruence by `lambda_t`, add `gamma_t*lambda_t` times the second relation, and sum over all `t`. All `x_t` terms cancel, leaving

`Q(S') = Q(S) (mod 9)`, where `Q(S)=sum_t 5^t*(L_t-H_t+gamma_t*Y_t) mod 9`.

At the canonical root `L_t=0`, `H_t=gamma_t`, and `Y_t=1` at overflow phases, hence every summand is zero and `Q(root)=0`. Therefore any `P`-periodic band cut reachable from the canonical root must have charge zero.

## Exact p16 / m4 application

The independent carry solver exhausts all `19^4 = 130,321` rows under the 16-step map for `g=(01)^8`. It finds 110 functional-graph cycles (60 fixed points and 50 three-cycles). There are 48 primitive reflection-symmetric spatial-period-4 fixed points and 16 primitive reflection-symmetric spatial-period-4 three-cycles. Each three-cycle lifts to a 48-phase row orbit. On every one of its four spatial cuts, `Q` is constant and equals either 3 or 6 modulo 9 (eight cycles of each value). Hence none of these 16 cycles can be attached to a canonical-root exterior in a fully 48-periodic template.

The 48 fixed points are not claimed to be excluded for arbitrary longer template periods here. The exact one-lap period-16 exclusion is the separate computed result `results/Agent11E2P16M4OneLap.md`.

## Reproduction and honest scope

Run `python3 calculation/new_structures/U32/verify_p16_m4_48cycle.py`. It independently checks the cyclic carry map, enumerates the row space, computes all target charges, and runs 64 real-bigint controls (16 cycles × q=20,40,80,160) against a separate digit-array reverse-and-add implementation. Those bigint controls use the actual measured overflow stream and validate the local bulk row map; they are not used as proof of root reachability.

For a full template period `T=48*k`, the repeated target charge is `k*Q_48 mod 9`, so this particular invariant also excludes `3 ∤ k`. It does not exclude periods divisible by 144, where the repeated charge can vanish. No claim is made about all base-10 bands, all periods up to 40, or existence of a decimal Lychrel number.
