# Actual spatial path lift for the scalar hierarchy

This package constructs the missing analytic lift from an actual decimal
pair-word orbit into the next spatial prefix graph. It also instantiates the
scalar root and its first two-column refinement. It does not instantiate the
remaining component tables and does not prove the numerical bounds 94 or 98.

Independent review found that the unrestricted semantic lift also admits
non-bit labels, including a concrete label-nine edge. The actual-path theorems
remain valid, but encoding into the saved bit-only finite graphs requires the
adapter in `../2026-10-15-bounded-prefix-lift-formal/`. That package proves all
actual labels are bits and supplies the applicable bounded-label transport
and actual component-hierarchy composition. The independent counterexample is
retained in `../2026-10-15-actual-prefix-lift-review/`. These Lean sources remain
unchanged; this note records the interface correction.

## Proved statements

`ActualPrefixLift.lean` defines a graph vertex by its phase, last prefix
coefficient, low outgoing carry, and eligibility predicate. An `ActualPath`
matches these fields to the actual whole-word orbit; every graph edge is
labeled by the actual carry entering the reflected high prefix. Its length
counts vertices, with edges only between two vertices in the interval.

The spatial lift has vertices `V × Fin 19`. Its exact edge equations are
`PrefixExtension.ExtensionChoice`, using the same parent carry and emission
formula as the stored Python graphs. `actual_path_lifts` constructs the
child vertex at time `t` by appending the actual coefficient `q_t(k)` and
proves the edge using the actual carry `carry q_t (L_t - k - 1)`. No choice
of independent interior controls is assumed. The hypotheses are admissibility
and `1 ≤ k < L`; width monotonicity supplies this inequality at all times.
Overlapping low and high windows are permitted.

`actual_component_interval_lifts` first restricts a path to a finite interval
whose vertices share a selected component, then constructs the child path in
the exact induced lift. The child has the same number of vertices and projects
to every original vertex, including both endpoints. This supplies the analytic
content required by the `hlift` interface of `ComponentHierarchy.lean` once
the finite child-job representations have been verified.

`actual_path_encode` transports a constructed path into a finite-ID graph
under a `Realization` proof: eligible vertices and their fields are preserved,
and every relevant source edge is present in the destination table. These are
finite table obligations, not an assumed existence of an actual lifted path.
For bit-only finite graphs, apply the new bounded-label adapter first; the
unrestricted `Realization` requirement alone is too strong.

`ScalarRoot.lean` defines the exact seven-vertex, ten-edge scalar root. The
kernel evaluates its transition equivalence on all 98 triples consisting of
two phases and one carry bit. `actual_root_path` places every actual scalar
clock interval, at any start time and phase, into this graph.
`actual_two_column_path` then constructs its actual 133-vertex refinement.
The ID `19 * phase + coefficient` has its range, quotient, and remainder
proved. The checker also compares the literal root edge list to frozen job
zero of the numerical component certificate.

## Architecture for the remaining finite instance

The scalar branch of the existing certificate uses jobs 0 through 15:
64,322 job-local vertex records, 106,543 edges, and 60,952 components in total.
These are sums across jobs, not distinct global vertices. The remaining
broader branch is separate. No new graph enumeration was run here.

Every raw spatial-lift vertex has ID `19 * retainedParentId + coefficient`.
All 19 coefficients are present for every retained parent; there is no
filtering during raw generation. Subsequent cyclic trimming preserves raw
order while densely renumbering retained IDs. A child job is the induced
subset whose parent lies in the selected parent component.

A complete scalar instance still needs the following kernel-checked data:

1. Finite maps between job-local IDs, raw IDs, and retained IDs, including
   validity and phase/last/low field preservation.
2. For each selected cyclic component, total encoding of all its
   `parent × Fin 19` vertices into the child job and forward completeness of
   the exact lift edges. Parent raw IDs must be converted to retained IDs
   using the checked map; phase/last/low alone do not identify a prefix.
3. Component labels, acyclic singleton exclusion, child selection and strict
   height decrease, component weights, and every weighted rank inequality.
4. A `JobPathFamily` instance for actual orbit windows and application of
   `component_hierarchy_path_vertices_le`, giving at most 659 vertices from
   the scalar root. Only then does `7R + 1 ≤ 659` give `R ≤ 94` at width 14.
   The already checked scalar warmup and width-one results would extend that
   bound to the stated uniform 98-period consequence.

For the final finite implementation, use checked direct row access and
inverse ID tables, with small batches of kernel `decide` certificates.
The semantic lift in this package ensures that checking inclusion is enough;
no assertion that arbitrary graph paths are globally realizable is needed.
The full rank/table work has deliberately not been launched before this
representation and soundness interface is reviewed.

## Reproduction

Run with Lean 4.19.0:

```sh
python check.py --lean /path/to/lean
```

The checker rebuilds the pinned `LychrelDigitSums.lean`, the three scalar
dependencies, `PrefixExtension.lean`, and both new modules in a fresh temporary
directory. It imports no old project object files. It checks source and direct
dependency hashes and audits every public theorem in the six non-base modules.
`verification.json` distinguishes the 15 new theorems from prerequisite audits.
`compile.log` records commands, hashes, and the full axiom output.

The environment uses Lean flags `-j1 -DElab.async=false`. Its existing
`readlink_self.so` compatibility shim redirects only executable-path discovery;
it does not modify the Lean kernel. A standard Lean installation does not
require that shim. Only the standard `Classical.choice`, `Quot.sound`, and
`propext` axioms are allowed by the checker.
