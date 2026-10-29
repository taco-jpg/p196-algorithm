# AgentW12SixDigitPumps20k
**COMPUTED**: Four distinct base-10 families 12 w^q 34, with w in {428571,461538,561726,273438}, have no palindrome in reverse-and-add states t=0..20000 for **every q>=2500**.
Every phase admits a centred insertion of a SIX-digit time-dependent word U_t when q increases by one; the same exterior contains a concrete mismatch with its reversal.
Ordinary digit-carry replay for q=2500 and 2501 is independently checked against a base-10000 limb/reversal implementation (all 20000 edges for q=2500, checkpoints for q=2501).
The all-q conclusion follows by the PAPER PROOF two-sample affine polynomial lemma in reports/AgentW12FourDigitPump.md, with X=10^(6(q-2500)).
All four have a genuinely nonconstant initial six-digit periodic core and at least 39 nonconstant phases, then a uniform bulk; this is not temporal closure.
At t=20000 the four final lengths are 23299,23265,23320,23287 digits; full hashes and period counts are in calculation/new_structures/agent-W12/six_digit_expected.txt.
Reproduce: g++ -O3 -std=c++17 calculation/new_structures/agent-W12/check_multi.cpp -o /tmp/w12multi ; /tmp/w12multi 2500 20000 428571 (repeat for each listed word).
Source+data: calculation/new_structures/agent-W12/check_multi.cpp, calculation/new_structures/agent-W12/six_digit_expected.txt.
Not claimed: an infinite decimal certificate, Lean verification, or the existence of a Lychrel number.
