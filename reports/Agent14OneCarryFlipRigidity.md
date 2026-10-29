# No one-bit carry-itinerary deformation of the decimal p8/m20 non-self-mirror bulk

**PAPER PROOF with an exhaustive finite integer certificate.** Scope: the two existing reachable decimal g=10101010, period-8, spatial-period-20 non-self-mirror bulk lattices rec0 and rec1. Preserve the overflow and every 8x20 ascending plus 8x20 descending binary *carry-in* position except for **exactly one flipped bit**. There are 2 lattices × 2 carry directions × 8 times × 20 columns = 640 precisely specified itineraries. For **every** integer base b>=2, no such itinerary supports a cyclic coefficient row with even the first **two** initial bulk coefficients integral. Hence no physical absorbing-lattice cycle of that exact one-bit itinerary exists. This does not exclude two or more carry changes, other periods/lattices, or any central construction.

Let W_t[j] be the bulk coefficient at spatial index j modulo 20, A_t[j],D_t[j] its two incoming carry bits, and g_t the overflow. The exact necessary row equation is

    W_(t+1)[j] = W_t[j] + W_t[j-g_t] + A_t[j] + D_t[j-g_t]
                 - b*(A_t[j+1]+D_t[j-g_t-1]).

The homogeneous eight-step return is F=16(I+S)^4 with Sx[j]=x[j-1]. Let H=I-F. Since H=I (mod 2), det H is odd and nonzero, so a specified carry itinerary uniquely determines the rational row W_0(b)=H^-1(v+b*u). Integrality of its first two entries is a necessary condition for every integer base, regardless of all other coefficients and carry inequalities.

The compact integer certificate sets D=4772995440505252811961825 and supplies 20 signed integers K_j satisfying the 20 integer identities

    K_j - 16*(K_j+4*K_(j-1)+6*K_(j-2)+4*K_(j-3)+K_(j-4))
        = D*[j=0]       (indices mod 20).

Thus K/D is the exact first column of H^-1 and all remaining rows are its cyclic shifts. For any one-bit itinerary the two coefficients of W_0(b) must satisfy the two linear integer congruences

    b*sum_k K_(-k)u_k + sum_k K_(-k)v_k = 0 (mod D),
    b*sum_k K_(1-k)u_k + sum_k K_(1-k)v_k = 0 (mod D).

A congruence a*b+c=0 (mod D) has a solution exactly when gcd(a,D) divides c. If so its solutions are one residue class modulo D/gcd(a,D). Two such classes are compatible exactly when their residues agree modulo the gcd of their moduli. These are full integer statements; no finite bound on b is involved. Exhausting all 640 itinerary masks gives:

| case | first congruence already impossible | second alone impossible | both individually possible, CRT-incompatible | total |
|---|---:|---:|---:|---:|
| rec0 | 94 | 56 | 170 | 320 |
| rec1 | 90 | 55 | 175 | 320 |
| all | 184 | 111 | 345 | 640 |

The primary agent14_onebit_main.py uses exact Fraction Gauss-Jordan elimination to reconstruct H^-1 and the resulting rational affine constraints. The independent agent14_onebit_independent.py never imports the primary, uses only signed integer operations, verifies the 20 K/D convolution equalities, and independently reconstructs all 640 modular obstructions. Both independently output identical six integer counts. The compact agent14_onebit_rec0.txt includes eight encoded rows; the primary reconstructs rec1 via the known translation and crosschecks both directly against the canonical p8_scc.txt. The inverse-kernel certificate is agent14_onebit_kernel.txt. No state cap.

Run from repository root (Python 3 standard library only):

    python3 calculation/decimal_frontier/lattice_formats/code/agent14_onebit_main.py
    python3 calculation/decimal_frontier/lattice_formats/code/agent14_onebit_independent.py

As mandatory **positive controls**, the independent checker replays actual ten-edge base-9 g1100011000, spatial m=4, |B|=61 and both ten-edge base-13 g1010010000, |B|=75,55 certificates by direct pairword digit normalization using previously committed data and Lean source. These controls are not claimed as new. The result neither proves a rooted exterior, a periodic centre, a decimal Lychrel number nor anything about the ordinary orbit of 196; it is not a Lean theorem.
