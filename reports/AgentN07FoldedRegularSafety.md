# Folded regular safety certificates: a non-template format

**PAPER PROOF (soundness); COMPUTED (implementation controls).** This is a *new proposed certificate format*, not an existence proof in base 10. It is different from a bounded-centre lattice: a single finite automaton can accept pair-coefficient words with variable-length / expanding interiors and arbitrary branching, and only needs to be forward invariant under reverse-and-add. In particular, an invariant could be a union of regular languages `B_t W_t^* K_t^* V_t^*` (with synchronized parity/phase) where `K_t` is a growing defect. No invariant with an accepted decimal seed has been found.

## Folded digit arithmetic

Fix b>=2. Write an n-digit number from the *two ends* as pair coefficients `P_i=d_i+d_{n-1-i}` for `0<=i<m=floor(n/2)`, outside to centre. If n is odd, record the middle digit `c` separately. `P_0>0` for canonical positive inputs n>=2, and `0<=P_i<=2b-2`. Conversely every such pair word and compatible centre has a canonical positive representative (use `lo=max(0,P_i-(b-1)), hi=min(b-1,P_i)`); ALL representatives produce the same successor pair word.

For each outside-to-centre index i, let `l_0=0`, `l_{i+1}=floor((P_i+l_i)/b)` and `a_i=(P_i+l_i) mod b`. Guess `r_0=gamma` (0 or 1) and a high-side carry path `r_{i+1}` satisfying `r_i=floor((P_i+r_{i+1})/b)`; let `z_i=(P_i+r_{i+1}) mod b`. At the centre, if n even require `r_m=l_m`. If n odd let `d=(2c+l_m) mod b` and require `r_m=floor((2c+l_m)/b)`. This is exactly column addition, from both ends.

If `gamma=0`, output paired coefficients `a_i+z_i` and (when n odd) centre digit `d`. If `gamma=1`, output pair coefficients `a_0+1` and `a_i+z_{i-1}` for `1<=i<m`; if n even, the new central digit is `z_{m-1}`; if n odd, append the last pair `d+z_{m-1}` (new length is even). For the n=1 special case the successor is `2c`, with the ordinary one-/two-digit split. Hence **the entire one-step action is a finite-state rational transduction of the folded pair language**: it remembers only two carry bits, previous high digit (at most b values), first-pair and parity flags. The gamma=1 delayed upper digit is the important additional phase missing from naive period-fixed band models.

## New certificate format and soundness

A finite DFA A reads coefficients `P_i` outside to centre, accepting either even-length digit strings (no middle digit) or odd-length ones after a final middle digit. The alphabet and centres are finite. Require:

1. The initial canonical integer N has an accepted folded encoding.
2. Each accepted word has at least one ODD `P_i` (this is a sound palindrome obstruction, indeed necessary and sufficient if all integer realizations of the coefficient encoding must be nonpalindromic).
3. Under the exact two-sided carry transducer above, EVERY accepted word maps to another accepted word, including both length parities and gamma cases.

Then **for all t>=0, reverse-add^t(N) is not a palindrome**. Proof: (i) grade-school addition and both carry recurrences show the output encoding is exact; (ii) by condition 3 it remains in the DFA language by induction, including arbitrary length growth; (iii) condition 2 supplies an unequal mirror digit pair on every iterate. Neither exact template equality nor a bounded/stationary centre is needed.

Both conditions 2 and 3 are *decidable by finite graph reachability*: (2) product of A with a one-bit `seen_odd` flag and nonzero-leading guard; (3) product of source A, target A and the transducer states, searching for an accepted source with an unaccepted successor. The implementation `regular_certificate.py` performs the full all-length inclusion check for simple centre-independent DFA acceptors, including the n=1 edge case. An arbitrary centre-dependent acceptance guard is a straightforward extension; current code does not claim to support it. The state space is finite, so empty counterexample BFS proves inclusion, with no bound on the number of pair columns. If A rejects all words the certificate is vacuous; the required accepted seed rules that out.

A Lean implementation needs (a) a digit-list theorem for the folded `P` transduction, (b) finite graph reachability as a reflected Boolean inclusion test, and (c) `lychrel_of_dfa_invariant` by induction. This is a proof sketch, NOT a Lean kernel result.

## Mechanism and controls

The base-146 control motivating this direction has a four-step neutral-band exterior with e and gamma `0101`, an exact palindromic centre and +1 band gain every four steps (`results/Agent10Base146NeutralCycle.md`). Its carry-through-band mechanism suggests replacing exact centre return by a **regular, growing family of centres** accepted by a phase-and-carry DFA. Folded automata can represent that family, and the gamma=1 transition automatically shifts the high-side digit alignment without a prescribed fixed centre.

Tested: 31,900 deterministic seeded random source pairs (bases 2..30, up to 10 folded pairs), plus exhaustive all positive source integers n<b^4 for bases 2..8 (8,764 cases). In each case the direct folded transition matches BOTH arbitrary-precision `n+reverse_b(n)` and a separate ordinary digit-list algorithm. The all-positive one-state DFA is proven forward-closed by exhaustive finite product reachability for bases 2..30 (but it is NOT palindrome-free). The odd-pair witness DFA is palindrome-free but fails closure in every tested base: decimal `10 -> 11` is a minimal obstruction. **Direction change:** replace the global odd-witness condition by a phase-aware regular invariant containing a *moving witness* and carry-state constraints, not a fixed short centre.

Separate independent C++17 ordinary decimal digit-list replay of seed 196: 20,000 updates, 20,001 nonpalindromic states, final length 8,296 digits. The overly simple odd-pair witness fails already at step 8 (`1067869`: pair coefficients `[10,6,14]`), and appears at only 19,998 of those 20,001 states. This tests why a DFA must encode a richer palindrome obstruction than 'odd coefficient somewhere'; it does **not** prove 196 is Lychrel. The format may need to enrich its alphabet with the low/high *individual* digits to exploit nonpalindromicity when all pair coefficients are even. A two-track folded alphabet supports that refinement with the same finite-state closure argument.

## Reproduce

From repository root: `bash calculation/new_structures/agent-N07/reproduce.sh`, requiring Python 3 and a C++17 compiler. No external dependencies, SAT solver, shell networking, or hidden data. The compact expected numeric results are in `results.json`. No source under `lean/`, no 196 proof, and no CLAIM of full-repository `tools/verify.py --changed` success (shell git DNS is unavailable in this environment).