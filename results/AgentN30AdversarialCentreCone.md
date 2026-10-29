# AgentN30AdversarialCentreCone
**COMPUTED**: a new exact, centre-independent moving exterior-cone certificate format and an explicit infinite family of decimal seeds `high[0..15999] ++ M ++ reverse(low[0..15999])` for **every nonempty centre word M**, with 20,000 provably palindrome-free reverse-and-add steps.
Soundness: normalization carry is reset by the rightmost known pair coefficient different from 9; the high-side output and overflow are then independent of *all* centre digits, with certified exterior width nonincreasing.
The 20,001 step-0-through-step-20,000 cone states retain at least 1,866 certified pairs; the first differing pair is always at index <=20. Exact base-10^9 big-integer replays of centres `0`, `3^37`, `9^123` agree with every step and detect no palindrome. Independent Python tests: 49,902 one-step centre variations.
**Scope:** This establishes a finite-horizon family, **not** a base-10 Lychrel number, not an infinite orbit certificate, and nothing about 196. Renewal of certified width remains open.
Proof and precise limits: `reports/AgentN30AdversarialCentreCone.md`.
Reproduce: `python3 calculation/new_structures/agent-N30/test_cone.py`; `c++ -O3 -std=c++17 calculation/new_structures/agent-N30/cone_family.cpp -o /tmp/n30_cone && /tmp/n30_cone 16000 20000 37 3`.
Data: `calculation/new_structures/agent-N30/cone_20000.json`.
