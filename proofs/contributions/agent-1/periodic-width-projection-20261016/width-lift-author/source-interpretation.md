# Width-lift author source interpretation

Prepared while the required `Agent1PeriodicOuterCatalog` object was still unavailable. This is an author interpretation of the proposed source, not an independent review or a compilation claim. The final compilation status and source hash belong in the frozen receipt.

## Definitions and coordinate conventions

`WidthNode` is `OuterNode × Nat`. An outer node retains the indexed coefficient phase and the physical outside coefficient. The width coordinate is a natural-number residue, bounded by catalog membership rather than by a `Fin` type.

`widthProjection B H w` is exactly `((w, outside B w), widthResidue B H)`, where the imported `outside B w = (B ++ w).headD 0` handles an empty exterior, and the imported `widthResidue B H = (2*B.length + H.length) % 8`. No phase rotation is identified, and no reflected-phase indexing convention is added.

`widthCatalog` is the list product of the original `outerCatalog` with `List.range 8`. Each original `OuterEdge` yields eight `WidthEdge` records. The source residue is r, the target residue is `(r + e.clock) % 8`, and the exact original source, target, clock, and exceptional carry label are retained. The all-nine carry label remains an ordered pair.

## Claimed theorem boundaries

* `widthCatalog_length` and `widthEdges_length` establish list lengths 7,024 and 11,664 using the imported checked base lengths 878 and 1,458. They do not certify archived traversal order, reachability, SCCs, or an enumeration algorithm.
* `widthCatalog_nodup` proves that the node list has no duplicates, using imported base-node uniqueness and the distinct residues in `List.range 8`. Together with the length theorem this gives 7,024 distinct lifted nodes. No edge-list uniqueness theorem is asserted.
* `mem_widthCatalog_iff` states precisely that a lifted node is listed if and only if its base node is listed and its residue is below eight. This makes the Nat-coordinate restriction explicit.
* `liftOuterEdge_mem` takes a listed base edge and an input residue below eight. The target residue is computed by that edge's clock.
* `widthEdge_target_mem` follows from base target closure and the modulus bound. It claims target closure for every listed lifted edge; it does not claim that every abstract edge is physically realizable.
* `quotient_width_catalog_edge` assumes the unchanged full `ValidPeriodic B H w` and membership of the actual input projection. It returns one listed edge with source equal to that projection, clock equal to the actual `rawGamma B H w`, exact all-nine carry label, and target equal to the projection of `quotientOuter`, `quotientCenter`, and `rawPeriod`.
* `quotient_valid_in_widthCatalog` preserves both the unchanged full validity predicate and lifted membership. Validity is obtained from the existing `quotient_valid`; no weaker replacement predicate is introduced.

The local modulus theorem requires only bounded coefficients and period length four. The actual edge theorem deliberately uses full validity because the existing outer-edge bridge requires it. No new positivity, safety, or exponent assumption is silently substituted.

The state quotient is the original executable maximal quotient. Its full finite-word one-step interpretation remains governed by the existing `quotient_step_bounded` exponent guard `3 <= k`. The new source has no exponent parameter and makes no statement that this guard automatically persists. Likewise it does not construct an ordinary decimal realization of an arbitrary abstract path.

## Dependencies and proof method

Only `Agent1PeriodicOuterCatalog` and `Agent1PeriodicWidth` are directly imported. The substantive bridge composes `quotient_outer_catalog_edge` with `quotient_widthResidue`; both use the same original `rawGamma`. Thus the residue increment is not a freely selected graph clock.

The finite sizes are obtained by list-length algebra, not by rerunning a graph search or evaluating the entire lifted graph in a large closed decision. The membership and target proofs destruct the list-product witnesses. A separate small generic list-support check passed under strict Lean checking; it was explicitly not a substitute for compilation of this module with its real imports.

The final author check must compile the exact source with the valid dependency objects, print axioms for all eight public theorems, and audit every constant originating in the new module, including structure/derived declarations and the private length helper. Dependency object reuse must remain explicit. Fresh combined closure checking is a separate parent/reviewer responsibility.
