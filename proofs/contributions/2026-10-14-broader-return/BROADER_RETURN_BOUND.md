# A finite bound on consecutive seven-step returns to the two-column prefix 44

Let \(G\) be the actual decimal pair-word update, with coefficients
listed from least to most significant position. Let \(Q\) be an
admissible canonical symmetric finite word of width \(L\ge2\), with
coefficients in \(\{0,\ldots,18\}\), even center coefficient when its
width is odd, and first two coefficients \((4,4)\).

**Theorem (complete finite certificates).** If

\[
G^{7k}(Q)[0:2]=(4,4)\qquad(0\le k\le R),
\]

then

\[
R\le228+\max\left(0,\left\lceil\frac{14-L}{3}\right\rceil\right)
\le232.
\tag{1}
\]

In particular, no finite admissible integer orbit can return to this
two-column prefix every seven updates forever. The numerical bound is
conservative; no sharpness claim is made. No palindrome-avoidance
assumption is needed, and leaving this return pattern does not imply
that the integer orbit reaches a palindrome.

This broadens the previous exclusion for the three-column prefix
\((4,4,0)\): the third coefficient is now unrestricted, and the
two-column return may follow any of three branches, changing branches
at successive seven-step returns.

## 1. Complete two-column return relation

For a current prefix \(p\), normalize it from low to high with input 0,
and normalize its reversal with the actual high incoming bit \(c\).
Let \(\ell_i,u_i\) denote the resulting digits in outside-index order,
and let \(e\) be the final carry of the high calculation. Its next
prefix is exactly

\[
p'_i=\begin{cases}
\ell_i+u_i,&e=0,\\
\ell_0+1,&e=1,\ i=0,\\
\ell_i+u_{i-1},&e=1,\ i>0.
\end{cases}
\tag{2}
\]

Enumerating all 128 seven-bit controls starting from \((4,4)\) gives
exactly 16 returns and three distinct prefix traces:

| Phase | Branch A | Branch B | Branch C |
|---:|---|---|---|
| 0 | \((4,4)\) | \((4,4)\) | \((4,4)\) |
| 1 | \((8,8)\) | \((8,9)\) | \((8,9)\) |
| 2 | \((16,16)\) | \((16,18)\) | \((16,18)\) |
| 3 | \((7,14)\) | \((7,16)\) | \((7,16)\) |
| 4 | \((15,8)\) | \((15,12)\) | \((15,13)\) |
| 5 | \((6,14)\) | \((6,9)\) | \((6,10)\) |
| 6 | \((13,9)\) | \((13,9)\) | \((13,0)\) |
| 7 | \((4,4)\) | \((4,4)\) | \((4,4)\) |

All returning branches have overflow schedule \((0,0,1,0,1,0,1)\),
so every successful return increases the whole word's width by exactly
3. If \(c_0,\ldots,c_6\) are the seven actual high incoming bits, the
exact return condition is

\[
c_1=0\quad\text{and}\quad
\bigl[(c_3=0\land c_5=1\land c_6=1)
\ \lor\ (c_0=1\land c_3=1\land c_5=0)\bigr].
\tag{3}
\]

Bits \(c_2,c_4\) are unrestricted. In the second disjunct \(c_6\) is
also unrestricted. The initially proposed single pattern \(00*0*11\)
covers only Branch A; the producer explicitly preserves this failed
restriction in its report.

`two_column_controls.py/.json` retain all 128 controls, not only the
returning ones. Equal phase/prefix states are merged into a base graph
with **15 vertices and 23 labeled edges**. Its complete seven-edge
return paths are checked to be exactly those 16 controls. The return
junction is shared, so the graph allows arbitrary branch switching at
successive returns. No single branch or temporal repetition is assumed.

## 2. Exact necessary spatial lift

