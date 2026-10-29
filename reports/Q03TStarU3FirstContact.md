# Q03: T* U3 first-contact interface table

**Label: PAPER PROOF.** This is a target-specific necessary-condition theorem for the rooted decimal p12/m9 T* family, not a full seam return or a decimal Lychrel certificate.

## Statement and quantifiers

Let B_t,W_t be the 12 phase rows in calculation/decimal_frontier/lattice_kinks/data/lat_p12m9.txt. Let g_t=1 iff t≡0 (mod 4). Let U_0 be any of the 30 distinct rotations of (9,a,18-a), a∈{0,2,...,18}, and define U_(t+1)=F_(g_t)(U_t) by the exact periodic low/high-carry bulk map in calculation/new_structures/T12/cut.py. Then U_120=U_0; every U_t is again one of those 30 words, has exactly one 9, has two even non-9 entries summing to 18, and has no adjacent 9s.

For any rooted canonical symmetric pairword

P_t = B_t ++ W_t^q ++ J ++ U_t^k ++ C ++ reverse(U_t)^k ++ reverse(J) ++ reverse(W_t)^q ++ reverse(B_t),

where J is any finite coefficient word, C is any realizable palindromic coefficient centre, and the tested contact coefficient j lies at least one full three-cell U block away from both ends of U_t^k, compare P_t with R_t, obtained by replacing just P_t[j]=P_t[n-1-j]=x by x', x'∈[0,18], x'≠x. Assume the actual next pairwords of P_t and R_t agree at every index 0,...,j and have the same final overflow. Then the first-contact interface is exactly the table below. The statement is independent of q,J,C,k except for the stated interior-margin requirement.

## Complete physically rooted gate table

| Actual overflow g_t | Only admissible contact site in the three-cell U row | Physical incoming carries (cL,cU) | Required one-cell replacement | Count per initial U motif over 120 phases |
|---|---|---|---|---:|
| 0 (t mod 4 ∈ {1,2,3}) | The unique coefficient 9 | (1,0) | 9 → 4 | 45 phases |
| 0 (t mod 4 ∈ {1,2,3}) | The unique coefficient 9 | (0,1) | 9 → 14 | 45 phases |
| 1 (t mod 4 = 0) | The even coefficient immediately before the unique 9, in LSD-first order | (1,1) and x≤8 | x → x+9 | 15 phases |
| 1 (t mod 4 = 0) | The even coefficient immediately before the unique 9, in LSD-first order | (0,0) and x≥10 | x → x−9 | 15 phases |

Every other site is forbidden by the universal Q03 first-contact theorem plus its actual physical carry ports. In a no-overflow phase, the two even sites do not satisfy any of the four universal ±5 gates. In an overflow phase, the site immediately after 9 is forbidden because its left neighbour is 9; the 9 site has carry pair (1,0) or (0,1), whereas a ±9 gate at 9 requires (0,0) or (1,1). The unique preceding-even site is therefore the only gate.

Across all 30 U motifs and all 120 phases, the finite table has 2,700 no-overflow rows and 900 overflow rows. The only directed changes are 9→4 (1,350 instances), 9→14 (1,350), x→x+9 (450), and x→x−9 (450). All listed transitions are physically realizable; none of these counts assert that the local edit returns the entire word.

## Why the table is valid at every width

For decimal pair-coefficient normalization, the carry map is T_x(c)=floor((x+c)/10). For every x≠9, T_x(0)=T_x(1), so a non-9 coefficient erases any dependence on an earlier carry. Every two consecutive symbols of every U_t contain a non-9, and the same is true in the reversed high-side direction. Consequently, at a contact column separated from the ends by a complete U period, both actual incoming carries equal the unique periodic low/high carries. This remains true for every q,J,C,k meeting the interior-margin condition. The physical overflow is fixed by the rooted B_t leading coefficient: g_t=1 exactly at t mod 4=0.

The universal first-contact theorem in reports/Q03FirstContactInterface.md says that, if next pairwords agree through the first changed coefficient, then no overflow allows only the four directed ±5 gates, while overflow allows only the twenty directed ±9 gates and requires the immediately outer coefficient to be non-9. Applying those exact gates to the physical low/high carries of all 30×120 U rows gives the table above. This is an all-width local argument; the finite enumeration checks the complete finite phase alphabet, not a finite orbit horizon.

## Independent physical controls

Run from the repository root:

    python3 calculation/new_structures/Q03/tstar_u3_first_contact.py

The checker reads the published p12/m9 data, enumerates all 3,600 (U_0,t) cases, constructs canonical 923-digit source integers with q=14, J=[5], k=100, C=[10], and checks the actual incoming carries at all 10,800 contact ports against the periodic carries. It tests every in-range ±5 or ±9 one-site mirrored edit at each of the three U residues: 16,560 candidate edits. Ordinary arbitrary-precision n+reverse(n) and a separately implemented schoolbook digit-array engine agree on every tested successor, and equality of successor pairwords through the contact index occurs exactly for the unique gate in each phase row.

These integer tests independently validate the local arithmetic. The universal statement follows from carry reset plus the complete 30×120 finite gate enumeration, not from the sampled q,k values.

## Exact remaining gap

A one-cell gate preserves only the next pairword prefix through first contact. It does not restore the full W9|J|U3 seam, and the gates at successive phases are not yet shown to form a reachable periodic interface state. The missing T* lemma remains an all-width, physically canonical 120-step return P(q,k;J,U,C) → P(q,k+5;J,U,C) for fixed J,C,U, with all 120 phase witnesses and the complete two-ended carry/overflow state restored. No decimal Lychrel number is claimed.
