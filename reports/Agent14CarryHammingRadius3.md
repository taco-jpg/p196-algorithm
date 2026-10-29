# Agent14: isolation of the radius-three carry-itinerary ball

**COMPUTED**, supported by an exact all-integer-base reduction and two independent exhaustive checkers. Scope: spatial period 20, temporal period 8, overflow word 10101010, and the two known reachable base-10 non-self-mirror reference bulk lattices rec0 and rec1. Each reference has 8*20*2 = 320 ascending/descending carry-in bits. For every integer base b>=2 there is **no physical cyclic bulk** whose complete carry-in itinerary differs from either reference at exactly one, two or three sites. The unchanged itinerary is realized at base 10. Nothing about four or more differences, other periods, rooted exteriors or periodic centres is decided.

Write S(x)_j=x_(j-1), indices modulo 20. For *any* proposed binary carry-in streams A and D, the exact physical transition forces:

    W_(t+1,j) = W_(t,j) + W_(t,j-g_t) + A_(t,j) + D_(t,j-g_t)
                - b*(A_(t,j+1) + D_(t,j-g_t-1)).

The homogeneous eight-step return is F=16(I+S)^4; H=I-F is invertible over the rationals, since H=I modulo 2 has odd nonzero determinant. The coefficients of every eight-phase cyclic row under a fixed carry itinerary are therefore uniquely forced, affine in b. The integer inverse-kernel certificate kernel.txt contains D0=4772995440505252811961825 and 20 signed K_j satisfying, for every j,

    K_j - 16*(K_j+4*K_(j-1)+6*K_(j-2)+4*K_(j-3)+K_(j-4))
      = D0 if j=0, else 0.

Thus initial coefficient j is (v_j+u_j*b)/D0, with explicit integers u_j,v_j computed by the exact eight-step recurrence. Its integrality is exactly the congruence u_j*b+v_j=0 modulo D0. The 20 congruences are solved by gcd and generalized CRT, deciding them for **all integer bases simultaneously**, without enumerating bases. The physical coefficient bounds 0<=W<=2(b-1), and the binary ascending and descending carry laws, are finitely many further necessary inequalities of the form slope*b+intercept>=0. A single inequality with slope<0 and 2*slope+intercept<0 (or slope=0 and intercept<0) excludes **every real b>=2**.

| Lattice | Flipped bits | Exhaustive masks | First 2 congruences feasible | All 20 congruences feasible | Exact real-base obstructions |
| --- | ---: | ---: | ---: | ---: | ---: |
| rec0 | 1 | 320 | 0 | 0 | 0 |
| rec0 | 2 | 51,040 | 28 | 8 | 8 |
| rec0 | 3 | 5,410,240 | 1,931 | 272 | 272 |
| rec1 | 1 | 320 | 0 | 0 | 0 |
| rec1 | 2 | 51,040 | 35 | 8 | 8 |
| rec1 | 3 | 5,410,240 | 1,980 | 272 | 272 |
| **Total** | 1..3 | **10,923,200** | **3,974** | **560** | **560** |

Every one of the 560 full-integrality survivors has a single-site, monotone contradiction valid for all b>=2; there are zero physical alternatives. No state cap, time extrapolation, floating-point arithmetic or finite base bound enters the claim. The primary program checks the kernel, reconstructs all 320 single-bit responses and the 8-phase coefficient/carry equations, uses integer CRT on each mask, then checks a universal inequality for each full-integrality survivor. The separate checker builds a full 20x20 rational inverse by Gauss-Jordan elimination and independently propagates each single-bit impulse; both finish the same full census with the same six counts and obstruction witnesses.

The compact rec0 input rows.txt are checked against the existing canonical lattice_formats/p8_scc.txt; rec1 is its known time/spatial translation, also checked against the source SCC. The mandatory **positive controls** are exact ten-edge pairword/digit normalization of the known base-9 g1100011000, spatial m=4, exterior |B|=61 certificate, and of both base-13 g1010010000, |B|=75 and 55 certificates, from preexisting committed repository data and Lean source. Those are regression controls, not new certificates.

Reproduce from repository root, Python 3 standard library and bounded single-core low-priority executions:

    bash calculation/decimal_frontier/lattice_formats/hamming3/reproduce.sh

The complete primary/independent source, both compact input files, regression controls (inside independent source), exact counts and command script are supplied together under calculation/decimal_frontier/lattice_formats/hamming3/. This is not a Lean result. No claim is made about central closure, actual integer reverse-and-add trajectories, decimal Lychrel numbers, the orbit of 196, different carry itineraries at distance >=4, other spatial periods or temporal superperiods.
