# W27 near-root odd-witness localization

**COMPUTED; finite scopes only.** This result adds an exact localized nonpalindromicity monitor to the previous W27 parameterized centre-9 family and to the actual integer 196 orbit. It does not produce an infinite Lychrel certificate.

Let the integer's digits be d_0,...,d_(n-1), least significant first, and P_i=d_i+d_(n-1-i). A palindrome has equal reflected digits, hence every P_i is even. An odd P_i is therefore a sufficient (but not necessary) obstruction. Define o_t as the earliest i<n/2 with odd P_i, or NONE when no such index exists; and m_t as the first reflected-digit mismatch.

Exact complete decimal digit-vector replays gave:

| Seed | times checked | max o_t when present | first maximum | all-even P states | max m_t | final digits |
|---|---:|---:|---:|---|---:|---:|
| 196 | 0..100000 | 28 | t=9777 | t=8,13,19 | 28 | 41490 |
| 196 ++ 9^12010 ++ 196 | 0..20000 | 18 | t=4852 | none | 18 | 20317 |

All 100001 and 20001 states respectively are nonpalindromic. The hybrid's first odd pair always occurs within the first 19 pair positions. Since the W27 centre-insertion lemma only inserts coefficients 18 in the central band, the entire 19-site obstruction trace is exactly the same for all Q>=6005, for every t<=20000. This provides an exact finite-horizon fixed-width guard for that infinitely parameterized family. The true 196 orbit does NOT inherit that insertion property. In the real-196 run, the three exceptional completely-even pairwords still have a digit mismatch and are not palindromes.

Reproduction:
```sh
c++ -O3 -std=c++17 calculation/new_structures/agent-W27/prefix_witness.cpp -o /tmp/w27-witness
/tmp/w27-witness
python3 calculation/new_structures/agent-W27/prefix_oracle.py
```
The C++ scan checks the full source word and computes the first actual mismatch and first odd coefficient every step; all 100001/20001 states are processed, not sampled. The Python control uses arbitrary-precision integers and independently verifies the actual-196 maxima (11 at t105 for 0..1000) and hybrid maxima (6 at t12 for 0..160). The repo's earlier N11 million-step 196 replay is not counted as independent validation of these new witness-depth numbers.

This is a **constructive finite-width safety target**: potential future finite-state certificates need only ensure that one of these small prefix slots stays odd, instead of controlling every interior cell, but a proof of unbounded-time protection still needs a closed prefix/carry/overflow invariant. No such invariant is claimed here.
