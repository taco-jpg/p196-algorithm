# AgentX12DualClockEnvelope
**COMPUTED**, exact finite base-10 two-counter phase diagram, not a certificate.
For P(q,r)=B0 ++ W0^q ++ C(r) ++ reverse(W0)^q ++ reverse(B0), with C(r) as in AgentX12TwoClockCentrePulse, compare genuine integer orbits for r and r+1.
At 12 tested q (1,2,3,4,5,7,10,16,20,30,50,65) and r=12000, first 39-site rooted-exterior failure exactly follows E(q)=88q+276; insertion and alternating overflow still hold through E(q)+2.
At 12 protected r (100,250,500,850,1000,1500,2000,3000,5000,10000,15000,20000), first whole-pairword symmetric-insertion failure equals L(5k+s)=6k+(13,15,16,16,17)[s-1] for s=1..5.
In these r cases the predicted guard threshold q_min=max(1,floor((L(r)-276)/88)+1) passes, while its q_min-1 predecessor first loses the B exterior at E(q_min-1). The largest pair is r20000, q_min270, L24011.
Three selected cases (r=100,500,850) independently replayed via Python built-in decimal integers: 3552 whole-number state checks, exact first splice failures, no palindromes.
Data: `calculation/new_structures/agent-X12/envelope_observations.json`; code: `envelope.cpp`, `envelope_bigint.py`; details: `reports/AgentX12DualClockEnvelope.md`.
Run `g++ -O3 -std=c++17 calculation/new_structures/agent-X12/envelope.cpp -o /tmp/x12env && /tmp/x12env --full && python3 calculation/new_structures/agent-X12/envelope_bigint.py`.
**Scope:** these finite examples ONLY; no all-q/r theorem, infinite persistence, Lean result, or statement about 196.
