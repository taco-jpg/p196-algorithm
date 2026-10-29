# STRONGER RESULT (supersedes the scope below)

See CONE_REPORT.md: a self-contained two-ended carry-cone proof eliminates BOTH fixed centres for all J, all q>=14,k>=100, and every U orientation under the proven phase-4 clock. The old odd-centre census below remains a valid redundant independent check.

# AC37 phase-4 J6, J[0]=0, odd fixed-centre elimination

**COMPUTED (exhaustive reference-width check); PAPER PROOF (mod-11 necessary gate); not LEAN-VERIFIED.** This is a restricted negative subcell, not a decimal Lychrel certificate.

## Exact scope and missing-lemma contribution

For rooted phase-4 p12/m9 B4/W4, a six-site J beginning with 0, any charge-zero U3 rotation among the specified thirty, and fixed odd palindromic C=(4,14,4), **no fixed J,U,C yields the same template after 120 ordinary decimal reverse-and-add steps with k increased by five for every sufficiently large independent q,k**, conditional on the published T12 reference-width cut/insertion reduction. The finite computation is at (q,k)=(14,100). The T12 reduction is not reproved here. No claim is made for even centres, other J[0], changing seams, a different C, or a return only at a single width.

The specific missing all-time-proof sublemma decided here is the absence of a physical uniform fixed-seam T* macro edge in this restricted odd-centre slice. A future positive certificate must lie outside it.

## Parity-complete necessary mod-11 gate (PAPER PROOF)

For alternating coefficient sum A(X)=sum (-1)^i X[i], the published phase-4 rows have A(B4)=31, A(W4)=4, and A(C)=-6; |B4|=34, |W4|=9, |J|=6, |U|=3. If H=B4++W4^q++J++U^k, the full symmetric pairword has A(P)=2A(H)+(-1)^(q+k) A(C).

The first phase-4 source coefficient is 10, forcing a length gain on the first reverse-and-add. The next integer has even digit length, so its following reverse-and-add is 0 mod 11. Every subsequent integer, and hence every returned pairword, remains 0 mod 11. Imposing A(P)=0 for all four parity combinations of independent q,k yields A(J)=5 mod 11 and A(U)=5 mod 11. Exactly U=(9,0,18) and U=(18,0,9) among the thirty specified rotations meet the second condition. This gate is not valid for even palindromic C, so those centres were not pruned.

## Exhaustive computation (COMPUTED)

All 19^5=2,476,099 J with J[0]=0 were enumerated once, partitioned by J[1]=0,...,18. Exactly 225,107 pass A(J)=5 mod 11. Both allowed U were tested for each: 450,214 genuine 120-step full pairword endpoints, zero exact returns and zero 120-bit overflow-clock violations. Clock is (1000)^30 with thirty actual length gains. First mismatches: coefficient index 134:90,397; 135:238,981; 136:6,597; 137:114,239. Every failure is inside the W9 band, before the junction at index 160. No intermediate/strict-phase W9 predicate was used: endpoint healing was allowed. The nominal all-width candidate domain is 30*19^5=74,282,970 J/U pairs; 73,832,756 fail the necessary uniform-return mod-11 gate.

Source realization is canonical with leading digit nonzero. The C++ checker uses independent input/output buffers, genuine carry-out overflow bits, and the entire endpoint pairword. Since all endpoints fail, an intermediate nonpalindrome guard cannot rescue any tested candidate.

Independent ordinary Python big-int n+reverse(n), not using the C++ carry recurrence, was run on 19 distinct J[1] partitions times both eligible U choices and five width pairs (14,100),(20,80),(40,160),(80,320),(160,640), 190 trajectories. A separate direct C++ checker matched their first mismatch, endpoint length and complete clock. Those sampled controls are not the exhaustive proof. Neither the all-width insertion lemma nor a Lean theorem is established here.

## Reproduction

Compile the self-contained source as C++17: g++ -O3 -std=c++17 calculation/new_structures/AC37/odd_census.cpp -o /tmp/ac37_odd . Run /tmp/ac37_odd 0 j1 for every integer j1=0,...,18 and aggregate the RESULT/MISMATCH lines. The expected totals and histogram above are exact assertions. Run the independent verifier, e.g. python3 calculation/new_structures/AC37/verify.py 0,0,0,0,0,0 9,0,18 4,14,4 .

No decimal all-time certificate was found. The physically rooted, complete non-depleting T* regeneration lemma remains open.
