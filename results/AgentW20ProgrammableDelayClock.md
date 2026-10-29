# AgentW20ProgrammableDelayClock
**COMPUTED:** the p8/m20 growing-centre collision gate is a three-level programmable finite delay line for true decimal reverse-and-add, not an infinite Lychrel certificate.
In the exact 19^3 payload scan from `AgentW20ProgrammableRenewalGate`, q=1 first 39-column exterior mismatch times are **300** (64 payloads), **324** (603), **364** (6,192), matching exactly the three t=264 W-prefix classes 8/13/20.
For each class representative and all q in `{1,2,...,16,32,64,128,240}`, exhaustive coefficient replay computes **first** root mismatch at `88q+212`, `88q+236`, and `88q+276`, respectively (20 q values per class). No universal-q proof is claimed.
Independent GMP ordinary-integer replays at q=240 verify the *first* mismatch at t=21,332 / 21,356 / 21,396, always at column 38, with zero palindromes from t=0 through those mismatch states.
Positive mechanism: three input coefficients select a quantized delay of 64 or 24 or 0 steps relative to the maximum, with an exactly tested +88 delay for each added full exterior period. This is a controlled finite clock, not a short kink cycle.
Code/data: `calculation/new_structures/agent-W20/clock_lifetimes.cpp`, `clock_gmp.cpp`, `clock_data.json`; full reproduction and caveats: `reports/AgentW20ProgrammableDelayClock.md`.
Scope: base 10, stated q values and all 6,859 payloads at q=1; no proof for arbitrary q, no palindrome claims beyond the tested mismatch states, no Lean proof, no decimal Lychrel number.
