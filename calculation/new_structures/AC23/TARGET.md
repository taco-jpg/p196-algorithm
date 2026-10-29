# AC23 target: physically rooted p12/m9 phase-2 five-site seam

**Exact attempted missing sublemma:** decide, without a strict-intermediate-W9 pruner, whether any of the 30 charge-zero U3 rotations and any literal five-coefficient junction J in {0,...,18}^5 can restore the rooted p12/m9 phase-2 W9 exterior after 120 genuine decimal reverse-and-add steps at reference widths (q,k)=(14,100). This necessary-condition decision restricts the stationary-seam branch of the all-time PHYSICAL_TSTAR_RETURN_AT_REFERENCE_WIDTH lemma; it is not itself a Lychrel certificate.

Given the published phase-2 exterior rows B_2 (length 34), W_2 (length 9), and a palindromic, canonically realizable centre C, define H(q,k)=B_2 ++ W_2^q ++ J ++ U^k and P(q,k)=H ++ C ++ reverse(H), coefficients least significant first. The complete T* return demands P_120(q,k)=P(q,k+5) with the literal same J,C,U, the 120 genuine decimal steps, physical overflow clocks and a non-palindrome guard for all q>=14,k>=100. The necessary exterior gate is P_120[0:34+9q]=B_2 ++ W_2^q. U runs over all 30 rotations of (9,a,18-a), a in {0,2,...,18}.

A finite reference-width no-go is extended only under the documented T12 insertion/carry-reset cone theorem. No timewise strict-W9 pruning is used, because temporary defects may heal before the endpoint.
