# T4 — Common center padding 和 finite generic-depth bounds

Agent 117 · 2026-10-27 · coordination issue #289.

## Result 和 scope

**PAPER PROOF.** For a fixed base, temporal period, carry stream `e`,
overflow stream `g`, 和 natural trim schedule `v`, existence of a finite
center cycle over all widths is unchanged by requiring at least one
phase's outer coefficient to be nonneutral. Remove the same number of
neutral endpoint pairs from every phase; the supplied `e/g/v` stay fixed.
This is an existence equivalence, not a fixed-width equivalence.

For the existing binary-trim center automaton, the forbidden all-neutral
first column produces one identifiable state. Deleting it **only after
the first layer** is exact even after state deduplication. If the remaining
reachable generic graph is acyclic, its longest path gives a finite upper
bound for the starting width of a reduced representative.

**COMPUTED.** The p11 driver 和 p12 driver repeated twice give acyclic
reduced graphs, with maximum generic depths 4 和 6. The resulting finite
starting-width bounds are 12 和 14 using the schedules below. The original
exact midpoint solver finds no centers in either finite range. These
corroborate previously known exclusions; they are not new decimal negatives.

No new Lean theorem, decimal certificate, unrestricted repetition result,
or global impossibility theorem is claimed. A spatial graph cycle would
certify only an infinite generic strip, with no finite midpoint closure.

## Prior work 和 dependencies

