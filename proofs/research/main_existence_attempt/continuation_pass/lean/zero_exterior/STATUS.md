# Three zero exterior columns cannot occur after time four

`ZeroExterior.lean` formalizes the all-time obstruction from the variable
return investigation. It imports only the unchanged `LychrelDigitSums`
source. The previously accepted intrinsic-seam and annihilation modules
are not modified or used as dependencies.

## Main statement

Let n be any positive decimal integer, and let the actual canonical pair
word at orbit time t start, in low-to-high order, with

    (p,0,0,0),  1 <= p <= 18.

Then **t <= 4**. The Lean theorem `numeric_threeZero_time_bound` permits
any canonical representation of the actual numeric state at time t. It
does not assume a preselected digit realization, constant width, absence
of previous palindromes, or a prescribed overflow clock.

The stronger symbolic theorem `iterPairs_threeZero_history` proves that
every earlier state has the same three zero exterior columns, every
preceding update has no overflow, the width stays constant, and

    p_t = 2^t * p_0.

Positivity of p_0 and the universal ceiling p_t<=18 give 2^t<=18, hence
t<=4. `fixed_outer_return_time_zero` additionally proves that the same
positive outer symbol cannot return with this exterior at positive time.

## Exact local argument

The predecessor lemma instantiates the existing exact folded column
equations with the actual low incoming carries, actual high outgoing
carries, and actual emitted digits. The finite local arithmetic is stated
separately and proved using integer arithmetic, without an enumerated
lookup table or an assumed transducer path.

If overflow occurs, the first three zero target columns force six
nonnegative emitted digits to vanish. The first high-column equation then
leaves only outer coefficient 9 or 10. Each case forces a high emitted
digit equal to 9 inside the allegedly zero target prefix, a contradiction.

Without overflow, zero target columns force the predecessor coefficients
at indices 1,2,3 to be zero and the high incoming boundary at the outer
column to be zero. Both outer digits then equal the predecessor outer
coefficient, so the target outer coefficient is exactly twice it.

The finite prefix definition requires all four displayed columns to lie
inside the word. Canonical symmetry and positive outer coefficient force
target width at least five, and therefore predecessor width at least four.
The same-word column identities allow overlapping low and high windows.
No independent-window assumption is introduced near the center.

## Sharpness and scope

The source kernel-checks that the fourth state from 10000000 has canonical
digits 80000008, pair outer coefficient 16, and the required three zeros.
Thus the time-four bound is sharp. Intermediate palindromes are continued
under the ordinary mathematical iteration, as the theorem permits.

It also kernel-checks the admissible pair word

    (9,10,9,0,9,10,9),

whose successor overflows and starts `(10,0,0,10)`. Thus two zeros cannot
replace three in the predecessor conclusion.

This theorem excludes infinitely recurring templates with a single
positive outer coefficient followed by at least three zeros, even if
their cores, widths, spacers, and return times vary. It does not cover
exteriors such as `(p,p,0)`, prove termination of arbitrary orbits, or
prove decimal Lychrel existence or the conjecture for 196.

## Reproduction

From the project root run:

    python main_existence_attempt/continuation_pass/lean/zero_exterior/check.py /workspace/scratch/fe6abe1df721/lean-runtime/lean

The checker rebuilds the decimal dependency and this module from source
in a clean local build directory. It audits the transitive axioms of
every new theorem and definition, permits only `propext`,
`Classical.choice`, and `Quot.sound`, rejects proof placeholders and
untrusted computation, and pins unchanged before/after source hashes.
Complete results are retained in `compile.log` and `verification.json`.

The fresh build completed with PASS: 12 theorems and 3 definitions were
audited transitively, with only the three standard axioms listed above.
The unchanged decimal dependency rebuilt in 57.71 seconds, this module in
6.67 seconds, and the generated audit in 0.58 seconds. The checked source
SHA-256 is
`17fce6b3fc182963b929fa85f3740f7dcb5197620621aa7f3aa260ec77e7b690`.

## Development history

Every source attempt and complete compiler output is preserved in
`development_checks/`. Early arithmetic attempts used quotient and
remainder expressions directly; automatic arithmetic either failed to
close the goals or reached its heartbeat limit. The final argument uses
equivalent exact digit-plus-ten-times-carry column equations and explicit
outer-column cases. No numerical side condition was assumed to rescue a
failed proof.

Other failures concerned normalization of constant natural-number
indices, simplification order after substituting the actual width, and
an underdetermined reflected-index argument. These were repaired without
changing the mathematical statement. The corrected minimum-width fact
also repairs the written draft's overly strong claim that seven columns
were necessary; five suffice, and the final proof includes that case.
