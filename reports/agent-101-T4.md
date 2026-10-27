# Agent 101 — T4 cumulative center reachability

## Result 和 exact scope

**PAPER PROOF:** for fixed base `b`, carry stream `e`, overflow stream `g`, 和
binary trim schedule `v`, existence of a center cycle of some finite width
reduces to cumulative reachability of complete generic-layer states, followed
by 两个 fixed tails. Equality or periodicity of whole frontier sets is unnecessary.
The reduction preserves the existing exact center transition relation.

`calculation/agent-101/cauto_reach.cpp` implements the reduction using the
upstream `Fast` transition engine from
`calculation/neutral_band/structure/cauto_fast.cpp`. It includes 那 source with
its `main` renamed; the original source remains untouched. Its supported domain
retains the original period, segment, base, 和 binary-trim bounds.

The query 是 **existence at any initial width for one specified schedule**.
`NONE` excludes centers at every width for precisely the supplied `(b,e,g,v)`.
A positive answer supplies one arithmetically replayed center cycle.
It does 不 enumerate all feasible widths or produce `FEASIBLE_CLASS` arithmetic
progressions. It does 不 decide other trim schedules, temporal periods, or
driver streams. A matching exterior cycle remains necessary for a full
`cycleOK` certificate. 这 report supplies neither a decimal certificate nor
a universal decimal one-band impossibility theorem.

**Verification status:** mathematical reduction plus the explicitly listed
computations below; **不 LEAN-VERIFIED**. Reusing the upstream transition engine
does 不 constitute an independently implemented center automaton. Tests written
within Agent 101's task do 不 count as independent campaign-agent review.

## 1. Model 和 length offsets

Fix `b >= 2`, period `P >= 1`, 和 binary vectors `e,g,v` of length `P`.
Centers 有 coefficients in `[0,2b-2]` 和 are symmetric, nonempty words.
At temporal phase `t`, normalize `C_t` from entering carry `e_t`, obtaining
digits `D_t`; its outgoing carry must equal `1-e_t`. Let `y_t=(b-1)e_t`.
The raw next center 是 the coefficientwise sum of a word 和 its reversal:
use `D_t` if `g_t=0`, or `D_t ++ [y_t]` if `g_t=1`. Remove exactly `v_t`
neutral coefficients from each end, requiring every removed coefficient to
equal `b-1`. The result must equal `C_(t+1)`, with temporal indices cyclic.

These 是 the existing `cauto_fast.cpp` model 和 `cstep_forced` conventions.
In particular, `v_t` specifies an exact trim; maximal trimming is 不 assumed.

Define

\[
\delta_0=0,\qquad \delta_{t+1}=\delta_t+g_t-2v_t.
\]

A closed cycle requires `delta_P=0`; otherwise the length equations themselves
exclude it. For balanced schedules put

\[
a=1-\min_{0\le t<P}\delta_t,\qquad m_t=m_0+\delta_t.
\]

Because `delta_0=0`, `a>=1`. Every phase length 是 positive exactly when
`m_0>=a`. The generic/tail boundary 和 total layer count are

\[
J_t=\left\lceil m_t/2\right\rceil,\qquad
J'_t=\left\lceil(m_t+g_t)/2\right\rceil,\qquad
j_0=\min_t J_t-1,\qquad J_{\rm all}=\max_t J'_t.
\]

## 2. Initial layer, stationary interior, 和 两个 tails

A complete layer state contains every phase's left/right carry bits, retained
right digit at overflow phases, 和 pending coefficient guess at trim phases.
The optimized representation interns segment states but retains their complete
global tuple. Let `S` be the prescribed boundary state, 和 write

\[
F_1=T_0(\{S\}),\qquad F_d=T^{d-1}(F_1)\quad(d\ge1).
\]

Here `T_0` 是 `Fast::step` with `j=0,generic=true`; `T` 是 its generic relation
at any `j>=1`. This distinction matters: the initial layer checks the neutral
trim symbol directly, whereas later layers check a pending guess.
`Fast::sigFor` shows stationarity exactly: generic signatures contain only the
`j==0` flag 和 `T_GEN` for every temporal phase.

The 两个 lengths `a,a+1` 有 `j_0=0`, so they require complete direct solves.
They exhaust the short exceptions. For `r in {0,1}`, choose representative
width `M_r=a+2+r`; it 有 `j_0=1`. Define `A_r` to be the composition of its
ordinary nongeneric layers `j=1,...,J_all(M_r)-1`.

**Tail translation lemma.** At width `M_r+2n`, the corresponding tail 是 `A_r`
for every `n>=0`.