This applies Agent7's neutral-padding covariance
([#315](https://github.com/taco-jpg/p196-algorithm/pull/315)); it does not
claim that identity as new. Agent107's equal-total schedule transport
([#336](https://github.com/taco-jpg/p196-algorithm/pull/336)) separately
permits a prescribed binary schedule for an all-width query. We keep
the tested schedules explicit rather than infer a bounded-width transfer.
REPORT_219 explains why infinite boundary trajectories need not represent
finite integers. Agent101's cumulative reachability engine
([#357](https://github.com/taco-jpg/p196-algorithm/pull/357)), Agent118's
MDD representation, Agent105's phasewise canonical prefix work, 和
Agent114's inner-window construction retain their separate scopes.

The C++ program includes the unchanged `cauto_fast.cpp` with its `main`
renamed. No solver source is copied or edited. Baseline main:
`eafbbbfd6b5b857597f95f68268c56dbd96b6bcb`; included source SHA-256:
`eb2e6b18b09fdfcae0a5b6b818d23291123ed6a76b59fb6e531589e7f6d00fff`.
The independent Python transition enumerator imports neither C++ nor the
Python mirror. The arithmetic audit uses source certificates only as fixtures.

## 1. Common-padding theorem, including short centers

Write `h=b-1`, `P_a(C)=h^a ++ C ++ h^a`, 和 let a legal center satisfy
`norm_b(C,e)=(D,1-e)`. Centers on a closed cycle are symmetric because
every raw successor is paired with its reversal 和 trimming is symmetric.
For `g=0`, let `F_(e,g)(C)=D+reverse(D)` coefficientwise. For `g=1`,
pair `D ++ [he]` with its reversal instead.

A neutral coefficient transmits either carry unchanged, so an all-neutral
word cannot satisfy the carry flip. This includes the empty word, `[h]`,
和 `[h,h]`. A legal symmetric center with neutral endpoints can therefore
lose those endpoints while leaving a nonempty legal center.

Put `x=h(1-e)` 和 `y=he`. Direct carrying gives

```text
norm_b(P_a(C),e) = (x^a ++ D ++ y^a, 1-e).
F_(e,g)(P_a(C)) = P_a(F_(e,g)(C)).                 (1)
```

For `g=1`, the augmented digit word is
`x^a ++ (D ++ [y]) ++ y^a`; pairing still gives (1), since `x+y=h`.
Thus the identity includes overflow, arbitrary widths, 和 all `a>=0`.

Suppose a cycle obeys

```text
F_(e_t,g_t)(C_t) = P_(v_t)(C_(t+1)).             (2)
```

If every `C_t=P_a(K_t)`, substitute (1) in (2), commute the literal
neutral paddings, 和 cancel their common prefix 和 suffix. The result is
`F_(e_t,g_t)(K_t)=P_(v_t)(K_(t+1))` with the SAME natural `v_t`.
No subtraction from a trim count is needed. Conversely, common padding
preserves every equation. Choose `a` as the minimum neutral-pair depth
across the finite family. The reduced cycle has a nonneutral phase head.
Every width drops by `2a`, preserving all phase-width differences.

This does not assert equality of feasible widths or equality of a solver's
`FEASIBLE_CLASS` output. Phase-dependent stripping generally changes trims
和 must not replace this common operation.

## 2. Exact deletion after the first column

At the initial interface, `l_t=e_t` 和 `r_t=1-e_t`. For coefficient
`c_t` in `0..2b-2` 和 inward reverse carry `r'_t`, the paired-column laws are

```text
l'_t = floor((c_t+e_t)/b),
1-e_t = floor((c_t+r'_t)/b).
```

The output conditions `l'_t=e_t`, `r'_t=1-e_t` force `c_t=b-1`:
for either value of `e_t`, the two inequalities become `c_t<b` 和
`c_t+1>=b`. Conversely `c_t=b-1` forces those carries.
Requiring this at EVERY time therefore identifies exactly the common
neutral column. A different nonneutral column cannot merge into that
packed state, because the stored `l'/r'` already force every coefficient.

Its complete state has `l=e`, `r=1-e`, `Rd=he` on overflow slots,
和 `Z=h` on trim slots. It differs from the initial state, whose `Z` is
`NONE`. Its generic outgoing relation equals the special initial relation:
the stored `Z=h` simply replaces the initial trim condition `cp=h`.
In particular it has the expected all-neutral self-loop.

Delete this state only from the first generated frontier. Later incoming
carries can differ, 和 later neutral coefficients remain legal. For widths
1 or 2, the first layer is a midpoint layer: odd closure forces
`l'=1-e`, while even closure makes the inward carries equal. Neither can
match the all-phase deletion predicate. These short cases remain covered
by direct finite-width checking.

## 3. Acyclic generic graphs give a finite width bound

Set `d_0=0`, `d_(t+1)=d_t+g_t-2v_t`, so `m_t=m0+d_t` 和 `d_P=0`.
Let `dmin=min(d_t)` 和 `J_t=ceil(m_t/2)`. Before any midpoint, every
finite solution projects to exactly the same generic relation. There are
at least `min(J_t)-1` such outer columns.

Let `L` be the maximum number of generic columns along a path starting
at the special initial interface after the first-column deletion. For a
finite reduced cycle, `min(J_t)-1 <= L`; otherwise its prefix would be a
longer path in the exhausted graph. Consequently

```text
m0 <= 2(L+1)-dmin.                              (3)
```

If a phase has width at most 2, (3) holds directly. A complete acyclic
exploration plus exact midpoint checks through (3) therefore decides
all-width existence for this fixed schedule. A capped exploration supplies
no bound. If a reachable spatial cycle survives, it supplies no finite
center by itself.

The tool performs exact DFS over complete packed tuples, retaining source
columns for replay. Longest paths use DAG dynamic programming, not DFS
stack height. `--complete` can finish a cyclic graph while retaining its
first cycle witness; otherwise the first detected cycle ends the search.
Only the generic relation is explored; finite midpoint checks use the
unchanged upstream executable separately.

## 4. Complete decimal computations

```text
p11:   e=10100110011
       g=11100010000
       v=11000000000
p12k2: e=101010010101101010010101
       g=100010001000100010001000
balanced v=000010000000100000001000
concentrated v=111000000000000000000000
```

| Driver/schedule | Initial states before/after | Generic vertices | Generic arcs | L | dmin | m0 bound |
|---|---:|---:|---:|---:|---:|---:|
| p11 | 23 / 22 | 636 | 614 | 4 | -2 | 12 |
| p12k2 balanced | 1000 / 999 | 152583 | 151584 | 6 | 0 | 14 |
| p12k2 concentrated | 752 / 751 | 259686 | 258935 | 6 | -5 | 19 |

All three graphs completed without caps 和 are acyclic. The tool's
`transitions` counter includes the ORIGINAL first frontier, including its
deleted state: totals are 637, 152584, 和 259687 respectively.
The concentrated 100000-state preliminary run was capped; its separate
1000000-state rerun above completed. No partial result is used as a negative.

The independent p11 enumerator reproduces all counts 和 exact surviving
frontier sizes `[22,70,320,224]`, followed by zero. The unfiltered complete
C++ control has 637 vertices 和 637 generic arcs; its recorded cycle is
the all-neutral self-loop. Removing common padding eliminates that cycle.
The independent p12k2 balanced enumeration also completes: all 152583
vertices peel, with nonempty frontiers
`[999,29592,62784,22752,23976,12480]`, followed by zero. It took 54.492s
under a hard 60s cap. The concentrated schedule is a supplementary C++
check; it has not received a second full independent graph enumeration.

## 5. Reproduction 和 validation

From the repository root, compile the two unchanged/owned sources:

```bash
g++ -O2 -std=c++17 calculation/agent-117/common_padding_graph.cpp -o /tmp/agent117_graph
g++ -O2 -std=c++17 calculation/neutral_band/structure/cauto_fast.cpp -o /tmp/agent117_cauto
/tmp/agent117_graph
/tmp/agent117_graph --unfiltered --complete > /tmp/agent117_strip.json
python3 calculation/agent-117/common_padding_verify.py /tmp/agent117_strip.json
python3 calculation/agent-117/common_padding_verify.py --reference 10100110011 11100010000 11000000000
python3 calculation/agent-117/common_padding_verify.py --reference 101010010101101010010101 100010001000100010001000 000010000000100000001000
/tmp/agent117_graph 101010010101101010010101 100010001000100010001000 000010000000100000001000 --cap 300000
/tmp/agent117_graph 101010010101101010010101 100010001000100010001000 111000000000000000000000 --cap 1000000 --edges 2000000
python3 calculation/agent-117/common_padding_audit.py
python3 calculation/agent-117/common_padding_verify.py --selftest --known-controls
```

Exact finite-width checks using bound (3):

```bash
/tmp/agent117_cauto 10 10100110011 11100010000 1 12 -v 11000000000 -w
/tmp/agent117_cauto 10 101010010101101010010101 100010001000100010001000 1 14 -v 000010000000100000001000 -w
/tmp/agent117_cauto 10 101010010101101010010101 100010001000100010001000 1 19 -v 111000000000000000000000 -w
```

Each prints `status=none`, `feasible 0`, 和 `capped/noperiod 0`;
the instance counts are 12, 14, 和 19. Invalid nonpositive phase widths
are rejected by the original solver. These are complete fixed-schedule
negative checks within the derived bounds, not timing extrapolations.

Independent arithmetic audit: 2232 neutral/short guards; 15372 first-layer
cases with 244 neutral matches 和 zero nonneutral deletions; 7564 short-layer
checks; 15664 symmetric words/15640 valid inputs; 93840 raw covariance
checks; 103152 fixed-trim checks; 2044 inverse edges; 768 long-trim controls
through `v=64`; eight known bases/80 padded-and-stripped cycle controls,
560 center edges, 和 48 removed common pairs. The arithmetic is ordinary
positional integer arithmetic, separate from the production mirror.
The second verifier independently parses the eight source fixtures:
56 center edges 和 168 padded/reduced fixed-trim checks pass. The three
fixtures with a fully generic first layer (bases 11,17,26) survive the
filter; the other fixtures have a width-2 phase 和 remain direct short-tail
controls. Its lasso test rejects nine corrupted witnesses, 和 its own
one-state successor cap returns `UNDECIDED` before a larger set is stored.

The graph tool guards base 2..62, period at most 32, binary `e/g/v`,
positive `sum(g)=2sum(v)`, 和 the 256-bit packed-key budget. Its maximum
configured budgets are 1000000 states, 4000000 emitted transitions, 和
30 seconds. Caps/timeouts return `UNDECIDED`; a spatial-cycle witness must
pass the separately authored Python carry-equation validator.
The general padding theorem covers natural trims; the included solver
implements binary trims only. No claim silently extends that implementation.

Representative optimized C++ timings: p11 approximately 0.003s;
p12k2 balanced 1.535s; concentrated 2.623s/72916 KiB peak RSS.
The independent arithmetic audit took 3.108s/10240 KiB.
These are measured local runs, not promises for other streams or machines.
Invalid numeric suffixes/bounds are rejected; a one-state cap returns
`CAPPED/UNDECIDED`, 和 a one-second interruption returns
`TIMEOUT/UNDECIDED` with exit 124, including interruption inside expansion.

`python3 tools/verify.py --changed` returned `ALL CHECKS PASSED`:
5217 Lean files, 301 projects, zero changed Lean modules 和 zero audited
endpoints. This is a repository-rule gate for code/report changes, not
Lean verification of the new mathematical argument.
