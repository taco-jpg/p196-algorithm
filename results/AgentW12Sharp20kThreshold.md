# AgentW12Sharp20kThreshold
**COMPUTED**: a sharper positive finite-horizon certificate for ordinary decimal seeds 12(0297)^q34, every q>=3042, all steps 0..20000, no palindrome.
The certificate's 20001 exact central four-digit insertion identities and outer nonpalindrome witnesses are verified by two ordinary-integer sample runs at q=3042 and 3043.
The PAPER PROOF of the 2-point linear-polynomial soundness lemma is in reports/AgentW12FourDigitPump.md and applies unchanged, so the result covers ALL q>=3042 (not merely one tested seed).
At t=20000, q=3042 has 20475 digits, gamma0=11697, gamma1=8303, final FNV64=335bb10132092c44. Digit centre: 47 period-four phases, 19954 uniform; pairword centre: 46 period-four, 19955 uniform.
Nearby control q=3041 loses the **specified 128-digit periodic-core witness** at t=19998. This is NOT a detected palindrome or an exclusion of a smaller-q Lychrel orbit.
Source: calculation/new_structures/agent-W12/check.cpp (from preceding W12 result); reproduction: sh calculation/new_structures/agent-W12/threshold.sh.
Expected outputs: calculation/new_structures/agent-W12/threshold_expected.txt.
NOT CLAIMED: infinite closure, a proof about 196, Lean verification, or minimal q under all possible certificate formats.
