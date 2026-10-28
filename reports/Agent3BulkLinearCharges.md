# Universal carry-eliminating additive charges of a cyclic pair-word bulk

**PAPER PROOF.** This classifies the universal *linear* modular observables on a spatially cyclic pair-word bulk, for every base b >= 2. It is a new restricted classification, not an all-width no-go or a decimal Lychrel certificate.

## Exact cyclic update equations

Let m >= 1, M >= 2, P[i] be a pair-word coefficient, a[i] the upward carry entering i, and d[i] the downward carry entering the reflected i. All spatial subscripts below are modulo m. For an overflow bit gamma, the algebraic bulk equations are

    gamma = 0: P'[i] = 2P[i]+a[i]+d[i]-b(a[i+1]+d[i-1]).
    gamma = 1: P'[i] = P[i]+P[i-1]+a[i]+d[i-1]-b(a[i+1]+d[i-2]).

These equations hold in the bulk, away from the finite centre and outer endpoints. They agree with the repository's exact window map. For classification, treat the a,d symbols as *formally independent*: this is deliberately stronger than their physical carry-chain constraints.

## Classification and proof

For q in (Z/MZ)^m, define Q(P)=sum_i q[i]P[i] modulo M. Every ascending and descending carry coefficient disappears from Q(P') for both gamma values **if and only if** there is a z in Z/MZ satisfying

    q[i] = b^i z,   (b²-1)z = 0,   (b^m-1)z = 0  (mod M).

Indeed, at gamma=0, the coefficients of a[i] and d[i] are q[i]-b q[i-1] and q[i]-b q[i+1]. Both must vanish. The first gives q[i+1]=b q[i], hence q[i]=b^i z. The second then gives (b²-1)q[i]=0. Cyclic closure requires (b^m-1)z=0. Conversely these conditions cancel the two coefficients for gamma=0 and, after shifting i, also the descending coefficient q[i+1]-b q[i+2] for gamma=1. The remaining terms give

    gamma = 0: Q(P') = 2Q(P);
    gamma = 1: Q(P') = (b+1)Q(P)   (mod M).

When m is even, b²-1 divides b^m-1, hence the number of valid z is gcd(M,b²-1). When m is odd, gcd(b^m-1,b²-1)=b-1, hence the number is gcd(M,b-1). This is a complete classification only of carry cancellation for *independent* formal carry streams.

## Decimal rec2 application (period 8, spatial period 48)

For b=10, m=48 and M=99, the weights are q[i]=10^i z, with 99 choices of z. By CRT, this carries precisely the familiar sum modulo 9 (10=1) and alternating sum modulo 11 (10=-1); there is no additional independent carry-free linear residue. For overflow word 10101010 the multiplier over eight steps is 2^4 11^4 = 22 (mod 99), and over 192 steps it is 22^96 = 55 (mod 99). A *cyclic-bulk charge* closing after 192 steps must therefore satisfy 54Q=0 (mod 99), or Q=0 (mod 11).

Direct checking of calculation/decimal_frontier/lattice_kinks/data/lat2.txt finds zero charge modulo 99 on every one of the eight 48-cell rows. The ascending and reconstructed descending carry chains satisfy every one of the 384 bulk updates. Thus no all-width centre obstruction follows from this fully classified family of linear carry-eliminating charges.

**Not claimed:** The classification does not rule out nonlinear charges, spatially varying boundary terms, use of actual correlated carry bits, time-dependent weight families, wider centres, or a decimal certificate. In particular it is not an exclusion of any width. The PAPER PROOF is independent of the auxiliary COMPUTED tests, and is not Lean-verified.

Reproduction (standard library only):
    python3 calculation/decimal_frontier/lattice_kinks/code/agent3_charge_invariants.py
