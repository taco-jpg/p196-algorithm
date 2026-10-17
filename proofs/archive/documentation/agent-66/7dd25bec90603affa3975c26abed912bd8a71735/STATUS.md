# Status

Migration input baseline: `2eb05ef47671d6b1883e54fec9f6a4f8de9ed8f5`. The reorganization mapped 10,964 original path/content/mode versions and selected 2,570 current versions.

Archiving files, copying source, and preserving ancestry do not by themselves verify any theorem. The owner explicitly waived content review and build checks for that reorganization; it does not claim that the source compiles or that the workflows are reproducible.

Read the current research entry points and claims together with the individual evidence labels in `RESULTS.md`. Finite computations, conditional lemmas, or a Lean pass within a particular scope must not be used to infer an all-time conclusion about 196.

## Evidence checkpoint, not a repository-wide verification claim

This status clarification is based on the registry present at main snapshot
`09271f10881699435067ac0502c1f1957c1cbcc0`, not on a new Lean execution.
The [pinned accepted-build registry][registry] has Git blob
`90221ac6053b5584602fed24eb93f7984359dff5`; its bytes match the registry in
the original-layout baseline above. It sets `catalogue_complete: false` and
retains the open `PREEXISTING_ACCEPTED_SCOPE_CENSUS` blocker. A result absent
from this registry is not thereby disproved or withdrawn: other accepted
scopes retain their own original evidence records.

The registry contains one project, `consolidation-core`, with **38 module
entries, five claim-family records, and 25 named endpoints**. These are
three different counting units, not repository-wide totals or a percentage
of progress toward a Lychrel proof. Its [prior independent AI-agent
review][review] records a combined Lean 4.19.0 build with the pinned
`6caaee842e94` release and the allowed logical axioms `propext`,
`Classical.choice`, and `Quot.sound`. That historical review and build are
not a fresh replay of every source selected by the reorganization.

The five families below retain their registry classification. The summaries
have been checked against the pinned source statements; no new acceptance,
compiler pass, axiom audit, or independent semantic approval is claimed by
this documentation update. The original-layout paths in the evidence links
are pinned to retained commit `2eb05ef47671d6b1883e54fec9f6a4f8de9ed8f5`.
Dependencies and source hashes remain recorded per module in the registry.

## What the scoped registry does establish

**The specific orbit of 196: a restricted exclusion, not complete avoidance.**
`Agent113.TwoDigit.no_196_thirteen_arith` states that, for every natural
`t` and `k`, if `orbit 196 t` is a palindrome, then its quotient by `10 ^ k`
is not any of `10, 20, 32, 40, 41, 60, 64, 65, 76, 80, 81, 82, 83`.
The family also contains the corresponding restricted ancestry bounds and
sharpness results. It does not eliminate every possible palindrome prefix.
See [the exact arithmetic endpoint][prefix].

**Outer-map charge: the residue modulo 11, not the integer charge.**
For every state `s : Nat × List Nat` satisfying `Valid s.1 s.2` and every
natural `n >= 5`, `P196.Agent3.Charge.charge_zero_from_five` proves
`charge (orbit n s).1 (orbit n s).2 % 11 = 0`. The positive-period return
corollary additionally assumes `orbit P s = s` and `0 < P`. The conclusion
is not the stronger equation `charge = 0`. These are the explicitly defined
outer list map's iterates; this family does not supply an ordinary decimal
whole-word correspondence. See [the statements and return hypotheses][charge].

**Spatial boundaries: the specified relation, not arbitrary decimal orbits.**
`Agent9.AlternatingScalarBoundary.no_six_boundary` and `no_twelve_boundary`
exclude, for every finite spatial length, a path in their exact `Step`
relation from the constant root trace to the specified constant six or
twelve trace. Temporal traces are forward-infinite; they are not assumed
periodic. The registry does not include an actual-exterior bridge in this
family. See [the quantified endpoint statements][boundary].

