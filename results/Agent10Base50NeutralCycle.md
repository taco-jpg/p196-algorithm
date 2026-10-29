# Agent10Base50NeutralCycle
**COMPUTED.** A new complete four-edge neutral-band reverse-and-add certificate exists in base 50 with overflow and lower carry streams `0101`.
Initial exterior B-width 36, initial palindromic centre `[62,15,22,32,32,22,15,62]`, initial neutral band width 12, neutral coefficient 49.
Exact four-phase centre lengths 8,8,9,7, exterior widths 36,35,36,35; trim (u,v)=(1,0),(0,0),(1,1),(0,0).
The initial exterior and all four complete exact edges are in `calculation/neutral_band/agent10_base50/cert_b50.json`.
All four `norm`, `nextB`, `nextC` transitions return B and C to their starting states; the neutral band gains +1 every four steps.
Independent Python integer checker verifies every edge and 2,000 ordinary big-integer reverse-add steps with complete pair words and no palindrome.
Independent C++ ordinary digit-list replay verifies 20,000 steps, complete pair words and no palindrome at every step (final digits 10,104).
Deterministic generator, data, checker, replay and complete control runner are under `calculation/neutral_band/agent10_base50/`.
Reproduce: `bash calculation/neutral_band/agent10_base50/reproduce.sh` from a clean repository checkout.
That runner also checks mandatory b9 g=1100011000 period-4 depth61 and b13 g=1010010000 SCC depths55/75 via repository bauto3.cpp.
Detailed derivation: `reports/Agent10Base50NeutralCycle.md`.
Scope: base-50 finite neutral-band certificate only; no Lean kernel verification, infinite-base family, decimal Lychrel, or conclusion about 196.
