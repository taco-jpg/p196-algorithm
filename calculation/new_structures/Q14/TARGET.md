# Q14 current target: T* morphic interface/centre reservoir (UNDECIDED)

The active family is the rooted phase-0 decimal p12/m9 template
\[
P(q,k;J,U,C)=H\,C\,H^R,\qquad H=B_{34}\,W_9^q\,J\,U^k,
\]
where B34 and W9 are the exact phase-0 rows in calculation/decimal_frontier/lattice_kinks/data/lat_p12m9.txt, U is one of the 30 charge-zero rotations of (9,a,18-a) for even a, and C is a palindromic coefficient word. Words are least-significant-first. The 120-step overflow clock has exactly 30 length-increasing steps.

The first centre-only candidate sigma(A)=BBBABBB, sigma(B)=B, with coefficient values A=8 and B=9, has centre growth 6 per macro and requires k to grow by 4. Its exact integer replay misses inside W at |B|+9q-22 before the centre can affect the interface. A W-prefix substitution also leaves the same mismatch. A three-state coefficient-only J cycle has its first mismatch retreating 23 coefficients into W per macro. The next route is a phase-aware morphic interface state whose letters encode both physical carries and the overflow lag, not only displayed coefficient values.

## Exact all-time target

Find a finite alphabet A, nonerasing substitution sigma:A->A+, coefficient projection pi:A->{0,...,18}, seed word c0, and nondecreasing exponents k_m, such that C_m=pi(sigma^m(c0)) is palindromic for every m. For some q0,k0,J,U, every q>=q0 and m>=m0 must satisfy:

1. P_(q,m)=B34 W9^q J U^(k_m) C_m (U^R)^(k_m) J^R (W9^R)^q B34^R has a positive canonical decimal realization N_(q,m)=val10(P_(q,m)).
2. Every R^t(N_(q,m)), 0<=t<120, is nonpalindromic.
3. R^120(N_(q,m))=N_(q,m+1) exactly, with both physical carries, every overflow lag digit, and the full interface state verified.

The exact 120-step length ledger is
\[
18\Delta q+2\Delta|J|+6\Delta k_m+\Delta|C_m|=30.
\]
For a centre-only substitution with q and J fixed, this becomes 6 Delta k_m + Delta |C_m| = 30. Nondecreasing k_m and nonerasing sigma force every centre-length increment to lie in {0,6,12,18,24,30}. The graph criterion in morphism_gate.py is the exact finite necessary-and-sufficient test for bounded increments of a proposed finite substitution. Passing it is not sufficient: the physical T* edge and all nonpalindrome guards remain open.
