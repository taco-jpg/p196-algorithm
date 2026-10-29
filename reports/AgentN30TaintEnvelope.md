# Agent N30: set-valued exterior taint envelopes

**COMPUTED.** A new finite-state decimal certificate format; no infinite base-10 Lychrel instance has been found.

## Exact format

For an n-digit decimal N with n >= 2k+1, record sets A[i], B[i] of possible low-side and high-side digits for every i<k. The middle is arbitrary. Compute coefficient sets P[i]={a+b: a in A[i], b in B[i]}, subsets of 0..18. For coefficient set X and carry set C subset of {0,1}, let Norm(X,C) return all digits (x+c) mod 10 and carries floor((x+c)/10).

Normalize P[0]..P[k-1] from initial carry {0}, obtaining low output sets L[i]. Separately normalize P[k-1]..P[0] from incoming carry {0,1}, obtaining high output sets H[i] indexed from the most-significant end and final carry set G. Define next A'[i]=L[i]. When 0 is in G, include H[i] in B'[i]. When 1 is in G, include {1} in B'[0] and H[i-1] in B'[i] for i>0. Union the relevant branches. This deliberately overapproximates correlations, never excludes a genuine possibility.

**One-step soundness (paper proof):** Each actual pair coefficient belongs to P[i]. Local normalization preserves membership, by induction on the known first and last k positions; an unknown interior enters the high scan only through a carry in {0,1}. The result's length is n or n+1. The high-side shift on overflow is exactly the second branch. Thus if actual N is represented by envelope E, actual N+rev(N) is represented by Step(E). Since N+rev(N)>=N, n>=2k+1 persists. **Palindrome guard:** if some A[i] and B[i] are disjoint, no represented number is a palindrome.

A **finite infinite-orbit certificate** would be any safe envelope list E0..Es with each edge equal to Step and Er=Es for some 0<=r<s, with a disjoint pair at every stage. The finite deterministic envelope map and induction imply all actual numbers in E0 have infinite palindrome-free orbits. This is a rigorous certificate format, not an extant decimal certificate. Lean sketch: implement masks as Finset (Fin 10), prove membership of digit and carry normalization, prove StepSound by the two scans, derive NotPalindrome from a disjoint pair, then iterate a checked finite lasso.

## Positive decimal family and exact computations

Generate 5,800 low digits and 5,800 high digits with xorshift64 seeded 0x9a702f4ed37008c5, alternating low then high draws modulo 10; replace high[0] with 1+(high[0] mod 9). For ANY nonempty decimal middle word M, seed N0(M) = high[0]...high[5799] ++ M ++ low[5799]...low[0]. The fixed-width set-valued envelope has a disjoint digit-pair witness at every time 0..20,000, with first witness index at most 20. At time 20,000, 5,737 of 5,800 pairs have at least one nonsingleton digit mask, but the witness persists. Unlike the preceding agent-N30 concrete shrinking cone, no known-position width is discarded.

Independent base-10^9 limb bigint arithmetic in taint_family.cpp verifies full N+reverse(N), every claimed outer mask inclusion, and the palindrome predicate on all 20,001 states. It passes with M=0, M=3 repeated 37 times, and M=9 repeated 123 times; the final integer lengths are respectively 19,847, 19,883, and 19,969 digits. The universal-centre conclusion follows from soundness, not sampling. An independent Python implementation validates 198,000 randomized exact-integer memberships/guard implications.

**Limits:** This does not prove that the orbit is infinite without a palindrome. No safe envelope cycle has been found; after enough steps, taint may erase the witness.

## Reproduction

Run Python: python3 calculation/new_structures/agent-N30/test_taint.py

Compile C++: c++ -O3 -std=c++17 calculation/new_structures/agent-N30/taint_family.cpp -o /tmp/n30_taint

Run: /tmp/n30_taint 5800 20000 1 0 ; /tmp/n30_taint 5800 20000 37 3 ; /tmp/n30_taint 5800 20000 123 9

Expected: PASS; checked_integers=20001; max_first_witness=20, with 5,737 uncertain pairs at step 20,000.
