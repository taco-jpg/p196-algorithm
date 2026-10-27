# Agent 6 — T1.C-prefix3-maxpath: uniform 55-step exit bound

## Scoped result (PAPER PROOF + COMPUTED)

This is a quantitative refinement of the sound necessary base-10 A120 center + padded-exterior-prefix graph from parent draft PR #345 (Agent 6's T1.C-prefix3-product-D6). For **every** legal `Agent120.Neutral` chain remaining under `|C_t|<=6`, regardless of its exterior B width, trim choices and temporal period, at most **54 consecutive transitions** can remain entirely within that bound. Equivalently, every length-55 chain of transitions satisfying the unchanged A120 `Hyp/edgeOK` either has an intermediate center coefficient word `|C|>=7` or cannot exist. **This is not a bound on ordinary 196 reverse-and-add steps.**

## Why a longest-path computation certifies the bound (PAPER PROOF)

Every actual chain induces a path in the finite graph of the parent result, because the exterior prefix overapproximates both possible unknown reverse carries while exact center transitions retain all symmetric 9-pair trims and carry-flip conditions. A directed acyclic graph has a well-defined finite longest path. On a Kahn topological ordering, initialize `dist=0` at every vertex and propagate `dist[to]=max(dist[to],dist[from]+1)` on each edge before decrementing indegrees. For a DAG this computes the maximum edge count of any path ending at every vertex. The maximum over all vertices is therefore a bound on **every** real trace inside the subgraph, not just on recurrent cycles.

## Computed exact values

Run the parent C++ enumerator augmented with one array and the topological longest-path propagation (the only changes to the parent code):

```sh
c++ -O3 -std=c++17 -Wall -Wextra -Wpedantic calculation/agent-6/prefix3_center.cpp -o /tmp/a6-maxpath
/tmp/a6-maxpath 1 4
/tmp/a6-maxpath 2 5
/usr/bin/time -f 'wall=%es peak_kb=%M' /tmp/a6-maxpath 3 6
```

| Exterior prefix R | Center length cap D | Vertices | Edges | Residual after Kahn | Longest directed path |
|---:|---:|---:|---:|---:|---:|
| 1 | 4 | 13,608 | 18,362 | 0 | 20 |
| 2 | 5 | 2,603,988 | 2,955,526 | 0 | 37 |
| **3** | **6** | **94,039,056** | **129,065,442** | **0** | **54** |

The sandbox R3,D6 maxpath run completed in 4.82 seconds, peak 1,105,264 KiB (about 1.05 GiB); no cap fired. A different pure-Python SCC/indegree graph implementation independently reproduced `R1,D4: 13,608 peeled, max_path_edges=20`. The R1/D4 and R2/D5 state/edge counts match the prior Agent 6/101 results as additional controls. This is a same-agent independent code check of the small case only, not second-agent reproduction of the 94-million-state long-path bound.

## Scope and provenance

This requires the parent PR #345 graph soundness/acyclicity result; the new contribution is the **sharp maximum path length within the same overapproximation**. It adds no Lean theorem and does not change the mathematical checker. Do not infer an upper bound for all centers or the actual integer 196 trajectory. No `RESULTS.md`/`README.md` modifications.

**UNVERIFIED / DO NOT MERGE** pending `python3 tools/verify.py --changed` on the actual full checkout, source review, and independent second-agent arithmetic confirmation. Parent dependency: draft PR #345; coordination: #289; scope: T1.C-prefix3-maxpath.
