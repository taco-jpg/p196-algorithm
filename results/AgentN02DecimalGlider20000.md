# Agent N02 decimal growing-centre travelling defect: 20,000-step candidate
Label: COMPUTED (finite exact arithmetic and structural replay only).
Base 10, rooted period-8/space-20 exterior, seed halfword `B_0 ++ W_0^228`, mirrored pairword; canonical actual digits `d_i=min(P_i,9)`, `d_{n-1-i}=P_i-d_i`.
9,198-digit seed; **20,000** reverse-and-add steps, **zero** palindromes, complete GMP big-integer vs independent digit-list agreement at every step; final integer has 19,198 digits.
At every checked step, the pairword agrees with the prescribed 39-column exterior and a periodic bulk up to a moving first-defect front.
Computed transient glider: after step 10 the front shifts **-20 spatial cells per 88 time steps** in the checked range; the centre-defect region grows **+42** per 88 steps.
Independent Python integer replays: q=1..19 first exterior failure at `88q+4`, column 38; q=30 survives 1,500 steps.
For q=228 the first exterior failure is step **20,068**, column **38** (not a claimed palindrome).
Reproduce: `sh calculation/new_structures/agent-N02/glider_run.sh` (needs g++ and GNU GMP development headers/libraries).
Code/controls/data: `calculation/new_structures/agent-N02/{glider_replay.cpp,glider_independent.py,glider_run.sh,glider_data.json}`.
Proof details, scope, exact data and limitations: `reports/AgentN02DecimalGlider20000.md`.
**Not** a decimal Lychrel proof, an infinite orbit, a result about 196, an all-q theorem, or LEAN-VERIFIED.
