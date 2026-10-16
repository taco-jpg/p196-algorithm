# Sharper return bounds from component-specific spatial restrictions

This contribution sharpens two previously checked bounds while reading
their graph checkpoints unchanged. It replaces a single global
next-level bound by the bound for the exact next-level subgraph reached
from each cyclic component.

| Actual orbit condition | Previous uniform bound | Refined uniform bound |
|---|---:|---:|
| Entire scalar clock \((4,8,16,7,15,6,13)\), repeated | 236 complete periods | **98 complete periods** |
| Prefix \((4,4)\) at every seven-step return | 232 consecutive returns | **94 consecutive returns** |

These remain conservative bounds, not sharpness claims. Neither result
asserts that leaving its prescribed pattern produces a palindrome.
All words below are admissible canonical decimal pair words, and all
updates are the actual pair-word update \(G\).

## 1. Statements and exact width dependence

Let the initial physical word width be \(L\).

**Scalar-clock theorem.** Put
\(a=(4,8,16,7,15,6,13)\). If

\[
G^t(Q)_0=a_{t\bmod7}\qquad(0\le t\le7R),
\]

then, for every \(L\ge1\),

\[
R\le\min\left\{98,\;
94+\max\left(0,\left\lceil\frac{14-L}{3}\right\rceil\right)\right\}.
\tag{1}
\]

The complete scalar schedule is the hypothesis. Merely requiring the
outside coefficient to be 4 at multiples of seven does not prescribe
this schedule and is not covered by (1).

**Two-column return theorem.** If \(L\ge2\) and

\[
G^{7k}(Q)[0:2]=(4,4)\qquad(0\le k\le R),
\]

then

\[
R\le90+\max\left(0,\left\lceil\frac{14-L}{3}\right\rceil\right)
\le94.
\tag{2}
\]

All three two-column return branches are retained, with arbitrary
switching between successive returns. There is no safety assumption
in either theorem and no assumed temporal period for deeper columns.

The exact root graphs, actual-carry equations, and overflow schedules
are those already established in
[`../2026-10-14-scalar-clock/SCALAR_CLOCK_BOUND.md`](../2026-10-14-scalar-clock/SCALAR_CLOCK_BOUND.md)
and
[`../2026-10-14-broader-return/BROADER_RETURN_BOUND.md`](../2026-10-14-broader-return/BROADER_RETURN_BOUND.md).
Every complete period or successful two-column return increases
physical width by exactly 3.

## 2. Restricted jobs and their exact spatial projections

Write \(A_j\) for the saved raw graph at prefix width \(j\), and
\(H_j\) for the induced graph on its cyclic SCC vertices. The next
saved raw graph \(A_{j+1}\) is the exact one-column lift of \(H_j\).
Its vertex records include a parent ID in \(H_j\).

A **job** is an induced graph \(A_j[S]\), for an explicitly saved
vertex subset \(S\). Its allowed paths are actual orbit projections
whose observed prefixes lie in \(S\), with the exact actual carry
labels. This is a subset of its abstract graph paths; no assertion that
every abstract path can be spatially realized is needed.

Let \(C\) be a cyclic SCC of \(A_j[S]\). Every vertex of \(C\) lies
on a nontrivial closed walk in the induced graph, hence also in
\(A_j\). Thus \(C\subseteq V(H_j)\), even when restriction to \(S\)
has split a larger global SCC into smaller components. The saved
raw-to-retained vertex map is therefore defined on every member of
\(C\).

Define the exact child subset

\[
S_C=\{z\in V(A_{j+1}):\operatorname{parent}(z)\in C\},
\tag{3}
\]

where the parent is interpreted back in raw width-\(j\) IDs. The child
job is \(A_{j+1}[S_C]\), including **every** edge with both endpoints
in that subset. No restriction on the next coefficient or deeper bit
is added beyond the previously checked local lift equation.

For each parent vertex, all 19 coefficients are present. For each
internal labeled parent edge, all 19 compatible coefficient/deeper-bit
choices are present. The producer checks

\[
|S_C|=19|C|,\qquad
|E(A_{j+1}[S_C])|=19|E(A_j[C])|,
\]

and checks the exact label projection of every child edge. If the new
coefficient is \(b\) and the child input is \(v\), the projected parent
input is \(\lfloor(b+v)/10\rfloor\).

**Actual interval lifting.** Any actual path interval contained in
\(C\) has all vertices and edges in \(H_j\). If the next physical
column exists, expose its actual coefficient and carry throughout
that same interval. The existing actual-extension relation gives a
path in the child graph (3) with exactly the same number of vertices.
Both endpoints are retained. This holds at every starting phase and
does not impose an independent or periodic deeper-carry schedule.

Overlapping low and high observations do not change necessity: their
actual carries are correlated, and the graph includes both bits. The
formal bridge `actual_extension_edge` in
[`../2026-10-14-prefix-extension-formal/PrefixExtension.lean`](../2026-10-14-prefix-extension-formal/PrefixExtension.lean)
requires only that the new coefficient index be smaller than physical
width. Physical width at least 14 therefore suffices for every job in
these finite hierarchies.

## 3. Recursive weighted bound and its soundness

All lengths in this section count **vertices**, including both path
endpoints. In a job \(J=A_j[S]\), an acyclic SCC is a loop-free
singleton and receives weight 1. A cyclic SCC \(C\) receives the
already computed bound \(B(J_C)\) of its exact child job from (3).
On the condensation DAG compute

\[
r(C)=w(C)+\max\bigl(\{0\}\cup\{r(D):C\to D\}\bigr),
\qquad B(J)=\max_C r(C).
\tag{4}
\]

These calculations terminate: every child exposes one more spatial
column, the saved final graph at width 14 is acyclic, and a restricted
job may become acyclic earlier. Memoization keys include the source
hierarchy, width, and exact allowed vertex set.

