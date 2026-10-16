# Independent semantic contract review: digit-sum density

## Review identity and verdict

- Reviewer: genuine subagent /root/coverage_census of Agent #52, reassigned as an independent semantic contract reviewer.
- Proof authorship: none. The reviewer did not write or modify Lean proof files.
- Review date context: 2026-10-16 UTC.
- Accepted task: agent52-digit-sum-density-20261016.
- Claim commit: 9f0140cc14e9b56f47e61d943d5bdb7f8616cbb2.
- Task blob: c6fc8bce82f48b2d99ced3e98065d34fbdda8777.
- Source main: 54ac7c885e54ce74190b85ec82cceca2b23c2e38.
- Intended Lean release: 4.19.0, commit 6caaee842e94.
- Intended Mathlib pin: c44e0c8ee63ca166450922a373c7409c5d26b00b.

**Verdict: PASS_SEMANTIC_CONTRACT.** The proposed definitions and quantified real conclusions correctly express the decimal lower asymptotic density and lower Banach density claims in the original source. No stronger dynamical assumption, hidden conclusion, or weakened finite substitute is required.

This verdict concerns the mathematical contract and the inspected existing interfaces. It is not an implementation acceptance, Lean compilation claim, axiom audit, proof-term review, or independent fresh rebuild. No newly authored generic or numeric density proof was inspected for this verdict. Later implementation acceptance must check the actual declarations against this contract.

## 1. Original mathematical source

Original path:

    proofs/research/continuation/strengthening_notes.txt

Original-layout commit:

    2eb05ef47671d6b1883e54fec9f6a4f8de9ed8f5

Preserved current path at the source main pin:

    proofs/archive/source-trees/2eb05ef47671d6b1883e54fec9f6a4f8de9ed8f5/proofs/research/continuation/strengthening_notes.txt

Git blob: 7103ee939d82740b970dd23fb91e9db50db4ea54.

SHA-256: 15e07772d87cc4ee469541f4fb39ce1d0dce28ac5f630b16980c8abb02db258f.

Section 6 states that, for the ordinary reverse-add orbit and threshold B, the excursion set

\[
A_B=\{t\in\mathbb N:S(T^t(n))>B\}
\]

meets every interval of F_b(B)+1 consecutive times, where F_b(B)=E_b(2B). It explicitly concludes lower asymptotic density at least 1/(F_b(B)+1), and the same lower bound uniformly over translated long intervals, identified as lower Banach density.

The source also explicitly says this does not prove pointwise digit-sum divergence or divergence of time-averaged digit sums. Those exclusions are preserved by the contract.

The current task formalizes the decimal specialization b=10. The general-base escape theorem remains outside this package. This is a faithful specialization of a source theorem, not a claim that the entire all-base source has been formalized.

## 2. Definitions reviewed

For P : Nat -> Prop with the unchanged appropriate decidability instance, let C_P(s,N) be the original Agent #9 intervalCount:

\[
C_P(s,N)=\#\{t\in[s,s+N):P(t)\}.
\]

The actual source definition is the length of the filtered list List.range' s N. It counts all satisfying positions exactly once, includes the left endpoint, and excludes the right endpoint.

The proposed real interval density is

\[
d_P(s,N)=\frac{(C_P(s,N):\mathbb R)}{(N:\mathbb R)}.
\]

**The coercions must precede division.** Casting a natural quotient after division changes the function and would invalidate the intended density. Similarly, the reciprocal density bound must be 1/(H:Real), not the real coercion of natural 1/H.

The proposed lower asymptotic density is

\[
\underline d(P)=\liminf_{N\to\infty}d_P(0,N).
\]

The proposed lower Banach density is

\[
\underline d_{\mathrm B}(P)
 =\liminf_{N\to\infty}\inf_{s\in\mathbb N}d_P(s,N).
\]

These are the correct lower densities for a subset of nonnegative integer times.

### Natural translates are essential

