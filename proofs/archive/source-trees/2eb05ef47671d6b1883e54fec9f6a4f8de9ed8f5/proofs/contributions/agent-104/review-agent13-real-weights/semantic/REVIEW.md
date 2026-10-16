# Semantic review of Agent13's real safe-weight obstruction

**Initial checkpoint: semantic review complete; independent compilation and
axiom audit pending.** No semantic gap was found in the fifteen stated
real-weight results or their correspondence to the specified written claim.
This is not yet kernel acceptance. Later execution acceptance belongs in a
separate addendum, preserving the initial status and source pins.

Claim: `agent104-review-agent13-real-weights`, coordination commit
`ac825edf3e77ce40aa6cf9d4b45913feb66cff9d`.
Reviewed source: `122367d4935f0b4cd9e0bee19e4121ec66b3164b`,
`proofs/contributions/agent-13/real-safe-weights/{CONTRACT.md,Weights.lean,SqrtBound.lean}`.
The mathematical source is section 3 of `FINITE_SEED_OBSTRUCTIONS.md` at
`c2b6977e43a79caa5ff3bb88801f3ba896986f38`. Exact hashes are recorded in
`source-pins.json` and `provenance.json`; all fifteen unchanged statement
headers appear in `statements.json`.

## Main mathematical meaning

Let `T(n) = n + reverse10(n)` be the repository's ordinary decimal operation.
Let `S` contain precisely the positive integers for which both `n` and `T(n)`
are nonpalindromic. For any real-valued function `w : Nat → ℝ`, assume only
that `w` is strictly positive on `S` and nonincreasing when two members of
`S` are compared in the usual integer order. Values outside `S` are entirely
unrestricted. Define the incoming sum over **all** safe predecessors of a
target, not just over the exhibited family.

For every natural `m ≥ 2`, at
`y_m = 10^(2*m) + 99*10^(m-1) - 1`, the claimed result is

```text
incoming(w,y_m) / w(y_m) ≥ 9*10^(m-2)
incoming(w,y_m) / w(y_m) > (9/100)*sqrt(10/11)*sqrt(y_m).
```

The target's membership in `S` and denominator's strict positivity are proved
from the family result and the weight assumption. They are not extra target
hypotheses supplied by the caller. For every real `C`, some safe `y` satisfies
`C*w(y) < incoming(w,y)`. Consequently no finite real uniform multiplier
bounds this full incoming sum on all safe targets.

This excludes the specified positive nonincreasing-weight method. It is not
an assertion that no weighting method works, no assertion of infinite
survival, and no theorem about the orbit of 196.

## Actual semantics and full-fiber completeness

The unchanged core defines `Lychrel196.step n := n + reverse10 n` and
`Lychrel196.Palindrome n := reverse10 n = n`. Its canonical decimal model
retains the usual behavior of reversing numbers with trailing zero digits.
`Agent13SafeFamily.Safe n` is exactly
`0 < n ∧ ¬Palindrome n ∧ ¬Palindrome (step n)`.

`safeFiber y` filters `Finset.range (y+1)` by `Safe n ∧ step n = y`.
`predecessor_le` proves `n ≤ y` directly from ordinary natural addition,
without a positivity premise. Therefore `mem_safeFiber_iff` proves both
directions of exact membership for every natural target, including zero.
The inclusive upper bound is intentional; `n=y` is retained by the range
and then tested by the predicate. Nothing in the full-fiber proof assumes
that every predecessor has the constructed digit pattern.

`incoming w y` sums each element of this finite set once. Safety excludes
zero and unsafe sources. Target safety is not built into the definition;
it is established for the quantitative targets and assumed explicitly only
where comparison with `w(y)` needs it. `full_safe_fiber_finite` identifies
the unrestricted set of actual safe predecessors with this finset's set.
No convergence, arbitrary truncation, or choice of a finite partial sum is
hidden in this definition.

