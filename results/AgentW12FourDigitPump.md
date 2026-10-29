# AgentW12FourDigitPump
**COMPUTED** (with a PAPER PROOF of the two-sample affine-word soundness lemma), base 10, not Lean-verified.
For every integer q>=6000, seed 12(0297)^q34 has no palindrome in reverse-and-add states t=0..20000.
At each of 20001 phases the digit word is A_t U_t^(q-6000) B_t with |U_t|=4, and an outer digit mismatch witnesses nonpalindromicity for all q.
Two exact ordinary decimal replays at q=6000,6001 and an independent base-10000 arithmetic engine establish every required one-step identity at two values of X=10^(4(q-6000)); linearity makes each identity universal.
The exact first three words are 12(0297)^q34, 55(8217)^q55, 111(5346)^q10, 127(9702)^(q-1)969721 for every q>=2.
The nonconstant spatial period-4 bulk becomes uniform at t=47; no infinite orbit, closing cycle, or assertion about 196 is claimed.
Reproduce: g++ -O3 -std=c++17 calculation/new_structures/agent-W12/check.cpp -o /tmp/w12 && /tmp/w12 6000 20000.
Independent motif discovery: g++ -O3 -std=c++17 calculation/new_structures/agent-W12/scan.cpp -o /tmp/w12scan && /tmp/w12scan.
Code, compact checkpoints and detailed argument: calculation/new_structures/agent-W12/, reports/AgentW12FourDigitPump.md.
