# Agent10Base1286NeutralCycle
**COMPUTED.** A new complete four-edge neutral-band reverse-and-add certificate exists in base 1286, period-four overflow and lower carry streams `0101`.
Initial exterior B-width 1204, palindromic centre `[1607,1044,742,548,548,742,1044,1607]`, initial neutral band width 12 and neutral pair coefficient 1285.
Exact centre lengths 8,8,9,7, exterior widths 1204,1203,1204,1203; trim (u,v)=(1,0),(0,0),(1,1),(0,0).
All four exact source/target edges, including the entire exterior, are in `calculation/neutral_band/agent10_base1286/cert_b1286.json` (133 KB).
Independent integer normalization checks establish all B/C edges return to the start with neutral-band gain +1 every four steps.
Independent Python big-integer replay verifies 1,000 genuine reverse-and-add steps with complete pairwords and no palindrome.
Separate C++ ordinary digit-list replay checks 20,000 steps, each complete pairword and nonpalindromicity (final digit count 12,440).
Deterministic generator, explicit data, independent checker, replayer and complete control runner under `calculation/neutral_band/agent10_base1286/`.
Reproduce from a clean clone: `bash calculation/neutral_band/agent10_base1286/reproduce.sh`.
The runner also checks mandatory base-9 g=1100011000 period-4 SCC depth61 and base-13 g=1010010000 depths55 and75 using bauto3.cpp.
Detailed derivation and exact commands: `reports/Agent10Base1286NeutralCycle.md`.
Scope: only this base-1286 finite certificate; no Lean kernel verification, infinite-base generalization, decimal Lychrel or 196 claim.