To prove the bound, induct downwards in the remaining spatial depth.
A path cannot leave one SCC and return to it, because that would make
the condensation graph cyclic. Its visits to each component therefore
form one interval. An acyclic singleton contributes at most one
vertex. By Section 2, an actual interval in a cyclic \(C\) lifts to
the exact child job, so the induction hypothesis bounds its vertices
by \(B(J_C)=w(C)\). Summing along its condensation path and applying
(4) bounds the total vertex count by its initial rank, and hence by
\(B(J)\).

This proof covers every finite transient; it assumes no entry-time
bound. It also does not require every abstract path in a parent graph
to lift. The claim concerns the restriction-closed family of actual
orbit intervals.

The generic component-specific weighted step is already formally
proved by `path_vertices_le_rank` in
[`../2026-10-14-scc-bound-formal/CondensationBound.lean`](../2026-10-14-scc-bound-formal/CondensationBound.lean).
The generic recursion is now also formally proved by
`component_hierarchy_path_vertices_le` in
[`../2026-10-14-component-hierarchy-formal/ComponentHierarchy.lean`](../2026-10-14-component-hierarchy-formal/ComponentHierarchy.lean).
It permits a different child job for each cyclic component, requires
strictly decreasing job height, and uses a restriction-closed family
of valid actual paths. Here height is \(14-j\), and early acyclic
jobs require no child. The older uniform-weight `LiftHierarchy.lean`
package remains applicable to the coarse bounds. These generic formal
theorems do not themselves instantiate the numerical job certificates,
child maps, or actual-orbit eligibility premises.

## 4. Where the improvement occurs

Only 31 jobs are needed: 16 for the scalar clock and 15 for the broader
return. The declared cap is 10,000 recursive jobs. All jobs completed;
no cap, timeout, or enlarged direct 14-column enumeration was used.

The significant branch distinctions are:

| Parent situation | Cyclic component size | Exact child graph | Child vertex bound |
|---|---:|---|---:|
| Width 3, either hierarchy, short branch | 12 | Width 4: 228 vertices, 323 edges; DAG | 14 |
| Width 3, scalar, long branch | 19 | Width 4: 361 vertices, 513 edges | 606 |
| Width 3, broader, long branch | 13 | Width 4: 247 vertices, 342 edges | 600 |
| Width 11, either hierarchy, short branch | 26 | Width 12: 494 vertices, 684 edges; DAG | 19 |
| Width 11, either hierarchy, long branch | 272 | Width 12: 5,168 vertices, 8,170 edges | 208 |

The previous calculation gave both components at a level the same
global next-level bound. The short components now receive their own
much smaller bounds. Propagating these distinctions through (4) gives:

| Root | Path vertices from phase 0 | Path edges | Complete seven-step blocks at width at least 14 |
|---|---:|---:|---:|
| Scalar | 659 | 658 | 94 |
| Broader two-column return | 636 | 635 | 90 |

For \(R\) full blocks the actual path has \(7R+1\) vertices. Therefore
\(7R+1\le659\) gives \(R\le94\) in the scalar case, while
\(7R+1\le636\) gives \(R\le90\) for the broader return.

For initial width \(L<14\), at most
\(s=\max(0,\lceil(14-L)/3\rceil)\) successful blocks are needed to
reach width 14. If that many blocks do not occur, the desired bound is
automatic; otherwise apply the width-14 bound to the remaining blocks.
For \(L\ge2\), \(s\le4\), giving uniform bounds 98 and 94.

The scalar width-1 case has the unique required pair word \((4)\).
Its exact trace is
\((4),(8),(16),(7,7),(14,14)\), so it fails the required scalar value
15 at time 4 and completes zero full periods. This previously checked
exception extends the scalar uniform bound 98 to all \(L\ge1\),
proving (1) and (2).

## 5. Certificates, dependencies, and reproduction

`component_bound.py` reads the frozen scalar and broader raw/retained
checkpoints. It checks their hashes, reconstructs exact
raw-to-retained maps, and reuses the previously audited SCC helper in
`../2026-10-14-broader-return/finite_bound.py`, with its dependency hash
recorded. No published source or graph artifact is modified.

`component_certificates.json.gz` preserves every job's full allowed
vertex metadata, exact induced labeled edges, component partition,
child restrictions and parent projections, condensation edges,
component weights, and sink ranks. Its SHA-256 is
`ff7a70ee2a6ed677cb9176e212dc0a69acd14eed30425a42b543d7a50823b47e`.
`component_bound.json` records all dependencies, artifact hashes,
completion status, the 10,000-job cap, and both final bounds.

`independent_component_audit.py/.json` independently checks all 31
induced jobs, comprising 128,234 vertex records and 212,453 labeled
edges. It checks the exact allowed sets, all 19 extensions per parent
vertex, complete induced edge sets, parent/carry projections, SCCs with
an independent Tarjan implementation, and every component weight and
rank. It confirms both refined uniform bounds and the direct
width-at-least-14 bounds. The underlying full graph arithmetic had
already been independently checked by literal integer normalization;
this audit verifies the new restrictions and recursive composition.

From the repository root, using the Python standard library:

```sh
python -B proofs/contributions/2026-10-14-component-specific-bound/component_bound.py
python -B proofs/contributions/2026-10-14-component-specific-bound/independent_component_audit.py
```

The source preserves incomplete jobs and reports `UNKNOWN_JOB_CAP` if
the cap is reached; the saved result here is `COMPLETE` with all 31
jobs finished. The stronger numerical bounds are finite consequences
of already checked necessary graphs. They do not settle the remaining
gate, exclude other scalar clocks, or establish an eventual palindrome.
