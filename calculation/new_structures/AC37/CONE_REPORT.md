# AC37 two-ended carry-cone obstruction for phase-4 fixed centres

**PAPER PROOF of the exact carry-adversarial window recurrences; COMPUTED for their sixty 120-step finite checks. NOT Lean-verified.** This is a negative obstruction, not a decimal Lychrel-number certificate.

## Statement and proof-relevant missing lemma

Take any canonical rooted decimal p12/m9 phase-4 symmetric coefficient template P=H++C++reverse(H), H=B4++W4^q++J++U^k, q>=14, k>=100, ANY finite junction word J over coefficients 0..18, any of the thirty rotations U of (9,a,18-a) (a=0,2,...,18), and **either C=(4,4) or C=(4,14,4)**. Every one of its genuine 120 reverse-and-add steps is soundly forced to have overflow clock (1000)^30. At t=120 the coefficient window consisting of C plus one adjacent U-side site on each side differs from [last(U)]++C++[last(U)] for all sixty U,C cases. Consequently the endpoint cannot be ANY template with the same oriented U and same C immediately adjacent to nonempty U bands on both sides, regardless of J, and in particular cannot be T(q,k+5;J,U,C).

This decides the PHYSICAL_TSTAR_FIXED_CENTRE_RETURN_AT_PHASE4 sublemma for those two centres for ALL independent q>=14,k>=100, **without T12 insertion, modulo-11 gates, strict-W9 pruning, or enumeration of J**. It does not exclude other C, change of U orientation, centre mutations, non-rooted clocks or other phases.

## Outer carry-cone lemma (PAPER PROOF)

For every symmetric pairword P_t with known first L coefficient sites X and therefore last L sites reverse(X), normalizing P_t into the digits of the next integer starts with known carry 0 on X. The carry entering reverse(X) from the unknown middle is exactly one of {0,1}. Normalize that high suffix with BOTH inlet choices. If both produce the same final carry bit gamma, the true digit-length overflow is gamma, irrespective of the middle. For gamma=0 the next coefficient at i<L is low_digit[i]+high_digit[L-1-i]. For gamma=1 its first coefficient is low_digit[0]+1 and its coefficient i in 1..L-1 is low_digit[i]+high_digit[L-i]. Retain the longest prefix on which the two inlet choices agree; this is the actual rooted prefix, so induction is valid without knowing the middle.

Starting at X=B4++W4^14 (L=160), 120 exact iterations in outer_clock.py show both carry choices have identical overflow each time, giving the prescribed (1000)^30 and leaving at least 70 guaranteed prefix coefficients. Every q>=14 has exactly that X and mirrored suffix; hence this establishes the complete true clock for all q>=14 and any J,U,C with sufficient interior. It assumes no phasewise preservation of the rest of W9.

## Inner carry-cone lemma (PAPER PROOF)

Suppose symmetric P_t of length 2a+M contains a known centred symmetric coefficient word S of length M; all 2a exterior coefficients may be arbitrary. Normalize S with both possible incoming carries e=0 and 1 to digit arrays d_e. Given the already established genuine overflow bit gamma, for each j=0,...,M-gamma-1 the next pairword coefficient at position a+gamma+j equals

    d_e[gamma+j] + d_e[M-1-j].

Both indices lie inside S. For each inlet branch this is a palindromic word of length M-gamma; discard symmetric end positions at which the two branches disagree, retaining their largest common central palindrome. Every true trajectory must match this common central block. Its offset change is gamma+trim; this construction is invariant under translating a, so it requires no knowledge of q, k, J, or the exterior carries. Induction for 120 steps is exact. It is a true two-ended carry argument, not an unsupported uniform radius assumption.

For all k>=100 choose only the innermost 100 U copies on each side of C as S0=U^100++C++reverse(U^100). All remaining copies and J,W,B are unknown exterior. The 120-step cone is therefore literally identical for every k>=100 and every q,J. The computed total inward cut is 150,151 or 152 coefficients for the three U rotation positions, leaving protected central lengths 332,330,328 for even C and 333,331,329 for odd C. Each of the three rotation classes has ten U words. The target centre-flank word is [U[-1]]++C++[U[-1]] and does not depend on k or outer lengths. For C=(4,4) all 30 protected flanks differ; for C=(4,14,4) all 30 protected flanks differ. These sixty exact finite checks are in cone_certificate.py.

## Reproducibility and independent check

From the repository directory calculation/new_structures/AC37, run:

    python3 outer_clock.py
    python3 cone_certificate.py
    python3 cone_crosscheck.py

The certificate checks sixty finite state transitions of depth 120 and asserts the centre-window inequality, with no sampling of J in the mathematical result. Output SHA-256 for the local cone_certificate.py run was e4c1aa1800124153b966e6c93bd7f5b48c1a032d93820419305fcd2db1b12ed4 (the artifact stdout may differ if formatting changes). The independent checker constructs genuine large Python integers and tests both asserted cones and the physical overflow at **every intermediate state** across 120 reference trajectories and 32 extra width controls: 18,392 physical pairword states total, all matched. That numerical cross-check is independent of the proof of cone soundness; the all-width quantification comes from the explicit two-carry induction and choosing the same inner 100-copy core for all k>=100.

The precise remaining problem is a return with a DIFFERENT centre, a different U orientation, another clock, or a more general moving/growing interface. No positive all-time cycle is claimed.
