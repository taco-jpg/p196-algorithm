# Agent X26: arbitrary 257-digit decimal centre protected for 20,000 steps
- **COMPUTED**, with a PAPER PROOF of the one-column carry-confinement lemma in the report.
- For every decimal word C of length 257 (leading zero allowed within C), N0(C) = 5 ++ 9^22000 ++ C ++ 9^22000 ++ 4 survives t=0..20000 genuine base-10 reverse-and-add with no palindrome.
- Universal claim is by induction against the C=9^257 reference, not by enumerating 10^257 centres.
- Reference exact digit and pairword check at every step: gamma(20000)=8274, n0=44259, n20000=52533, maximum first nonpalindrome witness index 25, minimum protected outer-pair width ell=10275.
- Every centre has two coefficient-18 collars of at least 22000-t paired sites at time t (minimum 2000 at t=20000); the arbitrary centre may grow.
- Nonconstant Thue-Morse (8/9) core independently replayed with GNU MP through all 20000 steps; 21 checkpoints match direct digit arithmetic.
- Programs and reproducible data: calculation/new_structures/agent-X26/.
- Detailed soundness and limitations: reports/AgentX26AdversarialCentreShields.md.
- No infinite decimal Lychrel certificate, no claim about the orbit of 196, no Lean verification.
