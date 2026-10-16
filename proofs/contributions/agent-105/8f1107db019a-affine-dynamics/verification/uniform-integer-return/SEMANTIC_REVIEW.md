# Independent review of plain and ordinary-integer return endpoints

Reviewer: `/root/ownership_audit`, session `agent105-8f1107db019a`.
The Plain source was authored by `/root/source_scout`, IntegerSafety by
`/root/lean_runtime`, and UniformIntegerReturn by `/root`. The reviewer made no
changes to any of these mathematical sources.

**PASS for the exact declared statements.** Their kernel and module-origin
checks are recorded in the execution report separately from this source review.

## Plain return clause

`Agent105UniformReturnPlain` supplies the two plain-return theorems separately
from the safe-return strengthening. Neither plain theorem assumes that outputs
avoid palindromes. `uniform_bounded_return` applies the finite selector to actual
return equality. `uniform_return_wordAt` derives its finite cover using eventual
canonicality, the exact eventual common head and width increment, and the
original actual return-time bound. The selected positive time is outside the
final parameter quantifier and is bounded by `4 * widthSlope rs * s`.

This preserves the scope of the written plain-return clause even in a family
whose returns contain palindromic outputs. The original safe-return endpoint
and its previously checked source remain unchanged.

## Integer palindrome equivalence

`Agent105IntegerSafety` exposes the existing local equivalence from the original
Compat development using the original `Lychrel196` orbit and palindrome
constants. The successor-time theorem is the existing compatibility chain
through `Agent109.step_palindrome_iff`. For arbitrary positive time `i`, the
proof uses `i - 1 + 1 = i`, with `1 <= i` explicit. Time zero is not silently
included. No assumption `n != 0` is needed for this equivalence.

The representation premise is exactly `Agent109.pairWord n = w`; the proof
substitutes that known representation in the correct direction. Its negated
version applies logical negation to the established equivalence, retaining all
representation and positive-time assumptions. It checks the normalized output
word, not a symmetric pair word.

## Integer uniform-return quantifiers and realizability

For each sufficiently large `k`, each integer theorem's hypothesis supplies
some `n != 0` and some positive `t`, a genuine pair-word realization of
`wordAt rs k`, and a return of the pair word of the original integer orbit to
`wordAt rs (k+s)`. The safe theorem additionally requires every original integer
output at times `1 <= i <= t` to be nonpalindromic. Neither hypothesis assumes
that the witness time is uniform.

Positive realizability is used explicitly to derive original CanonicalPair via
`Agent109.Endpoints.pairWord_canonical`. Original Compat semiconjugacy transfers
the integer pair-word return to the exact Agent8 return needed by the proved
plain or safe uniform theorem. The final cutoff is the maximum of the original
realization cutoff and the uniform-return cutoff.

The conclusion retains both of the following for every parameter on that tail:

1. Existence of a positive ordinary integer realizing the family member.
2. For every ordinary integer with that same pair word, the single selected
   positive time produces the required pair-word return. In the safe theorem,
   every positive output through that time is nonpalindromic according to the
   original `Lychrel196.Palindrome` predicate.

The universal realization clause therefore is not left vacuous. A return
time obtained from one original witness applies to every other realization
because the pair-word dynamics and positive-time palindrome equivalence depend
only on that pair word. The conclusion is deliberately a pair-word return.
No injectivity of `pairWord` is used, and the theorem does not claim that an
integer orbit equals an arbitrary chosen representative of the shifted family.

## Scope retained

Theorems still assume actual variable-time returns, positive family growth and
a positive parameter shift. They do not provide those hypotheses for 196 or
construct an unconditional family of nonpalindromic returns. The positive-time
safety range includes its endpoint and makes no assertion about the initial
integer at time zero. All signed affine intercepts and the finite initial
parameter exceptions permitted by the list theorem remain available.