The infimum must be over s : Nat, exactly as in the contract. Extending the set by false to negative integers and taking the infimum over all integer starting positions would create arbitrarily far negative empty intervals and would force the resulting lower Banach density to zero. That is a different object and is not the source's one-sided orbit-time density.

No restriction to translates that are multiples of H is acceptable in the final endpoint. The existing counting theorem already works for every natural translate.

### Order of infimum and liminf is essential

The correct quantity is liminf_N (inf_s d_P(s,N)). It is not enough to prove inf_s (liminf_N d_P(s,N)). The latter only controls each fixed translate separately and can miss arbitrarily long sparse intervals whose starting points depend on N.

The asymptotic density at s=0 is weaker than the Banach density conclusion. Both are valid exports. Establishing the ordinary lower density alone would not close the source's uniform translated assertion.

## 3. Correct uniform epsilon contract

With H a positive natural and a=1/(H:Real), the appropriate uniform conclusion is

\[
\forall\varepsilon>0\;\exists N_0\in\mathbb N\;
\forall N\ge N_0\;\forall s\in\mathbb N,\qquad
a-\varepsilon\le d_P(s,N).
\]

An equivalent version may place the universal s before the universal N, provided N_0 is chosen before both. Replacing this with

\[
\forall s\;\forall\varepsilon>0\;\exists N_0(s,\varepsilon)\;\forall N\ge N_0
\]

loses the uniform translated guarantee and is insufficient for the Banach claim.

The threshold may be chosen positive, so finite-window division is only used with N>0. It may depend on epsilon and H. The existing count bound also permits a threshold independent of the particular seed and translate, since H depends only on B in the numeric application; that additional uniformity is compatible with the contract.

For positive N, the original count bound provides the exact mathematical estimate

\[
d_P(s,N)\ge\frac{\lfloor N/H\rfloor}{N}>
\frac1H-\frac1N.
\]

This is an explanation of the semantic link, not a supplied Lean proof. The error is uniform in s. A non-strict version of this inequality also suffices. The floor cannot simply be erased to claim d_P(s,N)>=1/H for every finite N.

## 4. Existing exact dependency correspondence

The reviewed original module Agent9WindowIntervalCounts.lean defines intervalCount and proves:

- intervalCount_append: adjacent half-open intervals concatenate with no duplicated endpoint.
- intervalCount_mono_length.
- window_property_interval_count: if every half-open length-H window has a witness and H>0, then N/H <= intervalCount P s N for all natural s,N.

The reviewed original module Agent9DigitSumIntervalCounts.lean proves:

\[
\frac{N}{\mathrm{sharpDigitSumEscapeBound}(B)+1}
 \le C_{P_{n,B}}(s,N)
\]

in natural division, where

\[
P_{n,B}(t)\equiv B<\mathrm{digitSum}(\mathrm{orbit}(n,t)).
\]

It uses the original DecimalUniformEscape.digitSum_uniform_window_sharp theorem and the original Lychrel196.orbit. No new digit semantics, alternative dynamics, or finite-subfamily counting is needed.

The definition in SharpUniformDecimal is exactly

    sharpDigitSumEscapeBound B = DecimalProfile.sharpEscapeBound (2 * B).

The inspected SharpUniformEscape source defines E(0)=0, E(1)=1, and the exact decimal manuscript recurrence for M>=2:

\[
E(M)=5\bigl(2(M-1)E(M-1)+2M-1\bigr).
\]

Thus the chosen bound is the source F_10(B), with a natural zero-threshold extension. The name "sharp" does not assert that this coarse escape bound is an optimal escape time.

### Why the +1 is necessary

The original uniform escape theorem yields a witness t with

\[
s\le t\le s+F(B).
\]

This is an inclusive window containing F(B)+1 times. To apply the half-open interval convention, set H=F(B)+1 and use t<s+H. Removing the +1 would strengthen the result without justification and would fail at the threshold-zero boundary.

## 5. Boundary and domain review

### N=0

