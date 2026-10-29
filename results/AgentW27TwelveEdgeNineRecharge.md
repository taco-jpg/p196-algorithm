# AgentW27TwelveEdgeNineRecharge
**PAPER PROOF.** A **base-10 12-edge exact symbolic orbit family**, for EVERY integer q>=2, with a six-step central-9 recharge followed by erosion; 13 genuine nonpalindromic integers, not a periodic certificate.
Initial decimal string: `2905 ++ 9^(2q) ++ 8723`. At t=6 it is EXACTLY `10 ++ 9^(2q+2) ++ 8900000`: the central 9 reservoir gains 2 digits (a +4 jump on transition 5->6).
At t=12 the string is `83600362 ++ 9^(2q-4) ++ 16399637`: the gain is consumed; the outer caps do NOT return, so this is not a renewal cycle.
All 12 edges are proven by polynomial identities in X=10^(2q-4), with independent affine coefficients for the original and reversed words; exact explicit 13-phase table is embedded in the checker.
At all 13 phases and for all q>=2, the first mirrored-digit mismatch is in one of the first TWO positions, independently of q. Thus no phase is a palindrome.
Reproduce: `python3 calculation/new_structures/agent-W27/recharge.py && c++ -O3 -std=c++17 calculation/new_structures/agent-W27/recharge_digits.cpp -o /tmp/w27-r && /tmp/w27-r`.
Python independently replays ordinary big integers at q=2,3,4,5,40,100,600; separate C++ decimal-digit engine confirms all 13 literal words for those q.
Full table and soundness statement: `reports/AgentW27TwelveEdgeNineRecharge.md`.
**Not claimed:** an all-time orbit, a closed centre cycle, a fixed decimal Lychrel number, or Lean verification.
