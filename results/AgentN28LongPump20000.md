# AgentN28LongPump20000
- Label: COMPUTED, exact finite-scope decimal candidate family; NOT an infinite base-10 Lychrel proof.
- Seed family: P=L ++ 2^k1 ++ (6,12)^k2 ++ 18^k3 ++ (8) ++ reverse(left), L=(18,7,18,12), independent counts k_j>=25000.
- Base seed k=(25000,25000,25000) has 200009 decimal digits; 20000 steps, 208244 final digits, zero palindromes, 8235 length increases.
- All 20000 steps passed two independent arithmetic paths and three exact carry-loop pumping contracts; external nonpalindrome anchors survived each step.
- Independent second C++ digit-list implementation: 20000 steps, identical final FNV64=5791061973543803658.
- This proves at most a uniform finite 20000-step prefix for all k_j>=25000, via the PAPER PROOF pumping lemma; the centre never closes in a finite cycle.
- Code: calculation/new_structures/agent-N28/long_pair_replay.cpp; controls: long_run_20k.json; independent replay_int.cpp and paired_pump.py already committed.
- Full explanation: reports/AgentN28LongPump20000.md.
