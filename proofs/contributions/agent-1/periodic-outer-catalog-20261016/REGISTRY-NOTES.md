# Scoped outer-catalog registry and interfaces

`proofs/Agent1PeriodicOuterCatalog.registry.json` describes the exact **25-module** import closure of `Agent1PeriodicOuterCatalog`, with SHA-256, Git blob, and literal imports for every source. It preserves all twenty frozen Phase-registry modules and adds `Agent1PeriodicSafetyAlphabet`, `Agent1PeriodicOuter`, `Agent1PeriodicOuterChoices`, `Agent1PeriodicCatalogOrder`, and `Agent1PeriodicOuterCatalog`. All eighteen public theorems of the four new modules are registered as endpoints. The Catalog root imports `Agent1PeriodicOuter` and `Agent1PeriodicCatalogOrder`; the order helper imports `Agent1PeriodicOuterChoices`.

**Provisional:** the Catalog root strict compile attempt-004 was active when these pins were prepared. All twenty-five source files match checkpoint `d6d2f6dc08a1fc43ea83d21f4f7f5fea51a0984d`, and the root matches the attempt-004 source snapshot. This registry is a source inventory, not a compilation receipt or accepted global catalogue. Root must confirm the actual final compile and refresh any changed source pin before marking completion. No Lean source or global accepted registry was edited for this assembly.

Current Catalog pin: SHA-256 `cb3be00b81a1d2281c7968a9fd0c027fd5b0f1a30ef067e059e1d15be4f1c75a`, Git blob `424e0ac0b14cbbbf4dc679699471073c271e1488`. CatalogOrder pin: SHA-256 `0f59e74ecb35b9bb648150319beb3de9f7965c6a1aea7171e67a40f4bcb199c7`, Git blob `bcaddd73d8187dbeb74741558c6566f9068a12e5`. Updated registry SHA-256: `f85ef02a01c5fa617f0c264c30fdbda957a48a8cd185a3f8118ae348ebb29a7b`.

Historical preparation, preserved for provenance: the previous 24-module registry had SHA-256 `cf6bc473526dde6728ded1c6c5ed7beef34b86f6b8c99827dc44c9849d9f9970`, with Catalog SHA-256 `6fdd1a6850553ecd56fe4663be3f9f9541e5315a1f3b489c4c9fa782b4c017d4` and Git blob `b258ea23af5a96826d6f3896f67b4e0694feead6`. It remains recoverable from the parent-published checkpoint history; it is not the current source pin.

## Exact arithmetic and enumeration APIs

All interfaces below are in namespace `Agent1.Periodic`; `Word` and the unchanged arithmetic are `Agent8` definitions.

```lean
def outside (B w : Word) : Nat := (B ++ w).headD 0

theorem outside_bounds (B H w : Word) (hv : ValidPeriodic B H w) :
  0 < outside B w ∧ outside B w ≤ 18

theorem quotient_outside_step (B H w : Word) (hv : ValidPeriodic B H w) :
  let e := Agent8.lastInput (periodicWord B H w 3)
  e ≤ 1 ∧ rawGamma B H w = Agent8.overflow (outside B w) e ∧
    outside (quotientOuter B H w) (rawPeriod B H w) =
      Agent8.nextExterior (outside B w) e
```

The actual outside coefficient remains correct when the stored exterior is empty or completely stripped. The inner carry and overflow clock come from the original whole word; neither is chosen freely.

`OuterNode` abbreviates `Word × Nat`. `OuterEdge` stores `source`, `clock`, optional all-nine `carries : Option (Nat × Nat)`, and `target`. `outerImages q g` enumerates the two incoming bits compatible with clock `g`, maps them through original `nextExterior`, and removes duplicate outer targets. `outerOutputs s` combines these with the existing source-matching labelled phase edges, preserving distinct all-nine carry labels.

