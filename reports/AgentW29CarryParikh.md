# W29: exact finite quotients for carry-spectrum safety
**PAPER PROOF (identities and one-step family); COMPUTED (finite runs).** No infinite base-10 Lychrel assertion.

Let a pair-coefficient word be over 0,...,2b-2. Normalization with incoming carry c in {0,1} emits digit (a+c)%b and outgoing carry floor((a+c)/b). Every block's carry map is monotone on {0,1}, thus identity or constant, hence idempotent.

**Histogram transducer.** Track carry and an XOR mask for emitted digit frequencies. After the first copy of a block w the outgoing carry is fixed, so copies two and three emit identical parity masks and cancel. Therefore F_w^3=F_w in every base. For any positive band exponent k, replace it with 1 (odd) or 2 (even). A palindrome has zero or one digit with odd frequency.

**Unordered-edge transducer.** Track carry, the previously emitted digit (or none), and the XOR parity of unordered adjacent pairs {a,d} where a!=d. Every palindrome has edge mask zero by reflecting every adjacency, while the central adjacency, if any, connects equal digits. After one w-copy the carry is stable; after two the last digit is also stable, so subsequent blocks contribute a fixed XOR mask. Copies three and four cancel: U_w^4=U_w^2. Every positive exponent reduces to 1, 2, or 3. Include the final overflow digit 1 in both masks.

By composition the reductions work in arbitrary contexts and for multiple independently varying band exponents. For r bands, 2^r frequency cases or 3^r edge cases suffice to prove every normalized successor nonpalindromic, without any maximum on band lengths. These finite tests are only a safety component: an infinite certificate ALSO requires independently verified exact successor-closure of a nonempty template cycle, positivity of the exponent updates, and an initially nonpalindromic integer. The proof of an infinite orbit would then be induction on its checked transitions.

**Constructive strict-gain control.** Define symmetric least-significant-first P(k)=[4,18]++[10,12,12]^k++[0]++[12,12,10]^k++[18,4], k>=1. All pair coefficients are even, so the odd-pair rule cannot help. For the outermost coefficient 4 split digits (low,high)=(0,4), for other low-half coefficients p split (min(9,p),p-min(9,p)), and set the central digit 0. This gives a canonical nonpalindrome N(k). The only needed exponent representatives give identical successor frequency mask 830 (seven odd-frequency digits) and edge mask 576742227289321472 (seven odd edges). Thus N(k)+reverse(N(k)) is nonpalindromic for EVERY integer k>=1. This is a universal ONE-STEP family, not a closed orbit.

**Reproduce** from repository root:
python3 calculation/new_structures/agent-W29/certificate.py
g++ -std=c++17 -O3 calculation/new_structures/agent-W29/replay.cpp -lgmpxx -lgmp -o /tmp/w29_replay
/tmp/w29_replay 196 20000
/tmp/w29_replay 88Z14000 20000
/tmp/w29_replay --sweep

Python control: 980 random carry blocks across bases 2,3,9,10,13,26,146 checked for the universal identities, 1000 synthetic palindromes, and exact integer replay of k=1,2,3,4,5,12,99,500 of the one-step family. Two full GMP-vs-decimal-vector trajectories each compared every digit at every state, with the GMP reversal explicitly parsed in base 10. For 196: 20,001 nonpalindrome states, length 8296 at step 20000, histogram witness on 19,801 states, odd-coefficient witness on 19,998, edge witness on all 20,001. For 88(0^14000)75: length 22258, histogram 19,798, odd-coefficient 20,000, edge all 20,001. Sweep: 900 seeds 100..999 and 1500 fixed-seed mt19937_64 random seeds length 6..20, stopping on first palindrome or after 1000 steps. 974 survivors, 1426 reaching palindrome; 981,786 nonpalindrome states, of which histogram certifies 969,752, odd-pair 980,954, and edge 981,596. All are covered by their union.

**Lean sketch:** define a two-element carry type, prove each coefficient carry map monotone and idempotent, compose XOR-labelled finite transducers, then prove F^3=F, U^4=U^2 and the reversal pairing lemma for palindrome edges; finally use the finite exponent-reduction checker as the safety predicate in an existing sound template-step theorem. No Lean files committed. None of these empirical results establishes closure or excludes a future palindrome.
