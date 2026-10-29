# AC09: phase-0 U-group 8 centre fixed-point screen

**PAPER PROOF (specialization of existing Q39): no recurrent odd centre for fixed J=[5]. COMPUTED: exhaustive even-centre |C|=8 reference-width necessary-condition screen. NOT A BASE-10 LYCHREL CERTIFICATE.**

## Model and exact scope

Use the official phase-0 p12/m9 B34/W9 words. Form the LSD-first symmetric pair-coefficient word P=H ++ C ++ reverse(H), where H=B ++ W^q ++ [5] ++ U^k, U in {(9,16,2),(16,2,9),(2,9,16)} and C is any legal palindromic coefficient centre (its midpoint must be even if length is odd). An exact 120-step edge would reproduce this template with k->k+5 and identical B,W,J,C; full physical carries and expected overflow clock g=(100010001000)^10 must also agree.

## All odd C lengths: two-epoch obstruction (PAPER PROOF)

Let A(X)=sum_i (-1)^i X[i]. The published data give A(B)=-11 and A(W)=-22, with |B|=34 and |W|=9. For an *odd* palindromic C and singleton J=[5], direct concatenation gives

A(P(q,k)) ≡ (-1)^q [10 - 2(k mod 2)A(U) - (-1)^k A(C)] (mod 11).

The leading pair coefficient B[0]=10 forces an overflow on the first addition, so the initially odd decimal length becomes even at step 1. For even-digit n, n+reverse(n)≡0 (mod11), and divisibility by 11 is preserved at all later steps. Thus at steps 120 and 240 the number and its symmetric pairword alternating sum are divisible by 11.

If P(q,k)->P(q,k+5)->P(q,k+10) are two genuine successive exact 120-step returns with the *same* J,C and q, the target U-exponents have opposite parity. Applying the displayed congruence at both endpoints forces A(C)≡10 and A(U)≡10 (mod11). The three U rotations have A(U)=-5,23,9, giving residues 6,1,9. Contradiction. **No recurrent two-epoch edge exists with any odd C length for this J and U-group.** This is a specialization, not an original generalization, of prior Q39 parity-aware mod-11 gates. It does not exclude an isolated single-epoch centre-window match.

## Even |C|=8: complete finite necessary-condition census (COMPUTED)

At exactly (q,k)=(14,100), each C of length 8 is determined by four arbitrary 0..18 entries. The attached exact C++ folded-pairword engine exhaustively checks 19^4=130,321 choices for each U (390,963 total). Every trajectory consists of **120 ordinary decimal reverse-and-add steps**: full-width LSD-to-MSD carry normalization and reflection, with each actual overflow recorded. At the endpoint it compares 10 flanking U coefficients on each side plus all eight centre coefficients against the exact k+5 target. This is necessary but not sufficient for a full T* return. Crucially, it applies **no strict intermediate W9 pruning**, which would be unsound for endpoint-only healing.

| U | Tested/total | 28-coefficient centre-window matches | Wrong overflow clock |
|---|---:|---:|---:|
| (9,16,2) | 130321/130321 | 0 | 0 |
| (16,2,9) | 130321/130321 | 0 | 0 |
| (2,9,16) | 130321/130321 | 0 | 0 |

The zero matches exclude full single-epoch fixed-J/C returns in this precisely stated *even C8 reference-width* cell. They do not decide C lengths 10,12,14 or another junction, seam trajectory or width.

## Reproduce / independent checks

Run: g++ -O3 -std=c++17 -o scan scan.cpp; for u in 0 1 2; do ./scan 8 "$u" 0 14 100; done.

The locally audited full enumeration used the same algorithm and obtained 0 hits, 0 incorrect 120-bit clocks for every U. Before publication, a direct-target comparator agreed with the optimized central-window comparison on **960** randomized C tests at q/k=(14,100),(40,160). Independently, Python arbitrary-precision actual n+int(str(n)[::-1]) agrees on **3,600 consecutive decimal transitions** with the folded recurrence for both C parities, three U choices and five widths (14,100),(20,80),(40,160),(80,320),(160,640); sample 28-coefficient windows match across C++/Python for all three U.

**No restored seam, all-width decimal certificate, or base-10 Lychrel number has been proved.** The remaining centre-only cells include even lengths 10,12,14 (19^5,19^6,19^7 words per U), for which a sound carry-aware pruner/transfer method is needed.
