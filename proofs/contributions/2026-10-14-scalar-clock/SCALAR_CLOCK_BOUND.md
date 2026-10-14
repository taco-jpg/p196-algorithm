# Finite obstruction to the scalar clock 4, 8, 16, 7, 15, 6, 13

Let \(G\) be the actual decimal pair-word update, with coefficients
listed from least to most significant position. Let \(Q\) be any
admissible canonical finite pair word of width \(L\ge1\). Put

\[
(a_0,\ldots,a_6)=(4,8,16,7,15,6,13).
\]

**Theorem (complete finite certificates).** If the actual outermost
coefficient follows this entire scalar clock for \(R\) complete periods,
meaning

\[
G^t(Q)_0=a_{t\bmod7}\qquad(0\le t\le7R),
\]

then

\[
R\le\min\left\{236,\;
232+\max\left(0,\left\lceil\frac{14-L}{3}\right\rceil\right)\right\}.
\tag{1}
\]

In particular no finite admissible orbit can maintain this scalar clock
forever. All other coefficients are free; neither their temporal period
nor their future carry choices are assumed. Bound (1) is conservative,
not claimed sharp. No palindrome-avoidance assumption is needed.

The hypothesis prescribes every phase of the scalar clock. It is
stronger than merely requiring the outer coefficient to be 4 at
multiples of seven: the different scalar trace
\((4,9,18,9,10,1,2)\) also returns to 4 and is a rotation of the separate
`seven_1` clock. The theorem does not exclude that clock or all possible
returns to outer coefficient 4.

## 1. Exact root graph and physical width growth

For a symmetric current word with outside coefficient \(q\), let
\(v\in\{0,1\}\) be the actual carry entering its highest original
column. The final overflow is \(e=\lfloor(q+v)/10\rfloor\), and the
next outside coefficient is

\[
q'=q\bmod10+
\begin{cases}
(q+v)\bmod10,&e=0,\\
1,&e=1.
\end{cases}
\tag{2}
\]

Retaining both inputs whenever they produce the prescribed next
coefficient gives this complete one-column graph:

| Phase | Current coefficient | Required next coefficient | Allowed input \(v\) | Overflow |
|---:|---:|---:|---|---:|
| 0 | 4 | 8 | 0 | 0 |
| 1 | 8 | 16 | 0 | 0 |
| 2 | 16 | 7 | 0 or 1 | 1 |
| 3 | 7 | 15 | 1 | 0 |
| 4 | 15 | 6 | 0 or 1 | 1 |
| 5 | 6 | 13 | 1 | 0 |
| 6 | 13 | 4 | 0 or 1 | 1 |

There are 7 phase vertices and 10 labeled edges. Every complete period
has exactly three overflows and therefore increases the actual whole
word's width by 3. Equation (2) also applies at width 1: the actual
incoming bit is then 0, and the two-bit graph remains an overapproximation.

## 2. Correlation-preserving spatial hierarchy

Expose one additional coefficient for every existing labeled graph
edge. If the known prefix has low outgoing carry \(\alpha\), last
coefficient \(p\), and high incoming edge label \(\gamma\), the next
coefficient \(b\) and deeper bit \(v\) must satisfy

\[
\gamma=\left\lfloor\frac{b+v}{10}\right\rfloor,
\qquad
b'=(b+\alpha)\bmod10+
\begin{cases}
(b+v)\bmod10,&e=0,\\
(p+\gamma)\bmod10,&e=1.
\end{cases}
\tag{3}
\]

The lift retains all such possibilities, with new label \(v\), and
the low carry for the extended prefix is
\(\lfloor(b+\alpha)/10\rfloor\) within the same addition. Full
preceding graph states and labels remain attached, preserving temporal
correlations. No same-period assumption is imposed on the new column.

