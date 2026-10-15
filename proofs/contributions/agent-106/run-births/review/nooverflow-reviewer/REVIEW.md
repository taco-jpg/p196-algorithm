# Independent review by nooverflow-births author

This reviewer did not write `BaseBirths.lean` or `PopulationObstructions.lean`.
Source files under review are read-only to this reviewer.

## BaseBirths: semantic review passed

Reviewed frozen source SHA-256:
`dcca96672161ac382020d476c6bf75d2b3b47456c76193cba55fdfcd6650af33`.

The two complete local classification theorems explicitly quantify an
integer base `b >= 2`, a bounded old coefficient `0 <= x <= 2*b-2`, and two
bits `0 <= a,c <= 1`. Their expression is precisely
`(x+a) % b + (x+c) % b`. The proof reduces each dividend to its two
possible base intervals, then proves all resulting linear cases.

For zero output, each residue must be zero: the possibilities are old
coefficient 0 with zero bits, old coefficient b with zero bits, or old
coefficient b-1 with one bits. For maximal output each residue must equal
b-1: the possibilities are old coefficient b-1 with zero bits, old
coefficient b-2 with one bits, or old coefficient 2*b-2 with one bits.
The three alternatives in either theorem remain disjoint at base two.

The fresh-birth theorems correctly remove precisely the unchanged old
extreme. The mixed-carry exclusion follows from both complete lists.
`births_have_interior_sources` requires `b >= 3`, and its strict source
bounds are correct; the separate binary example correctly shows why
this stronger base restriction is needed. No theorem assumes its target
classification, and none claims an actual overflow transition follows
the same-width mirror formula.

The frozen source was copied into a build directory that did not exist
before this review and compiled by Lean 4.19.0 with `-j1 -DElab.async=false`.
Its compiler result is PASS; see `BaseBirths.log` and `rebuild.json`.
The independent combined exported-declaration audit covers all 39 public
definitions and theorems in these two modules, and passes. Every transitive
axiom set is a subset of `propext`, `Classical.choice`, and `Quot.sound`.
See `ExportedAxioms.lean`, `ExportedAxioms.log`, and `axioms.json`.

## PopulationObstructions: semantic and kernel review passed

Reviewed frozen source SHA-256:
`9b5a0a25fc19dc9f6ceab3f724981ace59e49f273a50197f476af1c25114957b`.

The reviewer independently checked the arithmetic witness by hand:

`196 -> 887 -> 1675 -> 7436 -> 13783 -> 52514 -> 94039`.

For the last transition the old little-endian digit word is `[4,1,5,2,5]`,
whose pair-sum word is `[9,3,10,3,9]`. The new digits are `[9,3,0,4,9]`,
whose pair-sum word is `[18,7,0,7,18]`. Thus both old populations and both
old maximal-run counts are zero; the new 0 population/run count are one,
and the new 18 population/run count are two. This is a no-overflow step.
The final source states these numerical facts in `orbit196_integer_certificate`
and `orbit196_population_certificate`, including the actual `orbit`,
`nextColumns`, `nextWidth`, and computed no-overflow carry. These closed
certificates use kernel `decide`, with an empty transitive axiom set.

The source's `runCount` definition counts precisely the rightmost member
of each maximal nonempty constant-symbol run; the final list member is
handled correctly because `head? [] = none`. The coefficient counts range
over the complete word and count the center once. The `integerWord`
definition uses the real decimal digit at each specified position.
`witness_inputs_canonical` establishes that all three supplied widths are
canonical, so the counterexamples cannot rely on extra leading zeroes.
The two additional witnesses correctly separate overflow and no-overflow:
`10499 -> 109900` and `10518 -> 92019`.

For positive integer coefficients, all three claimed potential classes
(populations, run counts, and their joint positive linear combination)
strictly increase at the same actual 196-orbit step. The stronger
`no_positive_*_potential` statements quantify nonincrease only on canonical
actual integer inputs; the proof instantiates that property at the certified
canonical integer 52514, so there is no abstract-word realizability gap.
The direct comparisons reduce to positive integer expressions, not finite
sampling of the weights.

`any_strict_score_obstruction` is explicitly only a definitional transfer of
the vector certificate to a supplied score/relation with a supplied
separation hypothesis. It is not a separate theorem automatically proving
strict monotonicity for every nonlinear score or every real/rational weight.
The formal all-positive-weight statements in this Std-only module concern
`Int`. The same real/rational consequence follows mathematically from the
exact vector, but that ordered-field extension is not independently
formalized here.

The reviewer rebuilt `LychrelDigitSums.lean` from source in the newly created
build directory, using only that directory as `LEAN_PATH`, then compiled
the frozen `PopulationObstructions` source against that fresh dependency.
Both compilation results are PASS. The baseline source SHA-256 is
`ca5f46523b7cff02c00918b6466a97963087b499fb5f184232b8b3d806dc0b57`.
There is no dependency on the author's or root's pre-existing oleans.
Compiler/preload hashes, exact commands, source/log hashes, elapsed times,
and exit codes are recorded in `rebuild.json`.

## Additional read-only semantic observation

The reviewer also read `ActualBaseBirths.lean` while waiting for the baseline
rebuild. Its bridge preserves the actual reflected index, computes each
incoming carry from a normalized prefix, derives carry-bit bounds from the
existing `terminal_bit` theorem, and connects the source coefficients to
actual input mirror sums in `canonical_reverse_add_extremes`. This was a
semantic reading only; the separate overflow-births reviewer owns its
independent build and final source-hash review. It is not included in the
39-declaration audit above.

## Limits

No finding here asserts a never-terminating 196 orbit, a bounded lifetime
of all future births, or global monotonicity of an unmentioned potential.
The population enumeration's exhaustiveness/minimality is not needed by
the formally accepted counterexamples. No open proof obligation remains
for the reviewed module statements.
