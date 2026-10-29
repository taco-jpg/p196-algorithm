# AgentW20ProgrammableRenewalGate
**COMPUTED:** an explicit decimal p8/m20 growing-centre three-outcome scattering gate, not an infinite Lychrel certificate.
From N18's rooted B (39 coefficient columns), phase-zero W (20 columns), and `C=[8,0,0] ++ U ++ [16] ++ reverse(U) ++ [0,0,8]`, use `|U|=43`, U all 1 except U[13]=7, U[20]=7, U[30]=6 and free U[40:43]=(x,y,z) in `{0..18}^3`.
For `P=B ++ W ++ C ++ reverse(W) ++ reverse(B)`, all 6,859 payloads return a full 20-column W after both 88 and 176 exact decimal steps, preserving all 39 exterior columns and a parity-obstruction witness through t=264.
At t=264 the exact matched prefix of W is **8** for 64 payloads, **13** for 603, and **20** for 6,192. The latter class returns 20 columns three times; at t=352 its next W prefix is 2 (not a fourth renewal).
Independent real-integer Python replays of one representative of each class at q=1..4 (12 orbits, 264/352 steps) agree on all centre-return words and show no palindrome.
A selected successful codeword (0,0,0) with q=240 retains the exact 39-column p8 exterior for **20,000** actual reverse-add steps, no palindromes, 9,771 -> 19,771 digits; both independent digit-array and GMP ordinary big-integer replay pass. The GMP final decimal FNV64 is `16422078354326034688`.
Mechanism: three independently addressable inner coefficients act as a 3-level delayed collision gate at the growing centre, rather than a periodic stationary kink.
Code/data: `calculation/new_structures/agent-W20/` (`renewal_gate.cpp`, `independent_gmp.cpp`, `ordinary_integer_oracle.py`, `gate_data.json`); details and exact commands: `reports/AgentW20ProgrammableRenewalGate.md`.
Scope: **finite computations only**, q=1 exhaustive payload scan and q=1..4 representative controls; no all-q proof, fourth renewal, symbolic cycle, Lean result, base-10 Lychrel number or result about 196.
