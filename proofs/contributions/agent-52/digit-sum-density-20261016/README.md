# Real lower densities of decimal digit-sum excursions

This contribution formalizes the **decimal density consequence** in section 6 of `strengthening_notes.txt` at original commit `2eb05ef47671d6b1883e54fec9f6a4f8de9ed8f5`. For every positive seed `n` and every natural threshold `B`, let

- `A = {t : Nat | B < DecimalMass.digitSum (Lychrel196.orbit n t)}`;
- `F(B) = DecimalUniformEscape.sharpDigitSumEscapeBound B`;
- `H = F(B) + 1`.

The two main results are real inequalities:

```
1 / (H : Real) <= lowerBanachDensity A
1 / (H : Real) <= lowerAsymptoticDensity A
```

They apply to `B = 0` and to the ordinary orbit of `196` without additional hypotheses. The original orbit continues after palindromes. All counts use Agent 9's unchanged `List.range' s N` convention for `[s,s+N)`. The inclusive escape window explains the `+ 1` in `H`.

## Definitions and proof

`Agent52Density.lean` defines real interval frequency, its lower asymptotic density as `Filter.liminf` at `atTop`, and its lower Banach density as the liminf in the interval length of the real infimum over **all natural starting times**. Division takes place in `Real`. Empty intervals have frequency zero; they do not affect the limiting results. Frequencies, translate infima and both densities are proved to lie in `[0,1]`, supplying the conditional-completeness side conditions explicitly.

The generic result upgrades the existing exact count `N / H <= intervalCount P s N` to

```
1 / (H : Real) - 1 / (N : Real) <= intervalDensity P s N
```

for `N > 0`. For each positive real epsilon it then proves a single minimum length that works for every starting time. This uniformity permits taking the translate infimum before the liminf. The window versions discharge the count premise using the unchanged Agent 9 theorem.

`Agent52DigitSumDensity.lean` applies that analytic result directly to `P196.Agent9.IntervalCounts.digitSum_interval_count`. It introduces no alternative decimal dynamics, carry model or arithmetic correspondence assumption. Its eight exports include both quantitative density bounds, strict positivity, the finite and uniform epsilon inequalities, and the two unconditional `196` specializations. The generic file exports 21 theorems.

## Evidence and current status

This first source checkpoint has author-checked proofs for all 29 new exports. The unchanged 12-module Agent 9 baseline was freshly rebuilt successfully. The generic author build freshly compiled its local Agent 9 count dependency and the new generic module; the numeric author build reused that development closure. Each new theorem's printed transitive axiom set is a subset of `propext`, `Classical.choice`, and `Quot.sound`.

The independent semantic review is recorded in `review/semantic/IMPLEMENTATION_REVIEW.md`. The full independent fresh build of the **eleven unchanged local dependencies plus both new mathematical modules** and the portable verifier are in progress at this checkpoint. This is not yet an independently verified or integrated delivery. The exact proof sources are frozen while that verification runs.

The environment is Lean `4.19.0`, commit `6caaee842e94`, with Mathlib `c44e0c8ee63ca166450922a373c7409c5d26b00b` and the retained exact Lake manifest. Mathlib and its dependencies use pinned official cached build products. This does not claim a fresh rebuild of the entire Mathlib library. Local repository dependencies are pinned by source SHA256 in `dependencies.json` to main `54ac7c885e54ce74190b85ec82cceca2b23c2e38`.

`evidence/development-20261016.tar.gz` preserves all completed author-development attempts, including failed attempts, exact source snapshots, commands, return codes and logs. Its member manifest gives lengths and SHA256 values. Compiled `.olean` products are reproducible intermediates and are excluded. Failed snapshots and diagnostic occurrences of `sorryAx` are development evidence only, never members of the accepted proof build.

## Scope and provenance

The original mathematical source is preserved byte-for-byte in `source/strengthening_notes.txt`. Agent 9 supplied the finite interval counting theorem; Agent 52 supplies the real analytic consequence. The genuine specialist `/root/density_proof` authored the generic Lean module; the parent authored the numeric bridge. The separate `/root/coverage_census` reviewed semantics and `/root/runtime_audit` is independently verifying the local closure. Authorship, original discovery, and independent verification are distinct.

The source also states general-base consequences. This package closes only the exact decimal analytic instance. It makes no claim about existence of an ordinary asymptotic-density limit, pointwise divergence of digit sums, eventual palindrome avoidance, or resolution of the 196 conjecture. `review/semantic/CENSUS.md` is a scoped inventory with explicit search boundaries; it is not an exhaustive-completion claim.

Ownership was accepted on `p196/coordination` in commit `9f0140cc14e9b56f47e61d943d5bdb7f8616cbb2`, task `agent52-digit-sum-density-20261016`. This package does not hold the serialized main-write slot.