```lean
theorem mem_outerImages_of_actual (q e : Nat) (he : e ≤ 1) :
  Agent8.nextExterior q e ∈ outerImages q (Agent8.overflow q e)

theorem outerOutputs_mem_of_phaseEdge (s : OuterNode) (e : PhaseEdge)
    (he : e ∈ phaseEdges) (hsource : e.source = s.1) (q' : Nat)
    (hq : q' ∈ outerImages s.2 e.clock) :
  (⟨s, e.clock, e.carries, (e.target, q')⟩ : OuterEdge) ∈ outerOutputs s
```

CatalogOrder adds the three actual public theorem names `strictNatKeys_pairwise`, `nodup_of_strictNatKeys`, and `outerCatalog_nodup_of_checked`. Its adjacent-key checker proves pairwise strict order, which implies source-node distinctness without assuming key injectivity. This helper does not change the literal catalog or edge ordering.

The Catalog root assembles these interfaces into `quotient_outer_catalog_edge` and `quotient_valid_in_outerCatalog`, using the retained 878 states and 1,458 labelled edges. The certificate targets exact output specification, counts, state distinctness, initial membership, and target closure. It does not prove all listed states reachable, arbitrary abstract paths realizable, an interface return, safety preservation, or an infinite ordinary orbit.

## Verification status and handoff

Static assembly checked the full import DFS for missing modules and cycles, the exact 25-module closure, all twenty inherited source/import/blob pins, the eighteen endpoint names, exact checkpoint bytes, and a second read of every source to detect concurrent changes. These checks passed; no Lean execution was performed for registry assembly. The global accepted registry remains unchanged at SHA-256 `241a659b1e77ac1c17fb404c6dccaa8e0f03ebc322efd1f4553b2b8be646cebd` in both worktrees.

Outer author evidence is in `outer-author/RESULT.md`: its first strict compile and complete new-module audit passed using eighteen previously checked dependency objects. Choices evidence is in `choices-author/README.md` and `choices-author/frozen-receipt.json`. CatalogOrder's strict author compile is documented in `catalog-order-author/README.md`. Their author increments are not independent clean rebuilds. The root Catalog compile and later combined fresh source build, literal public axiom prints, full module-origin audit, independent semantics/data review, and publication are separate gates. No pending outcome is claimed by this provisional registry.

## Provisional width registry handoff

The separate width worktree now has `proofs/Agent1PeriodicWidthLift.registry.json`, SHA-256 `c58939e3dae1fe6295055364162cf5fdf23009f55fafc381956333b6157b595a`. Its two roots are `Agent1PeriodicWidthLift` and `Agent1PeriodicWidthPath`, and its exact DFS closure contains **28 modules**: the same twenty-five outer modules plus Width, WidthLift, and WidthPath. Thirteen named public theorems are registered: four width-residue results, seven proposed lift results, and two finite-path accounting results. Both roots are necessary because WidthLift does not import WidthPath.

All outer pins come from the exact checkpoint above. Width and WidthPath match published width checkpoint `80345e62faf39e814b0c7bc23da5dbcd12a55989`. WidthLift SHA-256 `2f2eb79dcbb657016edc48ca0541db2bd3a51ee5e0c24ffd4ef1fd76305ae7e7` is explicitly **proposed, not frozen or fully compiled**, as confirmed by its author. The existing shared source files match byte for byte across worktrees; CatalogOrder and OuterCatalog are still absent from the width worktree. Their exact origin paths and hashes are recorded in `pending_source_materialization`. No source was copied by this metadata task.

Before completion, root must materialize the final outer sources, recheck all twenty-eight local source pins, refresh any changed WidthLift or Catalog hash, confirm the actual root results and audits, and run the intended combined verification. The width registry states local list lengths and necessary projection, not saved traversal order, reachability/SCC equality, arbitrary path realizability, positive overflow count, temporal-period divisibility, or finite-interface return existence. The finite path result concerns the sum of actual overflow clocks and formal signed increments; an ordinary exponent trajectory requires its separate guards.

Root remains the sole Git writer and owns the final Catalog source/pin and publication. This metadata task changed only the outer scoped registry, this note, and the new width scoped registry. No author-owned Lean file, global registry, or Git metadata was changed.
