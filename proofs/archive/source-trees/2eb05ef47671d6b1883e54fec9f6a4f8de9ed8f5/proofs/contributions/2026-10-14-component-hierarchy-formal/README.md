# Component-specific hierarchy bounds

`ComponentHierarchy.lean` proves the induction needed when each cyclic
component has its own child graph, instead of sharing one global next-level
bound. It imports the unchanged `CondensationBound.lean` package. There are
four new public theorems; the checker freshly rebuilds both modules and
audits all 19 theorems.

## Jobs and valid paths

The type of jobs `J` is arbitrary. No finite job list is assumed. Each job
has a component map, cyclic-component flags, candidate component ranks, a
candidate total vertex bound, and a natural-number height.

`JobPathFamily` specifies which finite paths are valid for each job and
explicitly proves that validity is preserved under taking any interval.
Actual orbit windows can be used instead of all paths in an abstract graph.
`orbitPathFamily` constructs this family from orbit projections and a
job-dependent eligibility predicate; `orbit_interval_valid` supplies each
eligible window's membership proof. Eligibility can include physical width,
the clock condition, induced-subgraph membership, and actual carry data.
There is no requirement that an interval begin at phase zero.

## Component-specific weighting and induction

For a job `j` and component `C`, the weight is

```text
weight(j,C) = bound(child(j,C))   if C is cyclic,
              1                 otherwise.
```

`component_hierarchy_path_vertices_le` concludes that every valid path in
job `j` has at most `bound(j)` vertices. Its premises are:

1. Whenever `C` is cyclic, `height(child(j,C)) < height(j)`.
2. Every nonempty valid path entirely inside cyclic `C` lifts to a valid
   path in exactly `child(j,C)`, preserving its number of vertices.
3. An acyclic component has no internal edge along a valid path.
4. Valid paths satisfy the weighted sink-rank inequalities from
   `CondensationBound.RankCertificate`, with the weights above.
5. Every nonempty valid path's initial component rank is at most `bound(j)`.

The proof is strong induction on the natural-number height. For each cyclic
interval, restriction closure supplies a valid source window, the lift
preserves both endpoints, and induction bounds its length by its own child
job's bound. `interval_bound_of_component_bounds` combines these varying
cyclic bounds with the weight-one acyclic intervals. The existing weighted
condensation theorem then bounds the whole path.

Jobs whose graph is already acyclic need no child lift, even if their height
is positive. At height zero the decrease premise prevents any cyclic
component. Empty paths need no assertion about their unused starting vertex.

## Application to induced subgraphs

In the refined graph calculation, a job is an induced subset of the raw
graph at spatial width `j`. A cyclic component of this induced graph can
be smaller than a global SCC. Its vertices are still globally recurrent,
so their retained parent identifiers exist. Its child job contains all
next-width vertices whose retained parent belongs to that component, and
all edges with both endpoints in that set. Actual constant-component
intervals therefore lift into that particular child job.

For widths at most 14, `height = 14 - j` decreases at each cyclic child.
An earlier acyclic job, for example at width 4 or 12, terminates without
requiring a child. These are application explanations; this package does
not certify the numerical job tables, component assignments, child maps,
rank values, terminal graphs, or actual-orbit realization premises.
Those remain separate certificate obligations.

The generic theorem makes no assertion of a finite Lychrel witness, an
all-time palindrome-avoidance result, or a proof of the 196 conjecture.

## Reproduction

```sh
python check.py /path/to/lean-4.19.0/bin/lean
```

The checker freshly compiles the exact dependency and new source, rejects
proof placeholders and extra axioms, and audits every theorem's transitive
axioms. Source SHA256 and Git blob hashes are in `verification.json`;
complete compiler output is in `compile.log`.

Development record: the initial source used a strong-induction theorem name
from another Lean library. Replacing it with Lean Std's `Nat.strongRecOn`
resolved that error; the complete module then compiled without warnings.
The saved report is a fresh clean rebuild, not an incremental result.
