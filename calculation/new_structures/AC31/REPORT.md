# AC31 phase-10 two-ended endpoint carry-cone correction

**Label: COMPUTED** (120-layer exact finite-state recurrence), accompanied by a **PAPER PROOF** of its physical soundness. Not Lean-verified. **Full fixed-seam phase-10 |J|=5 return remains UNDECIDED. No all-time decimal Lychrel certificate.**

## Exact missing lemma supplied

A sound physical, endpoint-only two-ended carry-cone enclosure covering **every** possible interior, without strict-phase W9 assumptions, supplies a reusable necessary-condition kernel for sound fixed-junction searches and disproves AB31's alleged index-8 exclusion.

## Universal statement

Let B10 and W10 denote the published rooted phase-10 rows of calculation/decimal_frontier/lattice_kinks/data/lat_p12m9.txt, of lengths 34 and 9 respectively. For ANY positive decimal integer whose palindromic pair-coefficient word has the first 160 coefficients, and symmetrically the last 160, equal to B10 ++ W10^14, with arbitrary legal interior, the first 120 **ordinary decimal reverse-and-add** steps have exactly the published overflow clock starting at phase 10 (30 overflows). After step 120, the first **40** pair coefficients are **exactly** the original first 40 coefficients, not merely compatible with them. Consequently this applies to **every q>=14**, every 5-coefficient J, every 30 charge-zero U3 rotation, every U repetition count and every palindromic realizable C of either parity. There is NO claim that the full W9 band, seam or C returns.

## Soundness argument (PAPER PROOF)

For an n-digit positive integer with LSD-first symmetric pairword P, coefficient P_i=d_i+d_(n-1-i) lies in [0,18], and its genuine next value is the ordinary decimal normalization of sum_i P_i 10^i. Suppose both outer L coefficients are known and n>=2L. Normalize the **low** L coefficients with incoming carry 0. Normalize the **high** L coefficients (the reversed same outer strip) with the entering carry from the unknown middle. The high inlet is **either 0 or 1**, since coefficients are at most 18, so explicitly branch on BOTH; no centre or W9 hypothesis is imposed. The top outgoing carry gamma is the genuine number-length increment. When gamma=0, pair aligned low/high digits; when gamma=1, add the new top digit 1 and shift the high digit pairing one position. Reject gamma=0 with leading output zero, because N+reverse(N)>=N cannot shorten. These cases contain every actual next outer pairword prefix of length L−1. Since the positive number never shrinks, its length is always >=2(L−1), permitting induction. Thus the finite enclosure is valid for every interior, even when intermediate W9 damage later heals.

The published prefix has L=160. The executable 120-fold set recurrence keeps every legal unknown high-carry branch; at each step it has exactly 1 or 2 distinct possible prefixes, **all** with the same forced gamma (the published phase-10 overflow clock), and at t=120 exactly one length-40 prefix remains. That prefix equals the original first 40 coefficients. All 120 exact states/clock counts are in PREFIX_STATES.tsv. The general enclosure theorem is a mathematical proof; the particular 120-step finite set calculation is COMPUTED, not checked by Lean.

## Correction of AB31 and independent physical verification

AB31's #476 CELL asserted that all its sample phase-10 junctions had a first mismatch at LSD pair-coefficient **8**, observed 10 versus the root target 9. That universal premise is incompatible with the correct published B10/W10: the universal cone forces coefficient **8 to be 9** after 120 steps for ANY interior. Hence rejecting seams based on index 8 is invalid.

Independent Python arbitrary-precision N+int(str(N)[::-1]) and a separate digit-array pairword normalizer agree at **every step** for 20 controls over (q,k)=(14,100),(20,80),(40,160),(80,320),(160,640), with odd C=[4,14,4], even C=[4,4] and four J/U choices. Their first q=14 mismatches are [138,135,142,135], never 8. There are 30 actual length increments in each complete 120-step replay.

Additional systematic, genuinely physical **1,140** q=14/k=100 controls cover J=(j,0,0,0,0), j in 0..18, all 30 U3 rotations and both fixed C above. Exact full-return count: ZERO. First mismatch histogram (LSD coefficient index : cases): **135:372, 136:288, 138:406, 139:34, 140:34, 141:6**. Each control was compared against the independent digit-array normalization for all 120 steps. This constitutes ONLY **PARTIAL(1,140/148,565,940)** in the two-fixed-centre |J|=5 cell and is NOT an exclusion of arbitrary J, let alone a proof of an all-time decimal Lychrel number. The 120-step cone's correct first-40 restoration is a necessary constraint only; later seam closure is open.

## Reproduction

From repository root:

1. python3 calculation/new_structures/AC31/test_phase10_cone.py calculation/decimal_frontier/lattice_kinks/data/lat_p12m9.txt
2. python3 calculation/new_structures/AC31/phase10_cone.py --audit --write-tsv /tmp/phase10_states.tsv
3. python3 calculation/new_structures/AC31/control_census.py calculation/decimal_frontier/lattice_kinks/data/lat_p12m9.txt 0 10
4. python3 calculation/new_structures/AC31/control_census.py calculation/decimal_frontier/lattice_kinks/data/lat_p12m9.txt 10 19

The one-step property was independently exercised on 15,000 randomly realized decimal integers; all four high-inlet/gamma combinations were hit. This corrects a false census pruner but leaves the all-time seam-regeneration lemma open.
