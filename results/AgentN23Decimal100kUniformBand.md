# AgentN23Decimal100kUniformBand
**COMPUTED** uniform finite-horizon decimal protected-band family: for every Q>=30037, the genuine decimal reverse-and-add orbit from seed 12(99)^Q34 has no palindrome in states t=0..100000.
Every state has LSD-first digit representation U_t ++ 9^L_t(Q) ++ V_t, equal-width exteriors with U_t != reverse(V_t), and L_t(Q)=L_t(30037)+2(Q-30037)>=2.
Exact two-ended carry transducer: 100000 transitions, overflow counts gamma0=58692/gamma1=41308, symmetric paired-9 trims=49310, final exterior width50692, final L(30037)=2.
Two independent literal-arithmetic implementations confirm Q30037 full 100000-step replay: base-10 byte-digit carries and base-1000 limb big-integer additions with ordinary decimal-string reversal. Both final digit length101386, full-number checksum mod1000000007 = 886568206, nonpalindrome and centre-18 throughout.
Exact minimal Q for this transducer at each horizon 1000,5000,10000,20000,50000,100000 recorded and boundary Q-1 tested; failure means loss of its L>=2 precondition, NOT palindrome.
Full source/checkers/threshold controls/reproduction under calculation/new_structures/agent-N23/; run bash calculation/new_structures/agent-N23/reproduce_100k.sh.
Sound local rule and no-palindrome pumping argument: reports/AgentN23ParametricDecimal20kBand.md; exact 100k controls and scope: reports/AgentN23Decimal100kUniformBand.md.
Finite 100000-step COMPUTED claim only; no Lean-verified or infinite base-10 Lychrel certificate, no 196 conclusion.
