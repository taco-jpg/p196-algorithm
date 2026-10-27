# Agent 3 — T5: four-digit center minimum projected loop and bounded exterior lifting

**Status:** PAPER PROOF of necessary orientation projection + COMPUTED complete finite graph/lift exclusion. **NOT LEAN-VERIFIED, NOT a decimal Lychrel certificate.** Builds on the arbitrary-exterior center≤3 negative in [#388](https://github.com/taco-jpg/p196-algorithm/pull/388). Reuses the exact full-phase signed boundary helpers from [#359](https://github.com/taco-jpg/p196-algorithm/pull/359), on which this proposed change is stacked.

## Projection with center length 1–4, arbitrary exterior

A center-only state is (M,c2), M an ordinary fixed-width block of 1, 2, 3, or 4 digits, including possible leading zeros, and c2 an incoming carry bit. Fixed width central add is R=low_m(M+reverse(M)+c2) and c3=carry. Inner neutral output requires c3=1−c2; define U=9(1−c3), V=9(1−c2). Two signed shifts a,d in {-1,0,+1} touch the left/right sides of R, one each in either order. For a true full-phase edge, **PAPER** width and neutral-band-gain identities prove a=R1, d=L2, **leading carry f=d−a∈{0,1}**. Retain precisely this necessary condition. As an intentional overapproximation, next c2 is unconstrained (both bits allowed), no exterior blocks are supplied.

A true positive-gain closed phase cycle must have total f>0 and consequently traverse different M length parities, by the earlier PAPER counting identity 2Σ(delta_g+delta_h)=Σ f.

The 1–4 projection has exactly 22,220 states, 28,400 directed arcs, 21,949 strongly connected components, and three cyclic SCCs of sizes [10,20,244]. The 244-state SCC **mixes even/odd center length**, whereas the other cyclic SCCs do not. Therefore the necessary center-only graph cannot exclude all positive-gain cycles with M up to length 4. This is a **survival of a relaxation**, not a full cycle.

## COMPUTED: shortest mixed-parity projected loop has length 9

Exhaustively enumerate all 22,220 states and all center operations, then find SCCs. For every parity-switching directed arc within a mixed-parity SCC, run BFS from its target back to its source; the minimum returned directed walk is a shortest mixed-parity closed walk. The exhaustive shortest length is **9 edges**, with a concrete replayed example below. Each row is (M, incoming c2); digits in M are most significant first:

~~~text
(010,1)
 -> (9021,0)
 -> (0230,1)
 -> (0551,1)
 -> (2102,1)
 -> (4115,1)
 -> (923,0)
 -> (252,1)
 -> (505,0)
 -> (010,1)
~~~

The exact center-adjacent signed shifts (a,d), together with the necessary leading overflow f=d−a, are

~~~text
(-1,0,1), (0,0,0), (0,0,0), (0,0,0), (0,0,0),
(0,+1,1), (0,0,0), (0,0,0), (0,0,0).
~~~

Sum f=2, so **the necessary global gain total equals 1** and is arithmetically consistent. This does not independently choose feasible full outer/inner run gains, or exterior carry transport. The script verifies every listed projected arc and both h=3 and h=8 literal center-run equality controls.

## COMPUTED: bounded full-phase lift of this exact nine-step itinerary

Now restore the exact five-block reverse/add and **all eight signed boundaries** using #359's full-boundary transition implementation, considering both relative move orders per shared fixed block. Evaluate full phases with:

- The central block M and central carry c2 fixed at the nine projected phases above (in that cyclic order).
- **|A|=|E|∈{1,2}**, all valid decimal A and E words; positive most-significant digit of A.
- **B=D=empty at every phase**.
- Source input neutral run digits restricted to 0/9 (PAPER: all closed signed cycles already use them).
- Each of the eight signed boundary moves in {-1,0,+1} exactly once (zero allowed), every relative order.
- A/E widths may **change between phases** so long as each remains in {1,2}; the full generated graph includes all such transitions.
- c2 is the carry of E+reverse(A), since B=D are empty; target c2 checked exactly. A positive leading fixed-block carry and the paired-run constraints are checked by the actual full image and finite moves.
- The graph deliberately does NOT need to enforce minimal g,h run-exponent nonnegativity on each candidate: ignoring such additional restrictions could only add spurious edges. Acyclicity remains a sound bounded exclusion.

The stage-indexed complete graph has 9×18,180 = **163,620 states**, **78,372** active complementary-output phase images, and **111,492** directed edges. Kahn peeling removes **all 163,620**, leaving **zero directed-cycle residual**. The exact per-stage edge counts, stages 0..8, are 3,960; 25,164; 4,320; 4,320; 4,320; 3,960; 25,164; 15,120; 25,164. Local run 16.59 seconds, no cap; independent first implementation with |A| fixed at 2 had 162,000 states / 99,540 edges / 0 residual.

**Precise COMPUTED negative:** the displayed 9-step center-only loop cannot lift to any exact signed full-phase cycle whose phases all have B=D empty, |A|=|E|≤2, and one bounded signed move at each of the eight interfaces. It remains entirely possible that the center projection loop lifts with A width≥3, nonempty B/D, multiple center moves, or that *another* center-only loop lifts.

## Reproduction, audit, and limits

A single Python standard-library command from the repo root, after the **#359 dependency** is checked out:

~~~sh
python3 calculation/agent-3/center4_lift.py
~~~

Outputs the complete center graph/SCC/minimum length, exact 9-edge witness, and the full bounded lift graph with guard assertions for all counts. New code/report are under agent-3 only.

**No** complete base-10 reverse-add pumping orbit was produced; no Lean file/registry entry or theorem was added. This is not a universal decimal one-band/two-band obstruction. The full repository verify.py --changed was **NOT RUN** here because an authoritative full checkout is unavailable. Draft PR should not merge until the #359 helper dependency is available and independently reviewed.