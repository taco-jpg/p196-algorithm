# Independent review of the all-base reverse-and-add interface

**Verdict: PASS.** Reviewed by the independent gate-review stream on 2026-10-15. This is a mathematical and source/provenance review of the fifteen new declarations in `ReverseAdd.lean`, using the previously reviewed all-base carry and physical-width interfaces. It does not claim a second independent Lean compilation.

The reviewed source has SHA-256 `ef99e631210b063b0ab76b15a57d0f5ee47f88c3bbbfededef9fd2d5b694dd7d` and Git blob `f536493264821dd9e69c65939b6b73c0f3b5e2ca`. The exact report, checker, README and log hashes are retained in `independent_source_audit.json`.

## Mathematical interface

Digits are stored from least to most significant. `DigitBounds` and `PositiveLast` describe a nonempty canonical positive numeral. Evaluating the reversed list correctly implements integer digit reversal even when the input has trailing zeros: zeros at the high end of the reversed list contribute zero. No false requirement that the reversed list itself be canonical is imposed.

The pair list is derived as the componentwise sum of a digit list and its reversal. The source proves its length, symmetry, bounds from zero through `2*b-2`, and positive terminal coefficient. In particular, positivity follows from the positive leading input digit and the nonnegative opposite digit; the singleton case is included. Any parity restriction on an odd central pair is already enforced by constructing pairs from actual digits.

`reverse_add_normalization` then invokes continuous carrying at the actual physical width. For every base at least two it gives bounded output digits, a positive leading output digit, the exact width `input length + actual terminal carry`, and the integer value equal to the input plus its reversal. The supplied reset flags are used for the comparison word only; `actualDigits` uses ordinary carrying. Neither a reset carry nor an artificial padded width is substituted for the actual terminal carry.

`reverse_add_defect_safety` derives the bounded symmetric pair-word hypotheses before applying the all-base carry-defect theorem. Its base restriction is at least three. The conclusion concerns the canonical **output**, whose integer value is also supplied, and does not assert that the input is nonpalindromic. An out-of-range defect index cannot create a spurious witness: both outgoing-carry lists have the same length and the same zero default. The explicit base-three control is correct: the palindromic input `212` has pair word `(4,2,4)` and output `1201`, with the stated reset/ordinary carry mismatch.

The positivity helper also checks: evaluation of the prefix is nonnegative, while the positive last digit contributes a positive multiple of a positive base power. This establishes a positive ordinary integer rather than allowing an empty or zero numeral.

## Source and build evidence

I read the complete new source, README, checker and report, together with the dependency definitions and theorem interfaces used by the bridge. The checker builds all six exact source modules in a fresh temporary directory, audits their declarations, rejects proof placeholders and unapproved axioms, and checks that the source files remain unchanged. The retained failed first attempt concerns elaboration of the addition expression in the elementary bound; the final proof exposes that expression without altering the hypotheses.

An independent byte and declaration check confirms:

- All six current source SHA-256 and Git blob hashes match the fresh verification report.
- All 82 theorem names extracted from those sources match the report and compile-log axiom records, including the fifteen new `ReverseAdd` declarations.
- The log and report agree exactly on each theorem's axioms; their union is `Classical.choice`, `Quot.sound`, and `propext`.
- The report records a successful fresh Lean 4.19.0 rebuild. The concrete odd-base control and `positive_terminal_append` need no axioms.

The resulting interface is an all-base one-step theorem for canonical digit lists and their integer values. It does not establish a persistent safe family, an infinite orbit certificate, a Lychrel witness, or a connection to the separate decimal orbit API beyond the explicit integer interpretation stated here.
