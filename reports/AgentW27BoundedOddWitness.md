# W27 million-step near-root pairword witness

**COMPUTED; finite scopes only.** This extends the previous 100,000-step W27 odd-witness measurement to the true 196 orbit's first million iterations (the N11 orbit replay was known, but not this complete pairword-witness localization). It also covers the W27 9-band lift. Not an infinite Lychrel proof.

Given n decimal digits d_0,...,d_(n-1) least-significant first, let P_i=d_i+d_(n-1-i). Define o_t as the least i<n/2 for which P_i is odd (NONE if all pair coefficients are even), and m_t as the first reflected-digit mismatch. An odd P_i is a sufficient but not necessary palindrome obstruction.

| Seed | t interval | max o_t when present | first maximum | all-even P states | max m_t | final digits |
|---|---:|---:|---:|---|---:|---:|
| 196 | 0..1,000,000 | 30 | 429911 | 8, 13, 19 | 30 | 414302 |
| 196 ++ 9^12010 ++ 196 | 0..20,000 | 18 | 4852 | none | 18 | 20317 |

These maxima include **every** state, not periodic sampling. The million-step run had 1,000,001 states and 0 palindromes; 196's final length 414302 agrees with the independently reported N11 full-orbit measurement. The first 196 odd-pair witness is at index 0 in 455282 of these states; the rare depth-30 witness occurs once. The all-even cases have a genuine mirrored-digit mismatch and therefore are not palindromes.

In the 196-shell hybrid, an odd pair coefficient occurs within the first 19 sites at EVERY t<=20000. Since adding a symmetric central 9 pair only inserts coefficients 18 far from those first 19 sites, this entire safety profile extends to **all Q>=6005** over those 20,001 states. This is an exact all-Q finite-horizon local guard, not a statement that the shell follows the true 196 orbit or that the guard lasts forever.

Reproduce:
```sh
c++ -O3 -std=c++17 calculation/new_structures/agent-W27/prefix_witness.cpp -o /tmp/w27-witness
/tmp/w27-witness
python3 calculation/new_structures/agent-W27/prefix_oracle.py
```
The C++ integer engine evolves all decimal digits and computes the first mismatch and odd-pair index at each state, failing if the prescribed bound is violated; it handles the three early even exceptions explicitly. Independent Python arbitrary-precision integer controls cover 196 t=0..1000 (max first odd 11 at t105) and hybrid t=0..160 (max 6 at t12). The earlier N11 million-step replay independently confirms the arithmetic trajectory length but not these new local-witness maxima.

**Next structural use:** a candidate periodic or resource-graded finite-state invariant could try to force one of 31 outer pair slots to remain odd (apart from the exact three early exceptions). The measured bound is NOT itself an inductive invariant.
