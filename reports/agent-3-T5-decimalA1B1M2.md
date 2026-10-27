# Agent 3 — T5.two-band.decimal-A1B1M2 exact bounded projection

**PAPER PROOF of finite graph reduction; COMPUTED bounded acyclicity.** Not Lean-verified; no decimal Lychrel existence/nonexistence proof. Second-agent independent review still required. Coordination #289; signed two-neutral-band format and checker under draft PR #320, prior distinct B=D=empty finite search under #348.

## Scope

Decimal signed two-neutral-band template `W(g,h)=A x^g B u^h M v^h D y^g E`, where all fixed blocks are ordinary digit words, x+y=u+v=9 and `A[0]≠0`. This search allows:

* `|A|=|E|=1`, `|B|=|D|=1`; every A∈1..9, E,B,D∈0..9;
* arbitrary middle fixed `M` of length 0, 1 or 2 and digits 0..9;
* **all** 100 choices of input x,u∈0..9, with complementary y,v;
* **arbitrary** nonnegative neutral run lengths g,h;
* only the eight ordered boundary moves (run0 L/R, run1 L/R, run2 L/R, run3 L/R), exactly once each, with each integer signed delta in −1,0,+1. All other trace lengths/orderings and wider blocks are outside scope.

## PAPER PROOF: projection and empty-middle elimination

Under neutral carry transmission, the finite reverse-add image and its four emitted run symbols depend only on source fixed blocks `(A,B,M,D,E)`, **not on incoming x,u**. Thus the directed graph over these fixed blocks, when it includes every permitted signed move trace, is a necessary overapproximation of the full 100-times-larger phase graph. Forgetting input run colors can create false candidate cycles but cannot remove a genuine one. Every target is required to satisfy the same fixed widths, valid leading digit and complementary output run characters. Band-length deficits are also forgotten, safely enlarging the graph.

For an empty `M`, the carry leaving B/D reaches the empty middle unchanged, i.e. c3=c2. The two emitted inner run symbols are then both 0 or both 9 and **cannot** sum to 9. Hence empty-M states have no legal edge and cannot appear on any closed cycle. Full enumeration therefore needs only M lengths 1 and 2.

For each fixed-block state satisfying both necessary complementary output conditions, enumerate all 19 ways to balance the two outer-run boundary shift sums (each individual movement ∈−1,0,1), independently with 19 inner-run ways. There are exactly 361 traces per state. For each, apply the exact signed rewrite, require successor block lengths `[1,1,m',1,1]`, m'∈{1,2}, and check successor legality. Cache identical `(output fixed blocks, run characters)` signatures; this is an exact equality reduction, not a cutoff. The resulting projected graph contains any accepted cycle within this restricted format. Kahn topological peeling and a separate iterative DFS check acyclicity. Kahn dynamic programming also yields the maximum number of consecutive bounded edges.

## Reproduction and exact computation

Requires Python 3 standard library only and the two source files in parent draft PR #320:

```sh
python3 calculation/agent-3/decimal_a1b1m2.py
```

Full observed output:

```text
unique_output_signatures 2520 source_triples 247500
independent_integer_crosschecks 368820 PASS
independent_iterative_DFS_acyclic True visited 247500
active_fixed_states_A1B1M1_M2 247500 implicit_phases 24750000 ordered_boundary_move_pairs 361
actual_accepted_traces 61470 triple_graph_edges 61470 kahn_removed 247500 cyclic_core 0 max_path_edges 3 rejections {'bad_width': 12797307, 'bad_move': 76414293, 'target_not_active': 74430}
```

Arithmetic audit: **all 61,470 exact accepted traces** tested at source run digits (x,u)=(0,0),(5,7),(9,9) and source lengths (g,h)=(3,4),(6,5); each normal decimal number is reversed digitwise, added, and compared to the target template with signed shifted band lengths. Exactly 61,470×6=368,820 independent bigint equality checks, zero mismatch. No state caps, incomplete timeouts or skipped branches: the complete enumerated transfer graph is exhausted. Runtime observed ~13.48s, ~170,296 KB peak RSS. Rejections plus accepts sum to 247,500×361=89,347,500 trace attempts.

**Bounded result (COMPUTED):** the overapproximating 247,500-state graph has *no directed cycle*; maximum directed path length is **3 edges**. Therefore no accepted closed positive-gain cycle for base 10 can remain inside this exact fixed-block-width and ordered ±1 move language, regardless of period or g/h lengths.

## Exclusions and review status

Does **not** rule out longer M, `B` or `D` length ≠1, multiple moves at same boundary, movement magnitude 2+, permutations of the eight moves, other certificate formats, or base-10 Lychrel existence. No Lean file was produced and `python3 tools/verify.py --changed` was NOT RUN. This is a computational negative awaiting genuinely independent second-agent replication. Submit as a stacked DRAFT PR based on parent #320 to avoid duplicating code and violating repository no-duplicate rules; it must be reviewed/retargeted before merge.