`predecessor_complete` from the older family package means that every
canonical high word occurs in the indexing of the constructed family.
It does **not** characterize the entire actual incoming fiber. The new
membership theorem, not that older indexing-completeness result, justifies
the use of the full incoming operator.

## Dependency identity and prior review

`Family.lean`, `TargetSafety.lean`, `Counting.lean`, and `LychrelDigitSums.lean`
at the reviewed weight commit were compared byte-for-byte against the prior
family source `8b1e5d15b94ea67bbb8a522b40ba6643c17ef5ee`. All four match.
Their SHA256 values also exactly match Agent109's retained
`reviewed_sources.sha256` at `c17fe7e9431331b58d34f467cb4e9d93b8a4dfa4`.
That review report was read and its semantic acceptance reused only for
these unchanged family/core sources. Neither Agent109's execution nor
Agent13's author/CI execution is relabelled as this reviewer's independent
execution.

The family represents the canonical string
`A || 99 || complement(reverse A)`, with the complement's entire fixed
width retained. For `k=m-1>0`, its pair coefficients are nine except for the
two central eighteens. The family is injectively indexed by
`Fin (9*10^(m-2))`. `safe_predecessor_family` proves every indexed source
safe, proves `Safe y_m`, gives its actual step equal to `y_m`, and proves
`source < 10^(2*m) < y_m`.

In particular the target has a canonical numeral with leading digit one
and units digit nine. Its outer pair sum ten excludes both exact
palindrome-predecessor classes, so both present and next-step safety are
substantive results. `safe_fibers_unbounded N` supplies `N` distinct actual
safe predecessors of a safe target for every natural `N`, including zero.
No all-time safety assumption appears in this dependency chain.

## Statement-by-statement review

All names in this table are in `Agent13SafeWeights`. Exact binders and
expressions are preserved in `ExactTypes.lean`, whose named `_type`
declarations explicitly apply every argument of the original theorem.

| Declaration | Exact obligation and scope check |
| --- | --- |
| `predecessor_le` | Every actual `step n = y` implies `n ≤ y`; no safe or positive premise is needed. |
| `mem_safeFiber_iff` | Exact full-fiber membership for all natural `n,y`. The range bound is derived in the reverse implication. |
| `full_safe_fiber_finite` | Finiteness of the complete actual safe predecessor set by equality with `safeFiber`. |
| `incoming_nonneg` | Positivity on safe sources gives nonnegative incoming sum for any target, without requiring target safety. |
| `family_sum_le_incoming` | An injective `Fin N` family with actual safe step equations gives a lower partial sum. Injectivity removes duplicate counting; nonnegativity of all omitted safe terms justifies enlarging to the full fiber. |
| `finite_family_weight_lower` | For safe target `y`, every safe predecessor is at most `y`, so antitonicity on safe arguments yields `N*w(y) ≤ incoming(w,y)`. No assumption on unsafe values enters. |
| `incoming_weight_lower` | The prior actual family supplies target safety and `9*10^(m-2)` distinct safe sources for each `m ≥ 2`; the result is the exact multiplication inequality. |
| `incoming_weight_ratio` | `hp y_m hy` proves strict positivity of the denominator. `le_div_iff₀` converts the multiplication inequality in the correct direction. |
| `no_uniform_multiplier` | For arbitrary real `C`, choose a natural `N > C`, use `safe_fibers_unbounded N`, multiply by the positive target weight, and compose strict `<` with the family `≤` bound. No `C ≥ 0` premise occurs. |
| `not_exists_uniform_bound` | Negates existence of a single real `C` bounding the full incoming sum at every safe target, using the preceding strict witness. |
| `target_size_bound_nat` | Proves `10*y_m < 11*10^(2*m)` integrally for `m ≥ 2`; controls the natural subtraction exactly. |
| `target_size_bound_real` | Casts that natural inequality to reals, preserves the whole natural target expression, and derives `y_m < (11/10)*10^(2*m)`. |
| `family_size_scaled_power` | Exact identity `↑(9*10^(m-2)) = (9/100)*10^m` in reals; `m ≥ 2` justifies cancellation of the truncated natural exponent subtraction. |
| `sqrt_scale_lt_family_size` | Uses the strict target-size inequality, nonnegative radicands, and nonnegative `10^m` to derive the strict square-root comparison; the scale `9/100` is positive. |
| `incoming_weight_sqrt_lower` | Composes the strict square-root comparison with the already justified ratio lower bound, keeping strictness. |

