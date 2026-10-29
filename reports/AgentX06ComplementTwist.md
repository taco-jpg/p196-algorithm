# Agent X06: nine-complement spin on a rooted decimal two-band orbit

**PAPER PROOF** for the antipodal cyclic-carry/bulk lemma in every radix. **COMPUTED** for the stated explicit 20,000-step base-10 orbit. Neither label proves a decimal Lychrel number.

## Exact antipodal carry identities

The local digit/carry complement identity is already stated in `reports/Agent14ComplementTwist.md`. The contribution here is the explicit bulk-spin corollary combined with a **new rooted two-band decimal orbit** and an independent long replay. The previously excluded globally aligned complement-twisted centre return is not used: only the interior V band is complemented.

In base b, write `J(x)=2(b-1)-x` for pair coefficients `0<=x<=2b-2`. If `x+c=bq+d`, with carry `c,q in {0,1}` and digit `0<=d<b`, then

    J(x)+(1-c) = 2b-1-(x+c) = b(1-q)+(b-1-d).

Consequently a *cyclic* carry solution on a periodic word `w` maps under `J` to the complementary cyclic carry solution on `J(w)`; normalized cyclic digits become their `(b-1)`-complements. If `w` contains some symbol different from `b-1`, its carry-return map is constant, so the cyclic solution is unique. Denote cyclic normalization of `w` by `L(w)`, and reversal of cyclic normalization of the reversed `w` by `H(w)`.

For either overflow phase `g=0,1`, the exact bulk row map is

    T_g(w)[i] = L(w)[i] + H(w)[(i-g) mod m],   m=len(w).

Hence `T_g(J(w))=J(T_g(w))`. This is an exact `Z/2` spin symmetry for **bulk** periodic lattices, not for the full rooted orbit. It holds for every radix, every spatial period and either phase. In particular, arbitrary finite prescribed temporal gamma words preserve the complemented orbit of a bulk cycle. This does not decide or repair interfaces between oppositely coloured bands.

A related *open-boundary* identity is more subtle. For a symmetric pair coefficient word `P` of length `n`, with `P[0] != b-1` and both terminal coefficients positive after J, let `D=digits(val_b(P))` and `D'=digits(val_b(J(P)))`. Their first `n` digits obey `D'[0]+D[0]=b-2` and `D'[i]+D[i]=b-1` for `1<=i<n`; their overflow bits sum to one. Equivalently `val_b(P)+val_b(J(P))=2(b^n-1)`. The failed carry-complement relation *only at the input boundary* produces a one-digit charge and flips overflow. This explains why a bulk spin can be free while a rooted exterior spin is not.

## A new explicit decimal two-band spin

Define the least-significant-first coefficient blocks

    B = (17,5,0,1,13,4,14,12,9,8,15,16,17,13,17,9,1,4,4,11,8,16,0,9,14,11,9,11,6,13,18,9,4,7,17,15,9,7,13)
    W = (17,3,1,13,17,11,14,3,18,1,2,0,7,3,14,12,15,9,7,13)
    V = (4,4,14,1,5,11,7,1,15,12,7,9,9,12,14,4,0,6,5,17,13,9,7,3,13,10,4,13,5,1,9,4,11,6,16,3,7,7,12,4,2,13,2,15,10,10,9,3)

For `k=500` set `H=B ++ W^k ++ [9] ++ J(V)^k`, `P=H ++ [9] ++ reverse(H)`, and `N_0=val_10(P)`. This differs from the previously published N01 seed by complementing the **entire interior 48-band**, while keeping the rooted exterior, all junction coefficients, and all lengths unchanged. The generalized complement lemma shows this is not a re-run of the same 48-band lattice: its eight phase rows are the antipodes of the original eight rows.

Let `W_t` and `V_t` be obtained from the original `W,V` by `T_(1-t mod 2)` (both return after eight steps). In all checked steps `t=0..20000` the actual coefficient word `P_t` of `N_t`, obtained from the previous integer's decimal digits, has `W_t` repeated for **50** entire periods at pair indices `439..1438`, and `J(V_t)` for **20** entire periods at pair indices `25040..25999`. Its coefficients are palindromic by definition; these matched subwords have the claimed exact pairword shape. All actual numbers, not pairwords, are **nonpalindromic** at all 20,001 states. Lengths: 68,082 initially, 78,082 finally; overflow pattern `1010...` for 20,000 operations. These finite facts do not provide an infinite certificate, since the interfaces are not proven to renew.

The code draws 9,600 random bulk cases over spatial lengths 1..32, checks 9,592 absorbing cases and skips 8 all-9 neutral cases, checks both 8-phase bulk returns, and independently replays each step with (1) manual digit-array decimal addition and (2) GMP `mpz_class` arithmetic and string reversal, comparing *every digit* and the complete pairword at every step, then checking the two protected full-period windows and palindrome exclusion. The production command is

    g++ -O3 -std=c++17 calculation/new_structures/agent-X06/twist.cpp -lgmpxx -lgmp -o /tmp/x06twist
    /tmp/x06twist 500 20000

## Limits and search direction

A direct mode-8 control using a half-`J(V)`, half-`V` band without a compensating seam still has the alternating exterior overflow word, but the uncorrected piecewise-periodic ansatz accumulates 1,425 mismatches at t=1,000, 7,166 at t=5,000, and 22,642 at t=20,000 (over 24,000 V-domain positions). A **complement-domain wall is not automatically a soliton**. The new search target is a finite compensated spin-flip interface with an eight- or 88-step temporal return, possibly translating by a whole spatial period. A cycle of such walls, proved to preserve the exterior and nonpalindromicity, would give a finite certificate via a twisted multi-band transducer. No closed wall or decimal infinite orbit is asserted here.