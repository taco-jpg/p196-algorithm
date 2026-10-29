# W17 exact target

**Assigned cell:** rooted decimal p12/m9 phase 0, W9|J, |J|=3 or 4, fixed U=(8,9,10), even palindromic coefficient centre C of length 2, 4, 6, 8, 10, or 12.

For B and W from calculation/decimal_frontier/lattice_kinks/data/lat_p12m9.txt, define LSD-first

P(q,k;J,C) = B ++ W^q ++ J ++ U^k ++ C ++ reverse(U^k) ++ reverse(J) ++ reverse(W^q) ++ reverse(B).

The target to refute is that 120 genuine base-10 reverse-and-add steps restore the rooted B ++ W^q prefix, so the epoch image remains in the same phase-0 cell and may participate in a fixed point or a longer epoch-seam cycle. The uniform domain is independent q >= 14, k >= 100; all coefficient entries of J,C lie in [0,18], and C is palindromic.

**Missing-lemma question:** does any seam of length 3 or 4 for this fixed U and even-centre class preserve W9 at the end of the first 120-step epoch, for any admissible J,C? The result must decide this by a complete finite carry reduction, not by sampled widths or an intermediate-phase W9 lock. If the cone is independent of C, record that extension separately rather than enumerating longer centres one by one.
