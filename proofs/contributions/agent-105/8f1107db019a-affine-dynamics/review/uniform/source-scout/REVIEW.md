# Uniform-return semantic review against the original written theorem

Reviewer: Agent #105 / `source_scout`, session `8f1107db019a`.

## Independence and scope

I did not author `Agent105UniformReturn.lean`. I did author its Normalize and
Shape dependencies. This is therefore an independent review of the final
uniform-return assembly, with that dependency authorship explicitly disclosed.
It is not an external peer review of the entire development.

During this review I identified the missing plain-return branch described in
Finding U1 below. The parent subsequently assigned its repair to me in the
separate `Agent105UniformReturnPlain.lean`. I make no independent-review claim
for that file; `lean_runtime` was assigned its independent review.

The reviewed UniformReturn source has SHA-256
`fba98eb095ca439835e82a90315254090ed03935c3d17d9e6ae8ebe5bb7b7fa7`.
The written reference is `VARIABLE_RETURN_THEOREMS.md`, section 1, taken from
main `ae8bbdfd2a18e8910eebc25fd2a81661c01abc16` at Git blob
`af8a18bf44cebf0fa56904338087d2f58f15de19`. Its complete source snapshot and
the reviewed Lean source snapshots are retained in `source/`; hashes and
provenance are recorded in `SOURCE-LEDGER.json`.

This review is read-only. It did not rebuild the memory-heavy dependency
closure. The parent's UniformReturn author receipt records a successful
`--trust=0 -j1 -DElab.async=false` compilation of this exact source. The final
full canonical closure check remains a separate verification action.

## Verdict on the reviewed safe-return assembly

The four declarations in the reviewed `Agent105UniformReturn.lean` correctly
establish eventual stability of the actual return and positive-output safety
predicates, select a bounded positive safe return time, and derive the bound
`4 * widthSlope rs * s` for the fixed affine-run family.

I found no off-by-one error, omitted positive output, unjustified head or width
premise, or switch from actual list dynamics to a fitted model. The safe theorem
matches the optional safety clause of the written theorem. The original
plain-return clause was initially absent; that coverage finding is preserved
below instead of being hidden by the later repair.

## Finding U1: the plain-return clause was initially absent

**Finding:** The written theorem first assumes only a positive return at every
large parameter and concludes a uniform positive return. It then adds safety
as an optional strengthening. Both high-level declarations in the reviewed
UniformReturn source require `SafeThrough` in the cover hypothesis. The safe
theorem consequently does not by itself cover the written first clause.

**Classification:** Statement-coverage gap, not a false theorem or a defect in
the existing safe proof.

**Response:** The parent confirmed the finding and explicitly assigned two
new declarations in the separate Plain module: `uniform_bounded_return` and
`uniform_return_wordAt`. The original UniformReturn source remained unchanged.

**Repair author result:** Plain source SHA-256
`0d4d048c017966827be4d146ef52d50de8ea3fc777fd7f21220c73694f5155af`
compiled successfully in its first author attempt with
`--trust=0 -j1 -DElab.async=false`; both printed axiom sets contain only
`propext`, `Classical.choice`, and `Quot.sound`. That is an author result,
not this review's independent certification. The independent repair review is
assigned to `lean_runtime` and recorded separately.

## Hypothesis-by-hypothesis correspondence

| Written hypothesis or conclusion | Lean representation | Assessment |
| --- | --- | --- |
| One natural parameter `k ≥ 0` | `k : Nat` | Same parameter domain. |
| Fixed finite run-symbol list | One fixed `rs : List Agent102.RunSpec` | The list is independent of `k`. Adjacent equal symbols and zero runs are also allowed. |
| Integer run lengths `a_i*k+b_i`, positive for all original parameters | `RunSpec.length : Agent102.Affine`, expanded by `Int.toNat` | On the original positive domain the expansion is exact. The Lean statement also permits negative intercepts and eventually disappearing negative-slope runs. |
| Literal pair coefficients in `0..18` | `SpecBound rs 18` | The lower bound is supplied by `Nat`. On the written positive-run domain all specified symbols occur, so this matches the intended literal-symbol restriction. |
| Positive total slope `A = sum a_i > 0` | `hA : 0 < widthSlope rs` | Exact agreement for the original nonnegative slopes; see the slope discussion below. Strict growth is a retained substantive premise. |
| Positive additive parameter shift `s` | `s : Nat`, `hs : 0 < s` | Same update `k ↦ k+s`; no multiplicative update is covered. |
| Canonical symmetric family | Eventual `Agent8.CanonicalPair (wordAt rs k)` | All list conditions needed by the actual potential are supplied. This predicate is weaker than integer realizability; see the canonicality discussion below. |
| Positive variable return at every sufficiently large parameter | `Eventually (fun k => ∃ t, 0 < t ∧ orbit (...) t = ...)` | The quantifier order is pointwise variable time before uniform selection. The reviewed safe theorem additionally requires the supplied segment to be safe. |
| Safe at every positive ordinary output of the supplied return segment | `SafeThrough w t` | Checks all `1 ≤ i ≤ t` using normalization after `i-1` pair-word steps. |
| One fixed positive time and a whole parameter tail | `∃ t, 1 ≤ t ∧ ... ∧ ∃ K, ∀ k, K ≤ k → ...` | The selected time is outside the parameter quantifier. This is a full tail, not an infinite or sampled subset. |
| Uniform upper bound `4*A*s` | `t ≤ 4 * widthSlope rs * s` | Derived from exact same-head width gain; it is not an additional cover assumption of the high-level theorem. |

