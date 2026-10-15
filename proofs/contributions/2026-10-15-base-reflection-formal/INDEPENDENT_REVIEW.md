# Independent mathematical and scope review

**PASS** for the 15-theorem `BaseReflection.lean` checkpoint with SHA-256
`719deff95d949dd14d337d7a6fe2ff04fe268a7119fd3caf84c993153ff1db4c`,
using the nine-theorem `SignedDigitUniqueness.lean` prerequisite with SHA-256
`2fcf33f52edfe006426ff521cca2a853e9c6180ffe8765fd6ec54622a1c75c64`.
This review reads both complete sources and the package's exact scope; the
producer's fresh 24-theorem compilation and axiom audit are recorded in its
`verification.json`. This independent review does not claim a second
compilation of that checkpoint.

The low-first raw list has exactly one more coefficient than the original
list. Its initial incoming carry and terminal outgoing carry are both
included. The ordinary-evaluation identity telescopes correctly, and the
reversed-evaluation identity has the required factor `1-b*b`. The source
proves the connection between reversed evaluation and list reversal; this
connection is not an extra symmetry premise.

For the `L+1` symmetry branch, comparing the two evaluations gives a factor
`b-1`, whose cancellation is justified by the explicit `b != 1` assumption.
The residual list is `q_i-(b+1)c_i`. `ColumnConditions` supplies its bounds
`[-2,b-1]` through the normalized local equation, rather than postulating
residual vanishing or the desired coefficient classification. At `b>=3`,
the signed uniqueness prerequisite applies also after reversal, giving
`q_i=(b+1)c_i`. Binary carries then give the claimed `{0,b+1}` classification.

For the `L` symmetry branch, `raw = e ++ [0]` explicitly removes the terminal
slot before reflection. `raw_length` forces `e` to have length `L`, so there
is no hidden free width. The evaluation identities imply
`(1-b*b)*high(C)=0`; `b>=3` makes the scalar nonzero. Carry coefficients
are binary and satisfy the signed uniqueness bounds, hence every carry is
zero. The local digit equation gives `q_i<=b-1`, and a separate list identity
then gives `e=Q`.

Empty lists and padded zeros cause no exception: the algebraic identities
include them, and the branch conclusions become vacuous or exact empty-list
identities as appropriate. Positive exterior coefficients and odd-center
parity are unnecessary for these algebraic implications. They belong to a
later canonical integer realization.

The important interface distinction is explicit and sound.
`ColumnConditions` existentially chooses an incoming bit for each pair;
it imposes no continuity or reset relation between adjacent pairs. It is
therefore an overapproximation of realized isolated normalizations. Proving
the implications under this broader condition is valid, but does not yet
construct a finite partition, prove that its raw placed sum is this list,
or select the correct width from an actual normalization. In particular,
the theorem named `overflow_classification` proves the padded-width
algebraic branch without itself asserting an actual final overflow.

The README and recorded audit scope correctly leave the partition interface,
ordinary normalization comparison, and reverse implication for separate
work. This checkpoint alone is not the full arbitrary-block equivalence,
an active-seam theorem, or an invariant infinite-orbit theorem. Subsequent
modules, including any `ResetNormalization.lean` checkpoint, require their
own review; they are not included in this verdict.
