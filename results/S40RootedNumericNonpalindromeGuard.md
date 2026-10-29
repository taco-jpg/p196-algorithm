# S40RootedNumericNonpalindromeGuard

- **PAPER PROOF:** For every canonical decimal source n of length L>=198 with p12/m9 rooted pairword prefix A=B0 W0^7 W0[:2] (99 coefficients), all 121 true integers R^t(n), 0<=t<=120, are nonpalindromic, for every centre parity and arbitrary interior.
- The exact two-port carry argument enumerates both possible inner high carries; the universal 120-step symbolic computation retains five coefficients at the endpoint, with first odd-witness indices by phase [4,0,1,0,2,0,1,0,2,0,1,0]. Actual overflows are (100010001000)^10 (30 ones).
- Thus every physically canonical rooted T*(q,k;J,U,C) with q>=8 has the **intermediate and terminal non-palindrome premise** for each separately proven 120-step regenerative edge.
- The source/successor phase indexing is explicit: P(n) certifies nonpalindromicity of n, while val10(P(n))=R(n); gamma=1 is handled with the correct one-position high-digit shift.
- Relative to the previous conditional pi135 106-cell guard, this requires only 99 rooted cells. The 98-cell version of this particular common-prefix checker loses its terminal odd witness, but no actual palindrome is inferred.
- Reproduce: python3 calculation/new_structures/S40/guard.py; soundness and all-width proof: calculation/new_structures/S40/TARGET.md. Independent numerical controls are not the universal proof.
- **UNDECIDED:** No renewable J/U/C seam, all-time decimal Lychrel integer, Lean verification, or proof for seed 196 is claimed.
