# Agent U47: cyclotomic carry-cocycle condition for T*

**PAPER PROOF.** Let `P_t(x)` be a genuine symmetric decimal pairword of length `n_t`, let `gamma_t` be the terminal normalization carry, and define `K_t(x)=sum_{i=1}^{n_t-1} c_{t,i}x^(i-1)+gamma_t x^(n_t-1)` from the exact LSD-first carry sequence. Then

`P_(t+1)=(1+x^gamma_t)P_t-L_t`, where `L_t=(10-x)K_t+x^(n_t+gamma_t-2)(10x-1)K_t(x^-1)`.

For `Phi(x)=1+x^3+x^6+x^9+x^12`, the exact T* endpoint difference `T(q,k+5)-T(q,k)` is divisible by `Phi`. The rooted clock has `product_t(1+2^gamma_t)=2^90*3^30=1 (mod 31)`, while `Phi(2)=0 (mod 31)`. Unlike U16's mod-999 scalar cocycle, this root evaluation cancels the homogeneous term and leaves a pure carry-only condition. Thus every genuine 120-step fixed-seam T* return must satisfy

`sum_t product_(s>t)(1+2^gamma_s) * [8K_t(2)+19*2^(n_t+gamma_t-2)K_t(16)] = 0 (mod 31)`.

This is an exact all-width necessary condition, not a sufficient return test, a no-go theorem for all seams, or a decimal Lychrel certificate. Checker: `calculation/new_structures/U47/cyclotomic_cocycle.py`.
