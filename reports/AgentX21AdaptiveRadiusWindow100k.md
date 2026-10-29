# X21: Adaptive 128-step radius relation, 100,000 decimal steps

## New FORMAT (PAPER PROOF)

For a decimal integer x let F(x)=x+rev10(x), k(x)=floor(len10(x)/2), and D(x) be the minimum absolute numerical distance from x to any decimal palindrome. The predecessor-radius universal bound D(x)<10^k(x) follows by reflecting the leading ceil(len(x)/2) digits.

Fix a positive macrostep length H. A finite certificate consists of phase-indexed regular folded-digit languages L_0,...,L_(H-1), an explicit seed x0 in L_0, and the following exact obligations:
(1) All the first H seed states x0,...,F^(H-1)(x0) are nonpalindromic.
(2) The exact reverse-add relation maps each L_i into L_((i+1) mod H).
(3) For every x in every L_i, the H-step relation satisfies D(F^H(x))>=10^k(x).

**Soundness.** All states belong to the corresponding L_i by induction. For any t, obligation (3) and the universal predecessor bound imply D(x_(t+H))>=10^k(x_t)>D(x_t). The first H states are nonpalindromic by (1); every subsequent state has positive D from (3). Therefore the decimal seed is a Lychrel number, with strictly increasing nearest-palindrome distance every H steps, *provided the finite obligations are actually certified*. No such decimal languages or closure check are supplied in this result.

**Why a finite check is possible:** the one-step reverse-add graph on outside-in folded digit pairs has a finite carry transducer, including the possible one-digit overflow. Composition for fixed H produces an exact finite-state relation with bounded length drift. The comparison D(y)>=10^k(x) between the H-step source x and target y is also regular on paired encodings: nearest palindrome is among the three reflected adjacent leading-half prefixes and two length-boundary palindromes; the subtraction borrow and relative half-length offset have finite state because len(y)-len(x) is between zero and H. A product automaton checks inclusion of each L_i followed by the H-step transducer into the desired radius relation; its emptiness is a finite witness. These are mathematical soundness/regularity statements, not an implemented DFA checker or Lean formalization.

Unlike the earlier uniform single-number guard with one fixed r, this is a **two-time relational cone** that permits temporary large palindromic proximity when a sufficiently large local length gain accompanies it.

## Hard test (COMPUTED, not infinity)

The byte-digit exact nearest-palindrome engine in the first X21 commit ran the 196 orbit t=0..100,000. There were zero palindromes; final decimal digit length 41,490. In all 99,873 windows t=0..99,872:
- Exact nearest-palindrome distance strictly increases from t to t+128.
- The stronger relational check floor(log10(D(x_(t+128)))) >= floor(len10(x_t)/2) holds without exception.
- The minimum gap-exponent gain is 1, and minimum half-length gain is 21.

The maximum deficit k(x)-floor(log10 D(x)) is 26 at t=44,105, whereas the minimum 128-step half-length gain is only 21. A uniform r=21 bound therefore cannot establish the longer result. Locally this does not fail: the window ending at t=44,105 starts at t=43,977 and gains 28 half-length digits; its successor radius deficit is 26.

Independent full decimal-string arithmetic replay checked all 100,001 states for palindrome status, length and Hamming mismatches, with zero differences against the byte-digit engine. At 202 sampled states (every 500th plus t=44,105) independent GMP full-integer palindrome-distance subtraction agreed on the decimal exponent and leading nine digits. The full exact distance comparison at every window was performed by the byte-digit engine, and the independent engine did NOT recompute every 100,001 full GMP distances. Scope is 100,000 finite steps, only seed 196, no theorem about its infinite orbit.

Reproduce with bash calculation/new_structures/agent-X21/run_100k.sh; requires g++, GMP C++ headers/library and Python3. Compact numerical data: calculation/new_structures/agent-X21/adaptive_radius_100k.tsv. Search direction: synthesize phase-indexed folded regular languages for the relational radius condition, using counterexample-guided abstraction. The current result is a mathematical FORMAT and a quantitative finite control, not a base-10 Lychrel certificate.