**High-base first hits: explicit digit and pair-sum hypotheses.**
`Agent11HighBase.numeric_interval_first_hit` assumes integer base `b >= 3`,
`DigitBounds b digits`, `PositiveLast digits`, every pair sum in
`[b-1, b+(b-1)/2-1]`, and the outside pair sum at least `b`.
Its first positive palindrome time is one exactly when all pair sums are
`b+1`, and otherwise is two. The numeral may already be palindromic at time
zero; the iteration continues after palindromes. This is not a theorem for
arbitrary inputs or base two. See [the full interval statement][first-hit];
the registry separately retains the wider two-step threshold and the
base-two counterexample.

**Carry reconstruction: equality of the next integers, not the starting ones.**
`DifferenceObservability.nine_carry_words_determine_next_integer` assumes
canonical representations of two natural numbers at the same initial width
and identical complete carry words at times zero through eight, including
both boundary indices at each current width. It concludes equality of their
`Lychrel196.step` values. The companion endpoint determines their initial
pair sums; neither conclusion asserts equality of the initial integers or
optimality of nine observations. See [the numeric endpoint][carries].

## What remains outside this checkpoint

None of these five registry entries supplies an all-time nonpalindromicity
proof for 196 or a general decimal Lychrel-existence proof. This is a statement
about the inspected registry, not a census of all later contributions.
A proposed arithmetic bridge, a new certificate instance, or an additional
accepted scope must be evaluated on its own exact statement and evidence.

The same registry explicitly lists
`contributions/agent-113/five-layer/FourColumnProjection.lean` as
`INTEGRATED_EVIDENCE_ONLY`, outside its independently verified thirteen-prefix
closure. Preservation or integration of that work in progress does not
accept a five-layer obstruction theorem. Keep this historical exclusion
separate from any later independently checked extension.

Use [RESULTS.md](RESULTS.md) for the migration's source classification, not
as a newly executed theorem audit. Use each result's source, hypotheses,
build record, review, and integration record separately. A source publication
is not automatically `LEAN_CHECKED`; a prior scoped Lean pass is not
repository-wide verification; and an independent review is not itself a
main-branch integration event. Unreviewed or unmerged additions must retain
those limitations instead of inheriting the status of a nearby accepted item.

The [pre-update status document][original-status] is preserved byte-for-byte.
The reorganization counts at the top remain historical migration metadata;
this update does not regenerate inventories or reclassify archived evidence.

[registry]: https://github.com/taco-jpg/p196-algorithm/blob/09271f10881699435067ac0502c1f1957c1cbcc0/proofs/ACCEPTED_BUILD.json
[review]: https://github.com/taco-jpg/p196-algorithm/blob/2eb05ef47671d6b1883e54fec9f6a4f8de9ed8f5/proofs/contributions/agent-1/consolidation-20261015/reviews/batch2.md
[prefix]: https://github.com/taco-jpg/p196-algorithm/blob/2eb05ef47671d6b1883e54fec9f6a4f8de9ed8f5/proofs/contributions/agent-113/two-digit-prefix/TwoDigitMain.lean#L157-L158
[charge]: https://github.com/taco-jpg/p196-algorithm/blob/2eb05ef47671d6b1883e54fec9f6a4f8de9ed8f5/proofs/contributions/2026-10-15-agent3-complementary-bulk/OuterOrbit.lean#L272-L290
[boundary]: https://github.com/taco-jpg/p196-algorithm/blob/2eb05ef47671d6b1883e54fec9f6a4f8de9ed8f5/proofs/contributions/2026-10-15-agent9-alternating-scalar-boundary/AlternatingScalarBoundary.lean#L214-L225
[first-hit]: https://github.com/taco-jpg/p196-algorithm/blob/2eb05ef47671d6b1883e54fec9f6a4f8de9ed8f5/proofs/contributions/agent-11/base-high-threshold/HighBaseFirstHit.lean#L138-L149
[carries]: https://github.com/taco-jpg/p196-algorithm/blob/2eb05ef47671d6b1883e54fec9f6a4f8de9ed8f5/proofs/contributions/2026-10-15-carry-observability/DifferenceObservability.lean#L284-L290
[original-status]: archive/documentation/agent-6/09271f10881699435067ac0502c1f1957c1cbcc0/STATUS.md

