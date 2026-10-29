# W29 Higher-gram reversal-orbit parity quotient
- **PAPER PROOF (all bases b>=2, all h>=2):** For every nonempty pair-coefficient block w, the carry/suffix/reversal-h-gram-parity transducer T has T_w^(h+2)=T_w^h.
- Every palindrome has zero asymmetric reversal-h-gram parity. An r-band template with positive unbounded exponents needs at most (h+1)^r representative checks to prove universal successor nonpalindromicity, if exact transitions are supplied separately.
- **PAPER PROOF strict decimal control:** P(k)=[2,8,12,4,12,6,16]++[8,12]^k++[8]++[12,8]^k++[16,6,12,4,12,8,2], k>=1, is symmetric with all-even coefficients. Every normalized successor has digit-frequency odd-count weight 1 and zero unordered 2-gram mask, but two odd 3-gram reversal-orbit counts (5,2,8) and (5,2,9); hence every N(k)+reverse(N(k)) is nonpalindromic for a canonical nonpalindromic split N(k).
- **COMPUTED:** 1,500 random quotient tests across h=2,3,4,5 and b=2,3,9,10, with direct normalization controls; ordinary big-integer decimal replay k=1,2,3,4,5,8,30,1000, all pass.
- Reproduce: python3 calculation/new_structures/agent-W29/kgram.py. Data: calculation/new_structures/agent-W29/highergram_control.json. Proof: reports/AgentW29HigherGram.md.
- **NOT CLAIMED:** an infinite decimal Lychrel integer, a successor-closed template family, Lean verification, or forward invariance.
