# Agent 3 — T5.two-band.decimal-A1B0M4 bounded trace-cycle exclusion

**COMPUTED negative with a PAPER PROOF finite-graph reduction. NOT Lean-verified.** This report rules out only a sharply restricted decimal signed two-neutral-band *phase/move language*, not all decimal Lychrel numbers or all two-band certificates. Requires independent **second-agent** reproduction before being treated as a closed negative task. Research coordinator: #289. Format definition and proof: draft PR #320.

## Scope (exact)

Base b=10 and phase word, most-significant first,

`W(g,h) = A x^g B u^h M v^h D y^g E`, `x+y=u+v=9`.

Restrict **every phase** to `|A|=|E|=1`, `A[0]∈{1,...,9}`, `E[0]∈{0,...,9}`, `B=D=empty`, and `0<=|M|<=4` with every coefficient an ordinary decimal digit. Every source repeated-digit choice `x,u∈{0,...,9}` is allowed (`y=9−x`, `v=9−u`). Parameter values `g,h` are unbounded nonnegative integers.

For an edge, use the existing `signed_edge` semantics, but constrain its **specific trace** to the *fixed order* run0 left/right, run1 left/right, run2 left/right, run3 left/right, with exactly one move of size −1, 0 or +1 at each of these eight boundaries. A move of size zero is a no-op. Other trace orderings, repeated nonzero moves at a boundary, absolute move size ≥2, larger M, or nonempty B/D are **NOT covered**.

## PAPER PROOF: finite graph and projection are necessary

A source phase's reverse-add image fixed blocks `O0,...,O4` and emitted run digits `R=(X,U,V,Y)` depend only on the five source *fixed blocks*, not on source `(x,u)`. This follows from `x+y=u+v=9` and the exact neutral carry transmission, credited to our two-band carry lemma in #320. Therefore each triple `(A[0], E[0], M)` has 100 possible source `(x,u)` choices, all with the **same outgoing signed-edge options**. Project all phases to this fixed-block triple; any accepted cycle under this restricted trace language projects to a directed cycle of triples. The projection deliberately forgets source run digits and movement-feasibility parameter bounds, so it can only ADD spurious walks; acyclicity safely excludes genuine cycles.

A raw image can be a valid target phase only if `R0+R3=9` and `R1+R2=9`. For M empty, the carry through B,M,D is unchanged, so inner emitted pair is either `(0,0)` or `(9,9)`, never complementary. Thus there is **no outgoing legal edge from an M-empty source**, and such a source cannot lie on a cycle. The remaining legal `|M|=1..4` states are explicitly enumerated, with arbitrary ordinary digits.

A necessary directed edge from source triple to target triple is emitted for **every** one of the 19 ways to balance left/right outer-run shifts (each side in −1,0,+1), paired independently with each of the 19 balanced inner-run ways: precisely `19²=361` ordered 8-move traces per source. Each trace is checked through `apply_moves`, matched against the exact target-block widths `[1,0,|M'|,0,1]`, with `1<=|M'|<=4`; targets lacking the outgoing neutral-complement condition are discarded. Each retained trace is additionally checked with `signed_edge`. Identical source `image_blocks` signatures are cached; this is an exact memoization, not a heuristic cap.

For a finite directed graph, Kahn peeling removes every vertex iff it is acyclic. Running topological longest-path dynamic programming at the same time gives a bound on the maximum number of consecutive legal edges whose phases all belong to this bounded family. A separate iterative DFS checks the cycle-negative independently of indegree peeling.

## COMPUTED complete finite enumeration

```sh
python3 calculation/agent-3/decimal_a1m4.py
```

Runs in ~22.1 seconds with peak ~244,468 KB RSS in the test container (one process, Python standard library). Exact output:

```text
unique_output_signatures 5202 source_triples 495000
independent_integer_crosschecks 900456 PASS
independent_iterative_DFS_acyclic True visited 495000
active_triples_M1_M2_M3_M4 495000 implicit_phases 49500000 ordered_boundary_move_pairs 361
actual_accepted_traces 150076 triple_graph_edges 150076 kahn_removed 495000 cyclic_core 0 max_path_edges 3 rejections {'bad_width': 24268635, 'bad_move': 154189665, 'target_not_active': 86624}
```

All 150,076 individual admissible traces were checked against independent actual decimal integer reverse-add: source band digits `(x,u)=(0,0),(5,7),(9,9)` and two band-length pairs `(3,4),(6,5)`, making **6 checks per trace = 900,456**. The exact reversed input coefficient word was converted to an integer, added, and compared against the target-phase word after signed shifts; zero mismatches. No state cap, time cap, or undecided branch occurs in this completed M≤4 run. The source counts every rejected trace as well; the totals above are authoritative and sum exactly to `495000×361=178695000` attempted traces: `150076+24268635+154189665+86624=178695000`.

**Result (bounded COMPUTED):** the overapproximating fixed-triple graph has no directed cycle and longest directed path has exactly **3 edges**. Thus within the specified phase widths and ordered ±1 trace alphabet, **no nonempty closed positive-gain signed two-band certificate** exists for base 10, even for arbitrary period and arbitrary band exponents. In fact no phase itinerary can take four consecutive edges and remain entirely within this particular bounded template family.

## Exclusions / limitations

This is not a no-go for the full signed two-band checker (#320), which allows larger fixed words and arbitrary finite signed traces. It does not rule out the documented base-10 one-band format, or establish nonexistence of decimal Lychrel numbers. There is no new Lean theorem and `python3 tools/verify.py --changed` has not been run. The script imports the signed format source in stacked draft PR #320, so review/merge order must respect that dependency. Before counting this as a completed negative, the Manager should request a genuinely independent second-agent computation.