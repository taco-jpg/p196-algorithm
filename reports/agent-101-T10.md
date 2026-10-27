# Agent 101 — T10 independent exterior-prefix / center graph review

## Status, attribution, 和 exact scope

**PAPER PROOF** below audits the projection 和 cycle decision used in the
independent implementation. **COMPUTED:** the full R3,D6 negative is reproduced;
the R3,D7 projection contains an independently replayed 24-edge loop. Its
overflow stream matches Agent 4's previously unresolved p24/G8 exterior case.
The complete results appear in Section 6. 这 deliverable is **不 LEAN-VERIFIED**.

Agent 4 supplied the original first-exterior-coordinate necessary recurrence.
Agent 6 supplied the primary three-prefix, center-width-6 result in
[PR #345](https://github.com/taco-jpg/p196-algorithm/pull/345) 和 the primary
center-width-7 result in [PR #361](https://github.com/taco-jpg/p196-algorithm/pull/361), claimed in
[comment 6432991631](https://github.com/taco-jpg/p196-algorithm/issues/289#issuecomment-6432991631).
Agent 101's earlier result with 两个 exterior coefficients is
[PR #332](https://github.com/taco-jpg/p196-algorithm/pull/332).
The present scope 是 a separately authored, second-agent review: reproduce the
full R3,D6 negative, then provide an independent D7 control. It does 不 transfer
primary authorship of either Agent 6 result or their longest-path follow-up.

For a specified exterior-prefix depth `R` 和 uniform center bound `D`, the
graph overapproximates every accepted decimal neutral-band cycle whose every
center phase 有 length at most `D`. Temporal period, exterior width, 和 legal
trim amounts are unrestricted. Acyclicity excludes exactly 那 bounded-center
class. A residual graph supplies only a projected cycle; missing exterior
coefficients 和 carries may fail to join. Neither outcome alone establishes a
decimal Lychrel number or a universal impossibility theorem.

## 1. Exact center factor

Use the unchanged definitions in
`calculation/neutral_band_search.py` 和
`lean/P196/Drafts/Agent120NeutralBandCalibration/A120Template.lean`.
For coefficient words over `0..18`, `Hyp` gives the carry relation
`e2=1-e1`. A center `C` admits entering carry `e` exactly when normalizing `C`
from `e` leaves carry `1-e`.

The empty word 和 an all-9 word preserve entering carry, so neither is legal.
For any other word, its last non-9 coefficient determines the outgoing carry:
0 for a coefficient below 9, 1 for a coefficient above 9. Thus a legal center
determines its entering bit `e` uniquely. For 那 bit normalize to digits `d`.
Given overflow `g`, put `W=d` for `g=0`, or `W=d++[9e]` for `g=1`.
The raw next center 是 `W+reverse(W)` coefficientwise. Enumerate every trim
`v>=0` whose removed prefix 和 suffix consist entirely of 9s; retain exactly
the nonempty targets of length at most `D` admitting their own flip bit.
This defines the exact center factor, with every arc labelled by `g`.

**Why symmetry is complete for cycle exclusion.** `Hyp` does 不 require center
symmetry. Nevertheless every raw next center is symmetric, 和 symmetric
trimming preserves symmetry. Every vertex of a nonempty closed cycle 有 a
predecessor, so its center is symmetric. Restricting the cycle graph to
symmetric centers loses no accepted cycle.

**Even-middle pruning preserves graph cycles.** If the raw center 有 odd
length, its middle coefficient 是 twice the middle digit of `W`, hence even.
Removing pairs of outer coefficients preserves length parity 和 the middle
coefficient. Therefore every center edge ending at an odd-length word ends
at an even middle. In the graph without 这 pruning, excluded vertices 有
indegree zero. The induced graph retaining even odd-length middles 有 exactly
the same directed cycles. Its vertex/arc counts can differ, so filtered counts
must be distinguished from Agent 6's unfiltered census.

## 2. Exterior-prefix factor, including short 和 empty exteriors

Extend every finite exterior by an infinite formal neutral suffix:

\[
\widehat B=B\,9^\infty.
\]

Retain its first `R` coefficients `a_0,...,a_(R-1)`. The first coefficient
belongs to `1..18`: a nonempty exterior 有 a positive head, while an empty
exterior gives `a_0=9`. Later coefficients belong to `0..18`.

Let `e=carry(B,0)`. The low-side carry is initially `l_0=0` 和 obeys

\[
\ell_{i+1}=\lfloor(a_i+\ell_i)/10\rfloor,\qquad
d_i=(a_i+\ell_i)\bmod10.
\]

The opposite normalization starts above finite `B` with carry `1-e`.
For a real edge its carry entering the retained prefix is some bit `h_R`.
Allow either bit 和 compute backwards

\[
h_i=\lfloor(a_i+h_{i+1})/10\rfloor,\qquad
r_i=(a_i+h_{i+1})\bmod10,\qquad g=h_0.
\]

The exact projected successor is

\[
a'_0=d_0+\begin{cases}r_0&g=0,\\1&g=1,\end{cases}\qquad
a'_i=d_i+\begin{cases}r_i&g=0,\\r_{i-1}&g=1\end{cases}\quad(i\ge1).
\]

This follows from the same-coordinate pairing in `nextB` without overflow 和
the one-coordinate opposite-side shift, including the new leading 1, with
overflow. Every displayed output is a sum of ordinary digits. The first is
positive: without overflow it equals `2a_0+h_1>=2`; with overflow it equals
`(a_0 mod10)+1>=1`.

**Padding boundary proof.** Beyond finite `B`, the low carry remains `e` 和
the opposite carry remains `1-e`. The padded digits are respectively
`9(1-e)` 和 `9e`, with sum 9. Without overflow the raw successor's neutral
tail starts at `|B|`; with overflow it starts at `|B|+1`. Thus the formula
computes exactly `nextB++9^infinity`, even when the retained prefix extends
beyond the finite exterior. For empty `B`, actual `e=0,g=1` gives raw
`nextB=[10]`, followed by neutral padding. Length-1 exteriors follow the same
carry calculation without a separate width assumption.

An accepted exterior trim satisfies `nextB=B2++9^u`; consequently
`nextB++9^infinity=B2++9^infinity`. Every legal trim preserves the projection.
The actual unknown `h_R` is included in the 两个 choices, proving inclusion
of every real edge. Choices on consecutive projected edges may be inconsistent
with any finite deeper exterior; the converse inclusion is 不 asserted.

**Independent sentinel implementation.** Append coefficient 0 or 18 to the
retained prefix 和 normalize the complete finite word. The forward exit is
respectively 0 or 1. Starting reverse normalization with its complement, the
sentinel leaves inward carry 0 or 1 respectively. Retained low digits are
unchanged, so truncating the raw successor realizes exactly the 两个 cut-carry
choices above. The center's entering bit remains independently constrained.

## 3. Product, reverse adjacency, 和 duplicate conventions

Vertices are complete pairs `(prefix,C)`. Couple a prefix arc 和 a center arc
only when their overflow labels agree. The center supplies its exact entering
bit; the prefix abstraction does 不 claim to determine the carry after the
unretained exterior. Allowing 那 unresolved information enlarges the graph.
Every real bounded-center certificate maps to a closed walk in the product.

Deduplicate exterior arcs with identical `(target_prefix,g)`: 两个 guessed
high carries can describe the same projected arc. Distinct center trims give
distinct target lengths. For a fixed source center, different `g` values give
opposite target-length parity, since `m'=m+g-2v`. Therefore after factor
deduplication the product enumerates every endpoint arc exactly once.

For target `(p',C')`, its predecessors are the disjoint union, over `g`, of
`prefix_predecessors(p',g) x center_predecessors(C',g)`. Every product arc 有
exactly one matching factor pair. Hence reverse-factor enumeration decrements
each predecessor's outdegree once for each removed outgoing arc, without
storing the product arc list. An explicit assertion must guard the chosen
degree integer type. For `D<=7`, a sufficient degree bound is

\[
\deg^+\le2\left\lceil\frac{D+1}{2}\right\rceil\le8,
\]

because there are at most 两个 distinct prefix arcs 和 at most
`ceil((D+1)/2)` nonempty symmetric trims for each matched overflow label.

## 4. Why sink peeling decides cycles

Initialize exact outdegrees 和 queue every sink. Repeatedly remove a queued
vertex 和 decrement the outdegrees of its remaining predecessors, enqueueing
each newly created sink. A vertex on a directed cycle always retains its
outgoing cycle arc until another cycle vertex disappears; therefore no cycle
vertex can be the first removed cycle vertex.

Conversely, if peeling leaves a nonempty finite residual, each remaining
vertex 有 an outgoing residual arc. Following such arcs must repeat a vertex,
producing a directed cycle. Thus complete removal is equivalent to acyclicity.
A residual vertex need 不 lie on a cycle: it can lead into a cycle.
This outdegree/reverse-factor implementation is separate from Agent 6's
indegree/forward-factor Kahn implementation.

## 5. Residual witnesses 和 resource semantics

A residual witness must list a literal closed sequence of product vertices
和 replay each prefix/center transition, including `g`, one witnessing high
carry bit, 和 the exact trim depth `v=(|C|+g-|C'|)/2`. Every chosen successor
must remain inside the residual. Retaining a first-visit map or using cycle
detection on a deterministic residual-successor choice identifies a closed
subpath. Independent literal arithmetic checks must verify its return.

Such a witness supplies an actual center cycle for its displayed driver bits
和 a compatible finite prefix loop, but 不 a full exterior cycle. It must
never be presented as an accepted `cycleOK` certificate.
Limits, allocation failures, index overflows, or interrupted computations are
`UNDECIDED`, never acyclicity. Exact scope includes the prefix depth, center
bound, parity filter, duplicate convention, state/arc counts, 和 completed
removal count. The review does 不 compute Agent 6's separately claimed longest
path statistic.

## 6. Reproduction 和 validation

Compile 和 run from the repository root:

```sh
c++ -O3 -std=c++17 -Wall -Wextra -Wpedantic calculation/agent-101/prefix_center_sink.cpp -o /tmp/a101_prefix_sink
/tmp/a101_prefix_sink --prefix 3 --center 6 --all-middles --seconds 1200 --memory-mb 4096
/tmp/a101_prefix_sink --prefix 3 --center 7 --seconds 1200 --memory-mb 4096 > /tmp/a101-prefix3-center7-witness.json
python3 calculation/agent-101/check_prefix_sink.py --witness /tmp/a101-prefix3-center7-witness.json
```

| Run | Vertices | Arcs | Peeled | Residual | Initial sinks | Maximum outdegree |
|---|---:|---:|---:|---:|---:|---:|
| R3,D6, every middle | 94,039,056 | 129,065,442 | 94,039,056 | 0 | 22,306,188 | 6 |
| R3,D7, even odd-length middles | 517,474,728 | 600,194,268 | 516,796,264 | 678,464 | 222,840,964 | 8 |

The complete D6 run returned `ACYCLIC` in 1.28826 seconds, peak 454 MiB;
its vertex 和 arc counts exactly reproduce Agent 6's primary result. The
complete D7 run returned `CYCLIC_PROJECTION` in 8.24834 seconds, peak 2487 MiB.
Neither run encountered a cap. Times describe 这 machine, 不 a runtime guarantee.
The D6 conclusion 是 an independent confirmation: every accepted decimal
one-band cycle must 有 some center phase of length at least 7.

### 6.1. Independent arithmetic 和 complete factor comparisons

```sh
python3 calculation/agent-101/check_prefix_sink.py
python3 -O calculation/agent-101/check_prefix_sink.py
python3 calculation/agent-101/check_prefix_sink.py --engine /tmp/a101_prefix_sink --factors 3 6 --all-middles
python3 calculation/agent-101/check_prefix_sink.py --engine /tmp/a101_prefix_sink --factors 3 7
python3 calculation/agent-101/check_prefix_sink.py --engine /tmp/a101_prefix_sink --guards
python3 -O calculation/agent-101/check_prefix_sink.py --engine /tmp/a101_prefix_sink --guards
```

Normal 和 optimized Python arithmetic controls 都 passed: 140,321 full exterior
words, 226,781 legal trim projections, 28,944 center cases, 和 56 positive
source-certificate edges. The Python oracle normalizes positional integers;
the C++ engine performs column normalization. Every emitted factor transition
was compared, including its stored boundary carry or trim label:

| Factor | States | Arcs with g=0 | Arcs with g=1 | Total arcs |
|---|---:|---:|---:|---:|
| R3 prefix | 6,498 | 6,137 | 3,610 | 9,747 |
| D6 center, every middle | 14,472 | 16,086 | 8,406 | 24,492 |
| D7 center, even odd-length middles | 79,636 | 88,704 | 15,462 | 104,166 |

Every comparison passed. The 12 malformed-input/resource/witness-cap guards
passed normally 和 under `python3 -O`; rejected or capped runs returned
`UNDECIDED`. An UndefinedBehaviorSanitizer build with libstdc++ assertions 也
returned `ACYCLIC` for R2,D5: 2,603,988 vertices, 2,955,526 arcs, zero residual.

```sh
c++ -O1 -g -std=c++17 -fsanitize=undefined -fno-sanitize-recover=all -D_GLIBCXX_ASSERTIONS calculation/agent-101/prefix_center_sink.cpp -o /tmp/a101_prefix_sink_ubsan
/tmp/a101_prefix_sink_ubsan --prefix 2 --center 5 --all-middles --seconds 1200 --memory-mb 4096
```

### 6.2. The independently extracted D7 loop

The emitted JSON contains the full 24-edge projected witness. Independent
literal replay passed every edge 和 its return, with `sum(g)=8`, `sum(v)=4`,
center lengths 6..7, initial prefix `[9,17,17]`, 和 initial center
`[9,14,13,18,13,14,9]`. In 那 exact phase order:

```text
g=110001001000110001001000
e=010100110100101011001011
v=100001000000100001000000
```

The separate Agent 101 T4 engine ([PR #357](https://github.com/taco-jpg/p196-algorithm/pull/357)) 也 returns a replayed `FEASIBLE,m0=7` for
这 same center instance: 348,521 cumulative generic states, about 0.119 seconds.
With 那 separate deliverable compiled as `/tmp/a101_cauto_reach`, reproduce by:

```sh
/tmp/a101_cauto_reach 10 010100110100101011001011 110001001000110001001000 100001000000100001000000 --cap 1000000 --seconds 300 --memory-mb 2048
```

那 是 an additional same-author, different-engine center check, 不 another
campaign agent's review. A finite full exterior with 这 exact `e,g` remains
unestablished. In particular, the displayed prefix does 不 determine the
complete exterior carry stream.

The `g` word exactly matches Agent 4's sole unresolved p24/G8 word among 415
survivors of the first-coordinate filter: 414 others exhausted. The source
[partial result](https://github.com/taco-jpg/p196-algorithm/issues/289#issuecomment-6432789174)
和 [Studio request](https://github.com/taco-jpg/p196-algorithm/issues/289#issuecomment-6432789604)
record caps/timeouts, 不 a complete exterior exclusion. 这 match supplies a
specific compatible center target for 那 exterior search. It does 不 establish
an exterior cycle, its carry stream, or a decimal certificate.

Agent 6's primary D7 result supplies a different 42-edge loop. Their deeper
prefix test of 那 fixed loop does 不 decide 这 24-edge loop. Agent 6 retains
the generic R4,D7/R5 refinement; 这 report makes no competing claim there.
Their center-pruned indegree residual 和 这 full filtered outdegree residual
need 不 agree: the vertex sets 和 deletion directions differ.

### 6.3. Repository gate

`python3 tools/verify.py --changed`: **ALL CHECKS PASSED**; 5,217 Lean files,
301 projects, zero changed Lean modules 和 zero theorem endpoints to audit.
This repository check is 不 a new Lean verification of the finite graphs.
