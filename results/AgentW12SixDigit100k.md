# AgentW12SixDigit100k
**COMPUTED** universal finite-horizon base-10 family: N0(q)=12(428571)^q34 for EVERY q>=16000 has no palindrome in states t=0..100000.
At all 100001 states, the q=16001 decimal word differs from q=16000 by exactly ONE six-digit central insertion; every phase retains a digit mismatch outside that insertion.
The all-q conclusion is a PAPER PROOF from the affine two-sample polynomial lemma in reports/AgentW12FourDigitPump.md, with X=10^(6(q-16000)).
The full decimal digit-carry engine replays both ordinary integer orbits for 100000 steps; an independent base-10000 limb/reversal arithmetic engine checks both at every 1000th transition.
For q=16000 the final decimal word has 137399 digits, 58605 no-overflow steps, 41395 overflow steps, full FNV64=e50e728d5a533a59.
The central 128-digit period is 6 for 40 phases and uniform for 99961 phases; the mirror-pairword period is 6 for 39 phases and uniform for 99962.
Code, resumable chunk runner, compact checkpoints: calculation/new_structures/agent-W12/{long.cpp,run_long.sh,long_expected.txt}; reproduce with sh calculation/new_structures/agent-W12/run_long.sh.
Scope is 100000 exact steps for all q>=16000, NOT an infinite decimal Lychrel certificate, a Lean proof, or any assertion about 196.