Proof: adding `2n` to `m_0` adds `2n` to every `m_t` 和 `n` to every `J_t,J'_t`.
Compare layer `j` at the representative with layer `j+n` at the larger width.
The comparisons defining `T_GEN,T_LODD,T_LEVEN,T_INP,T_INZ` 都 agree; length
parities 都 agree; the `j==0` flag remains false. Driver digits 和 temporal
segment order are independent of width. Every local signature, hence every
complete-state transition, agrees. The generic prefix at the larger width
有 `n+1` layers. Therefore its exact acceptance condition 是

\[
A_r\bigl(T^n(F_1)\bigr)\ne\varnothing.\qquad\square
\]

Final acceptance means a nonempty frontier after `J_all` layers, as in the
upstream solver. Its last odd/even cases join the carry traces at each center.
The virtual overflow layer checks an added central output. Pending trim guesses
也 finish: when `v_t=1`, the length equation gives `J_(t+1)=J'_t-1`, so every
active pending coefficient receives its checking layer before termination.

## 3. Cumulative reachability theorem

Let

\[
U=\bigcup_{n\ge0}T^n(F_1).
\]

Then a center cycle exists at some positive width if 和 only if one of

\[
\operatorname{Accept}(a),\quad \operatorname{Accept}(a+1),\quad
A_0(U)\ne\varnothing,\quad A_1(U)\ne\varnothing
\]

holds.

**Proof, including different-depth provenance.** A layer transition 是 a
relation on complete states. For every family of state sets,

\[
R\left(\bigcup_i X_i\right)=\bigcup_iR(X_i).
\]

The source realizes 这 identity literally: `Fast::step` processes one complete
parent tuple at a time; its Cartesian product uses only the local successor
lists belonging to 那 parent. Composition gives the same identity for `A_r`.
Consequently

\[
A_r(U)=\bigcup_{n\ge0}A_r\bigl(T^n(F_1)\bigr).
\]

Every surviving tail path therefore starts at some complete state reached at
one definite generic depth. The tail translation lemma supplies its concrete
width. Conversely, every legal width is either a short exception or uniquely
`a+2+r+2n`, so every center cycle appears in the displayed union. This proves
the 两个 implications. Unioning individual segment components separately 和 then
taking their Cartesian product would invalidate the argument. `U` contains
complete global tuples only. \(\square\)

For finiteness, after the first generic layer a sufficient state bound 是

\[
N=4^P b^{G}(2b-1)^K,\qquad G=\sum_tg_t,\quad K=\sum_tv_t.
\]

There are `2P` carry bits, `G` retained ordinary digits, 和 `K` pending
coefficient guesses. Thus uncapped cumulative reachability terminates without
a depth bound. A simple shortest path 也 gives a finite witness-width bound
`m_0<=a+2N+1` if a witness exists. The algorithm avoids enumerating 那 bound.

## 4. Delta-frontier implementation 和 witness replay

The implementation stores every discovered complete tuple once. Its breadth
first delta `D_d` contains tuples first discovered at generic depth `d`, with
`F_1` at depth 1. At each delta it applies the 两个 representative tails, then
expands only unseen complete generic successors. The deltas partition `U`, so

\[
A_r(U)=\bigcup_{d\ge1} A_r(D_d).
\]

Skipping a tuple seen earlier is sound: its generic successors 和 its 两个
tail relations depend only on the tuple, 不 its discovery depth. A positive
tail from `D_d` gives the concrete initial width

\[
\boxed{m_0=a+2d+r.}
\]

The engine reruns `witness_fast` at 那 width 和 checks the reconstructed words
with `verify_cycle`, using the specified exact carries, overflows, trims, 和
temporal return. It does 不 invoke `get_witness`'s legacy fallback. A replay or
reconstruction failure cannot become a certified positive or a negative.
After every delta's 两个 tails reject 和 the discovery queue empties, the engine
may return `NONE` for the complete width range of the specified schedule.

## 5. Supported scope, attribution, 和 limits

The executable retains `base in 2..62`, `P<=MAXP=32`, binary `v`,
`1<=sum(v)<=MAXNS=16`, 和 temporal segment lengths `<=MAXL=32`.
Invalid stream syntax or lengths fail closed. Unsupported cases, including
zero trims, nonbinary trims, or larger periods, are 不 negative results.
这 deliverable 没有 an Agent 101 extension to `P=33` or `P=48`.

Run from the repository root:

```sh
c++ -O3 -std=c++17 calculation/agent-101/cauto_reach.cpp -o /tmp/a101_cauto_reach
/tmp/a101_cauto_reach BASE E G V --cap 1000000 --seconds 1800 --memory-mb 8192
```

