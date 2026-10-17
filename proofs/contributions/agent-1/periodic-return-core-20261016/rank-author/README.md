# Local outer component and rank certificate

Frozen source: `proofs/Agent1PeriodicOuterRank.lean`, SHA256
`e345ef2c5fe7734f64ead7e971f0ea8b807dfcc2d84e3d50625109871fe10477`.
Author: Agent1 specialist `/root/research_status/numeric_bridge_review`.
The module imports only the unchanged `Agent1PeriodicOuterCatalog`.

## Exact public interface

All declarations are in namespace `Agent1.Periodic`:

* `outerComponent : OuterNode → Nat` uses the original stored partition
  indices on catalog nodes. Three constant phases have labels 131, 129,
  and 130; 128 singleton overrides retain their exact original labels;
  the default is 8. Outside catalog membership this is just a total
  function extension, not an SCC interpretation.
* `componentRank c := 132 - min c 131` agrees with reversed stored index
  `132-c` on all original labels and is positive on every natural input.
* `componentRank_pos c` proves that positivity.
* `outerEdge_rank_le e he` proves weak rank decrease on every listed edge.
* `outerEdge_rank_drop e he hne` proves
  `1 + componentRank (outerComponent e.target) ≤
   componentRank (outerComponent e.source)` when the two labels differ.
* `outerEdge_internal_component e he heq` proves that the source label of
  every listed internal edge belongs to `[8,129,130,131]`.
* `outerComponent_zero_phase s hs hc` proves `s.1 = [0,0,0,0]` for a catalog
  member with label 131.
* `outerComponent_initial_core s hs hphase hc` proves `s.2 = 9 ∨ s.2 = 10`
  for a catalog member whose phase is `[14,14,4,4]` and label belongs to
  `[8,129,130]`.

The exact elaborated types and public axiom prints are retained in
`audit-001/lean.log`. These are local certificate facts only. The module
asserts no SCC maximality, reachability, return existence, path realization,
zero-component exclusion from general paths, safety, or ordinary numeric
orbit. Downstream closed-path reasoning remains separate and can reuse
the existing `CondensationBound` soundness.

## Data and proof structure

The preserved `outer_filtered_graph.json.gz` has compressed SHA256
`c3eb0a4bd4bc8e390d7681746e66300851035dff1b102412e2d14977ed1088e5`
and decoded SHA256
`cbd5c62ac2af58d0d0ce1cbb6f0cf9199ac49c75291d062179caf15f96e1ad50`.
`generate.py` reads that exact partition without recomputing SCCs. Its
finite diagnostic checks all 878 stored memberships against the emitted
piecewise function. The stored 1458 edges split into 310 strict label
increases and 1148 internal edges: 1040 at label 8, 54 at 129, 27 at 130,
and 27 at 131. These Python findings are explicitly finite diagnostics.

The actual Lean graph checks use literal node and edge blocks copied from
the original catalog source, SHA256
`1e6ebcc4e47df94162467d52826cee4e64c5707a622ac775008671d3fb0391e2`.
There are 59 separately proved node checks and 59 separately proved edge
checks. Structural list assembly combines them; two `rfl` theorems identify
the flattened certificate blocks with the actual original `outerCatalog`
and `outerEdges`. Thus the exported local facts concern those exact lists,
including their clock and exceptional carry labels. No original graph
source, ordering, visibility, or labels were changed.

## Actual verification and scope

Official Lean 4.19.0, commit `6caaee842e94`, was run with
`--trust=0 -j1 -DElab.async=false`, a 1500 MiB RSS stop threshold sampled
every 10 ms, a 600-second timeout, and no virtual-address cap.

| Invocation | Result | Seconds | Kernel peak RSS (KiB) |
| --- | --- | ---: | ---: |
| `probe-001`, original phases 00 and 04 | PASS | 1.32 | 497444 |
| `attempt-001`, complete new module | PASS | 17.98 | 700020 |
| `audit-001`, complete new-module origin audit | PASS | 1.66 | 782376 |

No Lean failures occurred and no watchdog fired. The author check reused
the exact 25-module dependency objects from the supplied successful parent
fresh Outer build. Every dependency source matches its registry SHA256,
Git blob, literal imports, working source, and successful build report;
object SHA256 pins are recorded and rechecked. This is an **author
increment**, not a new complete dependency rebuild. `run.py` retains every
invocation in a new labelled directory with source snapshots, exact
commands, dependency pins, logs, and receipts.

The full audit covers all **133 theorem constants, 136 safe definitions,
and 0 safe opaque constants** originating in the new module. It prints the
literal types and axioms of all eight public declarations, rejects custom
safe axioms, and checks transitive logical axiom dependencies against the
standard three. The actual union is only `propext` and `Quot.sound`.
There are zero unsafe implementation axioms, zero partial definitions, and
zero unsafe opaques. The audit separately inventories 5261 generated
unsafe compiler implementation definitions for literal data, matchers, and
code stages; none expands the audited logical axiom union.

`audit-001/origin-summary.json` checks audit inventory counts and export
coverage. The source is frozen with no remaining local proof obligation.
Parent integration, independent combined source compilation, and final
publication remain separate gates. This helper made no Git or external
service writes and changed only its owned module and evidence directory.