The filtered list has length zero. Lean's real division gives 0/0=0, so intervalDensity P s 0=0 is exactly the stated convention. The single index N=0 has no effect on an atTop liminf. No positive lower-density estimate is required at N=0.

### H=0

The generic theorem must require H>0. This avoids a meaningless reciprocal and an impossible length-zero witness window. The numeric application always has H=F(B)+1>=1.

### B=0

The source's main recurrence discussion starts with B>=1; the existing Lean interface already allows B=0. The extension is mathematically correct. The inspected definitions give F(0)=E(0)=0 and H=1. For positive n, every iterate remains positive and has positive digit sum, so the excursion predicate holds at all times. Both densities are therefore one. The contracted lower bound is exactly one, not a problematic infinity or zero.

A separate equality theorem for B=0 is optional; acceptance must at least retain the valid all-natural-B endpoint and its denominator convention.

### Positive seed

The hypothesis 0<n is necessary. At n=0 and B=0, the orbit stays zero and the excursion set is empty, contradicting a positive lower bound. The generic combinatorial density theorem does not itself need a seed hypothesis; the numeric theorem must discharge its finite-count premise using the existing positive-seed theorem.

### Iteration after palindromes

The source and the original Lean orbit continue ordinary reverse-add indefinitely after reaching a palindrome. Stopping the orbit, deleting later times, or making a palindrome an absorbing state would change the statement. No hypothesis that n is Lychrel, nonpalindromic, or always safe belongs in the accepted numeric theorem.

### Exact inequalities

The event is B<digitSum, as in the source, not B<=digitSum. Replacing it by the latter would weaken the coverage. Times are all natural times, including time zero; time zero itself does not affect density, but the bridge must use the original predicate consistently.

## 6. Real infimum and liminf are conditionally complete constructions

Real numbers are conditionally complete, not a complete lattice with usable arbitrary extrema. Their sInf/sSup are total operations, but standard order properties require the relevant boundedness and nonemptiness hypotheses.

For every natural s,N, the actual list-count semantics gives

\[
0\le C_P(s,N)\le N,\qquad 0\le d_P(s,N)\le1.
\]

The N=0 ratio is handled by its zero convention; for positive N use the positive real denominator.

For each fixed N, the translate family has nonempty index type Nat and a range bounded below by zero. Therefore its infimum is the genuine greatest lower bound and lies in [0,1]. An upper bound can be obtained from any translate, for example s=0.

For the outer sequences, both d_P(0,N) and inf_s d_P(s,N) are bounded between zero and one. This supplies the required boundedness/coboundedness for real liminf rules and prevents unintended reliance on a default value of a conditionally complete operation.

The inspected pinned Mathlib files explicitly show:

- Mathlib/Order/LiminfLimsup.lean defines liminf via the supremum of eventual lower bounds.
- Filter.le_liminf_of_le requires IsCoboundedUnder with the order relation reversed for a lower-bound conclusion.
- Filter.le_liminf_iff and le_liminf_iff' expose both coboundedness and boundedness hypotheses.
- Mathlib/Order/ConditionallyCompleteLattice/Indexed.lean has le_ciInf for a common lower bound and a nonempty index.
- ciInf_le requires BddBelow of the range.

**Review requirement:** these hypotheses must be established from the actual interval-count bounds. They must not appear as unexplained additional assumptions in exported numeric results. The filter atTop on Nat is nontrivial, so eventual statements have their usual meaning.

## 7. Is a separate Banach-limit existence theorem required?

**No, not for the explicit contract.** The task defines the lower Banach density by liminf of infima and proves a lower bound for that precise quantity. This is a standard one-sided lower Banach-density formulation and matches the source's uniform long-interval statement.

For completeness, the conventional definition often uses an ordinary limit rather than liminf. These agree here by an elementary fact about interval counts. Put

\[
m(N)=\min_s C_P(s,N).
\]

The minimum exists because the nonempty set of possible counts is a subset of the finite set {0,...,N}. Count concatenation implies

\[
m(N+M)\ge m(N)+m(M).
\]

