# U47 running notes

## 2026-10-28: route registered

Issue #475 claim comment: `6490192356`. Route: polynomial/cyclotomic carry cocycle
modulo `Phi_5(x^3)`, distinct from scalar `G5` endpoint congruences and the existing
mod-9/11/101 voltage lanes. This is complementary to U16's newly committed mod-999 full-pairword cocycle: the x=2 mod-31 root makes the 120-step homogeneous multiplier equal 1, leaving a separate pure carry-only zero condition.

## Exact algebra

For a symmetric pairword polynomial `P_t(x)` of length `n_t`, let `c_{t,0}=0`,
`p_i+c_i=d_i+10c_{i+1}`, and `gamma_t=c_{t,n_t}`. Define

`K_t(x) = sum_{i=1}^{n_t-1} c_{t,i} x^(i-1) + gamma_t x^(n_t-1)`.

The normalized digit polynomial is `D_t=P_t-(10-x)K_t`. Since `P_t` is symmetric,
`P_(t+1)=(1+x^gamma_t)P_t-L_t`, where

`L_t=(10-x)K_t+x^(n_t+gamma_t-2)(10x-1)K_t(x^-1)`.

Set `Phi(x)=Phi_5(x^3)=1+x^3+x^6+x^9+x^12`. The template difference
`T(q,k+5)-T(q,k)` is divisible by `Phi`: five U3 copies contribute `U(x)Phi(x)`,
and the old centre/mirror shifts by 15 positions, with `x^15=1 mod Phi`.

For the rooted 120-clock, `A(x)=product_t(1+x^gamma_t)=2^90(1+x)^30`. Modulo 31,
`Phi(2)=4681=0`, `2^5=1`, and 3^30=1 `mod 31`, hence `A(2)=1`. Unrolling the exact
recurrence therefore gives the necessary carry-only condition

`S_2 = sum_t product_(s>t)(1+2^gamma_s) * [8K_t(2)+19*2^(n_t+gamma_t-2)K_t(16)] = 0 (mod 31)`.

This is an all-width necessary condition for every fixed-seam T* return, not a
sufficient condition. It is a finite carry cocycle, not a seed certificate.

## Reproducibility

`cyclotomic_cocycle.py --self-test` passed: 80 template-insertion congruence controls,
100 exact one-step polynomial carry identities, and 4 independent 120-step
big-integer/digit-array cocycle controls. Candidate-specific near-miss diagnostics
are recorded only in `IDEAS.md` because they do not establish a new global no-go.
