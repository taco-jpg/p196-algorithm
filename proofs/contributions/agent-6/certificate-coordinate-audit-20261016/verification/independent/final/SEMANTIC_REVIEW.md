# Independent semantic review: certificate coordinate audit

Reviewer: Agent #6 runtime/reproducibility specialist, a separate same-project
review role from the three source authors. The reviewer authored no theorem
source, repaired no dependency, and made no Git or remote changes.

## Verdict and exact scope

Semantic verdict: **PASS** for the frozen three-module contribution. The new
results establish necessary signed-coordinate conditions for the existing
Agent109 Boolean checker, an executable necessary filter, equality of the
filtered checker with the original checker, and explicit rejected controls.
The full execution and axiom verdict is recorded separately in
`audit/verification.json`. This semantic review does not establish an accepted
certificate instance, an actual infinite reverse-and-add orbit, a new universal
cycle exclusion, or a conclusion about 196.

| Frozen module | Public theorem exports | Private source theorems | Source SHA256 |
| --- | ---: | ---: | --- |
| CertificateCoordinates | 11 | 3 | 8ed2868cd53b9de494d5568a901f7280ad57746bfcefcede6ccfa02855c4a47e |
| CertificateFilter | 6 | 0 | 29c684a2f83335bd9fa69a4881f415990d9eb33cb1e52206131a4cc1b172e8ff |
| CertificateControls | 12 | 0 | 578424a22b753be50fb7a3a5ba93d9acd9f8740d4c29c3a446dbf6f17b26845f |

The three files define nine named data/functions in total. The 29 public
theorem exports include transport lemmas, wrappers, and controls; this is a
source inventory, not a count of independent mathematical discoveries. All
seventeen existing dependencies retain their previously pinned bytes. The
exact source manifest, the copied registry, and `registry-source-comparison.json`
record the full twenty-module mapping. Publication identity is appended
separately, preserving the original snapshot and execution receipts.

## CertificateCoordinates: exact projection and finite sums

`rowOuter cert i` is definitionally the existing
`Agent116.CertificateExterior.stateOuter (cert.st i)`. That projection keeps
the row phase and maximally strips its phase-valued exterior suffix.
`rowContribution` evaluates the previously reviewed `highContribution` on this
normalized exterior. `rowContributionSum` uses Agent110's integer `sumPrefix`
over precisely the indices `0,...,cert.P-1`, where `cert.P` is the listed-state
length. No raw exterior is silently substituted for a normalized one.

The first private helper equates the coordinate iterator with the original
Agent109 exterior iterator by their common initial state and common successor
map. `rowOuter_orbit` then transports the existing certificate projection
theorem, including its modulo-period index, into the coordinate iterator.
`rowOuter_orbit_of_lt` explicitly requires `i < cert.P` before removing the
modulus. `rowOuter_closed` uses the period endpoint, whose index reduces to
zero. These are exact equalities of exterior states, rather than an assumed
coordinate return or an approximate correspondence.

The original projection theorem already handles certificates with partial,
nonmaximal supplied trims. Its proof obtains the relevant phase and boundedness
premises from `LocalOK` and applies the existing maximal-normalization bridge.
No maximal-trim hypothesis is added to the new theorems. The imported cap-two
development is fully included in the checked dependency closure, but the new
row-orbit argument calls the general projection theorem rather than a cap-two
escape result.

The second private helper compares `orbitSum` with `sumPrefix` by their zero
case and identical successor recurrence. Consequently `rowSum_eq_orbitSum`
transports an arbitrary integer-valued observable, with the index hypothesis
used exactly where required. Specializing it to the contribution observable
identifies the finite row sum with the previously reviewed literal-orbit
contribution sum. The existing exact telescope then proves zero contribution
sum on a valid certificate's closed orbit.

For both-sign witnesses, validity supplies `cert.P > 0`. Applying its first
checked link supplies `Phase (cert.st 0).c`, hence positivity of the unchanged
row phase. The previously reviewed positive-phase closed-orbit sign theorem
then supplies a strictly positive contribution and a strictly negative one,
each at an index below the period. Transporting those states back to the listed
rows preserves the strict inequalities. Positive exterior digits, an integer
realization, and `Admissible0` are not additional hypotheses here. This is
supported by the actual theorem statements and proof dependencies: the sign
argument uses phase positivity, not the separate canonical-head validity
argument used by the older cap-two certificate obstruction.

The `checked_*` wrappers obtain all validity premises through the unchanged
`Agent109.Cert.check_sound`. They add neither a closed-orbit premise nor a
numerical zero-sum premise. `checked_coordinate_conditions` packages precisely
zero total contribution and the two strict-sign witnesses.

## Weighted balance and the distinction between carries

`checked_row_weighted_balance` transports the existing weighted orbit balance
through the same arbitrary-observable sum equality. Its third private helper
relates the integer sum of `overflowBit` to the natural-number `overflowCount`,
including the zero case and the exact successor cast.