Consequently, for each fixed block length k>=1 and N=qk+r,

\[
m(N)\ge q\,m(k),
\]

and the resulting superadditive normalized sequence m(N)/N converges to sup_{k>=1} m(k)/k. For N>0, inf_s d_P(s,N)=m(N)/N. Therefore the defined liminf equals that conventional limit.

This paragraph is independent mathematical justification of the terminology, not a Lean theorem supplied or audited by this reviewer. The source's lower bound can be formalized directly without a separate Fekete/limit-existence module. The package must not claim it has formally proved this additional convergence theorem unless it actually does so.

The ordinary density at s=0 need not have a limit for an arbitrary syndetic predicate. Thus the contract's explicit exclusion of an ordinary-density limit-existence claim is correct and should remain.

## 8. Semantic sanity checks and conclusion

The periodic predicate t mod H=0 meets every H-window and has both lower densities 1/H. This shows the generic constant is attainable; no universal stronger constant follows merely from one witness per H-window. In a shorter finite interval N<H the count can be zero, so the endpoint must be asymptotic/uniform epsilon rather than an incorrect pointwise finite bound by 1/H.

The empty predicate has both densities zero and does not satisfy the positive-window premise. The always-true predicate has both densities one and intervalDensity=1 for positive N. These are mathematical consistency checks, not executed Lean tests.

No semantic blocker was identified in the accepted contract. The remaining acceptance obligations are:

1. Verify the authored definitions literally match the reviewed count, casts, natural translates, and order of operations.
2. Verify the generic theorem retains H>0 and uses the original full interval count.
3. Verify both real liminf conclusions and the uniformly quantified epsilon conclusion.
4. Verify every conditional-infimum/liminf boundedness obligation is discharged.
5. Verify the numeric bridge quantifies all positive n and all natural B, with the exact original orbit and sharp bound.
6. Compile the actual modules in the pinned environment, audit exported transitive axioms, and obtain a separate fresh build.

The reviewer authored this document and CENSUS.md only. No remote write, Git mutation, source proof modification, compiler run, or build acceptance was performed as part of this semantic review.

## 9. Exact inspected local input hashes

The following hashes identify the actual bytes read for this review. Source excerpts were also fetched directly from the pinned GitHub source blob described in §1.

| Inspected input | SHA-256 |
|---|---|
| proofs/contributions/agent-52/digit-sum-density-20261016/CONTRACT.json | 86b6242e6b4331ed56a89d85a944bfd70e18bbbacf3b0eee4b211b3cae0e1d32 |
| proofs/contributions/agent-9/digit-sum-interval-counts-20261016/Agent9WindowIntervalCounts.lean | 597bfe85a6d5ee332aeaf96845e2dc7c96631080ec3a9c5c6c97f3ce17247ff9 |
| proofs/contributions/agent-9/digit-sum-interval-counts-20261016/Agent9DigitSumIntervalCounts.lean | 0747bb708957e9d3ab8a2f9afbe5e7222a3ca3daedccc2796d644831d9d7dad4 |
| proofs/SharpUniformDecimal__c7370132a3682d7b.lean | 1d46f0bfcadc86ca41573b09f8b588af6a38a8b5798897625459e6f29b714b33 |
| proofs/SharpUniformEscape__a2423abeea30044f.lean | 74def1ba139fef73734b52163f7690d8c6895299c05dc082c69d107617969348 |
| mathlib/Mathlib/Order/LiminfLimsup.lean | 4bdbf74997a94f7f60ac8afffd4692312d5351cfbc2e05afc05273fe83e5bb95 |
| mathlib/Mathlib/Order/ConditionallyCompleteLattice/Basic.lean | 77267735a6f11099f3c6f8883a43e79df259108003ffe75d136023b085bf620a |
| mathlib/Mathlib/Order/ConditionallyCompleteLattice/Indexed.lean | 3877f2fa0e03d7d27ab962c58ecf99612878ed8a142d792437b51298f55aebdb |
