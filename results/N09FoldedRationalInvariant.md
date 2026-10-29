# N09 Folded Rational Regular-Invariant Certificate Format
PAPER PROOF: decimal reverse-and-add on symmetric pair-coefficient words is an exact two-ended finite-state rational relation on their folded encodings (including the centre parity marker).
PAPER PROOF: for any finite DFA language L over valid folded words, seed-in-L, successor closure R(L) subset L, and disjointness from the regular predecessor-of-palindrome language imply an infinite non-palindromic orbit, provided the starting integer is not palindromic.
COMPUTED: independent 20,000-step decimal vector/GMP/pair-normalization replay of seed 196, zero palindromes, final 8,296 digits; all-even folded coefficients at steps 8, 13, 19, showing parity-only safety is inadequate.
COMPUTED: 12,999 short/random transducer differential cases and 2,500 full decimal-196 folded-relation checks; product-DFA smoke tests return exact counterexamples and empty-graph proofs as expected.
UNDECIDED: whether there exists a nonempty closed safe regular language containing the pairword of 196 or any other decimal seed; no base-10 Lychrel number is proved.
Code and data: `calculation/new_structures/agent-N09/` (`transducer.py`, `dfa_checker.py`, `replay.cpp`, `replay_196_20000.txt`, `run_checks.sh`).
Full definition, soundness argument, limitations and reproduction: `reports/N09FoldedRationalInvariant.md`.
