# Agent X22: exact two-step coalescence through a positive-entropy Markov fibre

**PAPER PROOF**, conditional only on finite integer-table assertions exhaustively checked by the supplied standard-library Python verifier. No Lean proof; no infinite base-10 Lychrel claim.

## Family
Write P(N)_i=d_i+d_(n-1-i) for the palindromic pair coefficient word of a canonical decimal integer N, least significant end first. Let B be the previously published 39-column p8/m20 rooted prefix (`sft.B0`); let W0,W1 be phases 0 and 1 of the 20-column bulk. Define the fixed carry port S=(1,1,4). Define T as all length-20 pair-coefficient strings p for which the exact overflow-1 two-sided carry transducer has a closed path S -> S emitting W1. This is a **completely finite definition**, with 40 possible edge states and explicit decimal transitions.

The exact checker enumerates all paths and establishes |T|=12800, with no duplicate coefficient word; every member has an odd coefficient. The old W0 belongs to T. For any integer Q>=1 and ordered choice (t1,...,tQ) in T^Q, let H=B ++ t1 ++ ... ++ tQ and P=H ++ reverse(H). Choose low decimal digits min(9,p_i), high digits p_i-min(9,p_i). The number N_Q(t1,...,tQ) has 78+40Q decimal digits and leading digit 8; different tuples produce different canonical integers. All initial numbers are nonpalindromic because P_0=17 is odd.

## Precise proof of coalescence
For overflow gamma=1, at each folded site i use carries a_i and r_i and digits L_i,U_i satisfying L_i=(p_i+a_i)%10, a_(i+1)=floor((p_i+a_i)/10), U_i=(p_i+r_i)%10, r_(i-1)=floor((p_i+r_i)/10). The next pair coefficient is L_i+U_(i-1) for interior i>=1, whereas at the first site the extra leading digit supplies U_(-1)=1. The graph state is (a_i,r_(i-1),U_(i-1)); the initial state is (0,1,1).

A direct finite path computation over the 39 literal input coefficients B gives **exactly one path** from (0,1,1) to S=(1,1,4). Its output prefix K of length39 is:
8,13,5,1,5,8,9,8,2,18,14,13,15,12,12,7,11,5,8,6,10,15,7,10,4,7,2,2,8,10,13,8,14,11,15,14,5,17,11.
By definition every chosen T tile is an S-to-S path emitting W1; concatenate arbitrary Q of them. At the even-length input centre, the closure requires the inward upper carry r_(h-1) to equal the lower carry a_h; both are 1 at S. The successor has one extra leading digit and an odd-length centre coefficient 2*U_(h-1)=8. Thus the **entire** successor pairword equals
`K ++ W1^Q ++ [8] ++ reverse(K ++ W1^Q)`,
irrespective of the selected T tiles.

This path assignment satisfies carry equations at every ordinary decimal position, with low initial carry 0 and leading overflow 1. Grade-school normalization carries are uniquely determined, so it equals the actual first successor pairword. The second iterate N2 is the base-10 value of that pairword, because for every number X, X+reverse(X) equals the positional value of P(X). Therefore all 12800^Q initial numbers have exactly the same second iterate, for **every** Q>=1. The shared first successor pairword contains odd coefficients (19 in K), so step 1 also is not a palindrome. This is the complete all-Q argument, with no extrapolation from finitely many integer orbits.

## Independent checks and implication
`coalescence.py` enumerates all 12800 source tiles and proves each has a valid closed arithmetic path, verifies the unique B path and centre port, and checks actual Python arbitrary-precision integers: **all 12800 Q=1 choices** and another **266** cases at Q=2,3,10,50,600. The common first pairword and exact second integers agree. These controls use actual integer conversion and reverse-and-add, not a reuse of the graph transition evaluator.

For Q=600 there are **12800^600 > 10^2464** distinct 24078-digit integers with the same second iterate. Since the previously committed `AgentX22MarkovSFTReservoir` deterministic Q=600 choice passed independent GMP and digit-array palindrome tests through 20000 iterations, the exact coalescence theorem plus the odd guards at steps 0 and 1 transfers that same finite-horizon nonpalindromicity to **every** member of the Q=600 family. This is a larger multi-step coalescing family than the earlier binary one-step decoders, but it is not an infinite certificate; after the second step all seeds follow the same as-yet-unproved orbit.

## Reproduction
Run `python3 calculation/new_structures/agent-X22/coalescence.py`; see `calculation/new_structures/agent-X22/coalescence.json`, `sft.py`, `validate.py`, and the previously published independent 20000-step replay. This result redirects the infinite search to **time-forward information injection**: the positive-entropy fibre has enough combinatorial room for huge backward branches but is *erased* after two steps. Any regeneration must couple a defect-carrying boundary port to a forward-moving centre, rather than relying on high spatial entropy alone.
