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
