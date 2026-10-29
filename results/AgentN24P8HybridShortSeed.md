# AgentN24P8HybridShortSeed
- **COMPUTED** base 10, exact finite steps 0..20,000, not an infinite Lychrel proof.
- New period-8 / spatial-48 rooted hybrid `B0 ++ W0^67 ++ 9^20 ++ [18] ++ mirror` gives a concrete 6,495-digit seed, versus earlier N24 p12/m9 seed 8,329 digits.
- Independent decimal big-integer and digit-list replays both pass all 20,001 palindrome, overflow and pairword checks: full 11-coefficient temporal root plus at least 256 lattice coefficients per half; 16,495 digits at step 20,000.
- Every iterate has least and most significant decimal digits unequal; matching lattice frontier 3216→297 (mean inward speed 0.14595 coefficient/step), no closed or regenerative interface proven.
- New positive transition: central `9^20` forms an interior zero run of length 17 by step 5; this absorbing band is finite-lived, not an invariant.
- Reproduction: `python3 calculation/new_structures/agent-N24/reproduce_p8.py 20000` (independent arithmetic checkers, SHA-256, shape and controls).
- Files: `calculation/new_structures/agent-N24/{p8_hybrid_data.json,p8_bigint_evidence.json,reproduce_p8.py}` and `reports/AgentN24P8HybridShortSeed.md`.