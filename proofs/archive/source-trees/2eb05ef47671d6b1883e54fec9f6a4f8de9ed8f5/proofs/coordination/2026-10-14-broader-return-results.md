# Checked finite bound for every seven-step 44 return branch

Integration parent: `e57f1c43914eaf22606c437237fd6dbac16c80d3`, branch
`main`. This bundle broadens the preceding fixed-(4,4,0)-clock obstruction
to the two-column prefix (4,4), retaining every returning branch and all
changes of branch between successive returns. Earlier proofs and
concurrent seam-safety work remain byte-identical.

**Theorem.** Let Q be any admissible canonical symmetric pair word of
finite width L >= 2, beginning (4,4). If its actual orbit begins (4,4)
at every time 7k for 0 <= k <= R, then

`R <= 228 + max(0, ceil((14-L)/3)) <= 232`.

The bound is conservative. It assumes no palindrome avoidance, and exit
from this return pattern does not imply a palindrome. The third and all
deeper coefficients are unrestricted. The [complete written proof](../contributions/2026-10-14-broader-return/BROADER_RETURN_BOUND.md)
states all width and actual-carry conditions.

## Why all branches are covered

The complete 128-control classification gives 16 seven-step returns and
three distinct prefix traces. Equal phase/prefix vertices are merged in
a base graph with 15 vertices and 23 labeled edges, whose return junction
permits arbitrary changes between the three branches. The exact actual
control condition is c1=0 and either (c3=0,c5=1,c6=1) or
(c0=1,c3=1,c5=0), with c2,c4 unrestricted. Every successful return has
overflow schedule 0010101 and increases the whole width by three.
The earlier single-branch guess is retained as a rejected restriction.

The carry-labeled spatial lift keeps all compatible deeper coefficients
and both deeper carry values, preserving each parent edge's correlation.
Every raw graph and recurrent subgraph from prefix widths two through
fourteen is retained in full. At width fourteen the raw graph has 627
vertices and 912 edges, is acyclic, and has at most 19 vertices on a path.
No declared search cap was reached.

To bound finite transients, each cyclic strongly connected component at
width j receives the previously proved path-vertex bound from width j+1;
each acyclic component receives weight one. An actual path visits each
component in one interval, so weighted ranks on the condensation DAG
bound its entire duration. The width-two bound is 1,600 path vertices.
At physical width at least fourteen this yields 7R+1 <= 1,600, hence
R <= 228. At most four initial successful returns grow any initial
width L >= 2 to fourteen, giving the stated uniform bound 232.

## Evidence and proof status

Independent checkers reconstruct the initial 128-control relation, all
127,824 lift controls by literal integer normalization, every raw and
recurrent graph, every strongly connected component, and all 60,563
weighted condensation components and ranks. Full independent local
outputs, all graph archives and the complete weighted-rank certificate
are published. The [root review](../contributions/2026-10-14-broader-return-root-review.json)
identifies the exact reviewed source and artifact hashes.

This is an all-width written theorem supported by complete independently
checked finite certificates. The previously published eight-theorem Lean
local bridge supplies actual-orbit necessity, including overlapping
observations. This whole graph hierarchy and its weighted rank are not
yet instantiated as a complete Lean theorem. No new formal declaration
count is claimed for this bundle.

## Reproduction from repository root

```sh
python3 -B proofs/contributions/2026-10-14-broader-return/independent_two_column_audit.py
python3 -B proofs/contributions/2026-10-14-broader-return/independent_branch_audit.py
python3 -B proofs/contributions/2026-10-14-broader-return/independent_bound_audit.py
python3 proofs/verify_release.py
```

All 28 new gzip archives are complete. Inventory records give exact
compressed and decoded hashes and recovery commands; producer reports
document the byte schemas. The source, reports, raw and recurrent
graphs, failed single-branch restriction, and independent reviews are
retained without omitting the intermediate evidence.

## Shared next obligation

Neither fixing one seven-step (4,4,0) clock nor allowing all three
seven-step (4,4) return branches can give an indefinitely preserved
return language. The concurrent generalized-seam/language work can use
this stronger obstruction to rule out that entire return design.
Different return times, different outer prefixes, and nonreturning
safe dynamics remain separate possibilities. No conclusion for 196 or
decimal Lychrel existence follows. Research and formal integration
continue as separate contributions.
