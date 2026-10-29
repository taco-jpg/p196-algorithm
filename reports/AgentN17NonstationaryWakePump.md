# Decimal rooted-particle spacetime pumping with an arbitrary nonstationary wake

**COMPUTED** (complete finite tests enumerated here); **PAPER PROOF** (conditional carry-guard lemma). The primary contribution is a *constructive covariance*, not a negative search result. Base 10 is still UNDECIDED.

## Geometry and exact finite claim

All words are least significant first. Let the rooted exterior A0 be the 39-cell preperiod and 20-cell period written in \`reports/AgentN17DecimalWake44.md\`. For each h, the initial pairword is P_h = A0[:h] ++ reverse(A0[:h]), with optional values a,b in 0..18 overwriting indices h-2,h-1 and their mirrors. Each pair coefficient p is realized by the digit pair (max(0,p-9), p-max(0,p-9)).

Write T(P)=pairs(normalize(P)). Fix cut J=39 and m=20k. For a symmetric pairword P of length n, the insertion I_{J,W}(P) inserts a word W of length m after the first J coefficients and reverse(W) before the final J coefficients. At phase 0, W is precisely the next m coefficients of the period-20 lattice. Thus the h+m seed is I_{39,W}(P_h), and the central arbitrary packet is *not repeated*.

The measured dynamical identity is **not just a matched glider head**. At every reported time t, the two literal integer trajectories X_t=RAA^t(N_h) and Y_t=RAA^t(N_{h+m}) satisfy:

- length(Y_t)=length(X_t)+2m, with identical overflow on each step;
- let P_t be the complete symmetric pairword of X_t, Q_t of Y_t. For every 0 <= i < length(P_t)/2, Q_t[i]=P_t[i] when i<J and Q_t[i+m]=P_t[i] when i>=J;
- both X_t and Y_t are nonpalindromic.

By symmetry the two displayed halfword identities determine the **entire** coefficient word. The central wake may have arbitrary spatial content; it is shifted as a whole. No periodic centre is inserted or assumed.

## Verified scopes (COMPUTED)

The 20,001 states from t=0 through t=20,000 of canonical h=8,000 and h=8,020 pass *both* independent complete tests: literal digit-list kernel and GMP mpz big-integer reverse-and-add (independent decimal-string reversal, addition and base conversion). Each engine compares all **210,008,000** positions across all states; no palindrome or carry/length mismatch, final smaller integer length 26,000 digits.

For all 361 pairs (a,b) in {0,...,18}^2 at h=500, m=20, both engines independently verify 541,861 paired integer states and **372,461,750** coefficient positions, up to t=1500 inclusive, with no mismatch, gamma discrepancy or palindrome. The digit-list engine additionally checks all 361 inputs against m=40,60,80 with the same counts; all 361 inputs with h=1000, m=20 for 2,500 steps (902,861 states, 1,184,892,250 coefficients); and 128 deterministic xorshift32 packets of width 40, m=20 for 600 steps (44,224,000 comparisons). The RNG starts at 0x817aff23 and ends 2616790242.

A crucial positive control of the *limit* of this mechanism is h=250 vs h=270, m=20: the exact padded equality first fails at t=951 in the central shifted-tail coefficients, after the rooted 39 coefficients first diverge at t=940. A checker which assumed the identity indefinitely would falsely pass this control. The smaller h=500 pair first fails after the successful horizon, at t=2095.

## Exact conditional carry-guard insertion lemma (PAPER PROOF)

For any base b>=2, a symmetric coefficient word P of even or odd length n, and a block W of length m inserted symmetrically at a cut J on each side, let f_W(c) be the carry after normalizing W with incoming carry c. Let c_L be the carry entering original P at index J and c_R be the carry entering it at index n-J (these are ordinary low-to-high carry states of P).

**Normalization-splice lemma.** If f_W(c_L)=c_L and f_reverse(W)(c_R)=c_R, then the normalized digit list of I_{J,W}(P) equals that of P with precisely two m-digit blocks inserted at the cuts J and n-J. The added blocks are the normalization digits of W starting with c_L and reverse(W) starting with c_R, respectively. The final overflow digit is identical. Proof: both inserted carry maps restore the incoming carry, so induction over the untouched blocks gives the same digits and carries; this works for any length/content of the intervening core.

**Pairing/alignment guard.** Normalize the two words as above and compare their symmetrized digit sums. For gamma=0, all uninserted pair coefficients match after the natural shift, and the new inserted block W' is the componentwise sum of the two normalized inserted digit blocks in opposite directions. For gamma=1, the overflow shifts the reflection alignment by one digit: there is an additional *one-cell seam condition* where the inner core meets the inserted block. The extra seam equation, plus the two carry fixed-point guards, is necessary and sufficient for T(I_{J,W}(P))=I_{J,W'}(T(P)), with W' computed from the explicit inserted output digits. These conditions depend only on the two carry bits at the cuts, gamma, and finitely many digits at the cuts, **not** on the length or periodicity of the interior word. They can be checked by a finite-state two-ended boundary transducer. This is a sound new conditional *format*, not a claimed all-time decimal certificate.

If a finite graph of phase-labelled guarded edges is found and closed under all outgoing core transitions, each edge supplies the commuting diagram above. Induction allows arbitrarily many insertions and an arbitrary evolving central wake. Combined with an indefinitely preserved odd root witness, such a graph would imply an infinite nonpalindromic orbit. The current experiment only certifies those commuting diagrams for the finite enumerated trajectories; **no closed graph for decimal base 10 has been obtained**.

## Reproduction and redirection

From the repository root:

\`\`\`bash
bash calculation/new_structures/agent-N17/run_pump.sh
\`\`\`

All files are under \`calculation/new_structures/agent-N17/\`. \`pump_universe.cpp\` and \`pump_gmp.cpp\` implement independent exhaustive two-packet checks; \`pump_long.cpp\` and \`pump_long_gmp.cpp\` independently check every coefficient of the 20,000-step pair. \`pump_random.cpp\` tests a seeded 40-cell centre. \`pump_exact_control.cpp\` demands the correct failure when the root is reached; \`pump_scope.csv\` records exact scope and totals.

The new search target is a **carry-guard invariant under arbitrary wake evolution** and a regenerative head that moves *away from the root*, or a continuously renewed root shield. Merely extending the observed 20,000 steps does not yield a Lychrel proof.
