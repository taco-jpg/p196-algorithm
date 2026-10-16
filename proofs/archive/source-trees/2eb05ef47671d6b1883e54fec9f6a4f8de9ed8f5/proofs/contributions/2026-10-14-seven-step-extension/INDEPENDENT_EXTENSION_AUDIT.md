# Independent audit of the seven-step spatial extension

The one-column relations in `extension_graph.json` pass an independent
literal-integer check. They imply a useful all-length necessary condition:
**if the prefix `(4,4,0)` returns every seven updates forever, then after
the first return the first five coefficients must be `(4,4,0,3,b)`, where
`b` is in `{6,8,9}`.** This is a necessary condition, not an infinite orbit
construction or a proof of nonpalindromicity.

The graph with states `{6,8,9}` has genuine branching, so replacing it by
one selected periodic path would lose possible actual trajectories. The
additional correlation-preserving lift audited in Section 5 eliminates
that branch. Together these checks prove that no admissible initial word
can return to the prefix `(4,4,0)` every seven updates forever. The direct
graph in Section 6 strengthens this to the sharp bound of three
consecutive returns, without an eventual-component argument.

## 1. Why every actual orbit gives graph edges

All coefficients are low-to-high. Suppose a canonical symmetric whole
pair word has width `L`, prefix `p` of length `k`, and next coefficient
`a`. Assume `k >= 1` and `L >= 2(k+1)`. Let `alpha` be the carry after
normalizing the low prefix, and let `v` be the actual carry entering the
high occurrence of `a`. Write

\[
\gamma=\left\lfloor\frac{a+v}{10}\right\rfloor,
\qquad d=(a+\alpha)\bmod10.
\]

The high prefix receives carry `gamma`. Its normalization determines
the whole final overflow `e` and the next outer `k` coefficients. The
next coefficient at index `k` is exactly

\[
a' = d+
\begin{cases}
(a+v)\bmod10,&e=0,\\
(p_{k-1}+\gamma)\bmod10,&e=1.
\end{cases}
\tag{1}
\]

For `e=0` the second contributing digit is at old index `L-1-k`. For
`e=1` physical reflection uses width `L+1`, and that digit is at old
index `L-k`, the first high-prefix column. This accounts for the change
of term in (1).

Each graph phase keeps both possibilities `v=0,1`, then retains only
those edges for which the outer prefix and overflow equal the prescribed
next phase. Actual carries therefore yield a path in the graph. No
independent choices of successive carries are asserted to be realizable.
This direction alone is sufficient for an exclusion proof.

Each accepted seven-step return increases whole width by exactly three.
Thus, in any hypothetical infinite sequence of returns, every fixed
finite prefix width eventually satisfies the displayed disjointness
bound. Middle zeros are retained; no positivity assumption is imposed
on the newly observed coefficients.

## 2. Complete first-column graph and the zero branch

For the prescribed three-column clock, the only nonempty seven-phase
macro transitions are:

| Start | Possible endpoints |
|---:|---|
| 0 | 0, 4, 5, 6, 7, 8, 9 |
| 1 | 0, 2, 3, 4, 5, 6, 7, 8, 9 |
| 2 | 0, 8, 9 |
| 3 | 0, 2, 3, 4, 5, 6, 7, 8, 9 |

All other states have no outgoing macro edge. Hence an infinite path is
eventually constantly `0` or constantly `3`. The self-edges have unique
coefficient sequences at phases 0 through 6:

\[
\begin{aligned}
0 &: (0,0,1,1,3,9,9),\\
3 &: (3,6,13,4,9,5,12).
\end{aligned}
\]

The statement is an eventual one: a graph path could traverse the `3`
self-loop arbitrarily many times before leaving for `0`. Finiteness of
the graph alone does not give a uniform time to the final cyclic
component.

Now suppose an actual trajectory eventually follows the zero clock.
Extending by one further coefficient gives only these macro edges:

| Start | Possible endpoints |
|---:|---|
| 4 or 7 | 0, 1, 2, 3, 4, 5 |

