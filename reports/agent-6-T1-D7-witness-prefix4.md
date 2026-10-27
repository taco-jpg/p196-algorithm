# Agent 6 — T1.C-D7-witness-B-prefix-lift

## Exact scoped obstruction

The explicit period-42 **three-prefix/center projected-only** loop from draft PR #361 (not a `cycleOK` certificate) **cannot lift to ANY exact full exterior B orbit matching that particular phase-labelled itinerary**. It already fails at exterior coefficient **number four**: the phase-indexed finite necessary automaton has **798 vertices, 774 directed edges, zero cycles**, and longest path **16 edges**. In fact, its fixed first-three-coefficient itinerary cannot be followed for 17 consecutive transitions from any phase even with arbitrary unrelated choices of the unresolved inward carry at every step.

This is a **PAPER PROOF of sound abstraction + COMPUTED exact graph exhaustion**, not Lean-verified. It does **not** disprove other D7 projected loops, other g/e streams, a base-10 one-band certificate, or a decimal Lychrel number.

## Reproduction and proof of the reduction

The previous projected loop in #361 has period 42, exterior low-three-coefficient tuples `Bprefix3[t]`, and overflow word

`g=101000101001001010100101000101001001010100`.

The three-coefficient tuple is periodic with period 21; the exact first 21 tuples are given in the accompanying Python program `calculation/agent-6/prefix4_witness_obstruction.py`.

For each phase `t∈0..41`, a state is an arbitrary **fourth** exterior coefficient `x∈{0..18}`. Given the known first three coefficients and x, enumerate **both** possible values of the unknown reverse-normalization carry entering column four, then apply exact elementary digit arithmetic of `nextB`: normalized forward digits, reversed-side carries, and the one-column shift on overflow. Add a directed edge `(t,x)→((t+1)%42,y)` iff the output overflow equals prescribed `g[t]` and the first three output coefficients equal the prescribed next tuple. All allowable trailing-neutral-9 trims preserve these padded prefix coordinates, so every hypothetical complete B lift would produce a path in this graph. Any such complete **periodic** lift, even after an arbitrary number of repetitions of the 42-phase itinerary, would force a directed closed walk, which an acyclic graph cannot contain.

Moreover, a DAG's topological longest-path DP gives the maximum 16-step trace; thus even a nonclosing hypothetical B state cannot obey the entire particular itinerary for 17 consecutive steps.

Run:

```sh
python3 calculation/agent-6/prefix4_witness_obstruction.py
```

Exact observed output:

```text
R4_ARITHMETIC_RANDOM_CHECKS=50000 PASS
R4_WITNESS_LIFT_ACYCLIC states=798 arcs=774 removed=798 residual=0 max_path_edges=16
```

The separate arithmetic test enumerates **50,000** deterministic randomized full finite exterior B words, including empty B, lengths 0..29, coefficients 0..18, actual complement carry, and every legal trailing-neutral trim of nextB. Every actual step's first four padded coefficients and g appear in the overapproximating fourth-coordinate model: zero mismatches. Runtime about 1.29s, peak ~98 MB in the sandbox. Additional independent depth-five and depth-six graph runs over this same fixed itinerary also return acyclic (15,162/14,706 and 288,078/279,414 vertex/edge counts), but depth four already suffices.

## Relation to prior results, scope and verification

Parent source/result #361 establishes the period-42 positive **projected-only** loop and exact center replay; parent #345 proves the unconditional **COMPUTED necessary `some |C|>=7`** result. This follow-up eliminates only that specific positive projected witness, not every possible D7 loop. Nothing was added to Lean, RESULTS.md or README.md. Full `python3 tools/verify.py --changed` in a repository checkout and a second independent agent's rerun are outstanding. The PR is **UNVERIFIED / DO NOT MERGE**.
