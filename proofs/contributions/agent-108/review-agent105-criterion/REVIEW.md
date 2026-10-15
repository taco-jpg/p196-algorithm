# Agent #108 independent statement and proof review

Reviewer: **Agent #108**, not an author of the reviewed Agent #105 modules.
Reviewed source commit: `4c8ae8abd2421af3e95ef6c6c07d4e69c0aa0519`.
Claim: `agent108-review-agent105-criterion`, published at
`775c0d474e347704a8442a391335d96c1962e55f`.

Verdict: **PASS — INDEPENDENTLY-REVIEWED** for `LocalHigh.lean`,
`ReturnCriterion.lean`, and `ReturnSafety.lean` at the pinned source identities.
No mathematical correction or source change is requested. This is a completed
independent execution and statement review, not external human peer review.

## Actual execution and dependencies

`runs/independent-local-20261015T051346Z-eb6de63e/manifest.json` records the new
empty build directory, exact source SHA-256 values, original command vectors,
every exit code and full log. All eleven source modules, including the eight
repository prerequisites, were copied from the pinned source and recompiled;
no pre-existing project olean was supplied. Source and official toolchain hashes
were unchanged across the run. All compilation and audit commands exited 0.

The independent audit obtains theorem names from actual Lean environment module
ownership rather than trusting the author's manually enumerated list. It checks
1309 local theorem constants, including private and generated auxiliaries, and
runs actual `#print axioms` for all 1258 exported theorem constants. The three
reviewed modules contain 14 explicit source theorems and 41 exported constants;
1217 further exports belong to their prerequisites. These numbers state audit
coverage, not mathematical novelty or result counts.

Every transitive axiom set is contained in `propext`, `Classical.choice`, and
`Quot.sound`. No `sorryAx`, custom logical axiom, `Lean.ofReduceBool`, or compiler
trust axiom occurs in those closures. Unsafe compiler-generated data-function
declarations are recorded separately and cannot occur in an allowed theorem's
axiom set. The source uses kernel-checkable `decide` for finite controls; it does
not import a `native_decide` proof into this accepted chain.

The local run uses Agent #108's disclosed readlink compatibility adapter for the
container's mismatched PID/proc namespace. Original Lean binary/library/olean
bytes are unchanged; exact adapter and tool hashes are in the manifest. The
adapter-free hosted reproduction passed in
[run 38685837436](https://github.com/taco-jpg/p196-algorithm/actions/runs/38685837436).
`HOSTED_VERIFICATION.json` records its exact identities; all downloaded source,
command, exit and axiom reports are retained. This separately confirmed official
run rebuilt all eleven sources from zero old project oleans with no LD_PRELOAD.
The local execution is not represented as adapter-free.

`InspectStatements.lean` and `statement-types.log` retain the actual checked
definitions and endpoint types printed from the rebuilt environment. That command
exited 0 with `LEAN_PATH` set to the same fresh source/build directory.

## Statement-by-statement scope

All three modules use the repository's ordinary decimal arithmetic: `reverse10`
is `reverseFuel n n 0`, `step n = n + reverse10 n`, and `Palindrome n` means
`reverse10 n = n`. `Canonical n d L` requires positive width, digits at most nine,
a nonzero leading digit and value equal to the actual integer n. There is no
alternative symbolic notion of palindrome in the numeric endpoints.

`HighCarryWord q L` means every in-range coefficient is in 9..18 and the exterior
is at least ten. `Admissible` supplies positive width, symmetry, boundedness and
even central coefficient. The numeric theorem derives this from the represented
canonical input; it does not ask the consumer to supply a future realizability
hypothesis. `NumericHigh` is defined using a canonical representation; its width
and column uniqueness lemmas and `iterPairs_representation` identify it with the
actual changing-width integer orbit.

| Reviewed declaration(s) | Interpretation checked |
|---|---|
| `LocalHigh.actualCarrySum_le_two` | Both summands are actual incoming carries at reflected positions, each bounded by one. |
| `LocalHigh.nextColumns_formula` | Under actual no-overflow, reflection is at width M; the three coefficient branches give the claimed exact formula. Natural subtraction in the high branch is nontruncated. |
| `LocalHigh.nextColumns_high_iff` | The allowed coefficient set and the special carry conditions at 4, 14 and 9 are exactly equivalent to a next coefficient in 9..18. The required bound on the carry sum is derived, not omitted. |
| `ReturnCriterion.second_outer_formula`, `second_outer_high_iff` | The actual exterior is `2*(q 0-9)+carry P L`; exterior at least ten is equivalent to source exterior at least fourteen. |
| `ReturnCriterion.high_return_outer_ge_fourteen` | A genuinely returning trajectory supplies second nonoverflow, then the necessary exterior threshold. |
| `ReturnCriterion.high_return_iff` | The complete equivalence uses the actual first successor P, its actual carries, and width L+1. The converse assumes neither target-highness nor a graph edge. |
| `ReturnCriterion.numeric_high_return_iff` | Transfers the equivalence to the same ordinary input n after exactly two steps using the formal representation bridge. |
| `ReturnSafety.numeric_first_palindrome_iff_all_eleven` | The general step-palindrome classification reduces to the all-eleven pair word under the high input hypothesis. |
| `ReturnSafety.numeric_second_safe_iff_large_adjacent` | Negates the existing exact numeric second-palindrome adjacency criterion; the witness has `0 < i < L` and adjacent sum at least 28. |
| `ReturnSafety.numeric_first_safe_of_large_adjacent` | The same adjacency witness contradicts the only possible first-output palindrome class. |
| `ReturnSafety.numeric_two_outputs_safe_iff_large_adjacent` | The conjunction concerns exactly T(n) and T²(n); it needs no high-return premise. |
| `ReturnSafety.large_adjacent_iff_next_pair_large`, `numeric_two_outputs_safe_iff_next_pair_large` | The adjacency witness is equivalent to an in-range coefficient at least ten in the actual first successor, with its actual next width. |

Namespace prefixes in this table are under `Agent105`.

## Adversarial checks and boundaries

The necessity direction may use target-highness to prove nonoverflow; the
sufficiency direction reconstructs the target from explicit source conditions.
This is not a circular assumption. Carry sums are functions of P, not freely
chosen control bits. The only parity premise is the ordinary admissibility of
the source word, supplied automatically for canonical inputs.

Positive widths one and two and overlapping reflected positions are included.
The local proof requires an in-range index, not distinct reflected indices. The
exterior formula only requires positive width. The adjacency interval is empty
at width one, exactly as in the imported second-output palindrome theorem; no
unjustified large-width restriction is hidden in the numeric endpoint.

Returning to the high region and avoiding a palindrome are separate properties.
The safety theorem asserts only the first two positive outputs and says nothing
about the starting integer or later iterates. The manuscript's additional
nearest-non-nine, carry-free language reformulation is not formalized by these
three modules and is not upgraded by this review. There is no new claim of a
permanent return mechanism, freely realizable graph paths, infinite safety,
decimal Lychrel existence, or resolution of 196.

The author supplied extensive finite controls. This reviewer did not rerun that
separate exhaustive experiment and does not count it as independent execution.
The verdict rests on the actual source-clean kernel builds, full dependency audit
and the exact-statement review above.

## Acceptance handoff

The core source had already entered main through PR #15, while the coordination
record still correctly marked the second package's independent review pending.
This review supplies that missing gate for the pinned bytes. The integration
owner can cite this report after confirming source identities; this reviewer
does not modify Agent #105's files, shared acceptance indexes, or main.
