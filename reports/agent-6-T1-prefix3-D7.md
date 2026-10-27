# Agent 6 — T1.C-prefix3-D7: center-pruned graph and a projected 42-cycle

## Precise scope

**COMPUTED:** The three-exterior-prefix / exact-center overapproximation from parent draft PR #345 becomes **cyclic** when center width bound rises from 6 to 7. An explicit 42-transition closed projected walk has `sum(g)=16`, `sum(v)=8`, and `max |C|=7`. It is **NOT** a full exterior B cycle and is **NOT** accepted by `Agent120.Neutral.cycleOK 10`; in particular **no decimal Lychrel existence claim** follows. The prior R3,D6 acyclicity and necessary `some |C|>=7` lower bound remain valid. This projected example shows only that the same *three-coordinate relaxation* cannot establish `some |C|>=8` by graph acyclicity.

## Soundness of center-only pruning (PAPER PROOF)

Project every R3 full-product edge to its symmetric-center transition with incoming carry `e`, overflow bit `g`, and arbitrary legal neutral-9 pair trim. A closed full-product walk projects to a closed walk in the center-only directed graph. In any finite graph, each vertex on a directed closed walk survives Kahn indegree-zero deletion. Therefore, **before constructing the expensive product graph**, it is safe to remove every center state eliminated by Kahn on the center-only graph; no full-product cycle is lost. The residual is an overapproximation of cyclic SCCs (some downstream transient vertices may remain), which is harmless.

The center-only enumeration at D7 consists of **144,792** valid carry-flip states, **183,800** directed edges. Center-only Kahn removes **137,886** and retains **6,906**. Coupling only these 6,906 states with all 6,498 padded exterior three-coefficient states via the *same overflow bit* is sufficient for all projected cycles, with completely unrestricted underlying exterior B length.

## Computed graph and explicit closed projected walk

Compile the 166-line standalone source (depends on no other repository file):

```sh
c++ -O3 -std=c++17 -Wall -Wextra -Wpedantic calculation/agent-6/prefix3_pruned_d7.cpp -o /tmp/a6-d7
/usr/bin/time -f 'wall=%es peak_kb=%M' /tmp/a6-d7 3 7
```

Exact observed output counts:

```text
center_prune original=144792 removed=137886 survivor=6906
R=3 D=7 P=6498 C=6906 states=44875188 edges=61129574 removed=43990024 residual=885164 status=CYCLIC_CORE
PROJECTED_ONLY_WITNESS period=42 sumG=16 sumV=8 maxC=7
```

Wall 1.48 seconds, RSS 359,152 KiB in sandbox; no resource cap fired. Kahn's residual alone does not certify any particular remaining vertex is on a directed cycle. The program therefore traces actual residual predecessors until repetition and replays the resulting **42-step closed directed walk** before printing it. (The center Kahn filter itself is a necessary reduction; it does not change the graph's cycles.)

Projected cycle streams, indexed starting from the extracted representative:

```text
g=101000101001001010100101000101001001010100
e=010100010111000101010101011101000111010101
v=000000010000200000010000000010000200000010
```

The first three projected prefixes / center words from its 42 explicit states are:

```text
t=0 Bprefix=[14,3,7]  C=[18,13,13,18]  e=0
t=1 Bprefix=[5,8,10]  C=[8,13,8,13,8] e=1
t=2 Bprefix=[10,17,1] C=[18,6,18,6,18] e=0
```

The standalone command emits **all 42** states, closing at the first. A separate Python implementation, using independent digit-by-digit normalization and both unknown reverse carry choices, checked every one of the 42 projected exterior updates, every one of the 42 exact center updates and its selected trim, center-carry flip at source and target, closure, and `sum(g)=16=2*sum(v)`: **PASS**.

The projected B-prefix returns after 21 positions but there is **no constructed finite exterior list B** closing under all 42 transitions. Do not represent this as a `cycleOK` certificate or Lean proof.

## Resource limitations, provenance, missing checks

The *unpruned* D7 product has about 941 million vertices and would exceed the current container's 4 GiB memory budget with a naïve 32-bit indegree/queue representation. The center-only preprocessing reduces the graph safely to 44.9 million vertices, requiring about 350 MiB. The code guards the product at <=100 million states and reports unsupported bounds instead of claiming absence. No higher-center bound was exhausted.

Credits: Agent 4 original first-digit exterior theory (#290); Agent 6 first-coordinate/exact-center graph (#313); Agent 101 R2,D5 graph (#332); Agent 6 R3,D6 completed negative (#345). This result is an **independent targeted D7 diagnostic** of that mathematical relaxation, not a negative theorem for all widths. `python3 tools/verify.py --changed` has not been executed in a full checkout; review PR is **UNVERIFIED / DO NOT MERGE**, pending second-agent source audit.
