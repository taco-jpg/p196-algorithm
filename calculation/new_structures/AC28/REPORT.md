# AC28: Centre-universal carry-prefix endpoint exclusion, phase 7

**Label: COMPUTED.** The soundness lemma below is a paper proof. This is not a decimal Lychrel certificate.

**Predicate.** In the rooted p12/m9 phase-7 template, let H = B7 ++ W7^14 ++ J ++ U^k, P = H ++ C ++ reverse(H), where B7 and W7 are the literal rows from lat_p12m9.txt, U=(9,0,18), J ranges over all length-5 coefficient words in {0,...,18}^5, k>=100, and C is any palindromic coefficient centre that admits a canonical decimal source (even or odd length). An exact 120-step fixed-seam return to P(14,k+5) necessarily restores the 160-coefficient prefix B7 ++ W7^14.

**Missing lemma supplied, in one sentence:** the phase-7 fixed-J return has a centre-independent, exact carry-quantified W9 endpoint obstruction for every J of length 5 when U=(9,0,18), at all k>=100 (q=14).

**Soundness (PAPER PROOF).** Every symmetric pair-coefficient word P represents the decimal value of N+reverse(N), and normalizing P from the LSD end computes the successor digits exactly. A known common outer prefix X of length L gives the first L low digits exactly. The unknown carry entering the mirrored high suffix reverse(X) must be either 0 or 1: coefficients are in 0..18 and decimal carries are binary. Normalize that suffix for both carries. If the final carry bits agree, the actual overflow bit is fixed; for every low-side paired coefficient where the two high-side outputs agree (including the one-position alignment shift when overflow=1), its value is independent of the unknown centre. Stop at the first disagreement. This is a sound common prefix of the next symmetric pairword. Induction through all 120 genuine steps proves the calculated common prefix for every possible centre and any additional U copies. A known mismatch in that prefix rules out an endpoint return. The program counts an unresolved overflow or insufficient known prefix as undecided, never as failure. No strict-per-phase W9 condition is imposed.

**Exhaustive computation.** Compile with:
g++ -O3 -march=native -std=c++17 -fopenmp prefix_census.cpp -o prefix_census
Run:
./prefix_census 0 4 0 2476099
U index 0 is (9,0,18), and each J base-19 code in 0..2476098 occurs exactly once. The abstraction starts from a 50-copy U collar (hence it applies to all k>=50, in particular k>=100). Four-thread run: about 226 seconds. Exactly 2,476,099 cases. gammaWrong=0; uncertain=0; short=0; W9 endpoint returns=0. Every first mismatch is in the guaranteed common prefix, at LSD index:

| Index | Count |
|---:|---:|
|136|822328|
|137|1028197|
|138|224296|
|139|353289|
|140|6282|
|141|35740|
|142|2410|
|143|1731|
|144|1470|
|145|177|
|146|165|
|147|5|
|148|9|

Total 2,476,099. These are endpoint **spatial** first-mismatch counts, not a temporal survival/pruning histogram. The preliminary 40-copy scan left 534 cases with insufficient known prefix; those cases were **not** counted negative. With 50 copies all are decided.

**Independent checks.** Run python3 bigint_verify.py, python3 prefix_check.py and python3 audit_slice.py from this directory. The first performs 50 actual unbounded-integer 120-step trajectories; the second checks 2,880 intermediate prefix/carry states against a separate BigInt engine for diverse even/odd centres; the third checks 180 full BigInt endpoint trajectories at widths (14,100), (20,80), (40,160), (80,320), (160,640), including extremal J codes. All passed.

**Scope.** One U out of 30, fixed J length 5, phase 7 and q=14. Other U words, moving or growing seams, q-changing returns, and arbitrary other clocks are UNDECIDED. No all-time decimal nonpalindrome invariant is produced. The theorem excludes this candidate class from the T* search, not the existence of decimal Lychrel numbers.