These actual-carry equations require only that the exposed index be
less than the actual word width. Overlapping low and high observations
can constrain the actual incoming bit, but allowing both possible bits
does not exclude an actual trajectory. The exact local and iterated
ordinary-integer bridge is supplied by
[`../2026-10-14-prefix-extension-formal/PrefixExtension.lean`](../2026-10-14-prefix-extension-formal/PrefixExtension.lean).

At each width the producer retains the union of cyclic SCCs before
lifting again. The full raw and retained graphs are saved. Their counts
are:

| Width | Raw vertices | Raw edges | Cyclic SCCs | Retained vertices | Retained edges |
|---:|---:|---:|---:|---:|---:|
| 1 | 7 | 10 | 1 | 7 | 10 |
| 2 | 133 | 190 | 1 | 24 | 38 |
| 3 | 456 | 722 | 2 | 31 | 44 |
| 4 | 589 | 836 | 1 | 50 | 77 |
| 5 | 950 | 1,463 | 1 | 227 | 397 |
| 6 | 4,313 | 7,543 | 1 | 399 | 687 |
| 7 | 7,581 | 13,053 | 1 | 691 | 1,160 |
| 8 | 13,129 | 22,040 | 1 | 675 | 1,103 |
| 9 | 12,825 | 20,957 | 1 | 87 | 139 |
| 10 | 1,653 | 2,641 | 1 | 277 | 470 |
| 11 | 5,263 | 8,930 | 2 | 298 | 466 |
| 12 | 5,662 | 8,854 | 1 | 586 | 968 |
| 13 | 11,134 | 18,392 | 1 | 33 | 48 |
| 14 | 627 | 912 | 0 | 0 | 0 |

Thus the hierarchy closes at width 14, with a raw DAG whose longest
path has 18 edges. The caps of 500,000 raw vertices, 2,000,000 raw
edges, and width 24 were not reached. From width 4 onward the retained
graphs agree with the broader two-column 44 investigation; the raw
width-4 graph still differs, so its finite transient bound must be
computed separately.

`scalar_clock.py` reuses the reviewed
`../2026-10-14-broader-return/branching_lift.py` and records that source's
hash. The completed `seven_4/scalar_clock.json` records all counts and
graph hashes; the adjacent compressed artifacts retain all vertices,
edges, parent mappings, and exact carry labels. None of the graph
construction imposes a bound on the temporal behavior of deeper columns.

`independent_scalar_audit.py` reconstructs all prefixes, checks all
128,644 raw local controls by literal integer normalization, and uses
an independent SCC calculation to check the entire graph hierarchy.
The report `seven_4/independent_scalar_audit.json` records
`PASS_EMPTY_AT_WIDTH14`, with complete local-control artifacts retained.

## 3. Weighted condensation bound, including transients

The following counts include **vertices**, so a path of \(n\) vertices
contains \(n-1\) edges. Assume first that actual physical widths are at
least 14 throughout the observed path.

At the last raw graph, every path has at most \(B_{14}=19\) vertices.
Inductively suppose \(B_{j+1}\) bounds realized paths in the next raw
graph. An actual path visits each SCC of the width-\(j\) graph in one
contiguous interval, because the condensation graph is a DAG. A
loop-free singleton contributes at most one vertex. An interval in a
cyclic SCC lies within the retained graph, and (3) lifts that entire
interval into the next raw graph. Its vertex count is therefore at
most \(B_{j+1}\).

Give each cyclic SCC weight \(B_{j+1}\) and each other SCC weight 1.
The maximum weighted condensation-path sum is a bound \(B_j\) for
every realized path in the current raw graph. The certificate checks
the defining ranks

\[
R(C)=w(C)+\max\bigl(\{0\}\cup\{R(D):C\to D\}\bigr).
\tag{4}
\]

This handles every finite transient explicitly; it does not assume a
uniform time of first entry into a recurrent component. The bounds are:

| Width \(j\) | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 | 11 | 12 | 13 | 14 |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| \(B_j\) | 1,629 | 1,629 | 1,619 | 795 | 777 | 750 | 702 | 663 | 567 | 494 | 466 | 208 | 157 | 19 |

