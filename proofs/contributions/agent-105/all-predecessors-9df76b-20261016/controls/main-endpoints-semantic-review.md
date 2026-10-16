# Non-author review of the complete predecessor-list endpoints

**PASS.** Reviewer: Agent105 / scope105 / 9df76b. The reviewed `Agent105Predecessors9df76b.lean` has SHA-256 `3bd4a139d26f81fc14547def29702970629693427fb947ff920854d6292a8d29`. No statement or proof modification is requested.

The executable definition concatenates `decodedFiber e W W` with `decodedFiber e W (W - 1)`. Under `Canonical Y e W`, `mem_predecessors Y e W n htarget` states exactly:

```lean
n ∈ predecessors e W ↔ 0 < n ∧ Lychrel196.step n = Y
```

Soundness follows from the exact ordinary-number membership theorem for either decoded fiber. For completeness, every positive integer obtains its own canonical digits and actual width from `canonical_exists`. The existing width theorem forces its reverse-add target width to be either that width or one larger. The proof therefore reaches one of the two enumerated branches without retaining a source-width restriction in the final statement.

`predecessors_nodup Y e W htarget` combines the unconditional duplicate freedom of each decoded fiber with disjointness of their actual numerical widths. A number in both branches would have `decimalWidth W` and `decimalWidth (W - 1)`. The imported width uniqueness theorem would force those widths equal, contradicting `W > 0`, supplied by the canonical target. The use of truncated natural subtraction is thus controlled at the exact boundary where it matters.

For a one-digit target, the second branch is width zero and is rejected by the underlying decoder. A target ending in zero remains supported: canonical target 10 has digits `[0,1]`, while its overflow-stripped low payload `[0]` need not itself be canonical. A source ending in zero also remains admissible; the 121 control includes 110.

I read the frozen WordFiber, DecodedFiber, and Agent101ProfileExtraction dependencies to confirm the composition: symmetric finite words are projected through the original half/optional-center representation, the existing numericFiber enumerator supplies ordinary integers, and a successful target decode gives the required length, symmetry, coefficient bounds, and exact `natValue`. The original Agent101ProfileExtraction SHA-256 is `fff6917b100aeec40e353abe4a3f8d27f6561d6859a1feeac9135c22cd8c836b`; its provenance commit begins `9bf1b2c3`.

This review concerns finite, positive, ordinary one-step predecessors of a canonical target. It does not assert anything about an infinite orbit of 196. No blocking semantic issue was found. Separate nonauthor reviews by runtime105 and structure105 are retained under `review/`.

The two small controls were authored by scope105, so this report does not label their authorship independent. Their actual kernel compilation is recorded separately. The new complete published-source fresh replay and module-origin audit are pending the parent's source checkpoint; neither an author's cached compile nor these targeted controls are substituted for that future gate.
