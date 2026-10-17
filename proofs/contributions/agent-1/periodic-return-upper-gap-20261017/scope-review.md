# Initial-phase upper clock-bound equality: source-only scope

Source inspection on 2026-10-17. Checkout
`/workspace/p196-agent1-prefix-saturation-20261016`, HEAD
`71e8fd6f3b7e4c14d1df1b0e792e4b5e6e0158c6`.
Coordination records were read at
`4b4f53d55a3ae3fc03176bb7fda0f7a81062144b`; the relevant Agent8/418 records
and Agent8 lower-growth package are unchanged at the later observed
`19fb9d120803739a3e3fa2142dc8c457e4629068`.

No Lean execution, new finite enumeration, graph search, proof development,
Git mutation, or external message was performed. Archive decoding and hashes
were used only to inspect exact existing source. Proposed statements below
are unproved obligations, not new accepted results.

## Finding and recommended narrow obligation

No exact theorem classifying every positive equality return `N = 4*C` into
the outside sequence `1,2,5,10` was found in the inspected original Agent8,
new Agent8 lower-growth closure, or mapped Agent110/Agent6 sources. There is
an existing checked four-state witness with those outside coordinates.
Its existence must not be confused with uniqueness of equality cases.

Nevertheless, the existing **phase catalog supplies a more direct route**
for the original initial phase. In `Agent1PeriodicPhaseCatalog.lean`, the
only literal edge whose target is `[14,14,4,4]` is line 111:

```lean
⟨[4,9,14,9], 1, none, [14,14,4,4]⟩
```

Thus the proposed finite lemma is simply:

```text
e ∈ phaseEdges → e.target = [14,14,4,4] → e.clock = 1.
```

This statement is not yet a theorem in the inspected source. Its proof
would check a property of the unchanged 124 literal edges; it needs no
new graph discovery, cycle classification, or arbitrary interface lift.

For a positive full quotient return at the original phase, existing
`quotient_return_initial_outside` makes the returned outside coefficient
9 or 10. The proposed incoming-phase lemma makes the last actual clock 1.
The final scalar edge then has positive slack in Agent8's lower potential.
The exact local obligation to formalize is:

```text
0 < p ≤ 18, e ≤ 1, overflow p e = 1,
nextExterior p e = 9 ∨ nextExterior p e = 10
  → 1 < 4*(overflow p e : Int)
          + lowerPotential p - lowerPotential (nextExterior p e).
```

Together with the existing telescoping inequality on the preceding `N-1`
steps, this should yield the narrow endpoint
`N < 4 * quotientClockSum B H w N`, hence `N < 32*G` under ReturnClock.
No new generic equality classifier is required. Reading the scalar formulas
suggests the stronger local defects 2 and 3 for returned outside 9 and 10,
respectively, so `N+2 ≤ 4*C` is a possible stronger endpoint. That arithmetic
has not been formalized or computationally checked in this scout; a new
claim should choose its intended scope explicitly.

This supersedes the initial concern that the head value 10 alone prevents
progress. The useful new restriction is the incoming **phase clock**, not
head-set disjointness. The observation was relayed to root and
`handoff_boundary` to avoid duplicating the phase-length scout.

## Exact existing bridges

All Agent1 declarations below are in namespace `Agent1.Periodic`.