The resulting identity concerns `weightedPhase`, `weightedReverse`, and the
overflow indicator of each **normalized** row. Its last summand is the finite
integer sum of those indicators. No equality with the legacy
`Agent110.Accounting.totalGam`, which evaluates the original listed state, is
assumed or concluded. The source comment makes this distinction explicit, and
the theorem type preserves it. The earlier general coordinate development
defines an indicator of nonzero overflow; it is not an unrestricted assertion
that numerical carry is always zero or one.

## CertificateFilter: exact predicate, sound rejection, preserved answers

`coordinateFilter` is a finite Boolean conjunction of three computations:

1. The normalized-row contribution sum is zero.
2. Some index in `List.range cert.P` has strictly positive contribution.
3. Some index in the same range has strictly negative contribution.

`coordinateFilter_eq_true_iff` identifies this computation with exactly the
three proposition-level conditions. The proof accounts for the associativity
of the Boolean conjunction and the range-membership inequalities. It does not
replace either strict sign with a weak inequality or admit an out-of-range
witness.

`checked_coordinateFilter` derives a passing filter from original-checker
acceptance. `check_eq_false_of_coordinateFilter_eq_false` is the Boolean
contrapositive: a failing filter gives a proved original rejection.
`filteredCheck` is the conjunction of the filter with the original checker.
The all-input theorem `filteredCheck_eq_check` handles each original Boolean
answer and proves equality without an acceptance premise. It therefore
preserves both acceptances and rejections. No claim about runtime improvement
or reduced computational cost follows from this logical equality.

All computations are defined on arbitrary finite candidate lists and natural
row data. The equivalence theorem is correspondingly universal; it does not
exclude out-of-range coefficients, excluded phases, mismatched link counts,
or malformed candidates by a hidden hypothesis. The original checker's
`getD` semantics for listed links remain unchanged. Whether such a candidate
passes the full original checker is determined by that original computation.

The period-zero case is expressly covered. Although the empty contribution
sum is zero, both range-based sign tests fail. The filter returns false, and
the original checker also rejects a zero period. Conversely a passing filter
supplies an in-range sign witness, proving the period is positive even without
a checker-acceptance premise.

## CertificateControls: concrete insufficiency and boundary cases

The cancellation candidate has exactly two states and two ordinary link
records. Its exteriors are `(2,[1])` and `(16,[8])`; maximal suffix stripping
leaves both unchanged. The checked contributions are `-11` and `11`, so its
sum is zero and both strict signs occur. The new filter therefore returns true.

The first link fails the original phase equation: the successor phase forced
by phase `2` is `4`, while the second listed state has phase `16`. The theorem
`cancellationCandidate_first_phase_failure` quantifies over arbitrary link
records, so rejection does not depend on the particular chosen trim or
lower-bound fields. The original full checker returns false. The filtered
checker also returns false by its equality theorem.

`coordinateFilter_not_sufficient` uses this specific passing-filter,
failing-checker candidate to refute the claimed sufficiency implication. It
does not assert an accepted example or the existence of a cyclic exterior
trajectory. The exact row/contribution/filter and boundary computations use
`decide +kernel`; they are subject to the fresh trust-zero kernel checks, with
no native-decision oracle.

The empty candidate has period zero and zero contribution sum but fails the
sign filter and original checker. The separate zero-phase candidate has
period one, a single zero contribution, and zero sum; it also fails both
checks. Thus positive listed length plus zero sum does not silently supply
phase positivity or either strict sign. These controls match the hypotheses
of the positive-phase orbit theorem used by the accepted-certificate result.

## Independent execution and accounting boundaries

The author baseline was built from all seventeen existing sources into an
empty object directory. For this review all twenty sources were then copied
as exact byte snapshots and rebuilt again into a different empty directory.
No author object or baseline project object was reused in the final build.
The common official Lean 4.19.0 runtime is pinned by version, binary hash,
shared-library hashes, and before/after integrity checks. Commands use
`--trust=0 -j1 -DElab.async=false` through supported execution escalation, with
no host shim and no inherited preload environment.

The audit checks explicit public declarations, all project theorem constants,
all safe definitions, and actual module origins. Private helpers, anonymous
source instances, and compiler-generated constants are included by their
environment origin. Unsafe generated implementation definitions and axioms
are inventoried separately. Every theorem and safe definition is checked
inside Lean against the allowed axioms and printed with `#print axioms`.
The complete multiline parse must match structured Lean records exactly.

The historical Agent116 receipt defect remains separately documented:
25 of its 1,991 manifest axiom lists were truncated by a physical-line parser.
The complete historical raw output still has only `propext`, `Classical.choice`,
and `Quot.sound`; it is a reporting defect, not a theorem failure. This review
does not edit those older receipts or inherit their incomplete lists.

The combined import environment assigns the generated
`P196.Agent7.Finite.normalize.eq_1` and `.eq_2` names to `OuterBridge`, whereas
the earlier coordinate-only environment assigned them to
`ExteriorFactorizationProof`. The dedicated origin comparison records this
observation. Explicit theorem origins and all pinned source bytes agree;
unique environment constants are counted once.