The phase-0 root bound is 1,629 vertices, hence 1,628 edges. Maintaining
\(R\) whole periods gives \(7R+1\) actual vertices, so

\[
7R+1\le1629,
\qquad R\le\left\lfloor\frac{1628}{7}\right\rfloor=232.
\tag{5}
\]

If the initial width is smaller than 14, let
\(s=\max(0,\lceil(14-L)/3\rceil)\). Either fewer than \(s\) full
periods occur, or the actual width after them is \(L+3s\ge14\).
Applying (5) to the remaining periods gives \(R-s\le232\). Since
\(L\ge2\) implies \(s\le4\), this proves (1) for all such widths.

The width-1 case is unique: the required initial word is \((4)\).
Its exact successive pair words are

\[
(4)\longrightarrow(8)\longrightarrow(16)
\longrightarrow(7,7)\longrightarrow(14,14).
\]

At time 4 its outside coefficient is 14 rather than the required 15.
It therefore completes zero periods of the specified clock. This proves
(1) at width 1 as well and improves the coarse width-preparation bound
237 to the uniform bound **236**. The producer separately records this
exact small-width calculation; no graph needs to be regenerated.

`scalar_bound.py` reads the frozen graph checkpoints and reuses the
generic, independently audited condensation helper
`../2026-10-14-broader-return/finite_bound.py`, recording its exact hash.
`scalar_bound_certificate.json.gz` contains every SCC assignment,
condensation edge, weight, and rank. `scalar_bound.json` records every
level bound and the source/artifact hashes. It does not rerun or modify
the graph construction.
`independent_scalar_bound_audit.py/.json` checks all 60,952 components
against the independently reconstructed partitions, verifies every
weight and rank, and independently checks the width-1 exception. Its
final status is `PASS_BOUND_236`.

The generic weighted path theorem is also formally checked in
[`../2026-10-14-scc-bound-formal/CondensationBound.lean`](../2026-10-14-scc-bound-formal/CondensationBound.lean).
Its `path_vertices_le_rank` and `cyclic_path_vertices_le_rank` prove the
composition used in (4) from interval bounds and the local rank
inequalities. This formal package does not itself certify the numerical
SCC tables or instantiate the complete scalar hierarchy; those are
supplied by the preserved finite certificates and independent replay.

## 4. Prior work, limits, and reproduction

The scalar outer cycle already appears among the fixed 14-phase
spatial-pump exclusions in
[`../../research/main_existence_attempt/boundary_resume/new_clock/STATUS.txt`](../../research/main_existence_attempt/boundary_resume/new_clock/STATUS.txt).
The necessary local extension and rank method also appear in
[`../../research/main_existence_attempt/correlation_pass/free_clock/STATUS.md`](../../research/main_existence_attempt/correlation_pass/free_clock/STATUS.md).
Here the complete labeled graph preserves arbitrary temporal histories
of deeper coefficients, and the weighted certificate provides an
explicit all-length finite bound on this scalar schedule.

This is a clock exclusion, not an eventual-palindrome theorem. It does
not settle the original remaining gate or establish that every finite
decimal integer eventually reaches a palindrome. Separate directories
for `seven_1` and `primitive14` record different capped investigations;
their results are not premises of this theorem and must retain their
reported status.

From the repository root, the bound alone can be reproduced without
regenerating any graph:

```sh
python -B proofs/contributions/2026-10-14-scalar-clock/scalar_bound.py
python -B proofs/contributions/2026-10-14-scalar-clock/independent_scalar_audit.py
python -B proofs/contributions/2026-10-14-scalar-clock/independent_scalar_bound_audit.py
```

The original completed graph construction is reproduced by
`scalar_clock.py seven_4`; independent audit sources and reports are
retained beside the contribution. All arithmetic is exact integer
arithmetic with Python's standard library.
