# Independent audit of the scalar clock `(4,8,16,7,15,6,13)`

The `seven_4` hierarchy passes a complete independent arithmetic and graph
audit. It excludes perpetual repetition of this scalar outer-coefficient
clock with **no condition on the second coefficient or deeper temporal
behavior**. The weighted finite certificate bounds complete periods by
232 once the whole word has width at least 14. The elementary short-word
check below makes 236 a uniform bound for every initial width.

This audit concerns `seven_4` only. It makes no verification or exclusion
claim for the other scalar-clock probes.

## Exact scalar root

For current outside coefficient `a`, let `v` be the actual carry into the
highest original column. Put `e=(a+v)//10`. The next outside coefficient
is exactly

\[
a'=(a\bmod10)+
\begin{cases}(a+v)\bmod10,&e=0,\\1,&e=1.\end{cases}
\]

This formula applies even at whole width one, where the actual input is
zero. The proposed seven-phase scalar clock retains input pattern
`00*1*1*`: phases 0, 1, 3, and 5 require inputs 0, 0, 1, and 1; phases
2, 4, and 6 allow both. Hence the root graph has seven vertices and ten
labeled edges, with overflow word `(0,0,1,0,1,0,1)` and width gain three
per complete period.

Each further spatial lift must match the specific parent edge's carry
label, rather than an uncorrelated set of allowable carries. The audit
checks that match using actual carries reconstructed from a literal
symmetric coefficient integer. Retaining every additional coefficient
in `0..18` and both deeper carries preserves every actual trajectory.
When low and high observations overlap, their actual carries remain
consistent; the graph permits extra possibilities but removes none of
the actual ones.

## Full hierarchy audit

`independent_scalar_audit.py` imports no graph-producer code. It decodes
every raw and retained checkpoint, reconstructs each full prefix through
its parent mapping, and checks its recorded low carry by evaluating the
prefix polynomial as an integer. For each prefix `p` and input `v`, it
normalizes

\[
p\,(18v)\,p^R
\]

as an ordinary integer. This supplies an independent local arithmetic
oracle; the central coefficient forces the requested high-prefix input.
The oracle checks both accepted and rejected controls, the exact next
prefix, overflow, and the carry into its parent prefix.

All **128,644** local controls pass, and every raw edge matches. Tarjan's
algorithm independently recomputes every strongly connected component;
the producer uses Kosaraju's algorithm. All retained vertices, edges,
component counts, and raw and retained file hashes match. The final
width-14 raw graph has 627 vertices and 912 edges. A separate Kahn
ordering removes all vertices, and its maximum path length is 18 edges.

The raw graphs at widths two through four were checked in full; equal
later graph sizes were not used as a substitute for checking them. Every
local control outcome is saved in
`seven_4/independent_scalar_controls.bin.gz`. The corresponding JSON
report records the schema, hashes, complete component partitions, and
final DAG certificate.

## Weighted bound and short widths

`independent_scalar_bound_audit.py` checks the complete weighted
condensation certificate against the independently obtained component
partitions. It checks all **60,952** components, every quotient edge,
every component weight, and every weighted rank in a separate component
ordering. Its topological calculation agrees with all reported ranks.

The bound counts vertices, including both endpoints. A cyclic component
interval of an actual path lifts into the next raw graph and has at most
that graph's vertex bound. Each acyclic component is a loop-free singleton
and contributes one vertex. Since the condensation graph is acyclic, the
weighted longest path bounds the sum of the interval lengths. This
accounts for every finite transient without assuming a uniform time of
entry into a cyclic component.

The root bound is 1,629 vertices, hence 1,628 edges. An actual orbit
following `R` complete periods has `7R+1` vertices, so

\[
R\le\left\lfloor\frac{1628}{7}\right\rfloor=232
\qquad(L\ge14).
\]

For arbitrary initial width `L`, each successful period adds three
columns. Thus the usual preparatory allowance is
`max(0,ceil((14-L)/3))` periods. For `L>=2` this is at most four,
giving `R<=236`.

At `L=1` the unique admissible initial word with outside coefficient four
is `(4)`. Its exact pair-word trajectory is

\[
(4)\longmapsto(8)\longmapsto(16)
\longmapsto(7,7)\longmapsto(14,14).
\]

The desired outside coefficient at time four is 15, so this word completes
zero periods of the clock. It follows that **236 is a valid uniform
bound for all initial widths**. No sharpness claim is made, and leaving
this clock does not imply that a palindrome occurs.

Run the independent checks from the repository root:

```sh
python -B proofs/contributions/2026-10-14-scalar-clock/independent_scalar_audit.py
python -B proofs/contributions/2026-10-14-scalar-clock/independent_scalar_bound_audit.py
```
