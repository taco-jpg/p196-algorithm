# AC05 exact centre-only predicate

Rooted decimal p12/m9 phase 0. B34 and W9 are row 0 of `calculation/decimal_frontier/lattice_kinks/data/lat_p12m9.txt`, J=[5], and U is one of (9,8,10), (8,10,9), (10,9,8). Let H=B ++ W^q ++ J ++ U^k and P=H ++ C ++ reverse(H), with C a palindromic coefficient centre of length 7..14 (the midpoint is even for odd lengths).

At (q,k)=(14,100), realize P into canonical decimal digits; perform 120 genuine reverse-and-add steps, then compare the centre window in the resulting pairword against the same P template with k=105 and unchanged J,U,C. Necessary full centre radius is 152+|C|. A mismatch inside the radius-160 subwindow is a sufficient rejection at any tested length; finding agreement inside this subwindow alone does not constitute a return.

The checks use actual digit carries and physical 120-step overflow. They do not impose strict intermediate W9 preservation. This predicate is necessary, NOT sufficient, for the full all-width/all-time T* certificate.
