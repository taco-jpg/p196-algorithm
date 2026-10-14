# Actual one-column prefix-extension bridge

This contribution supplies eight public Lean theorems connecting the
finite extension graph to actual admissible decimal pair words and the
ordinary integer reverse-and-add operation. It is a necessary local
relation, not a proof that arbitrary graph paths are globally realizable.

## Exact formula and actual carries

For an admissible symmetric coefficient word q of width L, choose any
index 1 <= k < L and put

\[
a=q_k,\quad \alpha=c_k,\quad v=c_{L-1-k},\quad
\gamma=c_{L-k},\quad e=c_L.
\]

Every c here is computed by the actual full-word decimal addition. Then

\[
\gamma=\left\lfloor\frac{a+v}{10}\right\rfloor,
\]

\[
q'_k=(a+\alpha)\bmod10+
\begin{cases}
(a+v)\bmod10,&e=0,\\
(q_{k-1}+\gamma)\bmod10,&e=1,
\end{cases}
\]

and the low carry entering the next spatial column is

\[
c_{k+1}=\left\lfloor\frac{a+\alpha}{10}\right\rfloor.
\]

That last quantity advances in space **within the same addition**. It is
not the carry entering position k at the next orbit time.

The theorem `actual_extension_formula` combines the existing exact
folded-carry and emission identities. Overflow changes the reflected
alignment from L-1-k to L-k, giving q_(k-1) in its branch.

## Width and quantifier conditions

The necessity theorem requires only 1 <= k < L. The stronger disjointness
condition L >= 2(k+1) is unnecessary here: when the two sides overlap,
their actual carries are correlated, but all displayed equations remain
valid. Disjointness can matter when constructing realizations for freely
chosen local controls, which is a different direction.

`actual_extension_edge` supplies the graph's existential deeper bit using
the actual carry v. `extensionEdge_iff_zero_or_one` shows that the graph's
two enumerated choices are exhaustive. `actual_extension_bounds` checks
all coefficient bounds 0..18 and carry bounds 0..1 used by enumeration.

`iterated_extension_edge` propagates the statement over the actual
`iterPairs` orbit. It derives admissibility and enough width at every
time. Its controls are the actual carries at that time, not an independent
chosen sequence.

`numeric_extension_realization` supplies a canonical representation of
the actual next ordinary integer and identifies the graph's next
coefficient with its actual digit-pair coefficient.

## Scope of graph exclusion

If a graph construction includes every edge described by this necessary
relation, an actual orbit with that graph's prescribed boundary data
would have to supply such edges. Excluding both deeper-carry choices at a
particular actual transition is impossible.

This module does not verify an external graph's entire enumeration,
establish a surviving graph path as a finite integer orbit, or produce a
Lychrel witness. Those are separate proof obligations. No palindrome
avoidance or safety assumption is needed for the local necessity result.

## Reproduction

```sh
python check.py /path/to/lean-4.19.0/bin/lean
```

The checker rebuilds the exact dependency and contribution sources in a
fresh directory and audits all eight public theorems. The private width
monotonicity helper is included transitively. Only `propext`,
`Classical.choice`, and `Quot.sound` are permitted. The final report
records SHA-256 and Git blob hashes after a source-stability check.

The first combined compilation found a misspelled existing helper name,
`NormalizationBridge.next_admissible`; replacing it with the actual
`NormalizationBridge.admissible_next` resolved the issue. The mathematical
formula compiled unchanged. The final interface was then strengthened
from a disjoint-width assumption to the weaker 1 <= k < L condition.
