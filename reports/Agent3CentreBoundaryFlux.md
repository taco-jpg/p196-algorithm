# Moving-centre boundary flux with physically correlated carries

**PAPER PROOF.** This exact finite-centre charge law holds for all bases b>=2, all valid digit words, and both overflow/parity cases. It is not an all-width no-go or a decimal certificate.

Let N have n significant base-b digits D[i], least significant first. Let P[i]=D[i]+D[n-1-i], and normalize P to output digits O with carries c[0]=0 and O[i]=P[i]+c[i]-b c[i+1] (i<n). Put g=c[n] in {0,1} and append O[n]=1 if g=1. Let P' be the next pair word, h=ceil(n/2), h'=ceil((n+g)/2), R=h-1, and take a fixed cut 2<=L<R. Set q[i]=b^i modulo M=b²-1 and d[i]=c[n-1-i]. Define Q=sum of q[i]P[i] for L<=i<=R, and Q' analogously for L<=i<h'. Then exactly

    Q' = A_g Q + X_L + Z   (mod M),   A_0=2, A_1=b+1.

The lower-boundary source is

    g=0: X_L=q[L](c[L]-b d[L-1]);
    g=1: X_L=q[L](P[L-1]+c[L]-b d[L-2]).

The correlated *physical midpoint* source is

    n even, g=0: Z=q[R](1-b)c[h];
    n odd,  g=0: Z=q[R](c[R]-b c[R+1]);
    n even, g=1: Z=q[R]b O[h];
    n odd,  g=1: Z=q[R](-b P[R]+(1-b)c[h]).

**Proof.** Sum the exact one-step bulk pair-word recurrence over [L,R], weighting position i by q[i]. The identities q[i+1]=b q[i] and b q[i+1]=q[i] (mod M) telescope all interior terms. The lower endpoints give X_L. At g=0, the upper endpoint is q[R](-b c[R+1]+d[R]); for even n, d[R]=c[h], and for odd n, d[R]=c[R], giving the first two midpoint cases. At g=1, the upper endpoint before accounting for a changed midpoint is q[R](-b P[R]-b c[R+1]+d[R-1]). For odd n, h'=h and d[R-1]=c[h], giving the fourth case. For even n, h'=h+1, d[R-1]=c[h+1], and the new odd-length centre is P'[h]=2O[h], with O[h]=P[R]+c[h]-b c[h+1]. Add q[h]P'[h] and reduce b²=1 modulo M; the third case follows. All carries are *actual schoolbook carries* of N+reverse(N), not independent symbols.

## Decimal p8/m48 rec2 consequence (necessary, not sufficient)

A return of the time-periodic centre against the rec2 exterior requires T=192k steps, k>=1, with lower-half length growing by 48k. The rec2 rows each have zero 48-cell charge modulo 99, and q[i] has spatial period two. Therefore for a genuinely returned template, Q_T=Q_0 modulo 99 when L is frozen in the exterior. The product of step multipliers is (2·11)^(96k)=22^(96k)=55 modulo 99, so the weighted sum S of all X_L+Z boundary sources satisfies S=(1-55)Q_0=-54Q_0 modulo 99. Consequently S=0 modulo 9.

The executable reconstruction from rec2 lattice data checks that for *every one of its 48 spatial cut residues*, with L>=nB+2, the corresponding 192-step weighted exterior source X_L is itself zero modulo 9. It remains zero after k 192-step laps. Thus a necessary all-width constraint on the real central source is

    sum[t=0..T-1] 2^(T-1-t) z[t] = 0 (mod 9),

where z[t], reduced modulo 9, is: 0 for even n_t/g_t=0; c[R_t]-c[R_t+1] for odd n_t/g_t=0; O[h_t] for even n_t/g_t=1; and -P[R_t] for odd n_t/g_t=1. This involves only the actual centre digits and carries, regardless of centre width. It does not rule out any width, provide an infinite orbit, or establish a base-10 certificate.

**Auxiliary COMPUTED checks:** python3 calculation/decimal_frontier/lattice_kinks/code/agent3_boundary_flux_check.py independently validates 90,000 schoolbook reverse-and-add steps in bases 2..31 (all 4 parity/overflow cases in each base) and all 48 rec2 cut residues. The mathematical statement is PAPER PROOF, not LEAN-VERIFIED.
