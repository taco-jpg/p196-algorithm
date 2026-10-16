# Agent #318 — exact arithmetic probe of n_k = 10^k - 26

## Status

This is WIP finite evidence, not a proof of an infinite-safe orbit and not a result about 196.

I selected the explicit family

    n_k = 10^k - 26,   k >= 4.

The family has a fixed finite defect at the right boundary of an arbitrarily long 9-block and was selected as an independent candidate for direct boundary-state analysis.

## Exact arithmetic

The first reverse-add states have closed forms, with small-width boundary exceptions caused by overlap:

    T^0(n_k) = 10^k - 26 = 99...9974                         (k >= 4)
    T^1(n_k) = 147 9^(k-4) 73                                (k >= 4)
    T^2(n_k) = 527 9^(k-5) 714                               (k >= 5)
    T^3(n_k) = 945 9^(k-5) 439                               (k >= 5)
    T^4(n_k) = 1880 9^(k-6) 8988                             (k >= 6).

Here 9^r denotes a block of r copies of the digit 9, not an exponent.

The exact small cases are:

    k=4: 9974 -> 14773 -> 52514 -> 94039 -> 187088
    k=5: 99974 -> 147973 -> 527714 -> 945439 -> 1879988
    k=6: 999974 -> 1479973 -> 5279714 -> 9459439 -> 18808988.

The included checker verifies the displayed parameterized identities for every k through 200 in their stated ranges.

## Finite orbit screen

Exact integer iteration was run for 5,000 additions for each k=4,...,12. No palindrome was encountered in any of these nine runs.

    k=4   no palindrome through t=5000
    k=5   no palindrome through t=5000
    k=6   no palindrome through t=5000
    k=7   no palindrome through t=5000
    k=8   no palindrome through t=5000
    k=9   no palindrome through t=5000
    k=10  no palindrome through t=5000
    k=11  no palindrome through t=5000
    k=12  no palindrome through t=5000

The test is exact integer arithmetic. It is nevertheless only a finite-horizon computation.

## Fixed-defect sweep

A second exact screen considered every fixed defect c with 1 <= c < 5000 and required n_k=10^k-c to avoid palindromes through 1,000 additions simultaneously for k=4,...,8.

Exactly four defects survived that filter:

    c = 26, 1402, 4112, 4832.

Extending those four candidates to k=4,...,12 with a 3,000-step cap gave:

    c=26:   no palindrome for every k=4,...,12 through t=3000
    c=1402: no palindrome for every k=4,...,12 through t=3000
    c=4112: palindrome at t=73 for k=9; no hit in the other tested k values through t=3000
    c=4832: no palindrome for every k=4,...,12 through t=3000.

This sweep is finite discovery evidence. It does not show that c=26, 1402, or 4832 defines an infinite-safe family.

## Affine-boundary test

For each fixed time t, I tested finite samples for consistency with an affine form

    T^t(10^k-c) = a_t * 10^k + b_t

using rational a_t,b_t inferred from k=20,21 and checked at k in {10,11,12,15,20,25}. The fit widths and validation widths overlap at k=20; a fit point is not an independent validation point.

For c=26, the formula agrees at all of those sampled widths through t=14 and first disagrees within that sample at t=15. This is not a theorem about all k or all sufficiently large k. The fitted coefficients through t=14 are:

    t=0   a=1           b=-26
    t=1   a=37/25       b=-27
    t=2   a=132/25      b=-286
    t=3   a=473/50      b=-561
    t=4   a=1881/100    b=-1012
    t=5   a=539/5       b=-10131
    t=6   a=107679/100  b=-12430
    t=7   a=183469/100  b=-135729
    t=8   a=177969/50   b=-271348
    t=9   a=306383/50   b=-531795
    t=10  a=1115631/100 b=-964579
    t=11  a=2360941/100 b=-10599468
    t=12  a=47109909/1000 b=-20108836
    t=13  a=93229807/1000 b=-39118662
    t=14  a=88274307/500 b=-78226423.

The first sampled mismatches occur at t=15 for c=26, t=8 for c=1402, and t=5 for c=4832. In each case, only the smallest sampled validation width, k=10, disagrees at that time. With fit widths k=30,31 and validation widths {20,21,22,25,30,35}, the corresponding first mismatches instead occur at t=31,23,23, respectively, only at k=20. These times depend on the finite sampling domain.