## Total slope and signed affine lengths

The original positive-for-all-parameters run-length condition rules out a
negative original slope: an affine expression with negative slope is negative
on a sufficiently long tail. Thus its `A = sum a_i` is a sum of nonnegative
integer slopes.

The implementation defines

```lean
widthSlope rs = (rs.map (fun r => r.length.positivePart.slope.toNat)).sum
```

The already-reviewed Shape module proves both:

```lean
widthSlope_eq_slope_toNat_sum rs
widthSlope_int_eq_slope_sum rs hs
```

The first identifies this value with the sum of original `slope.toNat` without
any sign premise. The second, assuming every original slope is nonnegative,
identifies its integer cast with the original integer slope sum. Consequently
the uniform theorem's `A` is exactly the written coefficient on the written
domain. Negative-slope runs in the broader Lean domain contribute zero after
they disappear; they are not incorrectly counted as negative width growth.

Nonempty or canonical words alone do not imply positive width slope. For
example, constant families can have positive width and total slope zero. The
theorem correctly retains `hA`; no positivity is manufactured from canonicality.

## Canonicality, nonemptiness, and ordinary integer realizers

The original `Agent8.CanonicalPair w` definition is

```lean
w ≠ [] ∧ w.reverse = w ∧ Agent8.Bounded w 18 ∧ 0 < w.headD 0
```

It supplies nonemptiness, symmetry, the coefficient bound, and a positive
outer coefficient. These are exactly the premises used by
`actual_return_bounds`, `actual_width`, and their family wrapper. The proof
only needs canonicality at the source parameter `k`; preservation under the
actual `Agent8.orbit` is established by the inherited actual-word bridge.

The written canonical-realizability convention also requires an even middle
coefficient at odd width. That condition is absent from `CanonicalPair`.
For example, `[1]` satisfies the displayed list predicate but cannot be the
one-column pair word of an integer, because such a column equals twice its
digit. The reviewed source explicitly acknowledges the distinction.

This is a valid broadening of the list theorem's domain. It must not be
presented as a theorem that every `CanonicalPair` has an integer realizer.
An ordinary-integer wrapper should carry an actual representation
`Agent109.pairWord n = wordAt rs k` and use the existing integer/list bridges.
The separately inspected `Agent105IntegerSafety` module provides the needed
positive-time palindrome equivalence on exactly such a representation.

The return is an equality of pair words. It does not assert that the returned
integer is a previously selected integer representative of `Q_(k+s)`;
different integers may have the same pair word. A wrapper quantified over
all actual realizers preserves the correct meaning.

## Time indexing and safety

`Agent8.orbit w 0 = w` and
`Agent8.orbit w (t+1) = Agent8.stepWord (Agent8.orbit w t)`. The step itself is
`Agent8.pair (Agent8.normalize w 0)`.

If `w = Agent109.pairWord n`, the pair word at integer time `i` is the list
orbit at time `i`. Its ordinary integer output at positive time `i` is tested
by normalizing the pair word at time `i-1`. Accordingly the definition

```lean
outputWord w i = Agent8.normalize (Agent8.orbit w (i - 1)) 0
```

has the correct positive-time index. `SafeThrough w t` explicitly requires
`1 ≤ i` and `i ≤ t`; it includes the return endpoint output `i=t` and excludes
the initial integer's time-zero palindrome status. The total definition at
`i=0` is never interpreted as the initial integer's output in the safety
theorems.

The separately inspected bridge
`Agent105.IntegerSafety.nonpalindrome_orbit_positive_iff_of_pairWord` uses the
same `i-1` index and the explicit positive-time premise. Its equality is about
the normalized digit list and its reversal. The proof does not incorrectly
test the pair word for nonpalindromicity; every canonical pair word is already
symmetric.

## Derived time bound and finite-tail argument

`wordAt_head_width_eventually` supplies one tail on which the head is constant
and every nonnegative shift has the exact natural-number length increment
`widthSlope rs * s`. The high-level proof takes the maximum of this cutoff and
the canonicality and variable-return cutoffs. Since `k+s ≥ k`, the target is
also on the head-stability tail.

The call to `word_family_return_time_bound` therefore has all required
premises: positive time, positive shift and growth, actual canonical source,
actual return equality, equal endpoint heads, and exact width gain. The
inherited potential bound then gives `t ≤ 4*A*s` with no extra additive four;
the endpoint potentials cancel because the actual heads agree.

For each fixed candidate time, `actual_return_tailStable` uses the proved
actual orbit closure, exact parameter shift, and Agent 102's literal word
equality stability. For each fixed positive output time, the analogous safety
lemma uses the actual normalized orbit and literal palindrome stability.
No closure or comparison theorem is left as an assumed arithmetic premise of
the final high-level theorem.

Only finitely many times `1,...,4*A*s` are selected. The finite selector combines
their eventual stability and the actual cover to obtain one predicate true
on a whole tail. Individual representation or comparison cutoffs may depend
on the fixed time, which is legitimate for this finite selection. No uniform
cutoff over all unbounded orbit times is assumed.

## Remaining verification boundary

This review accepts the frozen UniformReturn safe assembly semantically,
subject to the separately reported kernel/canonical verification results.
Finding U1 requires the separate Plain module for full coverage of section 1.
The Plain author result and its independent review must remain distinct.
The ordinary-integer family wrappers being assembled by the parent are not
certified by this record merely from the existence of the word-level theorem.

The return-cover assumptions remain mathematical hypotheses. These results
do not supply a concrete affine family satisfying them or establish the
assertion for the starting integer 196.
