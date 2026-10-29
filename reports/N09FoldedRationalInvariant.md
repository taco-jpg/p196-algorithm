# N09: Folded rational transducer and DFA-invariant certificate format

**Status:** PAPER PROOF for the exact symbolic transducer and conditional induction theorem; COMPUTED for finite tests and a 20,000-step replay. **UNDECIDED** whether any nonempty, safe, inductively closed decimal regular language contains an actual orbit seed. This is NOT a decimal Lychrel certificate or a claim about infinity.

## Encoding

For a positive decimal integer with little-endian digits d[0..n-1] and nonzero most significant digit, let P[i]=d[i]+d[n-1-i] (0..18). This is symmetric. Write its folded encoding as the first k=floor(n/2) coefficients x[0..k-1] and terminal symbol E for even n, or O(z) for odd n with central coefficient z=P[k] even (0..18).

Valid input words have x[0]>=1 when k>0. For k=0 the sole permitted word is O(z) with positive even z. Every valid word is physically realizable by choosing digit pairs of the given sums with a positive most significant digit. The exact integer successor N+reverse(N) is the base-10 normalization of P with initial carry 0. Hence the next folded pairword depends only on the current folded pairword.

## Exact two-ended rational transducer

Choose final overflow gamma in {0,1}. At the outermost symbol start with low carry c[0]=0 and high/backwards carry t[0]=gamma. Reading an outer coefficient x[i], guess t[i+1] in {0,1} and enforce all four arithmetic identities:

    low[i]  = (x[i]+c[i]) mod 10
    c[i+1]  = floor((x[i]+c[i])/10)
    high[i] = (x[i]+t[i+1]) mod 10
    t[i]    = floor((x[i]+t[i+1])/10)

The output folded-pair coefficient at i is low[i]+high[i] if gamma=0. If gamma=1, the first output is low[0]+1 and each later output is low[i]+high[i-1]. Thus the state needs only the two carry bits, the previous high digit (0..9), a first-symbol flag and gamma.

On source terminal E, enforce c[k]=t[k]. Destination terminal is E if gamma=0 and O(2*high[k-1]) if gamma=1. On source terminal O(z), put a=(z+c[k]) mod10 and enforce t[k]=floor((z+c[k])/10). Destination is O(2*a) if gamma=0; if gamma=1 append a+high[k-1] to the output outer coefficients and use terminal E. For a one-digit source k=0, replace high[-1] by the literal leading digit 1 in this final gamma=1 rule.

These terminal cases account for every parity and possible length increment. The backwards carry is guessed by a finite NFA, but the centre consistency equation makes the surviving transition exactly equal to true normalization; there are no approximate or omitted carries. The output length can increase by one outer coefficient at the terminal, so this is a **rational transduction with finite terminal epsilon moves**, not necessarily a strictly synchronous Mealy machine.

## Exact palindrome-predecessor language

The same finite transducer recognizes whether the normalized integer is a palindrome. For gamma=0 require low[i]=high[i] for every outer i. For gamma=1 require low[0]=1 and low[i]=high[i-1] for i>0. On an odd source with gamma=1, also require centre-normalized a=high[k-1]; for k=0 require a=1. For gamma=0 an odd-length centre needs no extra equality. These checks define a regular language **PrePal** over folded words, and correctly handle all-even inputs which are not themselves palindromes.

This is strictly stronger than the naive condition "some odd pair coefficient": seed 196 has no odd pair coefficient at steps 8, 13, and 19, but all three corresponding integers are nonpalindromic.

## PAPER PROOF: soundness of a proposed finite certificate

Take any complete finite DFA A on outer symbols 0..18 and terminal E / O(0),O(2),...,O(18); restrict its language L to valid folded words. Suppose:
1. The folded pairword of a specific positive *nonpalindromic* starting decimal integer N0 belongs to L.
2. The exact transduction R of the preceding section obeys R(L) subseteq L.
3. L intersect PrePal is empty.

**Theorem.** Every integer N[t+1]=N[t]+reverse(N[t]) in this orbit is non-palindromic.

**Proof.** Pair addition and ordinary low-to-high carries show that normalization of P(N[t]) is N[t+1]. By the explicit carry identities and centre equations, R takes exactly P(N[t]) to P(N[t+1]). The seed belongs to L, so closure in (2) proves by induction that every P(N[t]) belongs to L. By (3), normalization of none of these pairwords is palindromic, so every N[t+1] is not a palindrome. The separate N0 hypothesis handles t=0. QED.

This is a sound *format*, not a found invariant. It can recognize irregular non-periodic interiors and does not require a fixed-width centre or a spatially periodic absorbing band.

## Finite DFA checker

The graph product A x PrePal decides (3). The product of the source DFA A, target complement DFA not-A, and the finite relation R decides whether R(L) minus L is empty. Both are finite-state reachability problems independent of source length. The supplied 'dfa_checker.py' performs these BFS checks and reconstructs a concrete witness if either obligation fails. An exhausted graph is marked PASS; a state-cap interruption is CAPPED and never asserted as a proof.

Controls: EMPTY is vacuously safe and closed (16 safety/82 closure states explored); ALL is closed (82 states) but unsafe; ODD is neither successor-safe nor closed. The ODD counterexample has input folded coefficient [1] and normalized integer 11, so the unsafe assumption "input has odd pair coefficient therefore its successor cannot be palindrome" is refuted. These are correctness smoke tests, NOT positive decimal certificates.

## Reproduction and computed decimal data

From the repository root run:

    bash calculation/new_structures/agent-N09/run_checks.sh

The runner needs python3, g++, and GMP development libraries (gmpxx/gmp). It compiles 'replay.cpp' then checks:
* 999 exhaustive source integers and 12,000 seeded random canonical strings of lengths 1..89; exact folded relation, successor-palindrome recognizer and deliberate wrong-output tests;
* 2,500 successive decimal-196 transitions, independently comparing the finite-state relation with digit-list reverse-add and palindrome testing;
* all 20,001 states at times 0..20,000 of the true 196 reverse-add orbit with independent GMP arbitrary-precision integer and little-endian digit-array arithmetic, complete pair-word normalization at each transition, and digit-for-digit equality across implementations.

Expected final replay numbers: steps=20,000; final_digits=8,296; overflows=8,293; pal_states=0; all_even_half_states=3 (exactly steps 8,13,19); FNV-1a digest 358f091cfd74470d. Replay log is a small tracked text file, 'calculation/new_structures/agent-N09/replay_196_20000.txt'; the runner diffs all lines against freshly generated output. Example output terminates with 'AGENT_N09_ALL_CHECKS_PASSED'.

**Scope limitation:** this is finite decimal computational evidence and a general finite-state conditional theorem. It does not discover a safe nonempty decimal DFA, does not establish a 20,000-step repeating shape, does not provide a Lean proof, and makes no claim about 196 or any other integer beyond the tested finite steps. The next constructive task is counterexample-guided DFA synthesis using real orbit positive examples with the exact two product-graph checks as the oracle.
