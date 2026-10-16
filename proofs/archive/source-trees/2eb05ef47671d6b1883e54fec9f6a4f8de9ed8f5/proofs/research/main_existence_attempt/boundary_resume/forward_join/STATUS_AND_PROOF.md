# Constructive forward/reverse language joins

No finite exterior was found. The arbitrary-width status remains UNKNOWN.
No finite decimal Lychrel witness or existence theorem is supplied.

The completed computation excludes the prescribed 8/17, alternating N,O
exterior through width 17 for the 525 target class, and through width 14
for the archived class of 334 cyclic three-coefficient motifs. These are
all-temporal-period, finite-spatial-width statements. They are not
arbitrary-width exclusions or exclusions of other overflow schedules.

## Exact forward image

An edge-labeled graph represents labels of its finite closed walks.
A letter is the cut state `(a,b,c,z)` for one N/O temporal pair. The
starting graph has one vertex and one loop labeled

    (0,1,1,7), encoded as 41.

It therefore represents the forced exterior cut immediately after the
first coefficient column 8/17, at every positive temporal pair count.

For an old letter enumerate Q in 0..18 and bits d,e. Retain exactly the
choices satisfying

    floor((Q+d)/10) = c,
    R = (Q+a) mod 10 + (Q+d) mod 10,
    R<9 => e=0,   R>9 => e=1,
    0 <= z+e <= 9,
    Q_next = (R+b) mod 10 + z+e in 0..18.

The new letter is

    (floor((Q+a)/10), floor((R+b)/10), d, R-10e).

The raw image graph has one vertex for each pair `(old graph edge,
local option)`. There is an edge from `(E,x)` to `(F,y)` exactly when
the old edges E and F compose and `x.Q_next=y.Q`. Its label is the new
letter of x. A closed walk in this graph is consequently exactly one
valid new spatial column, together with its old cut's closed walk.
Conversely every valid column chooses such a closed walk. Removing
edges outside strongly connected components preserves all closed walks.

Every retained vertex stores its old edge index and local option. This
is sufficient to recover the coefficient column Q,R and the prior graph
walk. No coefficient column or temporal alignment is guessed during
reconstruction.

## Quotients, intersections, and lifting

Each trimmed image is compressed by successive forward and backward
bisimulation quotients. Every quotient edge has a matching edge from
every original member of its source block (or, for a backward quotient,
the corresponding statement in the reversed graph). The local quotient
conditions are independently checked for every saved operation.

Projection sends every genuine graph closed walk to a quotient closed
walk with exactly the same labels. Conversely a quotient closed walk
lifts to a closed walk of a positive power of its label word: repeat the
quotient walk, lift each step, and use repetition of the finite original
vertex at the same quotient phase. Thus the compression preserves
existence of periodic words up to positive powers. It need not preserve
the exact least temporal period.

The product of a forward and reverse graph pairs edges carrying equal
labels. A directed cycle in the product gives a common cyclic cut word.
Its forward and reverse lifts may require different positive powers.
The reconstruction repeats both decoded spatial strips to the least
common multiple of those powers before joining them. The forward strip
is reversed in spatial order during extraction, the reverse strip is
already extracted outside-to-inside, and the mandatory first 8/17 column
is supplied once. A positive result must then pass the separate ordinary
two-direction carry checker, including the overflow seam. There was no
positive intersection in this run.

For a negative result, no lifting hypothesis beyond projection is needed:
an actual exterior would project to a closed walk in both compressed
graphs and hence to a directed cycle in their product. An acyclic
complete product therefore excludes every temporal period at its
specified total exterior width.

## Completed coverage and resource bounds

The forward graphs completed through depth 8, where depth counts spatial
columns after the first 8/17 column:

| Forward depth | Vertices | Edges |
| --- | ---: | ---: |
| 0 | 1 | 1 |
| 1 | 5 | 6 |
| 2 | 4 | 4 |
| 3 | 26 | 40 |
| 4 | 149 | 266 |
| 5 | 810 | 1,530 |
| 6 | 2,764 | 5,286 |
| 7 | 13,249 | 25,340 |
| 8 | 62,862 | 120,332 |

The next raw image required 2,249,617 option vertices, exceeding the
2,000,000 cap. It was not completed. The saved reverse histories cover
depths 0..12 for the 525 class and 0..9 for all 334 motifs. Those reverse
histories had separately stopped at their stated raw graph caps.

All 207 forward/reverse depth combinations were considered:

- 172 products were completely generated and acyclic.
- 35 products exceeded the 2,000,000 product-edge cap and remain UNKNOWN.

The strongest completed products needed for the reported width bounds are:

| Target class | Forward depth | Reverse depth | Exterior width | Product vertices | Product edges |
| --- | ---: | ---: | ---: | ---: | ---: |
| 525 | 4 | 12 | 17 | 703,789 | 526,080 |
| All 334 motifs | 4 | 9 | 14 | 1,178,901 | 860,741 |

The completed 525 product at forward depth 5 and reverse depth 11 is a
second check at width 17, with 1,850,641 vertices and 1,392,645 edges.
The total width is `1 + forward depth + reverse depth`.

These exclusions extend to all smaller positive prefix widths in their
respective target classes. A valid shorter exterior can be padded inward
by exact columns of its periodic bulk until the specified width is
reached. Moving the cut merely cyclically rotates the spatial bulk motif.
Both target classes include all these rotations. Thus a shorter exterior
would give an exterior of the excluded width. This padding argument does
not increase or otherwise prescribe its temporal period.

The 525 target class includes the cyclic spatial permutations of (5,2,5)
and its coefficientwise complement (13,16,13). The larger target class is
the archived 334 cyclic three-coefficient motifs, organized into 66
cycles of the N/O pair map. Singular all-nine normalization is outside
that target enumeration. Nothing here excludes other spatial periods,
nonperiodic bulks, or other overflow clocks.

## Verification and reproducibility

`audit_forward.py` independently checks:

- all 1,640 local options at all 88 letters by ordinary decimal arithmetic;
- completeness of every saved SCC-trimmed forward image, with exact
  origins and edges;
- every saved forward/backward quotient map, 30 operations in total;
- an explicitly lifted cycle from each positive forward depth, with
  eight finite strips replayed using ordinary low and high carries;
- positive product-cycle controls by intersecting graphs with themselves;
- the two strongest product exclusions above, rebuilding every
  equal-label product edge and deleting sinks. The main search used
  source deletion, so this is a separate cycle-absence calculation.

The ordinary strip checks validate finite prefixes and their specified
terminal cuts. They are not complete exteriors and are not reported as
finite integer witnesses. The complete candidate replay code is present
but was not exercised on an actual positive exterior because none was
found.

The results are in `summary.json`, `audit_forward_result.json`, `run.log`,
and `audit.log`. Graph JSON files retain all quotient operations and
column origins. The stable reverse histories they reference are
`../reverse525/bidirectional525/` and `../reverse525/all_bulk_bidir/`.

Reproduce from this recovered project's root:

    python main_existence_attempt/boundary_resume/forward_join/forward_join.py --layers 24 --cap 2000000 --product-cap 2000000
    python main_existence_attempt/boundary_resume/forward_join/audit_forward.py

No timeout, graph-size cap, or finite-width exclusion is interpreted as
an arbitrary-width obstruction. The constructive exterior problem for
these remaining target classes is unresolved.
