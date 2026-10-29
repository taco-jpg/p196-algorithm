# EPOCH_INVARIANTS: rooted decimal W9/U3 seam-map gates

**PAPER PROOF.** Necessary conditions for all widths; **NOT** a decimal Lychrel certificate or an all-time returning seam.

## Setting and exact mass identity

Work with least-significant-first genuine palindromic pair-coefficient words P_t[i]=d_t[i]+d_t[L_t-1-i] of canonical decimal n_t, where n_(t+1)=n_t+rev10(n_t). Write S_t=sum(P_t)=2*digitSum(n_t), and c_t for the **total number of unit carries** when normalizing the actual P_t to n_(t+1), including an outgoing overflow carry. In each column, carry is 0 or 1. Exact decimal mass conservation gives

    S_(t+1) = 2*S_t - 18*c_t.                            (1)

The rooted phase-0 p12/m9 values in calculation/decimal_frontier/lattice_kinks/data/lat_p12m9.txt are B34 (sum 307), W9 (sum 60). For canonical T(q,k;J,U,C)=H++C++reverse(H), H=B++W^q++J++U^k, take |U|=3, sum(U)=27 and palindromic C (with an even middle coefficient for odd |C|). Then

    S_0 = 614 + 120q + 54k + 2sum(J) + sum(C).            (2)

Suppose **120 actual ordinary-decimal reverse-and-add steps** produce a pairword T(q,k+5;J',U',C') with sum(U')=27, identical B/W and 2|J'|+|C'|=2|J|+|C|. Define

    D = 2(sum(J')-sum(J)) + sum(C')-sum(C).

This endpoint hypothesis forces 30 more coefficients and S_120=S_0+270+D. For a strictly stationary fixed point J'=J, U'=U, C'=C, D=0.

## Full list of necessary gates

**Length and parity:** 2|J'|+|C'|=2|J|+|C|, hence |C'| and |C| have identical parity. With arbitrary band drifts dq,dk and fixed seam length, the 120-overflow ledger is 3dq+dk=5. Fixed literal seam charge mod9 gives dq=0,dk=5 if drifts are nonnegative (Q36 already gave this ledger).

**Modulo 9:** As reversal preserves digit sum modulo 9, n_(t+1) = 2n_t (mod9). Since 2^120=1 (mod9), S_120=S_0 (mod9). Thus D=0 (mod9). Both endpoint coefficient masses are even for genuine canonical pairwords, so in fact D=0 (mod18). This applies for **even and odd** centre lengths.

**Modulo 11 (previous Q39/R33/R07 theorem, not new):** Let A(X)=sum_i (-1)^i X_i. For even-length palindromic C, A(T)=0 identically and NO mod11 pruning of J or U is justified. For odd-length palindromic C and all independently variable q,k, using A(B)=-11 and A(W)=-22, the necessary gates are A(U)=A(C) (mod11) and 2A(J)+(-1)^|J| A(C)=0 (mod11). Do not apply those odd-only gates to even C.

**New mod81 normalization-carry gate:** Unroll (1) over 120 genuine steps, setting K=sum_(t=0)^119 2^(119-t)*c_t, so S_120=2^120*S_0-18K EXACTLY. Because 2^120=46 (mod81),

    18K = 45S_0 - 270 - D (mod81).

The already-proved 9|D permits division by 9, followed by inversion of 2 modulo 9:

    K = 7S_0 - 6 - 5(D/9) (mod9).                        (3)

For an identical stationary seam D=0, substitute (2):

    K = 8 + 3q + 5sum(J) + 7sum(C) (mod9).                (4)

This is independent of k, and requires independent **q modulo 3** classes for any universal fixed point, in addition to all four independent q and k modulo-4 classes associated with the separate R05 mod101 physical carry cocycle. These residue-class probes are NOT an all-width proof by themselves.

**New mod81 palindrome projection:** For any palindromic pair-coefficient word P of length N and sum S, symmetry gives 2sum_i iP_i=(N-1)S. As 10^i=1+9i (mod81),

    val10(P) = S + 9(N-1)S/2 (mod81).                     (5)

The division by two is valid modulo 81. For the above return, with 9|D and N_120=N_0+30, equation (5) yields

    n_121 - n_1 = 27 + D + 54S_0 (mod81).                (6)

In particular a fixed seam has n_121=n_1 (mod27), and for a moving seam n_121-n_1=D (mod27). The fixed-seam mod81 increment is independent of q,k because S_0 modulo 3 equals 2+2sum(J)+sum(C).

**Modulo 101:** R05's separate weighted physical-carry cocycle uses 10^4=1 (mod101) and demands all 16 independent (q mod4,k mod4) classes. Its carry-index convention was not independently re-proved in this note and is not substituted for the mod81 conditions. Combined residue coverage needs q modulo 12 and k modulo 4; even complete finite coverage would still need a symbolic carry-pumping proof.

## Reproduction and precise limitation

Run python3 calculation/new_structures/S20/carry81.py. It uses independently computed Python big-integer n+rev(n) and schoolbook LSD digit arrays on the rooted R02 J19 one-epoch near miss, an even-centre case, and an odd-centre case, at independent (q,k)=(20,20),(21,23),(40,40),(80,80),(160,160). All 120 phase updates agree, including actual overflow 1000 repeated 30 times, carry-count identity and palindrome projection. All tested cases fail a stationary return; that finite diagnostic is NOT evidence of a no-go for other seams. Equations (1)-(6), unlike those tests, are exact mathematical necessities **for every width** under the explicit 120-return hypothesis. Neither existence nor impossibility of a decimal Lychrel number follows.