Each run is bounded by at most 1800 seconds 和 8 GB. Runtime, memory, explored
state, or other active limits produce `UNDECIDED`, never `NONE`. The explored
state cap applies to cumulative discovered tuples, 不 merely one layer.
Cumulative storage can exceed a single frontier's storage; the theorem promises
exact existential semantics, 不 a speed or memory improvement on every case.

Credit: the pre-existing `cauto_fast.cpp` author supplied the exact segmented
transition, its local caches, 和 the fixed-width witness code. Agent 10's static
period/segment/packing guard audit identifies 为什么 unsupported bounds must be
rejected. Agent 107's general trim-transport work 和 Agent 110's balanced-schedule
corollary are separate; neither is silently assumed to enlarge 这 binary-trim
implementation. Other agents' `P=33/P=48` extensions 和 concrete center decisions
are 也 separate. The new contribution here 是 the cumulative complete-state
reduction 和 its delta-frontier implementation.

## 6. Validation

**COMPUTED**, from the repository root:

```sh
c++ -O3 -std=c++17 calculation/agent-101/cauto_reach.cpp -o /tmp/a101_reach
c++ -O3 -std=c++17 calculation/neutral_band/structure/cauto_fast.cpp -o /tmp/a101_old
PYTHONDONTWRITEBYTECODE=1 python3 calculation/agent-101/check_cauto_reach.py --engine /tmp/a101_reach --old /tmp/a101_old
```

The independently authored regression driver uses positional integer arithmetic
to replay returned centers. Its exhaustive cases cover bases 2–5, periods 2–4,
every binary carry/overflow/trim stream satisfying the supported balance.
The complete comparison, including the credited base-20 control, completed in
10.77 seconds:

| Check | Output |
|---|---:|
| Exhaustive cases | 2,240 |
| Seeded random cases | 32 |
| Selected p11/p22/p24 fixtures | 9 |
| Completed old/new agreements | 2,278 |
| Disagreements | 0 |
| Returned witnesses independently replayed | 140 |
| Short-exception witnesses | 13 |
| Existing Lean-source positive controls | 8/8 |
| Invalid-input/resource guards | 9/9 |

Three p22 fixtures return `UNDECIDED` in BOTH engines at the regression cap
200,000. The driver prints their exact streams 和 reasons; its overall result
explicitly records these unresolved comparisons. They are 不 negative results.
The quick suite 也 passes under `python3 -O`, with explicit checks still active.
Source positives include the base-11 width-42 和 base-17 width-20 centers;
their cumulative visited counts are 1,395 和 462 respectively.

Three separate known decimal exclusions reproduce at cap 1,000,000:

| P | e | g | v | Visited | Depth | Result |
|---:|---|---|---|---:|---:|---|
| 11 | `10100110011` | `11100010000` | `11000000000` | 637 | 4 | NONE |
| 22 | `1010011001110100110011` | `1110001000011100010000` | `1111000000000000000000` | 583,737 | 6 | NONE |
| 24 | `101010010101101010010101` | `100010001000100010001000` | `111000000000000000000000` | 259,687 | 6 | NONE |

For each row run `/tmp/a101_reach 10 E G V --cap 1000000 --seconds 30
--memory-mb 1024`, substituting the exact table streams. These are reproductions
of prior scoped center negatives, 不 new period exclusions.

A practical positive control uses **Agent 116's** independently discovered
base-20 driver 和 trim schedule (issue #289, comment 6432893018):

```sh
/tmp/a101_reach 20 10100101 10001000 00100000 --cap 250000 --seconds 30 --memory-mb 1024
/tmp/a101_old 20 10100101 10001000 1 1 -v 00100000 -allm -cap 250000
```

The new engine returns `FEASIBLE`, `m0=27`, `visited=3931`, `generic_depth=12`,
`max_frontier=744`, `tail_calls=24` (0.053 seconds). The old engine returns
`NOPERIOD`, `maxstates=249893`, `tails=0` (2.69 seconds). The regression separately
replays the new center. This establishes a concrete benefit from checking tails
during cumulative exploration; it does 不 establish that the old frontier
sequence never becomes periodic. Agent 116 retains the base-20 discovery 和
certificate work. These center-only controls are 不 decimal certificates.

The regression 也 contains an explicitly synthetic 121-state directed cycle:
whole frontiers do 不 repeat within a 120-layer horizon, while cumulative
reachability terminates. It is a finite-graph illustration, 不 a claim about a
center instance. Repository gate `python3 tools/verify.py --changed` passes:
5,217 Lean files, 301 projects, **zero changed Lean modules/endpoints**.
No new Lean statement is asserted.
