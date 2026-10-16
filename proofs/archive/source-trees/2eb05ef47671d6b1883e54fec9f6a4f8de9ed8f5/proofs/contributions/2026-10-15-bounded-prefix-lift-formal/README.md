# Bit-label adapter and actual component-hierarchy composition

This package resolves an interface limitation found during independent review
of `2026-10-15-actual-prefix-lift-formal`. It then connects actual orbit paths
to `ComponentHierarchy.component_hierarchy_path_vertices_le` using local
finite graph conditions. No scalar numerical bound of 94 or 98 is asserted.

## Why the adapter is necessary

The earlier semantic `lift G` accepts natural-number edge labels. Its actual
path theorems are correct, since actual carries are bits, but the unrestricted
`Realization.edges` interface requests forward completeness even for impossible
labels. There really is a label-nine edge in `lift ScalarRoot.root`, from
`(phase 0, coefficient 0)` to `(phase 1, coefficient 9)`. Consequently, that
entire unrestricted graph cannot map into a graph whose labels are only bits.

The independent review's `LabelNineCounterexample.lean` proves this obstruction.
The present checker freshly rebuilds and audits its three declarations along
with the adapter. The earlier package is preserved unchanged.

`BoundedPrefixLift.bounded G` keeps the graph's vertices and fields and replaces
its edge relation by `c ≤ 1 ∧ G.edge u v c`. `actual_label_bound` proves this
restriction for every actual carry label. `actual_path_bounded` therefore
preserves every actual orbit path. The bounded component-interval theorem
constructs the same child path and parent projections while using exactly the
two labels accepted by the finite tables.

Finite certificate implementations must use

```lean
ActualPrefixLift.Realization
  (BoundedPrefixLift.bounded
    (ActualPrefixLift.lift
      (ActualPrefixLift.select parentGraph (fun v => component v = c))))
  childGraph encode
```

This requires completeness only for the appropriate bit-labeled source edges.

## Actual hierarchy application

`ActualJobFamily.family` instantiates the generic path-family interface with
actual finite orbit windows, existentially recording start time and phase.
Its interval restriction law is proved from the earlier actual-path theorem.

`constructive_child_lift` derives the generic hierarchy's lift requirement
from the actual child path construction and checked finite child encodings.
It assumes no existence of lifted orbit paths. Its spatial width condition is
`1 ≤ width job < L`, and every cyclic child increases prefix width by one.
For scalar jobs of widths 1 through 14, physical width at least 14 covers all
cyclic parents of width at most 13. No disjoint-boundary condition is needed.

`actual_path_vertices_le` then proves that every actual path in a job has at
most that job's bound. Its remaining certificate conditions are local:

- Cyclic children have smaller natural-number height and the expected width.
- The bounded selected spatial lift has a verified encoding into the child.
- At each valid vertex, component weight is at most its rank, which is at most
  the job bound.
- A bit-labeled edge from an acyclic component changes component; every edge
  that changes component decreases rank by at least the source weight.

The proof derives both the actual-path rank certificate and the acyclic
condition from these local checks, then applies the existing hierarchy theorem.
Correctness of an SCC computation is not needed: any component partition and
certificate satisfying these explicit conditions is sufficient.

All job, vertex, and component types remain generic. The proposed finite
implementation uses natural-number IDs, a deterministic two-label transition
table, and compact child IDs `19 * memberOrdinal + coefficient`. Its row data
and finite checks are separate work; none are assumed to have passed here.

## Verification

```sh
python check.py --lean /path/to/lean
```

The checker uses Lean 4.19.0, rebuilds every project dependency from source in
a fresh temporary directory, and audits all public theorem axiom dependencies.
It records source, object, output, and direct-import hashes. There are eight
new declarations in this package and three independent review-counterexample
declarations, in addition to the prerequisite audit. It accepts only standard
`Classical.choice`, `Quot.sound`, and `propext` axioms.

The supplied environment uses `-j1 -DElab.async=false` and a path-discovery
compatibility shim named `readlink_self.so`. The shim does not modify the Lean
kernel and is unnecessary on standard installations. No old compiled project
objects are used by the checker.