Suppose a graph vertex records the first \(j\) coefficients of the
actual current word, their phase, the last coefficient \(p_{j-1}\),
and the actual low carry \(\alpha\) leaving that prefix. An edge is
labeled by the actual high incoming carry \(\gamma\). Expose the next
coefficient \(a\in\{0,\ldots,18\}\) and the next deeper actual carry
\(v\in\{0,1\}\). Necessarily

\[
\gamma=\left\lfloor\frac{a+v}{10}\right\rfloor,
\qquad
a'=(a+\alpha)\bmod10+
\begin{cases}
(a+v)\bmod10,&e=0,\\
(p_{j-1}+\gamma)\bmod10,&e=1.
\end{cases}
\tag{4}
\]

The low carry leaving the extended prefix is
\(\lfloor(a+\alpha)/10\rfloor\), within the current addition. The
new edge label is \(v\). The lift retains every pair \((a,v)\) satisfying
(4) for each existing labeled edge. Thus it preserves the entire
preceding temporal relation, including correlations between choices at
different phases and the three branching return traces.

These are actual-carry equations, so observing overlapping low and high
prefixes causes no loss of necessity. All that is needed to expose
index \(j\) is \(j<L\). The formal actual-word and ordinary-integer
bridge is
[`../2026-10-14-prefix-extension-formal/PrefixExtension.lean`](../2026-10-14-prefix-extension-formal/PrefixExtension.lean),
including `actual_extension_edge` and `iterated_extension_edge`.
Enumerating both deeper bits overapproximates actual possibilities; a
surviving abstract path is not asserted to have an integer realization.

## 3. Complete hierarchy through width 14

At each width, take the union of cyclic strongly connected components
(SCCs), retain all edges with both endpoints in that union, and lift
that retained graph by one coefficient. Every infinite path in a
finite graph has a tail in a cyclic SCC, which already makes this a
sound method for excluding perpetual returns. Section 4 handles finite
transients explicitly and supplies bound (1).

| Prefix width | Raw vertices | Raw edges | Cyclic SCCs | Retained vertices | Retained edges |
|---:|---:|---:|---:|---:|---:|
| 2 | 15 | 23 | 1 | 15 | 23 |
| 3 | 285 | 437 | 2 | 25 | 35 |
| 4 | 475 | 665 | 1 | 50 | 77 |
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

The last raw graph is acyclic; its longest path has 18 edges and 19
vertices. The declared caps of 500,000 raw vertices, 2,000,000 raw
edges, and prefix width 32 were never reached. The result is complete
exclusion at a finite width, not a timeout or an extrapolation from
growth or contraction of graph sizes.

`branching_lift.py/.json` preserve the construction and metadata. Every
raw graph and every retained graph is saved in deterministic compressed
binary form, including parent mappings and carry labels, in
`branch_width_*_{raw,recurrent}.bin.gz`. The report records each
file's schema, byte count, and SHA-256 hash.

The independent audit reconstructs full prefixes from those parent
mappings, checks all **127,824** local controls by literal integer
normalization, and independently checks all SCCs and the final DAG.
Thus neither the original producer's recurrence nor its SCC routine is
the sole arithmetic/graph check.
Its source and report are `independent_branch_audit.py/.json`, with
every local control output retained in
`independent_branch_controls.bin.gz`. The separate
`independent_two_column_audit.py/.json` checks the initial 128-branch
calculation and formula (3).

## 4. A bound that includes all finite transients

All lengths in this section count **vertices**, including both
endpoints of a path. For an actual path whose physical word widths are
at least 14, every spatial column used in the hierarchy exists.

At width 14, set \(B_{14}=19\), the maximum vertex count of a path in
its raw DAG. Work downwards. In a width-\(j\) raw graph, assign each
acyclic SCC weight 1: it is a loop-free singleton and can be visited
only once. Assign each cyclic SCC weight \(B_{j+1}\).

