# Agent #314 — ordinary-exterior bridge audit

Date: 2026-10-15
Task: M99-C314

## Finding

The repository contains a Lean theorem named
`P196.Agent6.ordinary_reverse_add_exterior`, but it does **not** establish
the ordinary-arithmetic bridge from an arbitrary ordinary reverse-and-add
state to the exterior construction.

Its critical hypothesis is:

`hshape : paired D = surrounded B c g W`.

The theorem then proves the arithmetic reverse-and-add semantics and applies
`actual_exterior_projection`. Thus the theorem is a conditional bridge:
**if** an ordinary mirrored pair word already has the exact `surrounded`
shape, **then** its normalized reverse-add output projects to the abstract
exterior transition.

This is materially different from proving that an arbitrary ordinary
trajectory satisfying the 6/12 alternating boundary hypotheses admits such a
`surrounded` decomposition.

## Exact counterexample to an overbroad representation claim

If one were to strengthen the bridge to "every ordinary input has a
`surrounded` representation", that statement is false by length alone.

Take the one-digit ordinary seed D = [1]. Then
`paired D = [2]`, hence its length is 1.

For every choice of B, W, c, g with the repository's definitions,
`surrounded B c g W` contains two copies of
`List.replicate (g+2) c`. Since g is a Nat, each such block has length at
least 2, so the surrounded word has length at least 4 (before accounting for
B, W, and B.reverse). It therefore cannot equal [2].

So the missing hypothesis cannot be silently promoted to a universal
ordinary-arithmetic fact.

## Relation to the 6/12 obstruction

`Agent9.AlternatingScalarBoundary.no_six_boundary` and
`no_twelve_boundary` are genuine all-width obstructions in their stated
abstract N/O Tile model. The file itself explicitly says that the connection
to an actual exterior is a separate bridge obligation.

Therefore the current rigorous status is:

1. The 6/12 scalar boundary is excluded in the abstract Tile model.
2. The exterior projection from an explicitly surrounded ordinary mirrored
   pair word is formally established.
3. The missing step is an ordinary-arithmetic realization theorem showing
   that the actual class of exterior states under consideration necessarily
   arises from such a surrounded mirrored pair word (or an equivalent
   representation).
4. The existing `ordinary_reverse_add_exterior` theorem does not supply
   that universal realization because `hshape` is an input assumption.

This is an exact identification of the bridge gap, not a proof of the main
196 conjecture.

## Source evidence

- `proofs/ExteriorArithmetic__3a0c5b42aa9a8043.lean`
- `proofs/ExteriorProjection__ff01957395979f49.lean`
- `proofs/ExteriorBridge__c63f5f7808ff21df.lean`
- `proofs/AlternatingScalarBoundary__83444ad98ef51706.lean`
- `proofs/CONSOLIDATION.md`

The current consolidation document independently records that ordinary-
arithmetic exterior bridges remain open.

## Verification status

This audit was performed by direct source inspection through the repository
API. No local Lean execution was available in this run, so this note is not
a LEAN-CHECKED artifact. The length counterexample is an elementary semantic
observation and is presented as an audit finding, not as a compiled theorem.

## Next task

Investigate the strongest nontrivial replacement for `hshape`: characterize
exactly which ordinary mirrored pair words can enter the exterior state space,
and determine whether the 6/12 boundary hypotheses themselves imply the
required representation.