For example, at c=26 and t=15 the fitted formula is (118990718/125)*10^k - 761380752. The residual at k=10 is 990000000, while it is zero at every tested k in {11,12,15,20,21,25,30,40,100}. The finite sample therefore does not establish failure of eventual affinity, nor does it prove eventual affinity or recurrence. The candidate cannot be promoted to a recurrent construction merely from its long 9-block.

## Structural observation

For fixed t and sufficiently large k, the first several iterates retain a long central 9-block while their boundary words change. This is materially different from asserting that one carry word is invariant: the boundary/carry state evolves.

The promising research question is whether the evolving boundary has a finite-state recurrence, possibly with a parameter shift in k. Such a recurrence would be necessary before this family could become an actual infinite construction.

A direct attempt to infer recurrence from the first states is not yet justified. In particular, the later orbit quickly leaves the five-step closed-form regime. No finite-state return has been established.

## Scope and next obligation

This family should remain classified as checked finite evidence / WIP. It does not establish decimal Lychrel existence and does not settle the orbit of 196.

The next substantive task is an exact boundary-state recurrence search for the strongest surviving fixed-defect candidates, beginning with c=26 and c=1402. The target is a relation of the form

    T^p(n_k) = F(n_(k+r))

or an equivalent finite-state conjugacy on the boundary data.

If no such recurrence exists, the exact first divergence should be preserved as a negative result and used to refine the construction search.

## Review note: overlap with the 196 orbit (independent check)

All numbers above were reproduced exactly (closed forms through k=200, the 5000-step screens for k=4..12, the four surviving defects, and the first sampled affine-fit mismatches at times 15/8/5).

However, the smallest members are not independent of the 196 problem. Comparing against the first 6000 iterates of 196:

- c=26, k=4: 9974 → 14773 → **52514**, which is the 5th iterate of 196 (196 → 887 → 1675 → 7436 → 13783 → 52514).
- c=4832, k=4: 5168 → **13783**, the 4th iterate of 196.
- c=4112, k=4: 5888 → 14773 → **52514**, again the 196 orbit.

So for k=4 these "survivals" are just the 196 orbit itself. For k=5..12 no member joined the 196 orbit within 3000 steps. Surviving a few thousand additions is also common for seeds of five or more digits, so this screen is weak evidence; only an exact boundary recurrence would make the family significant.

## Agent #452 correction provenance

This proposed correction preserves all original numerical orbit screens and fitted coefficients. It narrows the interpretation of the affine-width tests, not their exact arithmetic. The original report is retained at PR head 9ec2bca9342b35fae43a1decb65b3aadfd8507ae, Git blob 9367805804428497f0da960775a528b975081951, and in the accompanying original-source snapshot. Its statements of first nonlinear interactions and failure of a fixed affine boundary system are superseded by the explicitly finite-sample statements above. Review 5543048799 records the independent reproduction. No all-time or eventual-affinity theorem is established by this correction.

## Agent #7 rebase verification

The Agent #452 correction was rebased against integrated main 09271f10881699435067ac0502c1f1957c1cbcc0, report blob 0370c44913a8864e0f6b2dcfeb60b40d4f59b9b2. The original final patch hunk no longer applied after addition of the 196-overlap review note. All original numerical sections and fitted coefficients are retained; the later review note now uses the same finite-sample terminology. This is a proposed documentation correction only. Local patch validation does not establish remote integration or a new mathematical result.

## User-authorized integration — 16 October 2026

The correction above is included in this revision following the user’s direct integration request. The preceding proposal/rebase notes describe the preparation checkpoint, not the current publication state. The complete pre-correction report remains byte-identical at `proofs/archive/integration-repairs/agent-7/pr79-09271f108816-REPORT.md`. Audit source, prior logs, the exact proposed patch, fresh numerical replay logs, 和 recovery instructions are retained under `proofs/coordination/audits/agent-7/A7-20261016/`.

This documentation-only integration preserves Agent #452’s correction provenance 和 the independent corroboration by Agents #431 和 #11. Executable research sources, coefficients, search bounds, 和 historical proof classifications remain unchanged. No new Lean build or all-time mathematical conclusion is claimed.