| Source / declaration | Exact reusable content |
| --- | --- |
| `PeriodObstructions__70ce034b31b5b218.lean:190`, `Agent8.path_potential_bounds` | Under positive bounded outside, binary incoming bit, and exact `nextExterior` evolution, its second conclusion is `n ≤ 4*total overflow n + lowerPotential(p 0)-lowerPotential(p n)` over `Int`. Apply to the initial `N-1` edges, then add a strict final edge. |
| Same file:177, `Agent8.exterior_bounds` | Local non-strict upper/lower potential inequalities. No strict-edge or equality-classification API is exported here. |
| Same file:209, `Agent8.closed_path_bounds` | Closed outside gives `N ≤ 4*C` and `2*C ≤ N`. |
| `Agent1PeriodicOuter.lean`, `quotient_outside_step` | Actual `lastInput(Q3) ≤ 1`, `rawGamma = overflow outside lastInput`, and exact quotient outside successor equals `nextExterior`. Empty stored exterior is already handled. |
| `Agent1PeriodicPhaseCatalog.lean:242`, `rawPeriod_catalog_edge` | From boundedness, period length four and phase membership, an existing `phaseEdges` member retains the actual `rawGamma`, exceptional carry label, source, and exact `rawPeriod` target. |
| Same file, `initial_mem_phaseCatalog`, `rawPeriod_mem_phaseCatalog`, `quotient_valid_in_phaseCatalog` | Existing initial membership and phase propagation. A short path induction can supply predecessor phase membership. |
| `Agent1PeriodicQuotientPath.lean`, `quotient_path_valid_catalog` | Existing full validity and outer-catalog membership through the endpoint. If using this route, `Agent1PeriodicOuterCatalog.outerCatalog_phase_mem` supplies phase membership; `outerCatalog_initial` supplies the initial row from `outside_bounds`. |
| `Agent1PeriodicReturnCore.lean:97`, `quotient_return_initial_outside` | Exact quotient path, initial full validity, positive N, full tuple return, and initial phase `[14,14,4,4]` imply initial outside 9 or 10. |
| `Agent1PeriodicReturnClock.lean`, `quotient_path_valid` | Validity at every predecessor. |
| Same file, `quotient_path_closed_outside_clock_bounds`, `quotient_return_clock_gain` | Existing actual clock identification and `C=8G`, positive G, signed delta G, `16G≤N≤32G`. The internal `quotient_path_clock_total` is **private**, so a new module cannot import it as a public helper. A small local sum adapter or a suitable public extension would be needed. |

The path supplies `w(i+1)=rawPeriod ...`; full return and initial phase identify
the last target. Positivity `0<N` is needed to use that predecessor. There
is no missing ordinary-integer realization bridge for this argument.

The new `physicalPrefix_step` is available but unnecessary for this narrow
route. If reused elsewhere, its control is actual `inputThree(Q3)`; this is
distinct from the `lastInput(Q3)` in the scalar exterior theorem. Do not
silently identify these controls.

Pinned local source SHA-256:

```text
PeriodObstructions__70ce034b31b5b218.lean
  83102a949036799a929ba72d74ce9d76bc2a11cb3adf61e0bc06b6013b22991a
Agent1PeriodicPhaseCatalog.lean
  44445a343635503c940ea125727d0bbb75bbf7dce24be62c28a660241363f9f9
Agent1PeriodicOuter.lean
  b30b54bce57542a649208c29900d511e9cc4b64429fb4a48f8da2a387d040678
Agent1PeriodicQuotientPath.lean
  7735197ffa2a779c6ff1e0d76c2ed338ceb1afef75623adb7f2ce9a62c0d4e67
Agent1PeriodicReturnCore.lean
  271fbd1e8c5487e515420ccd145391c039f8dccab3b8f134cf31ff9b8dd7255f
Agent1PeriodicReturnClock.lean
  ef4b8ae6380db3b2286ed166e26fe432626eb36a812c8de5c72d54d0c6bb309e
```

## Existing lower-growth results and their limits

Agent8's current package is at coordination path
`proofs/coordination/patches/agent-8/lower-growth-20261016/`.

`P196.Agent8.LowerGrowth.slow_edges`, `slow_evolution`, and `slow_valid`
in `Agent8LowerGrowth.lean` give the legal periodic prefix walk

```text
(1,5,10) → (2,11,1) → (5,2,3) → (10,4,6) → (1,5,10),
inputThree controls 1,0,0,0; overflow labels 0,0,0,1.
```

`universal_potential_slope_le` proves `4*p≤q` for every universal integer
three-column potential with slope p/q; `no_three_tenths_potential` follows.
These exhibit a sharp abstract slope obstruction, not an equality-case
classification. Source blob `3897f5f19084f48209c863d70c6e35517a92f734`,
SHA `fc5236c1abba6d219bdefd38ace506dfda36b4c5a5dbd5be7fdb930cbd42e0d0`.

