# S38 running notes

- Read the current AGENTS.md, OPEN_PROBLEMS.md, docs/FOCUS_SWARM.md,
  FORMATS.md, N-series audit, R30 checker target, and the last available
  page of #475 comments. Issue #475 has 1,743 comments; fetched only its last
  API page with per_page=40&page=44 (23 comments on that page).
- Registered CLAIM agent-S38: F1/K1 ODD-CENTRE MOD-101 CARRY-SOURCE LIFT
  in #475 (comment 6497991848), following the explicit parity-extension
  concern in the latest S12 audit relay.
- Proved that the S12 carry-source delta algebra does not depend on |C|
  being even: U and reverse(U) reset the carry after one block; the carry
  trace across C is therefore unchanged and simply shifts by 15 positions.
  The suffix shifts by 30 positions. This includes odd palindromic C with an
  even midpoint coefficient, so the pairword is physically realizable.
- Compiled odd_centre_delta.cpp with g++ -O3 -std=c++17 -Wall -Wextra -Werror.
  It passed 69,120 controls: 30 U motifs x 3 junctions x 3 odd centres x 256
  independent q/k pairs from q,k in {20..23,40..43,80..83,160..163}.
  For every case, both P(q,k) and P(q,k+5) were realized as actual canonical
  decimal integers; cpp_int n+reverse(n), a fresh-buffer schoolbook adder,
  and coefficient normalization agreed, and the exact predicted delta of K
  matched direct K(P(q,k+5))-K(P(q,k)).
- Independent Python bigint verifier passed 8,370 controls: the full 3x3
  junction/centre cross-product at q,k in {20,40,80,160}, plus the off-diagonal
  q=20..23, k=40..43 phase grid across all U/J/C choices. It independently
  checked both real source and target integer steps and the K identity.
- The all-width proof is symbolic and uses only the exact carry reset and
  period-four identities. Finite controls validate the implementation, not
  the universal quantifiers. No 120-step return or Lychrel number is claimed.
- No Lean file is included because this environment has no Lean/lake toolchain
  and the repository's tools/verify.py --changed could not be run locally.
