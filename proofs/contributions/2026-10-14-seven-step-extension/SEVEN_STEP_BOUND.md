# At most three consecutive seven-step 440 returns

Let \(G\) denote the actual decimal pair-word update, with coefficients
ordered from least to most significant position. An admissible word is
canonical and symmetric, has coefficients in \(\{0,\ldots,18\}\), and
has an even center coefficient when its width is odd.

**Theorem (finite certificate).** If an admissible finite word \(Q\) has
width at least 6 and begins with \((4,4,0)\), its orbit cannot begin with
\((4,4,0)\) at all four times \(7,14,21,28\). Thus the number of
consecutive seven-step returns to this prefix is at most three. This
bound is sharp, even when every ordinary addition through those three
returns is required to be nonpalindromic.

The stronger intermediate bound is sharp as well: an actual orbit can
follow the displayed seven-phase prefix-and-overflow schedule for 26
transitions, but no such orbit can follow it for 27 transitions.

The theorem has no safety assumption. It excludes indefinite repetition
of this particular return pattern; leaving the pattern does not imply
that the integer orbit reaches a palindrome. It does not settle the
remaining original gate or the decimal Lychrel problem.

## 1. The forced seven-phase clock

The exact return criterion in
[`../2026-10-14-seven-step-reset/SEVEN_STEP_RESET.md`](../2026-10-14-seven-step-reset/SEVEN_STEP_RESET.md)
shows that a return after seven updates forces the following prefixes
and final overflow bits:

| Phase \(t\) | Prefix \(P_t\) | Overflow \(e_t\) |
|---:|---|---:|
| 0 | \((4,4,0)\) | 0 |
| 1 | \((8,8,0)\) | 0 |
| 2 | \((16,16,0)\) | 1 |
| 3 | \((7,14,7)\) | 0 |
| 4 | \((15,8,15)\) | 1 |
| 5 | \((6,14,14)\) | 0 |
| 6 | \((13,9,9)\) | 1 |

Here \(P_7=P_0\). Equivalently, the actual carries entering the high
three original columns have pattern \(00*0*01\). All 128 binary control
words are checked by the return certificate; exactly four return.
The same calculation applies at every subsequent return.

The local necessity calculation also holds at width 6. Its two
three-column observations are then adjacent; every carry is still the
actual carry of the full addition. The usual padded-middle domain
\(Q=(4,4,0)W(0,4,4)\), with nonempty symmetric \(W\), already has
width at least 7. Padded zero endpoints of \(W\) remain allowed.

## 2. A necessary six-column transition

Consider any symmetric current word \(q\) of width \(L\ge6\), and let
\(p=(q_0,\ldots,q_5)\). Normalize these six coefficients from low to
high with incoming carry 0, obtaining retained digits \(\ell_i\).
Independently describe the actual high end by normalizing
\((q_5,\ldots,q_0)\) with incoming carry

\[
v=\operatorname{carry}(q,L-6)\in\{0,1\}.
\]

Write its retained digits back in outside-index order as \(u_i\), and
write its final carry as \(e\). The next actual six-column prefix is
exactly

\[
T_v(p)_i=
\begin{cases}
\ell_i+u_i,&e=0,\\
\ell_0+1,&e=1,\ i=0,\\
\ell_i+u_{i-1},&e=1,\ 1\le i\le5.
\end{cases}
\tag{1}
\]

This statement does **not** require disjoint low and high observations.
For \(6\le L<12\), they overlap, but both calculations describe the
same actual normalized digits and carries. Overlap correlates the
incoming bit with the low calculation; allowing both possible bits
only enlarges the graph. At \(L=6\), the actual bit is 0. Every actual
transition is included in the two-bit graph in all cases.

The formal relation and its ordinary integer interpretation are supplied
by
[`../2026-10-14-prefix-extension-formal/PrefixExtension.lean`](../2026-10-14-prefix-extension-formal/PrefixExtension.lean),
especially `actual_extension_formula`, `actual_extension_edge`, and
`iterated_extension_edge`. Its column condition is \(1\le k<L\), so
all extensions through index 5 apply at width at least 6. Admissibility
and width do not decrease under \(G\).

## 3. Complete graph and rank certificate

The graph has every state

\[
(t,a,b,c),\qquad 0\le t<7,\quad 0\le a,b,c\le18.
\]

Its observed prefix is \(P_t\mathbin{\|}(a,b,c)\), where \(\|\)
denotes concatenation. Hence it has exactly \(7\cdot19^3=48{,}013\)
vertices. For each of its two inputs \(v\), compute (1), and retain
the edge precisely when the actual computed final overflow is \(e_t\)
and the first three output coefficients are \(P_{t+1\bmod7}\).
The output tail supplies the destination's three free coefficients;
the edge retains label \(v\).

`direct_six_graph.py` enumerates all **96,026** controls and retains
**61,731** labeled edges. No bound on a middle width, middle period,
temporal period, number of iterations, or choice of future inputs is
used in this enumeration. An actual orbit following the prescribed
clock supplies a path in this graph, even if its deeper carry sequence
is aperiodic.

The complete graph is acyclic. The certificate assigns to each vertex
\(z\) a nonnegative integer rank \(r(z)\), with

\[
r(z)=\max\bigl(\{0\}\cup
\{1+r(w):z\longrightarrow w\}\bigr).
\tag{2}
\]

In particular every edge strictly decreases rank. All vertices were
removed by sink deletion; the source also checks (2) directly for every
vertex and edge. The maximum ranks by starting phase are:

