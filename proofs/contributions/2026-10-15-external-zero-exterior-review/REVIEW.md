# Source review of the three-zero exterior theorem

PASS, source and mathematical review only. The reviewed source is
`proofs/research/main_existence_attempt/continuation_pass/lean/zero_exterior/ZeroExterior.lean`
at external commit `60d4348349a80c513008df9263905e7955b4ce79`.

Root read all twelve theorems and three definitions. The local arithmetic
uses the two actual carry fronts, includes the overflow reflection shift,
and requires the observed four columns to lie inside the word. Symmetry
and positive exterior exclude width four when the last of those columns
is zero. The predecessor theorem therefore has the valid column bounds
needed in both overflow branches, including possible overlap.

The overflow branch is ruled out by the three zero emissions. Without
overflow, the same three predecessor zeros and zero high incoming carry
are forced, so the outside coefficient doubles exactly. Backward
induction preserves the whole zero history and width. Positivity of the
initial coefficient and its ceiling eighteen then imply 2^t <= 18,
hence t <= 4. The numeric theorem correctly transfers through canonical
width equality and digit-value injectivity, rather than assuming the
pair representation of an arbitrary numeric orbit state.

The fixed-outer-symbol corollary uses positivity to exclude a nonzero
return time. The explicit time-four witness begins at 10000000 and
continues the ordinary map even after an earlier palindrome; it is not
a palindrome-avoidance example. The two-zero counterexample retains
actual overflow and shows why the third zero cannot simply be omitted.

The source has no new assumptions asserting the desired orbit behavior.
This review does not repeat the external compiler/axiom audit and does
not claim a new fresh build. The conclusion concerns only the specified
three-zero exterior. It does not address (p,p,0) patterns or prove
termination or nontermination of 196.

Reviewed source SHA-256: `17fce6b3fc182963b929fa85f3740f7dcb5197620621aa7f3aa260ec77e7b690`.
Computed Git blob identity: `0bd8c18a82754f960eec38540cac787a9d3b90c0`.
