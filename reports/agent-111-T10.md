# Agent 111 — exact MDD review and the p11/k3 center exclusion

**Status: PAPER PROOF + COMPUTED. No new Lean theorem.**

## Result and exact scope

For base 10, the prescribed streams
`e=(10100110011)^3`, `g=(11100010000)^3` have **no closed center cycle
at any finite center length**, for the original neutral one-band format.
The computation uses `v=(01000010000)^3`. The credited equal-total
trim-schedule transport theorem extends the all-length exclusion to arbitrary
natural trim schedules with total 6. Center length closure forces that total.

This resolves the p11 driver repeated three times, P=33/G=12. It does not
exclude other P33 exterior streams, higher repetitions, every decimal
certificate, or decimal Lychrel numbers. The earlier explicit-frontier run in
PR #344 was correctly UNDECIDED; the new representation completes its scope.

Primary segment-MDD design and the separate P48 application belong to
Agent118 (issue #289, comment6432936525). This PR is the independently
implemented delayed-output image, its correctness review, and Agent111's
retained P33 application. Agent118's required-coefficient recurrence differs
from this implementation. No Agent118 source was used to implement it.

Dependencies: PR #344 supplies `long_center.py`, `center_controls.py`,
`schedule_optimizer.py`, and `p33_trial.py`; this PR is stacked on its branch.
Local arithmetic is reused from the original `cauto_fast.cpp`, with the exact
source pin and guards documented in #344. Thus this is an independent
frontier-representation implementation, not independent center arithmetic.
The whole-integer control oracle is independent of that arithmetic.
Padding covariance and schedule transport are credited to Agents7/107/110
(PRs #315/#336/#338). Agent101 retains cumulative-reachability attribution;
this engine uses exact whole-frontier periodicity, not that new algorithm.

## Exact finite-language representation (PAPER PROOF)

A frontier is a set of complete segment tuples `(s_0,...,s_(K-1))`.
Keep one MDD level per segment, including singleton levels. Empty node 0
denotes the empty language; terminal node 1 denotes the singleton empty suffix.
A node at level i denotes the union of `(label,) ++ suffix` over its edges.

The constructor removes empty branches, recursively unions children sharing
one label, sorts labels, and interns the exact `(level, edge-vector)`.
Induction from the terminal level shows equal canonical roots iff equal finite
languages. Hash collisions are checked by full structural equality. Nodes are
immutable in stable storage; the same arena and per-segment label meanings
persist through every generic layer and terminal tail. No marginal-product
approximation, hash-only equality, or skipped variable level is used.

Let the existing local table for segment i map s_i to rows `(y_i,c_i)`.
The exact next tuple has coordinate `encode_i(y_i,c_(i+1 mod K))`.
After selecting segment0's row, our recursion retains
`(input suffix node, previous y, first c)`. At level i>=1, select an actual
input edge s_i and a local row `(y_i,c_i)`, emit
`encode_(i-1)(previous y,c_i)`, and recurse on that input edge's child with
pending y_i. At the terminal input node, emit `encode_(K-1)(last y,first c)`.
Union all resulting output suffix languages, including equal-label branches.

Induction on the remaining levels proves that this is exactly the relational
image. The input suffix node retains every correlation imposed by the chosen
input prefix; pending y and first c retain the remaining cyclic dependencies.
For K=1 the terminal rule correctly uses the same selected row's y and c.
Memoization is fresh for each image/signature; its key includes all three
retained quantities. Signed inactive c=-1 is retained. Zero trims explicitly
use the existing legacy fallback instead of an unsupported empty relation.

## Why every center length is covered (PAPER PROOF)

For fixed streams and trims, `m_t=m_0+d_t`, where
`d_t=sum_(s<t)(g_s-2v_s)`. Increasing m_0 by 2h increases all half-widths,
the generic-prefix length, and the total layer count by h. Center parity and
the relative terminal-tail signatures remain unchanged.

The MDD computes the same exact generic frontiers as explicit enumeration.
An equal root at indices >=1 therefore establishes periodic frontiers under
the stationary generic relation. F0 is deliberately excluded because the
first layer has a special boundary signature. An empty frontier is absorbing.
If the period is q, a finite initial-width prefix and 2q eventual
representatives suffice: parity and the generic-frontier index determine
every remaining tail. This is the original cauto all-length argument with an
exact alternative set representation. All short positive widths are checked.

For P<=48 and the default 120-layer horizon, the representative threshold
occurs below 290. The optional horizon<=10000 remains within the explicit
100000 threshold-search bound. Failure to detect a period is UNDECIDED.
This implementation recomputes equivalent tails instead of memoizing them;
its `tails` field counts width invocations, not the original cache misses.

Every closed center itinerary is symmetric because every incoming center
map is symmetric. Empty centers violate the required complementary carry.
Thus the nonempty symmetric search domain loses no accepted center cycle.

## Witness extraction and resource semantics

For a chosen output tuple T_i=(y_i,z_i), the required local row at segment i
is `(y_i,z_(i-1 mod K))`. Find one COMPLETE path in the preceding input MDD
under those row-existence predicates. Backtracking through saved finite-width
roots recovers complete layer columns; no independent-coordinate choices are
substituted. The engine then replays every recovered center edge. Python
controls independently replay witnesses with whole-integer normalization.

The executable supports the guarded #344 domain: P<=48, base2..62, binary
streams/trims, equal trim/overflow length totals, and the conservative 256-bit
legacy fallback guard. `-cap` now limits cumulative historical DAG nodes;
`-work-cap` limits image recursion work. Local tables still consume memory,
so the wrapper's address-space, CPU, and wall limits remain necessary.
All cap, allocation, horizon, timeout, unsupported-input, and process-error
outcomes are explicitly unresolved. Tuple-count overflow saturates only the
display; it is never used for set equality, termination, or acceptance.

## P33 computation

From a combined checkout of this PR and #344:

```bash
python3 calculation/agent-111/mdd_center.py build /tmp/agent111_mdd
python3 calculation/agent-111/p33_trial.py /tmp/agent111_mdd \
  --schedule balanced --cap 1000000 --timeout 60 --memory-mb 4096
```

Exact generic counts F1 through F6:

```text
42875 657443 34755075 414911363 752450435 752450435
status=none jstar=5 period=1 mlo=67 classes=2 feasible_classes=0
arena_nodes=85385 union_cache=39438 images=106 tails=68
STATUS=NO_CENTER_FOR_THIS_DRIVER_AND_SCHEDULE
```

The equality F5=F6 is exact root equality, not merely equal cardinalities.
All widths1..66 and both eventual representatives67/68 reject. The first run
took0.458s with34MiB peak RSS; a repeat took0.575s/34MiB. No resource cap fired.

The already available F1-optimal schedule independently completes too:

```bash
python3 calculation/agent-111/p33_trial.py /tmp/agent111_mdd \
  --schedule min-first --cap 1000000 --timeout 60 --memory-mb 4096
```

```text
v=001000000000010000000011100000001
1728 2548480 41746464 188397536 346292192 372099040 372099040
status=none jstar=6 period=1 mlo=67 classes=2 feasible_classes=0
arena_nodes=140752 union_cache=68390 images=141 tails=68
STATUS=NO_CENTER_FOR_THIS_DRIVER_AND_SCHEDULE
```

This run took7.808s/2144MiB, with no cap. Minimizing the first explicit
frontier does not minimize local-table size, total DAG nodes, or runtime.
The balanced schedule is the preferred reproducer.

## Credited reciprocal controls requested by BOARDv6

```bash
python3 -O calculation/agent-111/mdd_crosscheck.py /tmp/agent111_mdd
```

The unchanged delayed-output engine independently reproduces Agent118's
primary P48 exclusion in PR #369 at commit
`19e13c356d9a917cf8bce074be71607f6b7cdd87`. All seven generic counts match:
`1000000,935560192,8574299136,8868958208,9157137472,9312887872,9312887872`.
Exact F6=F7, `none`, period1,mlo97,classes2,zero feasible classes. Our engine
checks98 width invocations, versus14 memoized tails in the primary engine.
Historical nodes96524, images152,1.184s/50MiB; no cap. This is independent
representation corroboration, with unchanged original local arithmetic;
Agent118 retains the result and primary MDD-design credit.

Agent116's newly verified base20 positive is retained at source width27:
`e=10100101,g=10001000,v=00100000`. The query is pinned to PR #356 commit
`b7a718b78d67cf54d362232ba1b8f90fbec23af8`, report `agent-116-T7.md`.
The engine reconstructs all8 phases; every edge passes independent integer
replay. Historical nodes9134,0.129s/69MiB. This is a center-engine control,
not a second Lean verification or a new base20 discovery.

## Independent implementation controls (COMPUTED)

```bash
c++ -O2 -std=c++17 -Wall -Wextra -pedantic \
  calculation/agent-111/mdd_selftest.cpp -o /tmp/a111_mdd_test
/tmp/a111_mdd_test
python3 -O calculation/agent-111/mdd_audit.py
python3 -O calculation/agent-111/center_controls.py --binary /tmp/agent111_mdd
python3 -O calculation/agent-111/mdd_regression.py \
  /tmp/agent111_mdd /tmp/agent111_cauto
```

Build `/tmp/agent111_cauto` with #344's `long_center.py build` command.
All checks use explicit failure conditions active under optimized Python.

| Check | Exact completed scope |
|---|---|
| C++ explicit finite-set oracle |2500 seeded cases;2502 unions;6673 complete image comparisons,4704 correlated inputs;731958 raw choice tuples;270716 distinct image tuples;18486 duplicate rows;1583 empty/5090 nonempty images;2 cap guards|
| Separate Python recurrence |600 cases;14968 explicit output tuples;2415 backward predecessors;600 changed-signature controls|
| Whole-integer center oracle |664 patterns;3218 widths;130974 starts;34 feasible/3184 infeasible;zero discrepancies|
| Source/padding arithmetic |8 original bases;56 edges;1264 retimed cycles/25760 edges;14 invalid cases reject|
| Extended positive witnesses |10 P36/P40/P48 cases;416 independently replayed edges|
| All original source positives |16 engine cases across8 bases;112 independently replayed edges|
| Explicit/MDD all-length differential |35 completed patterns,8 positive/27 negative;143 equal generic counts;986 independently replayed witness edges|

The C++ finite-set oracle was written from the public interface before its
author inspected the MDD internals. It enumerates the full Cartesian choices
for each complete input tuple. It does not reproduce the image recurrence.
Cases test K1/K2 cyclic seams, arbitrary input correlations, duplicate labels,
full uint32 labels, empty relations, construction order, changed signatures,
and chained images. The separate Python implementation also checks backward
predecessors. None of these finite tests is asserted as a Lean proof.

ASan/UBSan on the complete synthetic corpus passed with identical counts:

```bash
c++ -O1 -g -std=c++17 -fsanitize=address,undefined \
  -fno-omit-frame-pointer -fno-pie -no-pie \
  calculation/agent-111/mdd_selftest.cpp -o /tmp/a111_mdd_test_san
ASAN_OPTIONS=detect_leaks=0 /tmp/a111_mdd_test_san
```

Leak detection alone is disabled because this sandbox blocks its process
inspection; address and undefined-behavior checks remain enabled.

Production-adapter sanitizer and interruption controls also pass:

```bash
python3 calculation/agent-111/mdd_center.py build /tmp/agent111_mdd_san --sanitize
python3 -O calculation/agent-111/mdd_adapter_smoke.py /tmp/agent111_mdd_san
python3 -O calculation/agent-111/mdd_guards.py --binary /tmp/agent111_mdd \
  --sanitizer-binary /tmp/agent111_mdd_san
```

The smoke run covers5 cases,19 COMPLETE production frontier comparisons,
64 integer-replayed witness edges,4 positive inactive-tail cases including
K1/K2/P48, and one fixed-width P33 negative. No ASan/UBSan finding occurred.
Guard controls reject23 inherited malformed inputs,13 extra MDD option
errors, a changed source hash, and an oversized324-bit key. Six incomplete
paths pass under both optimized and sanitizer builds: fixed/all-width node
caps, fixed/all-width work caps, the generic horizon, and the comparison cap.
An actual64MiB allocation failure, actual1-microsecond timeout(return124),
and9 invalid wrapper settings also pass. Each incomplete run is explicitly
checked for absence of `status=none` or `status=hit`; failures are not mocked.

## Review and repository gate

Independent within-task proof review covered exact image semantics,
canonical-root identity, generic-vs-tail signatures, all-width coverage,
signed inactive values, stable local labels/storage, and full-path witnesses.
Agent118 independently reproduced all P33 counts and its all-width negative
with the separate required-coefficient implementation (#289/comment6433150364):
10488 DAG nodes,12 memoized tails,0.224s/13536KiB. The primary P48 published
source was independently read at its pinned commit; its required-coefficient
image, stable labels, exact root comparison, and two-tail memoization match
the proof. Both directions of the requested cross-reproduction now pass.
The PR remains a draft for campaign review.

No Lean file, registry entry, README, RESULTS, or other agent's file is changed.
The actual `python3 tools/verify.py --changed` gate passes:5217 Lean files,
301 projects,0 changed Lean modules,0 endpoint audits, `ALL CHECKS PASSED`.
Its zero-module scope does not formally verify this computation.
