# X21 palindrome-radius cone: quantitative nonperiodic-centre certificate format

## Exact nearest-palindrome distance: PAPER PROOF

For a positive decimal integer x, define D(x) as its absolute numerical distance to the nearest nonnegative palindrome. Let n be its digit length, k=floor(n/2), and a its leading ceil(n/2) decimal digits interpreted as an integer. The nearest palindrome must be among five candidates: reflect a, a-1 or a+1 into an n-digit palindrome (only valid-length prefixes); or the boundary palindromes 10^(n-1)-1 and 10^n+1. This holds because palindromes of a fixed length are strictly ordered by their leading-half prefixes, and only the immediate neighboring prefixes can improve the distance. The two boundary palindromes handle the adjacent digit lengths. Moreover 0<=D(x)<10^k, because reflecting a changes only the last k digits. D(x)=0 precisely at a palindrome.

For a fixed positive integer r, the radius guard G_r(x) means D(x)>=10^(floor(len(x)/2)-r). When the right side is below one, this is simply the nonpalindrome requirement D(x)>=1.

## Proposed finite certificate FORMAT: PAPER PROOF

Supply integers H,r>=1 and regular languages L_0,...,L_(H-1) of canonical decimal representations folded into digit pairs from the outside inward, with an optional centre. Required four finite proof obligations:

1. A specified decimal seed x0 belongs to L_0.
2. Every word in every L_i satisfies G_r.
3. The genuine reverse-and-add function F(x)=x+rev10(x) maps L_i entirely into L_((i+1) mod H).
4. For every x in every L_i, the H-step image gains at least r in its half-length: floor(len(F^H(x))/2)-floor(len(x)/2)>=r.

Soundness theorem: all iterates x_t=F^t(x0) are nonpalindromic, and D(x_(t+H))>D(x_t) for EVERY t>=0. Inductively x_t belongs to L_(t mod H); the guard forces D(x_t)>0. Write k_t=floor(len(x_t)/2). The guard and drift imply D(x_(t+H))>=10^(k_(t+H)-r)>=10^k_t>D(x_t), using the universal upper bound.

Finite checkability of the FORMAT: the one-step reverse-add graph is a finite-state relation on folded digit pairs. Low-side decimal carry advances inward; the high-side carry can be guessed and consistently verified on the reverse traversal, with a one-column buffer for the possible leading overflow. The guard is regular at fixed r: a finite-state subtract-with-borrow automaton compares x to reflected leading prefixes a,a-1,a+1 and the two boundary palindromes, and remembers whether a nonzero subtraction digit occurs among the highest r+1 positions. Inclusions are tested by product-automaton emptiness. For fixed H, compose H copies of the one-step relation and count overflow increments, checking the exact parity-corrected half-length drift. This describes a finite-checker architecture and a mathematical soundness argument, NOT an implemented universal automata checker, a completed DFA instance, or a Lean proof. A potential Lean endpoint only needs the elementary gap inequality plus correctness of Boolean inclusion checks, proved without axioms/sorry/native_decide.

## Hard decimal tests: COMPUTED, finite horizon only

Independent C++ byte-digit reverse-and-add, nearest-palindrome subtraction, and separately GNU MP whole-integer reverse-and-add and exact numerical subtraction tested all 20,001 orbit states from each seed:

seed | final digit length | maximum gap deficit r | location t | minimum 128-step half-length gain | minimum gap decimal-exponent gain
--- | --- | --- | --- | --- | ---
196 | 8296 | 21 | 12877 | 21 | 8
879 | 8245 | 22 | 6353 | 22 | 5
1997 | 8282 | 21 | 3100 | 21 | 10

Every one of the 19,873 overlapping 128-step windows on each orbit has D(x_(t+128))>D(x_t). All states are nonpalindromic in both independent engines. Deficit means floor(len(x)/2)-floor(log10(D(x))). Finite bounds r=21,22,21 match the corresponding smallest observed 128-step half-length gains, furnishing quantitative potential-function witnesses up to step 20,000. They do NOT imply that those guards, growth bounds, or orbit nonpalindromicity persist indefinitely. In particular a genuine certificate still needs explicit inductively closed regular L_i; increasing finite-horizon distance alone is not closure. Hamming distance to palindrome is not monotone (the 196 run has 9,863 decreases), which motivates numerical radius instead of edit distance.

Reproduce: bash calculation/new_structures/agent-X21/run.sh. The code runs two independent implementations over 20,000 steps each and checks the exact distance, length and palindrome predicates at every step. The summary file is radius_summary.tsv. The open search direction is counterexample-guided DFA refinement of phase-indexed radius guards, rather than a short periodic decimal kink. No base-10 Lychrel certificate is claimed.
