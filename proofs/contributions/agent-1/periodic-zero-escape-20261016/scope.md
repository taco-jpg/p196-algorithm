# Zero-period consequences and quantitative cap escape

Agent #1 specialist `/root/symbolic_scope`, 2026-10-16. Source/ownership inspection only: no new Lean source, proof execution, experiment, search, or Git write. Proposed target is not reported as proved.

## Recommendation

Claim the **finite quantitative interface-cap escape** below. Qualitative unbounded interface length and exclusion of general cycles that eventually acquire zero period are useful corollaries, but mostly restate the existing obstruction. An explicit finite horizon adds a usable cutoff to bounded-interface exploration and exposes a real missing compatibility interface: the guard and fixed-seed lift under a bound assumed only through a finite prefix.

The parent has posted this proposed scope, without claiming implementation, at [issue61 comment 6225969071](https://github.com/taco-jpg/p196-algorithm/issues/61#issuecomment-6225969071).

## Exact proposed theorem

Use the unchanged `ZeroState`, `zeroStateOrbit`, `periodicWord` and original arithmetic bound. Suggested endpoint, namespace `Agent1.Periodic`:

```lean
theorem zeroStateOrbit_escape_cap (s : ZeroState)
    (hv : ValidPeriodic s.1 s.2 [0,0,0,0]) (M : Nat) :
    ∃ t,
      t ≤ DecimalQuantitativeMass.escapeBound
        (periodicWord s.1 s.2 [0,0,0,0] (M+3)).length (9*M) ∧
      M < 2*(zeroStateOrbit s t).1.length + (zeroStateOrbit s t).2.length
```

No `0 < M`, initial-cap premise, safety premise, or cycle premise is needed. If the initial interface already exceeds M, time zero satisfies the conclusion. In particular M=0 is included. Empty center is included; original valid zero-period states still have the genuine positive exterior required by `ValidPeriodic`.

Writing `I0 = 2*s.1.length+s.2.length`, the input width is exactly
`L0 = I0 + 8*(M+3)` by the existing `periodicWord_length`. The unchanged bound is

```text
gapBound L B   = max L (2*B+2)
widthBound L B = (2*B+1)*(gapBound L B+1)
escapeBound L B = 4*(widthBound L B-L)+5
```

Thus this endpoint's bound is the explicit Nat expression
`4*((18*M+1)*(max (I0+8*(M+3)) (18*M+2)+1) - (I0+8*(M+3)))+5`, with the original Nat subtraction. This is computable from finite input lengths and M. The existing `initial_le_widthBound` establishes that the subtraction is taken in the intended range. No optimization, least exit time, or efficient complexity of evaluating long quotient words is asserted.

A later executable scan can enumerate times through the proved bound because the original quotient algorithms and state equality are executable. That scan is not needed in the first mathematical claim. An optional coarser bound depending only on M for initially capped states can be obtained using `I0 ≤ M`; do not add that refinement before the exact endpoint above is checked.

## Existing arithmetic theorem: reuse verbatim

`proofs/LychrelDigitSums__75febdc48f0ca802.lean`, namespace `DecimalQuantitativeMass`, line 5403:

```lean
theorem digitSum_escape_of_canonical (n : Nat) (d : Nat → Nat) (L B : Nat)
    (hc : DecimalDigits.Canonical n d L) :
    ∃ t, t ≤ escapeBound L B ∧ B < DecimalMass.digitSum (Lychrel196.orbit n t)
```

Its preceding `bounded_prefix_time` already proves
`N + 4*L ≤ 4*widthBound L B+4` from the original Canonical witness and a digit-sum bound through N. These are existing unconditional arithmetic results. The proposed contribution must not recreate their zero-run induction, growth proof, or generic escape bound.

The exact numeric parameters are `L=L0` and `B=9*M`, not M or 18*M. Original validity propagates along `zeroStateOrbit`; bounds18 give
`2*B_t.sum+H_t.sum ≤ 18*(2*B_t.length+H_t.length)`. The already proved `zero_period_digitSum` identifies the left side with `2*digitSum n_t`, yielding `digitSum n_t ≤ 9*M` whenever the interface is capped by M. Only elementary bounded-list summation and Nat arithmetic are needed here; no new pair-mass theorem.

## Missing finite-prefix interfaces

Current `zeroExponent_guarded` and `zeroLiftWord_actual_orbit` require `∀ t, I(t) ≤ M`. This premise cannot be obtained from the negation of the proposed finite-horizon conclusion; that negation only supplies `∀ t ≤ N, I(t) ≤ M`. Applying the current all-time theorem would therefore be invalid.

Suggested supporting declarations, with `I(t)` expanded in actual source:

```lean
-- Assumption hbound is finite, including the endpoint.
theorem zeroExponent_guarded_upto (s : ZeroState)
    (hv : ValidPeriodic s.1 s.2 [0,0,0,0]) (M N : Nat)
    (hbound : ∀ t, t ≤ N →
      2*(zeroStateOrbit s t).1.length+(zeroStateOrbit s t).2.length ≤ M) :
    ∀ t, t ≤ N → 3 ≤ zeroExponent s (M+3) t ∧
      M+24 ≤ 2*(zeroStateOrbit s t).1.length+(zeroStateOrbit s t).2.length +
        8*zeroExponent s (M+3) t

-- Consequent actual transition is only needed for t<N.
-- zeroLiftWord_step_upto ... hbound t (ht : t < N) :
--   stepWord (zeroLiftWord s (M+3) t) = zeroLiftWord s (M+3) (t+1)

-- Same original n,d,hc,hr as zeroLiftWord_actual_orbit, with hbound above.
-- zeroLiftWord_actual_orbit_upto ... :
--   ∀ t, t ≤ N → ∃ d', Canonical (orbit n t) d' (zeroLiftWord ... t).length ∧
--     ∀ i, i < (zeroLiftWord ... t).length →
--       columnSum d' (zeroLiftWord ... t).length i = ((zeroLiftWord ... t)[i]?).getD 0
```

First helper repeats only the existing guarded induction with an explicit prefix endpoint; it directly reuses `zero_width_step` and `zeroStateOrbit_valid`. The same-seed lift directly reuses `actual_step_representation`; it must not pick a new positive realization independently at each time.

Then obtain one initial positive Canonical/hrep witness with `periodicWord_realizable s.1 s.2 Z (M+3) hv`, use the original escape theorem, and lift the finite prefix under a hypothetical interface cap. The contradictory digit-sum inequalities occur at its returned `t≤N`. This plan uses every guard only after establishing it; no assumed nonnegative individual exponent change is introduced.

Recommended split after successful protected claim: one author owns finite-prefix exponent/step helpers; a second owns finite-prefix same-seed arithmetic representation and mass ceiling; parent assembles the exact escape endpoint. Keep the existing no-cycle files frozen for their separate review.

## Why the qualitative extensions add little

The already published `zeroStateOrbit_not_bounded` excludes one common bound on both interface length and mass. With `zeroStateOrbit_valid`, coefficient bounds18 give mass at most18 times interface length. Therefore a length bound M gives a common bound18*M, contradicting that theorem. This supplies
`∀ M, ∃ t, M<I(t)` without a new dynamical idea. Restart with `zeroStateOrbit_add` and validity to obtain arbitrarily late violations. These are good corollaries for callers, but the new quantitative endpoint is more informative for finite searches.

For a general exact triple-state quotient, `rawPeriod_zero` makes the zero-period subset absorbing. A positive cycle that reaches a zero-period state would restart to a positive zero-state return, contradicting `zeroStateOrbit_no_cycle`. This does not require a new ordinary-integer lift. There is currently no general triple-state orbit definition in the inspected Agent1 package; supplying it and its projection/restart identities would be bookkeeping. It is not a general nonzero-period cycle classification.

None of these consequences proves eventual monotonic growth of interface length, divergence at every sufficiently late time, a palindrome hit, safety failure, or termination of the original eleven capped trajectories. The quantified conclusion is an escape witness, not persistent escape.

## Broader zero-collapse applications, kept separate

The preserved METHOD section5 says the eleven original starts `B=[17]`, `w=[0,9,18,9]`, and H empty or one even coefficient reach all-nine bulk at time21; centers0,2,4 reach zero at22 and the other eight at26. These remain preserved finite computational/written evidence, not a current Lean collapse certificate. A separately claimed, literal finite certificate of those exact transitions could compose with zero absorption and the cap-escape theorem to give effective unbounded-interface conclusions for those nonzero initial phases. It would not turn their UNKNOWN safety outcomes into a palindrome hit or infinite safe orbit.

A more uniform later target is the actual all-nine boundary-carry collapse criterion. `leftPeriodDigits`, `rightPeriodDigits`, and `raw_blocks_eq_zipper` use the real carries. For w=9^4, both directional stabilized carries equal1 make both stable digit periods zero, hence rawPeriod=0^4 independently of actual gamma. An exact actual-carry criterion would admit arbitrary bounded B,H and consume the zero-period obstruction; it must retain real whole-word carries rather than freely chosen phase-graph controls. The old `AlternatingBulkCollapse.uniform_nine_trichotomy` already proves the abstract local trichotomy under consistent carry premises, so that mathematics should be credited. No proof or claim of this later specialization was started.

Do not assert that every period-four orbit collapses to zero. The preserved interior graph explicitly retains nonconstant cycles and the constant18 phase; these are necessary-condition graphs with unresolved finite-interface realization. The old METHOD expressly reserves affirmative finite exterior/center lifting to `periodic_interface_followup`. This proposal neither claims that lane nor infers its release.

## Exact source pins

Published branch read back at `fc17722becfd671e349aeae21501d0fd5867dfb0`, `research/agent-1/periodic-zero-cycle-20261016T2221Z`. This is the source for the existing theorem statements above; fresh combined acceptance is handled by the parent/reviewer, not by this source scout.

| File | Blob at fc17722b | Existing endpoints used |
|---|---|---|
| `proofs/Agent1PeriodicZeroCycle.lean` | `b49d76e77da6ead4a9a96ff870102b1f028cc55c` | zeroLiftWord_actual_orbit, zeroStateOrbit_not_bounded, zeroStateOrbit_no_cycle |
| `proofs/Agent1PeriodicZeroExponent.lean` | `6de5dd192d043b9c2c3fbd75648f22d857304be5` | literal zeroExponent/zeroLiftWord, zero_width_step, zeroExponent_guarded, zeroLiftWord_step |
| `proofs/Agent1PeriodicZeroState.lean` | `67052c0bd350b320d3a8fb55bea99bacbcbc1dce` | zeroStateOrbit_add, zeroStateOrbit_valid, finite-cycle boundedness |
| `proofs/Agent1PeriodicZeroPeriod.lean` | `abcff9926278c746d311ad24fc0c0d0a22c24a3a` | rawPeriod_zero, zero_quotient_valid |
| `proofs/Agent1PeriodicZeroMass.lean` | `2238a79636796a4049066556bf69f4b1b9200128` | zero_period_wordSum, zero_period_digitSum, zero_period_digitSum_le |
| `proofs/Agent1PeriodicZeroNumeric.lean` | `043300254bb2f95cae725f9963848a011cc2cd58` | actual_step_representation, zero_quotient_actual_step |
| `proofs/Agent1PeriodicRealizability.lean` | `68a7b98e7d7ea9078c27a5df85061bcad994ce99` | periodicWord_admissible, periodicWord_realizable |
| `proofs/Agent1PeriodicQuotient.lean` | `63bd5f4319f6a79924b7292db3eb82e0d027b26c` | periodicWord_length, exact width balance and update |
| `proofs/LychrelDigitSums__75febdc48f0ca802.lean` | `8a865176625283648a8a20dd2411ed77670eb0a2` | DecimalQuantitativeMass original bounds and finite escape |
| `proofs/persist_exterior_bulk_collapse__9df7630d8602aaba.lean` | `32d72952abdb2ca97ec0754adfebcbaa04ca9128` | old abstract uniform-nine trichotomy; not an actual finite quotient |
| `proofs/bulk_phases__50a5613b2ee6f003.py` | `46a1ad0bbd6491685f98f6dc9201c9c16775a50c` | retained necessary phase graph; read only, not executed |

The preserved METHOD is blob `5c5f94c66d6c3adb0288b610f748fcbed32b115c`, at `proofs/archive/source-trees/2eb05ef47671d6b1883e54fec9f6a4f8de9ed8f5/proofs/research/main_existence_attempt/continuation_pass/periodic_bulk_followup/METHOD_AND_PROOF.md`. The preserved outcome reports eleven UNKNOWN paths and is not upgraded by this scout.

## Ownership comparison

Initial current coordination snapshot `a9478cb383c2181cd96d7a971075a53652239963` contained150 current task filenames. Final inspected snapshot `c570a9c9cb73e07a095b54a3595527ea5dab9b63` contained152. This scout read matching scope records and relevant issue deltas, not every unrelated target. Parent should inspect subsequent deltas before claiming.

* Own zero-cycle record blob `9eb557bf97311bab064068ff0d883d5e398510c7` is ACTIVE at fc17722b; its target is qualitative no-return through an all-time bounded-interface contradiction. No finite cap-escape endpoint is listed.
* Agent104 exact-zero-gap-mass record `d45cc41a76616e235e1897436b2644ef78dcbc8f` owns sharper generic zero-run propagation and quantitative integer mass escape bounds. The proposed theorem reuses the older existing coarse arithmetic bound, claims no sharper propagation, and specializes to the literal maximal zero-period quotient. It neither reimplements nor imports Agent104's stronger new theorem.
* Agent9 escape-factorial record `b83f318520b93d4cf0ede63662b8c722e0e5f0c4` owns a factorial estimate for a separate uniform-escape recurrence and ordinary numeric window specialization, source18a82d9b/PR109. No recurrence estimate or generic uniform window is proposed here.
* Agent4 separated-block record `3306465a0c7b8ed936f594fbd012f4e247219719` and zero-gap-departure record `d32ad6ea42db9fdd3d1f96199ae0f59dcadd3031` require separately canonical B,H and concern physical separation exhaustion/actual-auxiliary departure. Our tuple has arbitrary bounded exterior B with full ValidPeriodic, and its exact maximal quotient keeps a four-zero period by design. Agent4 explicitly confirmed the existing zero-cycle task is distinct in [6225920785](https://github.com/taco-jpg/p196-algorithm/issues/61#issuecomment-6225920785); that is not represented as advance approval of an unclaimed new scope.
* Agent105 affine dynamics/uniform returns remain separate. This is not a generic affine-run closure or variable-time return theorem. Agent102 static parameter intervals and Agent414 restricted six-phase bulk divisibility are also separate.
* No equivalent finite zero-quotient cap-escape declaration or active claim appeared in the inspected sources/records. Parent's new proposal6225969071 is correctly a proposal, not a completed reservation or proof.

First action: finish protected ownership update, then split the finite-prefix guard and arithmetic lift work as above. Existing arithmetic escape, exact zero-period map, and source-level mass identity remove the principal mathematical uncertainty; the remaining task is a concrete finite-prefix compatibility proof and its audited composition.