| Phase | 0 | 1 | 2 | 3 | 4 | 5 | 6 |
|---:|---:|---:|---:|---:|---:|---:|---:|
| Maximum path length in edges | 26 | 25 | 24 | 26 | 25 | 28 | 27 |

Suppose four consecutive seven-step returns existed. Section 1 would
give the prescribed clock for 28 transitions. Section 2 would project
those transitions to a path of 28 edges starting at phase 0. But its
initial rank is at most 26, contradicting strict rank descent. This
proves the upper bound. In fact no actual orbit can follow this exact
prefix-and-overflow schedule for even 27 transitions from phase 0.

`direct_six_graph.json` retains a 26-edge phase-0 path, demonstrating
that the abstract phase-0 rank bound is exact. Its freely chosen deeper
inputs have not been shown jointly realizable by a finite integer;
sharpness for both the three-return and 26-transition bounds instead
uses the separately checked actual example in Section 4.

The deterministic compressed certificate is
`direct_six_graph.bin.gz`, SHA-256
`6b9fc4d21f146b87e1204619511191074797a613f0fb0ddfe64f5dbdaaf124b4`.
Its uncompressed content begins with `P196DAG1`, then little-endian
32-bit unsigned vertex and edge counts, one 32-bit rank per vertex, and
edge records consisting of two 32-bit vertex IDs and a one-byte input
label. Vertex IDs are
\(t19^3+a19^2+b19+c\). This retains the full graph and rank certificate,
not just aggregate counts.

`independent_direct_audit.py` reconstructs every one of the 96,026
controls using literal ordinary integer normalization of
\(p\mathbin{\|}(18v)\mathbin{\|}p^R\), without importing either graph
producer. It independently reconstructs all edges, obtains a source
deletion topological order, and checks every rank and maximum path
length against the compressed certificate. The result is
`PASS_COMPLETE_DAG` in `independent_direct_audit.json`. Its complete
control outputs are retained in `independent_direct_controls.bin.gz`.
The mathematical projection in Section 2, rather than these disjoint
literal controls alone, justifies necessity when observations overlap.

## 4. Sharpness in an ordinary finite orbit

The independently checked example in the seven-step-reset contribution
starts with

\[
Q_0=(4,4,0)\,(1,1,14,16,14,1,1)\,(0,4,4).
\]

It has the returning prefix at times 7, 14, and 21, and all 21 positive
ordinary successors are nonpalindromic. Its padded middle words are
recorded in `ACTUAL_RETURN_EXAMPLES.json` in that contribution. Its
fourth attempted return has control word \(0010111\), and its prefix
at time 28 is \((4,4,1)\). Thus three returns are possible, while four
consecutive returns are impossible for every admissible middle width.

More precisely, the independent direct audit preserves all 29 actual
states through time 28. This example follows the complete prescribed
prefix-and-overflow schedule for its first 26 transitions and first
deviates at transition 27: its fourth cycle has carry 1 at phase 5,
where the return condition requires 0. Thus the maximum of 26 valid
transitions from phase 0 is attained by an actual finite integer orbit.

## 5. Spatial-lift discovery and prior work

The local extension equation and the use of decreasing ranks to exclude
arbitrary deeper input histories already appear in
[`../../research/main_existence_attempt/correlation_pass/free_clock/STATUS.md`](../../research/main_existence_attempt/correlation_pass/free_clock/STATUS.md)
and its `check_prefix_extension.py`. This contribution applies that
existing method to the exact seven-step return, retains temporal
correlations through a branching spatial extension, and obtains the
complete six-column rank certificate above. No general novelty claim
is made for the method.

The intermediate records are preserved because they explain why simply
searching equal-period coefficient schedules would have been insufficient:

- The first unknown column has only cyclic macro states 0 and 3, each
  with a unique seven-phase self-loop schedule. The 0 schedule forces
  one more schedule, whose next extension graph is acyclic.
- The 3 schedule has a genuinely branching next-column component
  \(\{6,8,9\}\). The analysis retains all of its edges; it does not
  replace this component by an assumed single periodic schedule.
- Keeping each carry label and lifting the full phase graph produces
  retained counts \((V,E)=(7,9)\) at width 4 and \((21,33)\) at
  width 5. Its next raw graph has 399 vertices and 627 edges and is
  acyclic, leaving no recurrent vertices at width 6.

`extension_graph.py/.json` preserve the macro analysis.
`spatial_lift.py/.json` and `lift_width_04.bin.gz` through
`lift_width_06.bin.gz` preserve every completed correlated graph.
`independent_extension_audit.py/.json` and
`independent_lift_audit.py/.json` independently check their arithmetic
and graph exclusions. The direct graph proof in Section 3 includes all
transients, so its finite bound does not depend on an eventual-SCC entry
time or on those exploratory reductions.

## Reproduction

From the repository root, using only the Python standard library:

```sh
python -B proofs/contributions/2026-10-14-seven-step-extension/extension_graph.py
python -B proofs/contributions/2026-10-14-seven-step-extension/spatial_lift.py
python -B proofs/contributions/2026-10-14-seven-step-extension/direct_six_graph.py
python -B proofs/contributions/2026-10-14-seven-step-extension/independent_direct_audit.py
```

The graph calculation is a complete finite certificate for the displayed
local relation. The all-width conclusion additionally uses the exact
actual-word projection in Section 2 and the seven-step return theorem
in Section 1. No successful actual orbit is inferred from a surviving
abstract path.
