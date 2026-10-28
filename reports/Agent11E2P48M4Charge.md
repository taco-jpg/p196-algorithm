# A mod-9 obstruction for the decimal 48-step alternating stream

Status: **PAPER PROOF** for an exact all-exterior-width necessary condition, supported by a fully finite exhaustive COMPUTED target classification. Neither Lean verification nor a decimal Lychrel certificate is claimed.

## States and charge

Fix base 10 and 48 cyclic time indices `t mod 48`, with overflow `g[2i]=0`, `g[2i+1]=1`. A cut state is `(L_t,H_t,Y_i)` for `0<=t<48`, `0<=i<24`, with binary carries `L,H` and overflow digits `Y_i` in `0..9`. Write `S'=(L',H',Y')` for the state after one spatial column. Let `lambda_t = 2^{-t} mod 9`, well-defined because 2 is invertible modulo 9 and `2^48 = 1 mod 9`; hence `lambda_{t-1}=2 lambda_t mod 9` even across the time-ring boundary. Define

`Q(S) = sum_t lambda_t (L_t - H_t) + sum_i lambda_{2i+1} Y_i (mod 9)`.

## Proof that Q is preserved by every legal spatial transition

Let `x_t` (0..18) be the column coefficient at time `t`, and `x_48=x_0` (cyclic time closure). The exact position-automaton equations, including carry normalization, read:

- Even `t`: `x_{t+1} - 2*x_t - L_t - H'_t + 10*(L'_t+H_t) = 0`.
- Odd `t=2i+1`: `x_{t+1} - x_t - L_t - Y_i + 10*L'_t = 0`.
- Odd `t=2i+1`: `Y'_i - x_t - H'_t + 10*H_t = 0`.

Multiply each first or second equation by `lambda_t`, and at odd `t` also the third equation by `lambda_t`. Sum modulo 9 over `t=0..47`. The coefficient of `x_t` is `lambda_{t-1}-2*lambda_t=0`; the remaining terms, using `10=1 mod 9`, are exactly `Q(S')-Q(S)`. Therefore **Q(S')=Q(S) mod 9 for every legal column**. No assumptions about spatial width, symmetry, or temporal behavior of an exterior prefix are needed.

The canonical root cut has `L_t=0`, `H_t=g_t`, and `Y_i=1`; each odd-time contribution `lambda_{2i+1}(-1+1)` cancels, so **Q(root)=0**.

## Complete finite target test

For the decimal primitive spatial-period-4 absorbing row map at overflow period 16, `Agent11E2P16M4AllTime` independently enumerated all 19^4=130,321 coefficient rows and found precisely 50 three-cycles of the exact 16-step map, of which 16 have self-mirror primitive spatial-period-4 rows. These are precisely the distinct rows with true temporal return after 48 steps in this spatial-4 self-mirror class. Enumerate every one of their three time-16 phase starts and four spatial columns: 16*3*4=192 physical cut states. The reproducer derives every `(L,H,Y)` directly from cyclic upward/downward carry maps and computes Q:

- 96 cut states have `Q=3 mod 9`.
- 96 cut states have `Q=6 mod 9`.
- None has `Q=0 mod 9`.

It independently checks all 192*48=9,216 exact arithmetic column equations and the mod-9 charge equality on each spatial edge. The previously published C++ and pure-Python full m4 functional-graph census agree on the 16 three-cycle target families. Mandatory exterior positive controls (base 13 `1010010000`, depths 55 and 75; base 9 `1100011000`, period 4 depth 61) are also replayed by the reproduction script.

Since every edge from the canonical root retains `Q=0`, **no path of any finite exterior width reaches any of the 192 cut states**, and hence none of the 16 true-time-48 self-mirror primitive-m4 bulk cycles is root reachable. This excludes no other bulk cycle, no centre, and no decimal Lychrel orbit.