Why is that weight sufficient? An actual path visits any given SCC in
one contiguous interval, because returning after leaving would create
a cycle in the condensation DAG. The interval in a cyclic SCC lies
entirely in the retained width-\(j\) graph. Exposing the next actual
coefficient and carry projects that entire interval to a path in the
next raw graph, by (4). It therefore has at most \(B_{j+1}\) vertices.
This argument needs no bound on the time at which an orbit first enters
a recurrent component.

On the condensation DAG, let \(w(C)\) be these weights and calculate

\[
R(C)=w(C)+\max\bigl(\{0\}\cup\{R(D):C\to D\}\bigr).
\tag{5}
\]

Every actual path starting in component \(C\) has at most \(R(C)\)
vertices: its component intervals follow a condensation path, their
vertex counts are bounded by their weights, and (5) bounds the sum.
Taking the maximum defines \(B_j\). The complete calculation gives:

| Width \(j\) | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 | 11 | 12 | 13 | 14 |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| \(B_j\) | 1,600 | 1,600 | 789 | 777 | 750 | 702 | 663 | 567 | 494 | 466 | 208 | 157 | 19 |

`finite_bound.py` reads the preserved raw graphs and saves all SCC
assignments, condensation edges, component weights, and ranks (5) in
`finite_bound_certificate.json.gz`. It checks every edge inequality and
every defining recurrence, not merely the final maximum.
`independent_bound_audit.py/.json` independently checks all 60,563
component weights and ranks against the separately replayed graph
partitions, obtains the same bounds, and reports `PASS_BOUND_232`.

If \(R\) seven-step returns occur starting at width at least 14, their
actual base-graph path has \(7R+1\) vertices. Hence

\[
7R+1\le1600,
\qquad R\le\left\lfloor\frac{1599}{7}\right\rfloor=228.
\tag{6}
\]

For a smaller initial width \(L\ge2\), put
\(s=\max(0,\lceil(14-L)/3\rceil)\). If fewer than \(s\) returns occur,
(1) is automatic. Otherwise the word after those \(s\) returns has
width \(L+3s\ge14\), by Section 1. Apply (6) to the remaining returns:
\(R-s\le228\). Since \(s\le4\), this proves (1) and the uniform bound
232. This final width handoff concerns the number of successful
returns; it does not assume unobserved intermediate prefixes return.

## 5. Prior work and scope

The necessary prefix-extension equation and graph-rank exclusion method
already appear in
[`../../research/main_existence_attempt/correlation_pass/free_clock/STATUS.md`](../../research/main_existence_attempt/correlation_pass/free_clock/STATUS.md).
The earlier
[`../../research/main_existence_attempt/boundary_resume/new_clock/STATUS.txt`](../../research/main_existence_attempt/boundary_resume/new_clock/STATUS.txt)
also excludes specified 14-phase spatial pumps with scalar outer clock
\((4,8,16,7,15,6,13)\) repeated twice. That fixed-period result does not
by itself exclude the arbitrary deeper temporal histories and switching
two-column branches considered here. The present graph retains those
possibilities and closes after 12 additional spatial columns.

The conclusion is an obstruction to this return pattern. It does not
exclude other clocks, longer return times, different boundary prefixes,
or an aperiodic finite decimal Lychrel orbit. The original existence
problem remains open in this contribution.

## Reproduction

From the repository root, using the Python standard library:

```sh
python -B proofs/contributions/2026-10-14-broader-return/two_column_controls.py
python -B proofs/contributions/2026-10-14-broader-return/branching_lift.py
python -B proofs/contributions/2026-10-14-broader-return/finite_bound.py
python -B proofs/contributions/2026-10-14-broader-return/independent_two_column_audit.py
python -B proofs/contributions/2026-10-14-broader-return/independent_branch_audit.py
python -B proofs/contributions/2026-10-14-broader-return/independent_bound_audit.py
```

Independent audit sources and their reports are retained in the same
directory. All finite-state arithmetic is exact integer arithmetic.