The only cyclic state is `4`, so the new coefficient must eventually
follow its unique phase sequence `(4,9,9,11,3,6,13)`. Extend once more.
The only macro edges then are

\[
\{9,14,17\}\longrightarrow\{10,11\},
\]

and neither `10` nor `11` has an outgoing edge. This graph has no
infinite path, contradicting the actual trajectory. The width growth
noted in Section 1 justifies observing all six outer columns at this
stage, regardless of the initial middle width. Therefore **no actual
infinite return trajectory can eventually follow the zero clock**.

For completeness, the finite-graph fact used here follows by passing to
the acyclic directed graph of strongly connected components. An infinite
path can change component only finitely often, and the component in which
it eventually remains must contain a directed cycle. A singleton cyclic
component with a unique one-period coefficient path forces the displayed
phase clock. This proof does not assume that every surviving graph path
has an actual realization.

## 3. The remaining necessary prefix

The zero-branch exclusion sharpens the initial eventual statement. In
the first-column graph, every infinite future beginning at `0` or `2`
eventually stays at `0`, and every state outside `{0,1,2,3}` is dead.
Beginning at `1` or `3`, every edge except the one to `3` either is dead
or eventually leads to `0`. Consequently a perpetual actual return
trajectory must start with first middle coefficient in `{1,3}` and have
that coefficient equal to `3` after every completed return.

When the initial middle has width one, the first observed coefficient is
central, but the necessary outer-index calculation still holds: its
actual incoming carry is one of the two retained possibilities. Equally,
one can apply the argument after the first width increase and inspect
the finite first-column transition separately. No free carry choice at
an overlapping center is needed for necessity.

Under the forced `3` clock, the next coefficient's only cyclic component
is `{6,8,9}`. Every other state has finite deletion rank. Its internal
macro edges are exactly

\[
6\to\{6,8,9\},\qquad 8\to6,\qquad 9\to\{8,9\}.
\]

Thus at every return from the first onward the necessary prefix is
`(4,4,0,3,b)` with `b` in `{6,8,9}`. Initial whole width is at least
seven and the first return has width at least ten, sufficient for these
five-column observations. Following this graph indefinitely remains only
a necessary condition. A deeper extension must retain its branching and
the correlation between each edge and the carry required from the next
column. Section 5 audits that further extension.

## 4. Reproduction and preserved controls

Run:

```sh
python -B proofs/contributions/2026-10-14-seven-step-extension/independent_extension_audit.py
```

The checker does not import the graph generator. For every phase prefix
`p`, coefficient `a` in `0..18`, and deeper bit `v`, it constructs

\[
q=p\,(a,18v,a)\,p^R.
\]

The even center `18v` forces outgoing carry `v` independently of the
carry entering it. The word is symmetric and admissible. The checker
evaluates its coefficient polynomial as an ordinary integer, extracts
the decimal digits, and forms their reflected pair sums. This supplies
an independent local realization of each proposed branch, including
rejected branches, without using (1) in the computation.

All **1,064** labeled phase controls pass. The checker recomputes every
macro path and obtains strongly connected components by transitive
closure, independently of the generator's Tarjan implementation. All
macro edges, unique self-period paths, components, and deletion ranks
agree. `independent_extension_audit.json` retains every literal control
and records hashes of the exact input and producer source it checked.

This audit proves local relations and finite graph exclusions. It does
not turn a sequence of separately realized branches into a single actual
decimal trajectory, and it does not remove the safety obligations of the
seven-step return theorem.

## 5. The correlated lift excludes a perpetual return

The remaining fixed four-column clock gives a directed graph with seven
phase vertices and nine edges. Each edge is labeled by the carry entering
the high four-column prefix. To expose a fifth column with coefficient
`a`, retain a deeper carry `v` only if

