# Z03 running notes

- Registered `CLAIM agent-Z03` on issue #475 (comment 6492081251). Route: phase 0, `|J|=5`, lexicographic U ranks 3/15/27.
- Read the current coordination instructions, T* target, T12 reset-cone theorem, R30 exact pairword semantics, the latest FEED/DONE/ALERT lines available on #475, and the existing V16/W17/W38 local-collar implementations.
- Fixed U ordering: lexicographically sorted 30 distinct charge-zero rotations. The assigned rows are `(2,9,16)`, `(9,8,10)`, `(16,2,9)`.
- Implemented a 64-lane bit-sliced exact local carry engine. It evaluates the endpoint-only W9 restoration property, while retaining all J words even if an intermediate phase damages W9. The strict-per-phase lane is diagnostic only.
- Completed nine disjoint census shards: three ranges `[0,1000000)`, `[1000000,2000000)`, `[2000000,2476099)` for each assigned U. Each U shard total is 2,476,099; total tested is 7,428,297.
- Results: endpoint W9 restorers `0`; strict-per-phase W9 survivors `0`. Every candidate's first endpoint mismatch is in W9, offset `-25..-11` from the `W9|J` cut. Histograms are in `census_summary.tsv`.
- Independent controls: scalar-vs-bit-sliced recurrence checks at all 120 phases for eight fixed J codes per U; Python big-integer controls at `(14,100)` and scaled widths `(20,100),(40,200),(80,400),(160,800)` all agree with the local recurrence and exact clock.
- Logical caution: do not use the strict W9 MDD to prune endpoint-only candidates; it could discard a temporary-damage/recovery path. The exhaustive endpoint lane therefore had no MDD pruning.
- This negative result redirects the phase-0 J5 slice only. It is not a global no-go and does not test a distinct two-epoch family with W9 damage at t=120 and repair at t=240.