<!-- BEGIN AGENT66 PR105 STATUS -->
## Later integrated conditional affine returns

**Checkpoint: PR #105, integrated on 16 October 2026.** This is a later,
separately verified package, outside the five-family registry checkpoint above.
The mathematical sources are frozen at
`87130870e6d17de1d9d2cd709395fbe664645c9b`; the complete source-and-evidence
head is `b312815ba86b086fa195768d685a2a0f355801be`.
[PR #105][a66-pr105] was merged into `main` as
[`ee508d3ecf07b7e4a6ca9b2272fc72e997cb59a3`][a66-integration].
The source statements and verification records below are pinned to that
retained integration commit.

### Exact family and return hypotheses

Let `rs : List Agent102.RunSpec` be a fixed finite run table satisfying
`Agent105.AffineDynamics.SpecBound rs 18`, and write
`Q(k) = Agent102.wordAt rs k` and
`A = Agent105.AffineShape.widthSlope rs`.
Run lengths use the original signed affine expression followed by
`Int.toNat`; empty runs, negative intercepts and eventually disappearing
runs remain allowed. The definition of `A` is the sum of the nonnegative
parts of the run slopes, as stated in
`widthSlope_eq_slope_toNat_sum`. The theorem assumes `A > 0` and a fixed
natural parameter shift `s > 0`. See the [run definitions][a66-run-defs],
[symbol bound][a66-spec] and [eventual-width identities][a66-shape].

For the list endpoint, assume eventual `Agent8.CanonicalPair (Q k)` and
that **every sufficiently large parameter** has some positive return time,
possibly depending on that parameter, with
`Agent8.orbit (Q k) t(k) = Q(k+s)`.
Then there are a single time `t` and a threshold `K` such that

```text
1 <= t <= 4*A*s
for every k >= K, Agent8.orbit (Q k) t = Q(k+s).
```

The safe version additionally assumes that each supplied return avoids
palindromes at every positive output through its return endpoint. It preserves
that safety on the uniform return segment. Its `SafeThrough` predicate tests
`Agent8.normalize (Agent8.orbit (Q k) (i-1)) 0` for `1 <= i <= t`;
it does not test the symmetric pair word itself or assert safety at time zero.

All four endpoints are in namespace `Agent105.UniformReturn`:

| Declaration | Exact scope |
| --- | --- |
| [`uniform_return_wordAt`][a66-plain] | Uniform positive pair-word return under eventual canonicality and actual variable-time returns; no safety premise. |
| [`uniform_safe_return_wordAt`][a66-safe] | The same return conclusion with safety of every positive output, including the endpoint. |
| [`uniform_integer_return`][a66-integer] | Positive ordinary-integer realizers and actual variable-time pair-word returns imply a uniform return for every natural-number representative with that pair word. |
| [`uniform_integer_safe_return`][a66-integer] | The integer statement with `Lychrel196.Palindrome` excluded at every time `1 <= i <= t`. |

The integer hypotheses explicitly supply, for every sufficiently large `k),
some `n != 0` and positive `t(k)` realizing `Q(k)` and the claimed return
under the original `Lychrel196.orbit`. Canonicality is derived from those
positive realizers. The conclusion retains existence of a positive realizer
for each parameter on the final tail and applies the same selected time to
**every** natural number with that pair word. Return means equality of the
target `Agent109.pairWord`; it does not mean equality to an arbitrarily chosen
integer representative. The [independent endpoint review][a66-semantic]
records these quantifiers and representation boundaries.

### Verification and remaining scope

The [final registry][a66-registry] pins all 26 local source modules and keeps
`catalogue_complete: false`. Its dependencies include the unchanged Agent102
run interfaces, Agent1 repeated-block source, Agent8 actual-word dynamics, and
Agent109 compatibility with the original Lychrel196 integer definitions.
All 26 registered Git blob identities match the inspected integration tree.

The retained [execution receipt][a66-receipt] and [verification guide][a66-verification]
record a fresh 20-module canonical build, followed by six additional module
compilations using those checked artifacts, then a complete 26-module-origin
theorem audit. The final audit reports 1,763 theorem constants and 115 new
public theorem endpoints, with theorem-axiom union
`Classical.choice, Quot.sound, propext`. These are different counting units.
The first stage retains the canonical verifier's actual default trust setting;
the extension and final audit explicitly use `--trust=0`. This is not a claim
that all 26 modules were rebuilt a second time. Separate non-author reviews
within the originating agent session are retained; no external peer review is
claimed.

Thus source publication, scoped Lean evidence, independent endpoint review and
default-branch integration each have their own records. Agent #66 checked the
source statements, published records and source identities for this
documentation increment; **no new Lean compilation** was performed here.

The actual variable-return cover remains a substantive hypothesis. This
package supplies no new concrete family satisfying that cover, no
unconditional infinite-safe decimal seed and no all-time conclusion about 196.
The plain-return theorem does not imply palindrome avoidance. Actual affine
closure, fixed-time tail stability, eventual common head and the finite time
bound are proved inside the package; they should not be listed as additional
unproved assumptions of these final endpoints.

The [previous complete status document][a66-original] is preserved byte-for-byte.
The historical checkpoint, its evidence labels and generated inventories remain
unchanged.

[a66-pr105]: https://github.com/taco-jpg/p196-algorithm/pull/105
[a66-integration]: https://github.com/taco-jpg/p196-algorithm/commit/ee508d3ecf07b7e4a6ca9b2272fc72e997cb59a3
[a66-run-defs]: https://github.com/taco-jpg/p196-algorithm/blob/ee508d3ecf07b7e4a6ca9b2272fc72e997cb59a3/proofs/Agent102RunDefs.lean
[a66-spec]: https://github.com/taco-jpg/p196-algorithm/blob/ee508d3ecf07b7e4a6ca9b2272fc72e997cb59a3/proofs/Agent105AffineBasics.lean
[a66-shape]: https://github.com/taco-jpg/p196-algorithm/blob/ee508d3ecf07b7e4a6ca9b2272fc72e997cb59a3/proofs/Agent105AffineShape.lean
[a66-plain]: https://github.com/taco-jpg/p196-algorithm/blob/ee508d3ecf07b7e4a6ca9b2272fc72e997cb59a3/proofs/Agent105UniformReturnPlain.lean
[a66-safe]: https://github.com/taco-jpg/p196-algorithm/blob/ee508d3ecf07b7e4a6ca9b2272fc72e997cb59a3/proofs/Agent105UniformReturn.lean
[a66-integer]: https://github.com/taco-jpg/p196-algorithm/blob/ee508d3ecf07b7e4a6ca9b2272fc72e997cb59a3/proofs/Agent105UniformIntegerReturn.lean
[a66-semantic]: https://github.com/taco-jpg/p196-algorithm/blob/ee508d3ecf07b7e4a6ca9b2272fc72e997cb59a3/proofs/contributions/agent-105/8f1107db019a-affine-dynamics/verification/uniform-integer-return/SEMANTIC_REVIEW.md
[a66-registry]: https://github.com/taco-jpg/p196-algorithm/blob/ee508d3ecf07b7e4a6ca9b2272fc72e997cb59a3/proofs/Agent105UniformIntegerReturn.registry.json
[a66-receipt]: https://github.com/taco-jpg/p196-algorithm/blob/ee508d3ecf07b7e4a6ca9b2272fc72e997cb59a3/proofs/contributions/agent-105/8f1107db019a-affine-dynamics/verification/uniform-integer-return/execution-receipt.json
[a66-verification]: https://github.com/taco-jpg/p196-algorithm/blob/ee508d3ecf07b7e4a6ca9b2272fc72e997cb59a3/proofs/contributions/agent-105/8f1107db019a-affine-dynamics/verification/uniform-integer-return/README.md
[a66-original]: archive/documentation/agent-66/ee508d3ecf07b7e4a6ca9b2272fc72e997cb59a3/STATUS.md
<!-- END AGENT66 PR105 STATUS -->
