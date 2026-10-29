# AC03 centre-only census and universal-junction cut

**Label: COMPUTED** centre lengths 7–10; **UNDECIDED** centre lengths 11–14. This is NOT a decimal Lychrel all-time certificate.

Predicate: rooted phase-0 p12/m9 at q=14, k=100. The LSD-first pairword is H C reverse(H), with H=B34 W9^14 J U^100, U in {(9,4,14),(4,14,9),(14,9,4)}, palindromic C of length7..14, all letters 0..18 (even midpoint required for odd C). The desired 120-step genuine decimal reverse-and-add return is the same J,C and W9^14, replacing U^100 by U^105. An exact central-window mismatch is a necessary-condition exclusion, not a claim about palindrome survival.

The all-J finite language lemma: at every fixed junction length |J|=0..50, replace each unknown J and C coefficient by all possible letters (except the odd-centre midpoint restricted to evens) and propagate bitmask sets of possible decimal normalization carry, output digit, overflow, and pairwise mirror sums through all 120 steps. These overapproximate every real physical orbit by induction; there is NO unsafe pruning, and no strict-W9 phasewise assumption. For all **8 centre lengths x 3 U words x 51 J lengths = 1,224 complete mask domains**, BOTH the 120-bit overflow clock and the incoming carry at s_t=279+|J|+t are singletons, with clock (1000)^30 and port bits IDENTICAL to J=[5]. Run junction_uniform.py 50 7 8, then 50 9 10, then 50 11 12, then 50 13 14.

The entire initial pairword between the two cuts at s0=279+|J| is unchanged after shifting to that relative cut, regardless of J word or length: it is the same suffix of U^100, same C and reflected suffix. Exact local recurrence uses only the local pair coefficients, forced carry port and forced overflow, and trims one column on each side per step. Induction gives the SAME centre-side window at every step as the J=[5] reference, independent of any transient damage to W9. Thus any failure of the exact J=[5] centre return excludes EVERY J word of each certified length 0..50.

Exact exhaustive physical centre census at reference J=[5] (all three U rotations, centre palindrome parity correct, 120 exact steps per case, ZERO returns, ZERO port exceptions):
- length 7: 3 x (10*19^3) = 205,770.
- length 8: 3 x 19^4 = 390,963.
- length 9: 3 x (10*19^4) = 3,909,630.
- length 10: 3 x 19^5 = 7,428,297.
TOTAL **11,934,660** U/C candidates with 0 centre-side window matches. Each of 12 exact first-mismatch histograms is in certified_census.txt, measured from final left cut s120=400 for J=[5]. No mod-11 even-centre gate or strict-W9 prefix MDD is used.

Reproduce from calculation/new_structures/AC03: compile g++ -O3 -std=c++17 centre.cpp -o centre; run for l=7,8,9,10 and u=0,1,2: ./centre scan l u; run python3 junction_uniform.py 50 7 8 and the three remaining length pairs; run python3 junction_probe.py. The latter has 792 separate full genuine Python-bigint n+=reverse(n) controls spanning J lengths0,1,2,17,24,40,50, three U rotations, two C parities, all-0/all-18/random J; each verifies real clock and same centre-side mismatch as J=[5]. Extra Python genuine-bigint controls at (q,k)=(14,100),(20,80),(40,160),(80,320),(160,640) were sanity checks, not a uniform pumping proof. Local C++ validate checks compared all 120 physical intermediate states and ports in stratified cases.

UNDECIDED centre cardinalities per U: length11 24,760,990; length12 47,045,881; length13 470,458,810; length14 893,871,739. Their singleton carry ports are proven for J length<=50, NOT their non-return. No all-q,k argument; no arbitrary-length J theorem; no moving-seam exclusion; no all-time nonpalindrome certificate.

Missing-lemma contribution (one sentence): a sound all-contents finite-junction carry-port theorem eliminates junction choice from the centre feasibility problem and completes the necessary centre-window fixed-point decision for lengths 7–10 over all junction lengths 0–50.
