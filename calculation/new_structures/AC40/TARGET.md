# AC40 target (2026-10-29)

Rooted decimal p12/m9 template, 0-based clock phase 7, B7 and W7 from `calculation/decimal_frontier/lattice_kinks/data/lat_p12m9.txt`. Put

`H(q,k)=B7 ++ W7^q ++ J ++ U^k` and `P(q,k)=H(q,k) ++ C ++ reverse(H(q,k))`, LSD-first pairword coefficients.

The desired all-time lemma (UNDECIDED): every ordinary decimal reverse-and-add orbit from a realization of P(q,k) has 120-step exact nonpalindromic edge `P(q,k)->P(q,k+5)` for all sufficiently large independent q,k, with q, J, U, C unchanged and phase clock reproduced. Inducting on k would then yield a decimal Lychrel instance.

**Finite cell attacked:** q=14,k=100, |J|=6, J[0]=0, all 19^5 remaining junctions, U=(9,0,18) only, and C=(4,4) or (4,14,4). Test exact endpoint-only equality after 120 physical reverse-and-add steps. The U word is one of the 30 charge-zero rotations. No universal claim over all J[0], all U, arbitrary palindromic C, or other widths without invoking and checking the hypotheses of the T12 lift. In particular, strict preservation of W9 at intermediate times is NOT assumed.

The required final pairword has coefficient 9 at zero-based LSD index `34+9*11+4 = 137` (W7[4]), since q=14. A sound rejection of each case is an exact physical endpoint value at that index different from 9.