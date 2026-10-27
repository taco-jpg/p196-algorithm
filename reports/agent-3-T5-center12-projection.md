# Agent 3 — T5: all-period decimal 1/2-center signed-format obstruction

**Status:** PAPER PROOF of a *necessary center projection* plus exhaustive COMPUTED finite SCC census. **NOT LEAN-VERIFIED.** This work belongs to the new signed two-neutral-band certificate format (Agent 3 draft [#320](https://github.com/taco-jpg/p196-algorithm/pull/320)), **not** to the original Agent120 one-band checker. The central parity lemma is independently documented in [#365](https://github.com/taco-jpg/p196-algorithm/pull/365). No decimal certificate is claimed.

## Precise scope

Fix base 10. Let every phase have a center block M of length **1 or 2**. All five-block template digit validity/complement conditions remain as in #320. The two signed moves that actually touch the middle block, i.e. the **right boundary of the inner-left run** and **left boundary of the inner-right run**, each occur exactly once with signed size from `{-1,0,+1}`, in **either order**. The other six boundaries can have any valid finite signed trace, and the lengths/contents of A,B,D,E are **unrestricted**.

Only under this restricted center-adjacent-move rule, no positive-gain closed signed two-neutral-band certificate can have all center lengths in `{1,2}`, for **any period**, regardless of exterior width and all choices of exterior moves.

Multiple moves on either center-adjacent boundary or magnitude greater than 1 are **outside** this result. This is not a general decimal Lychrel nonexistence theorem.

## PAPER PROOF: why the projected graph is necessary

Use state `(M,c2)`, where `M` is a one- or two-digit base-10 block and `c2 in {0,1}` is the incoming carry from the fixed right-side block addition. At the central addition,

```text
n = val_10(M) + val_10(reverse(M)) + c2;
R = n mod 10^|M|;
c3 = floor(n/10^|M|).
```

Here R is written as exactly `|M|` decimal digits, including any leading zero. The central pair of neutral output run digits are `U=9(1−c3)` immediately left of R and `V=9(1−c2)` immediately right of R. A legal target phase requires `U+V=9`, hence **c3=1−c2**. Reject every state violating this necessary constraint.

Now enumerate both center-adjacent moves, `a,d in {-1,0,+1}`. A positive move extracts the matching U (left edge) or V (right edge) digit from R; a negative move absorbs the adjacent run digit into R. Test both local orders. Retain only the resulting one- or two-digit M'. The projected transition then permits **either next incoming carry** c2' equal to 0 or 1, deliberately forgetting any constraint from the exterior fixed blocks. Thus every actual signed edge with the specified two center moves maps into the finite projection. In general, the converse is FALSE: a projected arc need not lift to complete A/B/M/D/E blocks or match an exterior carry.

Any actual closed phase itinerary would induce a closed directed walk in this center graph, because M and c2 return to their starting values.

By the independent PAPER identity in #365, every accepted signed edge satisfies

```text
|M_next| - |M| ≡ f (mod 2),
```

where `f in {0,1}` is its leading carry. Summing fixed-word lengths along a closed phase itinerary gives `2 Σ(delta_g+delta_h)=Σf`. An accepted positive-gain cycle must therefore include at least one f=1, equivalently an edge **switching center-length parity**. Such a closed walk lies entirely inside some strongly connected component containing both lengths 1 and 2.

**Consequently, a finite graph census showing no cyclic strongly connected component with both lengths disproves all positive-gain cycles in the exact scope above, independent of exterior widths and period.** The actual graph may have same-length cycles; they necessarily have zero leading-overflow gain and are not positive-gain certificates.

## COMPUTED exact graph census

Reproduce with Python 3 standard library, no external package:

```sh
python3 calculation/agent-3/center12_projection.py
```

Observed uncapped complete result:

```text
states 220 allowed_sources 100 raw_center_moves 122 arcs 244
SCCs 208 cyclic_SCCs 2 cyclic_sizes [4, 10]
mixed_parity_cyclic_SCCs 0 center_word_tests 244
bounded_center_projection_no_positive_gain_cycle PASS
```

The 220 states are exactly `(10+100)*2` possible one/two-digit M words times free incoming carry bit. There are 100 active states satisfying complement-carry and at least one allowed signed central boundary operation. The two actual cyclic SCCs have 10 vertices **all length 1** and 4 vertices **all length 2**. Both lengths appear in the *graph* and there are cross-parity arcs, but **no cyclic SCC contains both parities**. This distinguishes the result from a mistakenly reported fully acyclic graph.

The script uses a standalone exact fixed-width central addition, explicit signed digit-word transformations for both move orders, arbitrary next-carry allowance, and a second-stage Kosaraju SCC decomposition. Each of 122 locally admissible move records is checked as a literal center-run word equality at run lengths `h=3` and `h=8`, yielding 244 successful word controls. These arithmetic tests supplement, but do not substitute for, the formal graph-overapproximation argument.

No resource cap, external solver, or long-period heuristic was used. Source and report are within the agent-specific allowed paths. `python3 tools/verify.py --changed` **NOT RUN** because a complete repository checkout is not accessible here. Keep draft unmerged pending independent code/proof review.

**Not claimed:** no base-10 Lychrel exists; all signed two-band certificate formats fail; arbitrary central move traces are covered; full-phase B/C witnesses were enumerated; Lean has certified this calculation. This is an all-**period** but center-length- and move-**restricted** negative.