The family partial-sum proof needs positivity only for the additional safe
terms. The target comparison needs antitonicity only between the two safe
numbers. A function which is negative outside `Safe` is therefore allowed.
Strict positivity cannot be replaced by zero-allowed nonnegativity in the
ratio statement: the identically zero function has incoming sum and quotient
zero and cannot satisfy the claimed positive lower bound.

Negative proposed multipliers cause no proof gap. `exists_nat_gt C` applies
to every real, not only a nonnegative one. If the chosen natural is zero,
the empty family still gives a nonnegative incoming sum, and multiplication
of `C < 0` by the positive target weight gives the required strict witness.

## Exact arithmetic of the square-root constant

All constants in the square-root result are real rationals. In particular
`Real.sqrt (10/11)` forces real division, not natural division to zero.
The target is first computed in `Nat`, then explicitly coerced to `ℝ`.
There is no floating-point arithmetic or approximate square root.

For `m ≥ 2`, `m-1` and `m-2` have their intended nonnegative values. The
integral proof uses
`10^3 ≤ 10^(m+1)` and
`10^(m-1)*10^(m+1) = 10^(2*m)`.
This controls the `99*10^(m-1)-1` correction strictly. The real proof obtains
`(10/11)*y_m < (10^m)^2`, applies the nonnegative square-root order theorem,
splits the product square root, and multiplies by `9/100 > 0`.
The final identity with the natural family count is exact.

The boundary `m=2` gives `y_m=10989`, family count nine, and the strict
integral comparison `109890 < 110000`. The excluded case `m=1` would give
`1980 < 1100`, which is false, so the lower width bound is material.

## Independent finite diagnostics

`check_semantics.py` rechecks all reviewed source pins and the four exact
prior-family source equalities. It enumerates the entire safe incoming
fiber for `y_2=10989` and obtains precisely
`1998,2997,3996,4995,5994,6993,7992,8991,9990`.

It evaluates the full sum for two exact rational weights: one on `Safe`
and negative seventeen outside, and `1/(n+1)` on `Safe` and negative
seventeen outside. The lower comparison and positive divisor hold in both
finite controls. Several negative and nonnegative multiplier controls are
also checked. For `m=2..12`, integer and rational arithmetic verify the
target-size inequality, family-count scaling, and squared version of the
strict square-root comparison. The failing `m=1` size comparison is retained.

These are finite diagnostics, not proofs of arbitrary real quantification,
of all family sizes, or of all complete fibers. They use no floating-point
values and no Lean process. Results are retained in `diagnostics.json`.

## Remaining acceptance gate and exclusions

No unsupplied mathematical bridge or circular premise was found in these
fifteen claims. The remaining gate is execution: independently rebuild the
exact contribution/core/family sources and type applications with pinned
Lean 4.19.0 and Mathlib `c44e0c8ee63ca166450922a373c7409c5d26b00b`; verify
the dependency manifest and source pins; inspect elaborated types; and
audit every compiled local theorem, including generated/private constants,
for transitive axioms outside `propext`, `Classical.choice`, `Quot.sound`.
Cached official library objects must be described accurately; a fresh
contribution build is not a full Mathlib source rebuild.

The accepted scope, if that gate passes, is the specified actual safe
incoming-weight obstruction. It imposes no global sign condition outside
`Safe`, no summability requirement, and no condition `C ≥ 0`. It does not
prove that the constructed family exhausts every fiber for arbitrary `m`,
exclude arbitrary target-dependent/nonmonotone weights or aggregate methods,
or prove decimal Lychrel existence or P196. No original mathematical
ownership is transferred from Agent13 by this review.
