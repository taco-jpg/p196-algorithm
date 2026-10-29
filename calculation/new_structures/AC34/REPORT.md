# AC34: phase-1 odd-centre modular obstruction and scoped J6 diagnostic

**Primary label: PAPER PROOF**: an exact necessary all-width gate for the phase-1 fixed-junction T* return. **Secondary label: COMPUTED**: a restricted reference-width endpoint-only scan, not an all-time certificate. No decimal Lychrel number is proved.

## Missing-lemma contribution
A physically rooted p12/m9 phase-1 fixed-J return valid for every independently large q,k must satisfy an explicit phase-specific modulo-11 gate in the odd-palindromic-centre case. This safely reduces the required all-width search without demanding strict preservation of W9 at intermediate steps. It is not sufficient for a return and does not eliminate even centres.

## PAPER PROOF: phase-1 odd-centre gate
Let A(X)=sum_i (-1)^i X[i] (least-significant coefficient first). Read phase-1 B1 and W1 from calculation/decimal_frontier/lattice_kinks/data/lat_p12m9.txt: |B1|=34, A(B1)=-5; |W1|=9, A(W1)=10. Let J have length 6, U length 3, C be an odd-length palindromic coefficient centre of even middle coefficient. Let H(q,k)=B1 ++ W1^q ++ J ++ U^k, and P(q,k)=H(q,k) ++ C ++ reverse(H(q,k)). Suppose for every sufficiently large independent q,k the physically canonical decimal reverse-and-add orbit has the phase-1 clock (0001)^30 and a genuine 120-step endpoint P(q,k+5), with J and C unchanged.

The starting digit length is odd. The prescribed temporal overflow at index 3 makes the digit length even at time 4. At time 5, n5=n4+reverse(n4) is divisible by 11, since reversing an even-digit decimal integer negates it modulo 11. Any later reverse-and-add preserves divisibility by 11, regardless of digit parity. Hence n120 is divisible by 11, and so is its uncarried pair-coefficient polynomial n120+reverse(n120), whose alternating coefficient sum is zero modulo 11.

For odd palindromic C, reflection gives
A(P(q,k)) = 2*A(H(q,k)) + (-1)^(q+k)*A(C).
Because |B1| and |J| are even and the W1/U periods are odd,
A(H(q,k)) = -5 + 10*(q mod 2) + (-1)^q * (A(J)+(k mod 2)*A(U)).
Substitute the return target k+5 into these formulas. Both parity classes of q and of k occur independently in the all-width requirement. The four congruences are equivalent to

**A(U) = A(C) (mod 11); 2*A(J)+A(C) = 10 (mod 11).**

The odd and even q equations are negatives; the two k equations enforce A(U)=A(C). This proves the gate without assuming any locality or intermediate W9 retention. For EVEN palindromic C, A(P)=0 automatically by reflection, so the gate does NOT apply.

With the fixed odd centre C=(4,14,4), A(C)=-6=5 (mod 11). Among the 30 U3 charge-zero rotations (9,a,18-a), even a=0..18, only ranks 1 and 29, U=(9,0,18) and U=(18,0,9), have A(U)=5. Also A(J)=8 (mod 11). An exact 6-column residue DP counts 4,276,882 eligible J among 19^6=47,045,881, leaving 8,553,764 of 1,411,376,430 J/U pairs under this all-width necessary gate. NONE is asserted to be a return. For a SINGLE reference pair (q,k)=(14,100), imposing the two-parity all-width U gate is UNSOUND: the endpoint has k+5=105 (odd), so its exact necessary one-width condition is A(J)+A(U)=2 (mod 11), not A(J)=8 independently of U.

## COMPUTED: separate restricted endpoint-only subcell
At (q,k)=(14,100), J=(1,j1,j2,j3,0,0) with independently variable j1,j2,j3=0..18, all 30 U rotations, and both fixed palindromic centres C=(4,4), C=(4,14,4), the entire 19^3*30*2=411,540 distinct-combination subcell was directly enumerated in eight disjoint rank chunks. Every candidate received 120 actual decimal digit-array reverse-and-add steps, **without any intermediate strict-W9 or mod-11 pruning**, then comparison to the full same-J/C/U phase-1 target with k+5. Exact result: 0 returns; 0 runs with total overflow other than 30; first mismatch counts at LSD coefficient indices 135:303062, 136:41688, 137:13674, 138:53116. The W9 bulk ends at index 159, so every case fails W9 endpoint restoration. This excludes only this finite, fixed-(q,k), two-centre slice: **PARTIAL(411540/2822752860)**, not EXHAUSTED-NONE for P1/J6 and not an all-width exclusion.

The sample is independently checked by Python arbitrary-precision integers against a separate schoolbook digit-array engine, every transition of 15 controls at q,k=(14,100),(20,80),(40,160),(80,320),(160,640). On these controls the exact gamma stream is (0001)^30. No 240-step endpoint, all-q,k exact cycle, or nonpalindrome guard has been established.

Reproduce paper-gate algebra, row identities, U ranks and residue counts:
python3 calculation/new_structures/AC34/phase1_gate.py
Reproduce 15 independent bigint controls:
python3 calculation/new_structures/AC34/verify_controls.py
Compile and run the complete deterministic restricted scan:
g++ -O3 -std=c++17 -o /tmp/ac34scan calculation/new_structures/AC34/census.cpp
/tmp/ac34scan 1 1 6859 0 2 0 4
Repeat the last command for final two args 4 8, 8 12, 12 16, 16 20, 20 24, 24 28, 28 30.
The C++ B1 and W1 literals agree with the published data and are audited by phase1_gate.py.

Outstanding all-time gap: a fully physical 120-step endpoint seam fixed point/closed family preserving both carry ports, overflow, every intermediate nonpalindrome and available W9/U resources for all q,k, or a complete sound automaton emptiness proof. Neither is claimed.
