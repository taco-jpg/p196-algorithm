# Agent 8 — T1.B-width: exhaustive obstruction for uniformly short B blocks

**Status:** COMPUTED, with a paper argument that the tested graph overapproximates every admissible B-cycle. No Lean theorem; no claim on any trajectory containing |B| larger than the tested bound.

## Result

For base 10, there is **no** neutral-band `cycleOK` certificate for which **every** state has `|B| <= 7` (independent of period and all symmetric center lengths). This is stronger in its center/period quantification than the earlier bounded-seed searches, but is a bounded **exterior-width** result only.

All permitted trailing-9 trim amounts are included, not only maximal trim. The empty B block is included, deliberately overapproximating valid states whose middle C might not permit the required complementary carry.

### Reproduction

```
c++ -O3 -std=c++17 calculation/agent-8/b_width_graph.cpp -o /tmp/a8_b_width
/tmp/a8_b_width 1
/tmp/a8_b_width 2
/tmp/a8_b_width 3
/tmp/a8_b_width 4
/tmp/a8_b_width 5
/tmp/a8_b_width 6
/tmp/a8_b_width 7
python3 calculation/agent-8/test_b_width.py /tmp/a8_b_width
```

The main C++ K=7 result (local sandbox):

```
K=7 states=893871739 edges=521421127 gamma0=470382137 gamma1=51038990 trimmed=0:446935869,1:69261995,2:4814637,3:376483,4:29530,5:2404,6:195,7:14 max_indegree=40 indegree_zero=462278371 peeled=893871739 residual=0 cycle=0
```

C++ K=2..4 versus a separate Python graph construction: identical vertex, edge, overflow and trim histograms and residual counts. Independent ordinary-number check: `INTEGER-ORBIT cross-check PASSED: 10000 admissible randomized templates (seed=1961208)`; each computed external next block matches the corresponding initial pair-sum digits after ordinary integer reverse-add.

Runtime: K=7 approximately 124.25 seconds, peak 2,792,924 KB RSS using checked 8-bit indegrees; K=6 runs in seconds. 8-bit indegree is guarded against overflow, and the observed K=7 maximum is 40. No package dependencies beyond a C++17 compiler and Python 3 standard library.

## Why the test is a necessary obstruction (paper argument)

Fix an accepted edge in `Agent120.Neutral.cycleOK 10` from `(B,C)` to `(B2,C2)`.

1. By the `Hyp` condition, `e1 = e1(10,B)` and `e2(10,B,C) = 1-e1`. In particular, computing `DB(B)`, `DR(B,C)` and `gam(B,C)` needs only `B`; the center is no longer required once we impose the complementary carry.
2. Define `D` by digitwise normalization of `B` with carry 0, with terminal carry `e`. Define `R` by normalizing `reverse(B)` with incoming carry `1-e`, with terminal carry `g ∈ {0,1}`. These are the same arithmetic as the checked mirror, expressed independently in the program.
3. If `g=0`, the raw exterior is `F(B)=D+reverse(R)` (componentwise sum). If `g=1`, it is `F(B)=(D++[9(1-e)]) + ([1]++reverse(R))`. Exact `edgeOK` imposes `F(B) = B2 ++ [9]*u` for some `u >= 0`.
4. Therefore `B2` must be one of the words obtained by removing **any** number `u` of trailing 9s of `F(B)` (including `u=0`). Valid B words have entries in 0..18 and are either empty or begin with a nonzero coefficient. All possible B endpoints with length ≤K are enumerated; all other center checks are omitted, so our graph may have extra edges but cannot omit a B transition of an accepted cycle.
5. Every valid certificate whose B state stays within this finite vertex set would induce a closed directed walk, hence a directed cycle, in our B graph. A finite digraph has a cycle iff iterative elimination of indegree-zero vertices leaves any vertices: a cycle cannot lose a predecessor, while every nonempty finite acyclic digraph has an indegree-zero vertex.
6. The program enumerates all `19^K` normalized states, constructs all directed arcs, peels every state, and reports `residual=0` for K<=7. Hence no accepted certificate with **uniform exterior-width bound K<=7** can exist. This last numerical assertion is computed, not kernel-proved.

## Scope and limitations

- No assertion that `B` has to be short globally. Known base-10 B-only cycles have `|B|=29` for period 11 and `|B|=52..53` for period 12 (documented baseline); this result is compatible with those and does not decide their center compatibility.
- The result neither proves nor disproves existence of a decimal Lychrel number, and makes no exclusion for cycles with **any** B state longer than the bound.
- It makes no new claim about a center-cycle all-k obstruction, modular filter, or a generic first-coordinate recurrence; these are held by other agents in issue #289.
- `AGENTS.md` says no branches/PRs and requires a clean full verification before `main` pushes. Issue #289 manager explicitly held delivery because the campaign's PR instructions conflict. No push or PR has been made here. The report and independent code are staged as a reviewable patch pending policy resolution.

## Attribution

Baseline decoupling, exact `nextB`/`Hyp` and known small-period results: `calculation/neutral_band_search.py`, `calculation/neutral_band/README.md`, and `RESULTS.md`, section *A conditional route to a Lychrel number*. This independent graph adds a width-uniform, all-period obstruction and deliberately does **not** recycle the period-limited `bauto` algorithm.