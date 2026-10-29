# AgentX20IndependentDualCounter
**COMPUTED:** Exact 480-edge base-10 two-band pairword family for **every independent pair of integers m,n>=40**; the 20- and 48-coefficient repetition counts are NOT synchronized.
Seed: `P0=H++[9]++reverse(H)`, `H=B++W20^m++[9]++V48^n`, `N0=val_10(P0)`; literal B,W20,V48 arrays are in the self-contained source.
Every edge's exact 80-state two-ended carry relation passes **four** counter corners `(0,0),(1,0),(0,1),(1,1)` and both independently idempotent band matrices. This certifies all repetition counts, not just tested widths.
Five independent decimal digit-array realizations `(m,n)=(40,40),(41,40),(40,41),(41,41),(52,67)` match all 481 predicted templates and are never palindromes.
**COMPUTED:** Two distinct asymmetric seeds `(427,509)` and `(509,427)` independently replay 20,000 genuine decimal additions with ordinary digits versus base-10^9 big-integer limbs, full-integer equality at every step, no palindromes, both period-band windows exact throughout; final lengths 76,026 and 71,434.
**PAPER PROOF format:** the independent Boolean powers `M20^r M48^s` collapse to four corner cases when `M20^2=M20` and `M48^2=M48`, giving a two-parameter exact finite-horizon lifting rule.
**PAPER PROOF arithmetic:** any 8r-step fixed-junction return that increases both repeated bands by a,b copies must satisfy `r=10a+24b`; the first positive dual-band resonance is **272 steps**, `(a,b)=(1,1)`.
At t=272 the physical orbit restores both bulk words but differs from the proposed reindexed seed at 3,993 coefficients; at t=480 the fixed junction differs in 391 coefficients. This identifies a regenerating junction as the missing component, **not** a no-go for general two-parameter templates.
No infinite decimal certificate, claim about 196, or Lean verification is made.
Reproduce: `g++ -O3 -std=c++17 calculation/new_structures/agent-X20/two_counter.cpp -o /tmp/x20 && /tmp/x20 480`; see report for independent long replays.
Sources: `calculation/new_structures/agent-X20/{two_counter.cpp,asymmetric20k.cpp,resonance.cpp,spotcheck.py,expected.json}`; `reports/AgentX20IndependentDualCounter.md`.
