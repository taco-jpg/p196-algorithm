# R08: exact two-ended carry-shield argument

## Statement and data

Use least-significant-first palindromic pair coefficients 0..18. B34 and W9 are the actual canonical p12/m9 root: B=(10,4,6,6,7,12,9,16,16,13,0,2,10,17,7,0,18,6,5,18,4,18,14,9,14,8,12,17,10,4,6,4,0,5), W=(5,18,4,8,1,15,4,0,5). Let U range through the 30 rotations of (9,a,18-a), a even in [0,18]. Let q belong to {20,40,80,160}. Claim: for EVERY r>=200 and EVERY valid palindromic middle D, canonical P=B W^q U^r D rev(U)^r rev(W)^q rev(B) cannot have a true 120-step reverse-add successor pairword beginning B W^q. No claim is made for other q, or when the active interface remains within 199 U copies of W.

## Lemma: three-column protected-prefix contraction (PAPER PROOF)

Let P and Q be canonical palindromic pair coefficient words, potentially of different total lengths, with identical first m>=3 coefficients. Assume the common coefficient p0 is not 9 and the last two coefficients of this common m-prefix are not BOTH 9. Then the true base-10 reverse-and-add successor pairwords have identical first m-3 coefficients.

Proof: for source P of length L, the next number is value(P), whose ordinary decimal digits e_i satisfy c_0=0, e_i=(P_i+c_i) mod 10 and c_(i+1)=floor((P_i+c_i)/10), with each c_i in {0,1}; append g=c_L if nonzero. Since P is palindromic, the final coefficient P_(L-1)=p0. For p0!=9, floor((p0+c)/10) is independent of c in {0,1}, so the two sources have the same overflow bit g. Their normalized lower digits e_i agree for i<m by the ordinary left-to-right carry recursion. Their mirrored upper suffixes have the same m coefficients, in reverse order. Carry into this suffix may differ, but an input coefficient x!=9 sends the SAME output carry floor((x+c)/10) for both c=0 and c=1. One of the first two suffix coefficients is !=9 by the last-two-prefix assumption; hence the upper normalized digits match from the third suffix position onward. The next palindromic pairword has coefficients e_i+e_(L+g-1-i) (with the appended overflow digit when g=1). Thus for i<m-3 the lower and mirrored upper digits agree for both sources, even with differing total lengths. QED. A 2000-case independent-integer randomized regression is included, but the proof does not rely on it.

## Exact finite-to-infinite reduction

For fixed q,U let H=B W^q U^200, m=|H| and P*=H [12] rev(H); [12] is a valid odd midpoint. For ANY claimed P with r>=200, the first m coefficients equal P*'s. The checked reference orbit has, for each t=0..119, pair coefficient zero !=9 and the coefficients at positions m-3t-2 and m-3t-1 not both 9. By 120 inductions of the lemma, the true 120-step output for arbitrary P agrees with P*'s 120-step output on its first m-360 positions. Since m=34+9q+600, this includes B W^q and a further 240 U coefficients. The arithmetic checker finds a nonzero defect in the last 30 W coefficients of the reference output, at index |B|+9q-d for d in {20,21,22,23}; this contradicts ANY literal return with initial prefix B W^q, for all possible r and D. QED.

## Kernel evidence, scope and consequence

The checker constructs physical base-10 integers from exact pair coefficients, independently computes each successor via big-integer string reversal and via a read-only schoolbook digit-list addition, and checks every gamma bit against (1000)^30; it validates the 120 carry-reset premises and the W-side mismatch for all 30 U and four q values. Distribution of earliest mismatches: -23 in 60 cases, -22 in 52, -21 in 4, -20 in 4. All are true 120-edge statements used to prove an ALL-r and ALL-core obstruction, **not** claims that a finite replay proves a Lychrel number.

Consequence for moving interfaces: splitting the inner U reservoir as U^r J U^s with r increasing every macrocycle eventually forces r>=200, where the theorem applies. A viable regenerative emitter for these q values must stay within a bounded distance of the W/U boundary (or modify W itself). This leaves boundary-attached, physically active junctions and other q values UNDECIDED.

Separate length gate: with q fixed, fixed centre width, 120 overflows=30 and k->k+5, conservation says 2*Delta|J|+Delta|C|=0; therefore J alone cannot grow each cycle without consuming centre width. This is a corollary of earlier length bookkeeping, NOT a novel result here.
