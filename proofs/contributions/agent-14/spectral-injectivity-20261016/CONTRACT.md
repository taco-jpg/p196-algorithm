# Exact spectral coordinate injectivity

## Source and mathematical scope

The source is `creative_global_spectral_notes.md`, retained under
`proofs/archive/source-trees/2eb05ef47671d6b1883e54fec9f6a4f8de9ed8f5/proofs/research/`.
Its Git blob is `cb1c355fa05916a770816a4d5ef680e54079cccb`.
The executable counterpart is `proofs/creative_global_spectral__8de5a77a944d0d04.py`,
blob `730acd722bf017b6bf1e51e5a0411169a7804da4`.
Both were read at main `5ff4f607535587d572fbc9e95ba9501d1fbe5fc5`.

For each fixed finite width, the integer spectral coordinate determines a
reciprocal coefficient word with coefficients in 0..18. The source's weights
are the literal second-order recurrences

```
T(0)=2, T(1)=20, T(k+2)=20*T(k+1)-T(k)
R(0)=1, R(1)=19, R(k+2)=20*R(k+1)-R(k).
```

At width `2*m+1`, the coordinate is
`q(m) + sum_(i<m) q(i)*T(m-i)`.
At width `2*m`, it is `sum_(i<m) q(i)*R(m-1-i)`.
The central odd weight is one. `T(0)=2` does not multiply the center.

## Exact Lean proposition

The endpoint `Agent14.Spectral.coordinate_injective` takes functions
`q r : Nat -> Nat` and a fixed `L : Nat`. Its only mathematical hypotheses are:

1. `q i <= 18` and `r i <= 18` for every `i < L`;
2. `q i = q (L-1-i)` and `r i = r (L-1-i)` for every `i < L`;
3. equality of the two literal source coordinates at width `L`.

Its conclusion is `forall i < L, q i = r i`. Values outside the width are
irrelevant. Natural coefficients represent exactly the source's nonnegative
integer alphabet. An optional explicit integer wrapper must preserve both
the lower and upper bounds.

The finite-sum helper is independently defined by ordinary addition. The
recurrences use natural subtraction; addition-form recurrence theorems prove
that subtraction never truncates. Neither domination nor the target
injectivity is a defining axiom or an added hypothesis of the final endpoint.

## Supporting proof obligations

- Derive positive weights and nineteenfold growth from the recurrences.
- Prove `18 * sum_(j<k) oddWeight(j) < oddWeight(k)`, where
  `oddWeight(0)=1` and `oddWeight(k)=T(k)` for `k>0`.
- Prove the analogous domination for `R`.
- Prove bounded finite weighted-sum injectivity, identify both formulas with
  those sums, and recover the other half using reflection.
- Reuse original `DecimalDigits.columnSum_bounded` and
  `columnSum_symmetric` for the ordinary decimal interface. A canonical
  representation is allowed in that corollary, but the general theorem
  retains bounded symmetric words with an odd central coefficient too.

## Boundary cases and exclusions

Width zero is an explicitly labeled algebraic extension, with empty equality
of words and coordinate zero. Width one has coordinate `q(0)`. Width two
also has coordinate `q(0)`, with reflection determining the other entry.
Leading-zero words are permitted relative to their stated width; their
polynomial need not have degree exactly `L-1`.

Equality of coordinates at different widths does not imply equal words.
Even at a fixed width the theorem recovers mirrored pair sums, not the
individual input digits: for example, 12 and 21 have the same pair word.
No absence-of-nine hypothesis, positive outer coefficient, or even central
coefficient is needed for the general theorem.

This claim does not include evaluation at the real number `10+sqrt(99)`, the
four spectral update laws, the carry-coordinate zero set, the spectral
palindrome criteria, the carry-defect ideal or its quotient cardinality, or
an infinite-orbit conclusion. Each remains a separate inventory entry.

## Ownership, attribution and acceptance

The published guarded claim is coordination commit
`82b9e59b5efa82fa463b9084da270ef646e39aeb`, task blob
`07b8587f411d2e3d47ec12e62cb77e41e2656547`. The two previous rejected or
uncertain ref attempts established no ownership. The parent read the new
task deltas before the successful non-force update and verified its bytes.

Agent14/coverage authors the weight module. Parent Agent14 authors the
finite encoding and decimal interface. Agent14/spectral_semantics authors
the independent semantic review and no proof source; Agent14/runtime authors
the independent runtime/build/audit evidence and no proof source. These are
genuine separate agents in the same session, not external peer reviewers.
All public inter-agent communication goes through issue61 by parent relay.

Acceptance requires actual Lean4.19.0 commit6caaee842e94 execution with
`--trust=0 -j1 -DElab.async=false`, no `sorry`, `admit`, new mathematical
axioms, or `native_decide`, a complete clean selected-source build, full
module-origin transitive axiom audit and independent semantic review. Only
`propext`, `Classical.choice`, and `Quot.sound` are permitted foundational
axioms. Source, attempts, commands, outcomes and substantive logs are retained.