\[
\left\lfloor(a+v)/10\right\rfloor
=\text{the parent edge's carry label}.
\tag{2}
\]

The next coefficient is then determined by (1). Equation (2) preserves
the correlation with the particular parent transition; taking the union
of allowable carries without preserving its edge would not suffice.

The resulting raw width-five graph has 133 vertices and 171 labeled
edges. Its cyclic vertices form one component with 21 vertices and 33
edges. Any actual infinite path has a tail in this component. Extend
this component by one more column, again using (2). The raw width-six
graph has 399 vertices and 627 edges. It is acyclic.

**Theorem.** For every admissible initial pair word
`Q0=(4,4,0) W (0,4,4)` with nonempty padded middle `W`, there is a positive
integer `j` such that `G^(7j)(Q0)` does not have prefix `(4,4,0)`.

**Proof.** If every seventh update returned, Section 2 would exclude the
eventual zero clock, forcing the four-column clock in Section 3. The
actual trajectory gives an infinite path in its labeled graph. At the
next column it gives an infinite path in the raw width-five graph, hence
has a tail in its cyclic component. At the sixth column this actual tail
would give an infinite path in the acyclic width-six graph, a
contradiction. At each finite level the observed whole width is
sufficient after finitely many returns because every return adds three
columns. Actual carries supply all labels, so the proof never requires
free temporal control or a converse realization theorem. ∎

This theorem excludes perpetual eligibility for this specific seven-step
map. It does not imply a palindrome occurs when eligibility is lost, nor
exclude a different later reset or a different infinite construction.

`independent_lift_audit.py` does not import either producer. It stores
full prefix tuples and computes each transition by integer normalization
of `p (18v) p^R`. It reconstructs the parent carry from the literal
coefficient integer, checks (2), and compares all three saved graph
checkpoints. It identifies cyclic width-five vertices by independent
reachability searches. At width six, Kahn's topological sort removes all
399 vertices; a stored integer rank strictly decreases along each of
the 627 edges. The maximum such rank is 10.

All **1,078** local arithmetic controls, all raw graphs, the complete
topological ordering, decreasing ranks, and hashes are preserved in
`independent_lift_audit.json`. The rank 10 describes this already-trimmed
graph; it is not asserted to be a bound on the initial trajectory's
transient before it enters the graph.

Run the independent audit with:

```sh
python -B proofs/contributions/2026-10-14-seven-step-extension/independent_lift_audit.py
```

## 6. Independent audit of the sharp three-return bound

`direct_six_graph.py` includes every phase and every three further
coefficients, rather than first removing transient states. Its graph has
48,013 vertices and 61,731 edges. `independent_direct_audit.py` reconstructs
all **96,026** controls by literal integer normalization of symmetric
words with a central coefficient 0 or 18. No producer module is imported.
Every retained edge agrees, including its carry label.

The independent checker uses source deletion, while the producer uses
sink deletion. All 48,013 vertices are removed. Backward evaluation on
the resulting topological order independently recomputes every stored
rank. The maximum ranks by phase are exactly
`(26,25,24,26,25,28,27)`. Thus phase 0 admits at most 26 consecutive
transitions of the required clock, and four complete seven-step returns
would require 28. The width-independent proof, including the actual
overlap-compatible projection, appears in `SEVEN_STEP_BOUND.md` and
passes this independent review.

The actual example with middle `(1,1,14,16,14,1,1)` follows the prescribed
prefix and overflow clock for 26 transitions and first deviates at time
27. It returns at times 7, 14, and 21, and the first 28 ordinary
successors are nonpalindromic. The complete actual pair-word sequence
through time 28, its prefix comparisons, overflows, ranks, and palindrome
tests are retained in `independent_direct_audit.json`. Consequently both
the three-return bound and the 26-transition clock bound are sharp for
actual words; sharpness does not rely on realizing an abstract graph
path's carry choices.

The checker validates the producer's entire compressed certificate and
its 26-edge abstract witness. It also preserves every accepted and
rejected arithmetic control in `independent_direct_controls.bin.gz`,
with a precise implicit-input schema and hashes in its JSON report.
Run:

```sh
python -B proofs/contributions/2026-10-14-seven-step-extension/independent_direct_audit.py
```
