# Sharp consecutive-change bounds for p12/m9 one-step-invisible bulk perturbations

**PAPER PROOF, all finite widths.** Work with the specific reachable decimal p12 spatial-m9 lattice and overflow word 100010001000. For the nine time phases with no overflow, consider any two different symmetric pair-coefficient words (entries 0..18) with identical exterior and centre and whose only lower-half changes are finitely many sites entirely within the established bulk. The bulk is long enough on both sides of the changed support for the incoming/outgoing carries to reset; both words normalize without length change. Suppose their full next reverse-and-add pair-coefficient words agree. Then, among the lower-half sites, the longest run of consecutive changed coefficients has length at most 3 in phases 1,5,9 and at most 5 in phases 2,6,10. Phases 3,7,11 admit no such finite-support collision. The 3 and 5 bounds are attained by ordinary canonical decimal integers, so they are sharp. Nothing here states nonexistence of periodic centres or a decimal Lychrel orbit.

## Exact 36-vertex graph

For baseline coefficient q and normalized next-pair coefficient s at a bulk site, let (a,b) denote the lower incoming carry and the upper outgoing carry under the modified pair word. Enumerate replacement x=0..18 and incoming upper carry u=0,1. A valid edge exists exactly when `(x+u)//10=b` and `(x+a)%10+(x+u)%10=s`; its new cut state is `((r+1)%9,(x+a)//10,u)`. Label it CHANGED iff x!=q. There are only nine spatial residues r and four carry pairs, 36 states. Both baseline q,s and entering baseline cut carries repeat every nine columns, which the scripts check from ordinary exact normalization for both input-length parities.

Let B be the nine phase-specific baseline carry-cut states (one for each residue). Let I be the state set one CHANGED edge after any B. Let R be all states reachable from I using *any* valid edge and C be all states that can subsequently reach B using *any* edge. Every coefficient position inside a finitely supported invisible perturbation after its first changed site lies on a path in the induced set A=R∩C. This direction uses the actual unchanged exterior, equal complete next pairword and eventual non-neutral carry reset. A run of k consecutive changed coefficients gives k consecutive CHANGED edges in A, except that its first edge may originate at a baseline cut before entering A. The program explicitly maximizes both cases, including one initial CHANGED edge followed by a longest path in A.

Exhaustive DFS proves the CHANGED-edge graph induced by A is acyclic. Longest-path dynamic programming on that exact DAG yields:

| temporal phase | max changed run | \|A\| vertices | all edges | first changed successors |
|---|---:|---:|---:|---:|
|1|3|15|39|2|
|2|5|15|39|2|
|3|0|0|34|0|
|5|3|15|39|2|
|6|5|15|39|2|
|7|0|0|34|0|
|9|3|15|39|2|
|10|5|15|39|2|
|11|0|0|34|0|

Every graph is fully decided, with no width cap or solver heuristic. The output `bounds.json` records this 9×4 table. Since k+1 consecutive changed positions would give a path of k+1 CHANGED edges, it is excluded for arbitrary bulk spans. Partitioning a support interval into blocks of 4 or 6 therefore gives at least floor(L/4) or floor(L/6) unchanged sites inside a span of length L in the respective phase. For phases 3,7,11 only the unmodified word can have a one-step identical pairword within the stated finite-bulk perturbation class.

## Sharpness and independence

The already published phase-1 seven-column motif `q=[4,5,10,14,13,12,9]` replaced by `[9,5,0,15,3,12,14]` has changed-bit pattern `1011101`, with maximum streak 3. The phase-2 motif `q=[9,11,1,10,8,5,9]` replaced by `[14,10,11,9,18,5,4]` has pattern `1111101`, with maximum streak 5. The time-shifted phases 5/9 and 6/10 use the same respective spatial motifs in the corresponding lattice row. Both positive controls are independently replayed as ordinary canonical positive integers at source lengths 400,401,800,801, for *exact* entire next pairword agreement.

The independent checker does NOT import the primary implementation. It builds its own 36×36 Boolean adjacency matrices using 36-bit masks, computes full and transpose transitive closures, and finds longest CHANGED paths by successive Boolean matrix-vector multiplication (rejecting a possible graph cycle at 36 steps). It independently obtains baseline next pairwords from Python big integers `N+reverse(N)`, and checks all 81 temporal/spatial entries at four lengths. This is a second method, not a reprint of the DFS result.

## Reproduction

Run from the repository root:

```
python3 calculation/decimal_frontier/lattice_kinks/sharp_streak/run_checks.py
```

The one atomic result contains `sharp_streak.py`, `independent_checker.py`, `run_checks.py`, the exact compact `lattice_input.txt` snapshot, `bounds.json`, this proof report, and the <=15-line result note. No third-party packages or network access are required. Terminal control lines include `SHARP_RUN_BOUND_3_5_ALL_WIDTH_PASS`, `INDEPENDENT_BITSET_36_STATE_GRAPH_PASS`, `INDEPENDENT_BIGINT_SHARPNESS_CONTROLS_PASS` and `SHARP_STREAK_FULL_REPRODUCTION_PASS`. The base-9/base-13 mandatory controls are for new exterior censuses, which this is not. This strictly strengthens the one-step no-fully-contiguous-erasure theorem but does not assert any new general no-centre result.
