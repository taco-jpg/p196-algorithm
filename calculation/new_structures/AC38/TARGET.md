# AC38: exact target

Rooted decimal p12/m9 phase 5, B5/W5 from calculation/decimal_frontier/lattice_kinks/data/lat_p12m9.txt, q=14,k=100, J length 6. The initial LSD-first pair-coefficient word is P=(B5 ++ W5^q ++ J ++ U^k) ++ C ++ reverse(B5 ++ W5^q ++ J ++ U^k). Test whether 120 genuine decimal reverse-and-add steps produce the identical literal J/C/U template with k increased by 5, for both C=[4,4] and C=[4,14,4].

Target missing lemma: a sound endpoint-only return/no-return decision, allowing temporary W9 damage. This result instead certifies a universally forced prefix and corrects a false early-prefix exclusion. The fixed reference-width guard alone does not solve the all-time decimal Lychrel problem.
