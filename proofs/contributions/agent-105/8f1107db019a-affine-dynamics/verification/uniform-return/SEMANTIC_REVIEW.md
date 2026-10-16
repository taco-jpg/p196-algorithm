# Semantic and quantifier review of the actual uniform-safe-return theorem

Reviewer: `/root/ownership_audit`, session `agent105-8f1107db019a`.
The reviewer authored the reused TailSelection component. The Normalize, Zip,
Orbit, Shape, Stability, ReturnTimeBound and UniformReturn sources were authored
by the other identified team members. This review's independent mathematical
assessment concerns those sources and their composition; it does not label the
reviewer's own TailSelection author work as an independent review.

## Exact reviewed statement

The frozen root is `proofs/Agent105UniformReturn.lean`, SHA-256
`fba98eb095ca439835e82a90315254090ed03935c3d17d9e6ae8ebe5bb7b7fa7`.
All imported source identities are recorded in `source-pins.json` and the
registry snapshot. The statement retains these substantive assumptions:

- A fixed finite `Agent102.RunSpec` list with each literal symbol at most 18.
- Positive eventual width slope `widthSlope rs` and positive natural shift `s`.
- Eventual original `Agent8.CanonicalPair` for the actual expanded word.
- At every sufficiently large parameter, existence of some positive return
  time, with actual `Agent8.orbit` equality to the shifted word and safety of
  every positive output through that time.

The conclusion quantifies one `t` before all sufficiently large parameters:

```text
exists t, 1 <= t and t <= 4 * widthSlope rs * s and
  exists K, for every k >= K,
    orbit (wordAt rs k) t = wordAt rs (k+s) and SafeThrough (wordAt rs k) t.
```

The selected time is independent of `k`; its final cutoff can depend on that
selected time. Eventual canonicality and eventual return existence may begin
at different thresholds. The proof explicitly combines their thresholds with
the eventual shape threshold. It does not assume canonicality at parameter
zero or at every earlier parameter.

## Safety and time indexing

`outputWord w i` is the original `normalize (orbit w (i - 1)) 0`.
`SafeThrough w t` ranges over exactly `1 <= i <= t`, including the endpoint.
The natural subtraction at `i = 0` has no effect on this safety predicate,
because time zero is excluded from its quantifier. At positive time one the
checked word is `normalize w 0`, as required.

The tested palindrome is that of the actual normalized output digits. It is
not a test of `orbit w i` itself: the latter is a symmetric pair word when
canonical. This distinction prevents the safety premise from accidentally
asking for a canonical pair word to be nonsymmetric.

## Derivation of the common finite bound

The Shape module provides one cutoff for a fixed actual head and for the exact
natural-number width increment `widthSlope rs * s`. The same width cutoff works
for every nonnegative `s`; the target head is valid because `k+s >= k`.
`widthSlope` equals the sum of the positive parts of the original slopes, and
its cast equals the original integer slope sum when all original slopes are
nonnegative. Negative intercepts remain integer intercepts and are not
silently replaced by natural-number initial widths.

For each sufficiently large `k`, the proof takes the return time supplied by
the hypothesis. Original Agent8 actual-path potentials and exact width give
`1 <= t <= 4 * widthSlope rs * s`. Equal endpoint heads cancel the potential
terms. The positive-time hypothesis is explicitly used; it is not inferred
merely from a return equation. This constructs the bounded cover from the
unbounded variable-time premise.

## Actual closure and eventual stability

The Normalize module uses unchanged Agent1 repeated-block identities on
constant runs. Empty runs retain the incoming carry. A nonempty run retains
its actual first digit and an affine-length remainder. Symbol nine retains
its incoming-carry dependence. The exact appended terminal carry is kept.
Original Agent102 affine comparison stability proves that each signed affine
run length is eventually zero or positive; this is discharged in the final
normalization endpoints.

The Zip module uses the original truncating `Agent8.zipAdd`. Structural
induction decreases the total number of run entries even for zero-length runs.
The two scalar premises in its helper are discharged by original Agent102
positive-part and comparison theorems. The residual length subtracts the
eventually nonnegative affine representatives, preserving the original
`Int.toNat` truncation order. The final zip endpoint has no closure premise.

Orbit composes these actual results: normalization yields symbols at most 9;
pairing with the reversed actual word yields at most 18. Natural-number
induction gives an affine-run representation for each fixed orbit time. The
representation and cutoff may depend on that fixed time. No theorem exchanges
this with a cutoff that works simultaneously for all unbounded times.

Stability transfers Agent102's literal-word equality and palindrome theorems
through eventual equality of actual words and their run representations. Its
`tailStable_of_eventual_iff` lemma correctly relocates the anchor to a maximum
cutoff. Fixed-time actual return equality and each fixed positive output's
safety therefore have stable truth values on a tail.

Only after deriving the finite bound does the proof combine the finitely many
candidate return times and output-safety predicates. The finite selector then
supplies one actual return time with every required safety condition on a
common tail. No target conclusion, arithmetic closure, equality dichotomy,
stable predicate, or bounded-cover conclusion is left as a hidden assumption
of `uniform_safe_return_wordAt`.

## Interpretation and verification status

The semantic and quantifier assessment is **PASS for the exact list-domain
statement**. Original `CanonicalPair` alone does not guarantee ordinary-integer
realizability; the independent time-bound review exhibits that boundary. This
root neither constructs a variable-time return family nor asserts a result
about the number 196. Plain returns without the safety premise and integer
interpretation are handled by separately named subsequent modules.

The canonical execution result is recorded separately in its unchanged report
and the final execution receipt. This semantic review is not a substitute for
a completed fresh-source compile or the exhaustive module-origin axiom audit.
The earlier Normalize-only attempt that was terminated with signal 9 is retained
as a failed attempt; its partial dependency build is not a successful check of
this root.