The exact archived five-module source was decoded in memory from the ten
`source-checkpoint/partNN.b64` parts. Archive SHA:
`fe73dfa2135767ffb041cf6b22c39a38ccefd010a1b3322af453af8b609b6185`.
In `Agent8LowerTheorems.lean`, `P196.Agent8.LowerBound.lower3_step` proves the
stronger three-column local quarter-rate potential;
`P196.Agent8.LowerBound.lower3_le_every_potential` proves pointwise
minimality among nonnegative potentials. Crucially, `Agent8LowerTable.EdgeCheck`
lines 401–409 gives decreasing `witnessRank` only for the selected
`witnessControl`, when the potential is positive. It is not a rank on all
tight edges, and does not classify recurrent tight walks.

`P196.Agent8.LowerBound.numeric_width_lower3` in `Agent8LowerOrbitBridge`
already transports this potential to ordinary canonical reverse-add orbits.
`strict_boundary_allowance` improves the potential at `(1,4,1)`, not at
every possible initial prefix or every return.

In `Agent8LowerSharpness.lean`,
`P196.Agent8.LowerBound.slow_cycle_finite_orbit` and
`P196.Agent8.LowerBound.slow_cycle_canonical_endpoints` give the actual finite trajectory
159100→161051→311212→523325→1046650, with widths 6 and 7 and equal endpoint
prefix `(1,5,10)`. Time 3 is palindromic. This is neither a safe infinite
trajectory nor a period-four quotient-return counterexample. It does show
that ordinary finite realization alone cannot dismiss the slow prefix
witness. Source blob `d8aa3c5270557d902eaacba3b5681f2722b8587c`,
SHA `ab57bc4a4ebebda8a6fb7639fe8ddb3d0de91963c0dd121e7ec2826e9e66eff9`.

Mapped Agent110/Agent6 cross-check, independently source-read by the existing
`agent6_limits` specialist, found no `N=4C` classifier:

- `Agent110.CarryBudget.certificate_carry_budget_of_positive`,
  `CertificateCarryBudget__5307cef97cfab646.lean:147`, gives only positive C
  and the two rate bounds. `outer_potential_step:115` is non-strict.
- `Agent110.Consequences.eighteen_overflows_gain_cases`,
  `CertificateConsequences__799ad43db1806ce1.lean:106`, classifies gain
  allocation, not outside states.
- `Agent110.CertificateSaturation.saturated_period_constraints`,
  `CertificateSaturation__80df3f83acb87b5d.lean:132`, and its Checked wrapper
  concern **2C=N**, with additional original scalar/SixPhase premises.
  They do not classify **N=4C**. The Agent2 eight-state saturated profile
  likewise concerns 2C=N.
- The mapped ten-module Agent6 exterior contribution contains dynamics,
  projection, arithmetic and escape/potential results, but no inspected
  minimum-overflow equality-cycle theorem.

## Ownership and acceptance limits

`agent8-correlated-lower-width-growth-20261016` is ACTIVE, claim
`a571b0ed89020e48584d27fd39eff897b56b3013`, latest source
`79ad9926307694fbebedffbb147f823225d3fc00`. Its target explicitly owns optimal
three-column lower-width potentials and their ordinary-arithmetic limits.
The record says six new modules/45 exports were Lean-checked with a fresh
five-module original dependency chain, standard axioms only, but **not
independently reviewed or integrated**. This scout did not repeat that audit.
A new generic quarter-rate equality classification would be adjacent to
that active ownership and should not be claimed silently.

Agent418's ACTIVE multiblock compatibility and CLAIMED balanced-block
continuation concern the opposite, eight-state saturated prefix skeleton
and actual odd controls. They are distinct from the proposed incoming
phase-label/one-column slack lemma; no odd-control constraint is proposed.
Historical `periodic_interface_followup` still reserves the affirmative
finite interface realization lane; no release was recovered. The proposed
argument does not enter it.

Recommended fresh claim: only the existing phase catalog's incoming label
at the original phase, its actual last-edge transport, and the resulting
strict upper length bound for exact original-period-four full returns.
Reuse original Agent8 potentials unchanged. Preserve all arbitrary-path,
safety, infinite-lift and existence exclusions. Root must post/confirm that
narrow claim before proof work; this report itself claims no theorem.
