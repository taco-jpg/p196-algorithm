# Agent X12: two-clock moving-centre splice and adaptive 264-step macro-envelope

**Label: COMPUTED.** This is a finite positive mechanism. The conditional format below is a suggested proof architecture, not a verified decimal certificate.

## Pairwords and the centre pump

For a decimal integer N, its palindromic pair-coefficient word is P_i=d_i+d_(n-1-i), least significant first. The exact next pairword is G(P)=pairs(normalize_10(P)), including any top overflow. It depends only on P, not the particular decimal realization of P.

Take the p8/m20 rooted B0 (39 coefficients) and W0 (20) as written explicitly in `beat.py`. Put U=forty copies of 1 with U[13]=7, U[20]=7, U[30]=6. Define

    C_r=[8,0,0] ++ U ++ 1^r ++ [16] ++ 1^r ++ reverse(U) ++ [0,0,8],
    P_(q,r)=B0 ++ W0^q ++ C_r ++ reverse(W0)^q ++ reverse(B0).

We compare TWO actual orbits starting from canonical decimal digit-pair realizations of P_(q,r) and P_(q,r+1). A symmetric splice at position k inserts coefficient s at low position k and its mirror, with *all* remaining coefficients identical after deleting those two sites. This is a full-pairword relation, not just an exterior-prefix agreement. At t=0 the splice is the extra pair of 1s beside the central 16.

## Measured mechanism

For q=7,r=850, the full-word splice survives for all t=0..1000. For every t>=1 in this finite interval the inserted coefficient is phase-cycled by 2,4,8,16,14,10 (period 6); s0=1. Write k_t for the maximal compatible splice position, and n_t for the current base orbit's digit length. All t=0..988 satisfy

    (k_(t+12)-floor(n_(t+12)/2)) - (k_t-floor(n_t/2)) = -5.

All t=0..736 satisfy k_(t+264)-k_t=-44. The overflows alternate 1,0 through step 999. The 264-step beat is the least common multiple of the 12-step inner displacement clock and the previously known 88-step exterior clock. In the stable regime, the geometric mechanism has a *second* glider: it moves -2 absolute digits per 12 steps, while the previously reported exterior defect moves -20 per 88. Over the 264-step beat their absolute displacements are -44 and -60, respectively; the distance between these fronts increases 16, rather than closing automatically.

For q=1,r=850 the full-word splice also survives through step 1000 (with no palindrome). However, the first 12-step **relative** drift disagreement occurs for the comparison starting at t=613, the first 264-step absolute drift disagreement begins at t=364, and the first departure from alternating overflow is the edge t=622. These timings are different because a 12/264-step comparison can span a later change. The coefficient phase still cycles with period six. Therefore an 88-only scalar band counter does not predict the pulse's displacement: the carry/overflow envelope has to be part of the macro-state.

A small-centre collision survey gives the following **finite** exact first splice-failure times: for r=5k+s with 1<=s<=5, L=6k+[13,15,16,16,17][s-1], checked for every r=1..100, using q=1. This is a deterministic 5-site/6-step collision staircase in that range, not a proof for r>100. A splice death is NOT a palindrome.

An independent Python built-in-integer replay builds four legitimate base-ten numbers for (q,r)=(7,850),(7,851),(1,850),(1,851), performs true N+reverse(N) on decimal strings for 1000 updates per number, and tests equality of each entire resulting pairword against a separate coefficient-normalization engine. All 4004 state checks and 4004 nonpalindrome tests pass. No external computational packages are needed.

## New proposed certificate FORMAT: adaptive two-clock envelopes

A putative all-time edge uses a state (phase in Z/264, q>=q_min, r>=r_min, k, carry-gates) and a two-band palindromic pairword

    B_phase ++ W_phase^q ++ L_phase ++ U_phase^r ++ M_phase
       ++ reverse(U_phase)^r ++ reverse(L_phase)
       ++ reverse(W_phase)^q ++ reverse(B_phase).

The W band has a temporal eight-phase exterior schedule, the U band a six-phase interior schedule, and L/M are finite literal interfaces. The distinguished symmetric splice k may move between literal and repeating regions; its value can be affine in q,r on each finite guarded mode. Crucially, the transition is allowed to branch on **actual two-ended incoming carries** and overflow, rather than declaring the -44 speed eternal. A macro-edge over 264 steps must establish an exact equality of whole pairwords, not just a local glider recurrence, with an affine parameter update (q,r)->(q+a,r+b). Both counters must remain in a nonempty invariant Presburger domain and every state must carry an odd pair coefficient (a palindrome would have only even pair coefficients).

**Precise conditional soundness.** Suppose a finite directed cycle of such guarded templates has an exact universal transition equation G^264(P_i(q,r))=P_(i+1)(F_i(q,r)) for ALL integer (q,r) in each invariant domain, including correct base-ten carry, overflow, leading digit, and gate conditions. Suppose F_i maps the domain into its successor, every P_i is realizable by a positive decimal integer, and an odd pair coefficient is present in every template. Then every integer realizing P_0(q,r) has an infinite palindrome-free reverse-add orbit. Proof: G is exactly the pairword transformer for any decimal realization, so induction gives the prescribed pairword and domain at every macro-edge; finite intermediate phases are included in the guarded edge check. A palindrome has all pair coefficients even, contrary to the witness. This is a mathematical induction, NOT a claim that the needed decimal closed edges have been found.

**Finite checker route.** Normalize each literal/repeated block with a two-state carry transducer (neutral/absorbing); treat each segment boundary as an affine function of q,r. Pairing with its reversal yields a finite system of comparisons between piecewise periodic words. Their validity for ALL q,r in a Presburger domain is decidable by a finite arrangement of affine endpoint-order cells plus fixed-modulus residue tests, or directly by Presburger arithmetic with bounded digit/carry case splits. This gives a sound way to check candidate macro-edges without extrapolating a single long integer orbit. One must include local gates and all intermediate states in the check, especially when the outer overflow schedule changes.

## Exact limitations and reproducibility

No 264-step renormalization return with nonnegative two-counter growth has been found; the observed inward outer-front loss of 60 per 264 is not replenished by the extra inner pair. The finite pulse law is not an infinite decimal Lychrel witness and says nothing about the orbit of 196. The next constructive search is a carry-gated renewal edge compensating the outward clock's -60 displacement, not another unbounded initial-reservoir replay.

Run `python3 calculation/new_structures/agent-X12/beat.py`. The Python result file `observations.json` records the exact observed scopes. GitHub DNS prevents local cloning in this environment, so repository-wide `tools/verify.py --changed` was not run. No Lean files were added.

