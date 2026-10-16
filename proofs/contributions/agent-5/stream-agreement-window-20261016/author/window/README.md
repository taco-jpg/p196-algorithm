# Agent #5 finite stream agreement window: author evidence

The frozen source is `../../StreamAgreementWindow.lean`, SHA256
`023c5c692fbdc66a67faba66eb2b3c76082f4b25def9a69b53e4a65527d59899`.
It exports seven theorems in `Agent5.OrdinaryStreamWindow`.

## Mathematical result

Let `n = B.length` and let `gamma` be the existing coordinate selector
`if 9 * 10 ^ n ≤ rhoNum c B then 1 else 0`. Under the original eight-phase,
coefficient-bound, and complementary-band shape hypotheses, the actual
ordinary output pair word agrees with the two literal coordinate streams
through length `n + 1 + q` whenever `q ≤ gap + gamma`.

The raw identity includes empty exterior and middle words and `gap = 0`.
It imposes no decimal-word or positive-last-digit premise. The ordinary
arithmetic wrapper adds those two premises and reuses the original three
`reverseAddDigits_correct` conclusions. The source also exports the
normalization-carry and coordinate-quotient variants.

The proof uses `surrounded_normalization` to expose both stable constant
bands. The low end permits `gap + 1` additional digits. The high end permits
`gap + gamma`, since the zero-carry branch consumes one stable digit in the
first complete exterior prefix. A list-prefix argument establishes the common
window. The original low and high literal-stream theorems and the published
carry selector/quotient interfaces then give the coordinate form. No carry or
ordinary-value arithmetic is reproved.

## Compilation record

All author compilations used Lean 4.19.0, commit `6caaee842e94`, with
`--trust=0 -j1 -DElab.async=false`. The private stage inherited 15 source and
object pairs from the published raw-prefix replay. Each source was compared
byte for byte with the corresponding current repository source; hashes and
paths are retained in `inherited-artifacts.json`. This author run did not
rebuild the dependency closure.

| Attempt | Scope | Result |
| --- | --- | --- |
| 001 | Three structural list-window exports | Failed: the simplifier expanded the constant band under `reverse` before applying `reverse_replicate`. The exact failed source and log are preserved. Its downstream `sorryAx` reports are elaboration-failure artifacts and are not accepted theorem evidence. |
| 002 | Same three exports, with only the desired output replicate rewritten | Passed, exit 0. |
| 003 | Final seven-export source | Passed, exit 0. |

The separate `audit/StreamAgreementWindowAxiomAudit.lean` imports the compiled
final module and runs `#check` and `#print axioms` for all seven named exports.
It passed, exit 0. The first two exports use `propext` and `Quot.sound`; the
other five use only `propext`, `Classical.choice`, and `Quot.sound`.
This audit covers the seven named exports; it is not a census of every
generated constant in the import closure.

Each attempt and the audit retain their exact command, environment path,
source hash, timestamps, exit code, and complete compiler output. The final
source contains no `sorry`, `admit`, `native_decide`, custom axiom, `unsafe`,
or `partial` declaration. `verification.json` records the final source and
object hashes and the completed checks. `artifact-index.json` hashes every
author evidence file except the index itself.

The sibling sharpness module and the independent review are separate work.
These author records do not claim to prove sharpness or to perform that review.
