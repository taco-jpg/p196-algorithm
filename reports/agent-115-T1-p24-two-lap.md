# Agent 115 — Two-lap exterior completion of the priority P24 center

Task: `T1.p24-center-two-lap-B`, issue #289, claim6433286508.
Main baseline: `eafbbbfd6b5b857597f95f68268c56dbd96b6bcb`.
Stacked dependency: Agent108/#423, `d2c893c8bdc73529358e926ca5e02d68c5f4d528`.

## Question 和 exact scope

Agent101's [PR381](https://github.com/taco-jpg/p196-algorithm/pull/381)
supplies an actual 24-step decimal center cycle, with

```
e = 010100110100101011001011
g = 110001001000110001001000
v = 100001000000100001000000
C0 = [9,14,13,18,13,14,9].
```

This task repeats the center 和 these streams twice, seeking an exterior
return after **48 steps**. No equation B_(t+24)=B_t is imposed. A solution
of smaller least period is allowed; there is no unjustified inference from
repeated streams to a repeated full exterior.

Agents117/108's one-lap negatives,101's one-lap solver,109's all-lap bounded
widths, 和106's all-lap language theory are separate. This report concerns
the specified **two-lap** driver.

**PAPER reduction + COMPUTED complete negative:** G48=g++g has no finite B
return for **ANY carry word e, ANY finite width, and ANY natural trims**.
The complete unpruned spatial frontier is empty at width79. In particular,
the supplied center cannot lift after two laps. Higher lap counts, other
overflow words, 和 global decimal impossibility remain open. Agent108 owns
the imported engine;109/#427 retains its distinct all-lap width16 result.
This is not a Lean-verified search exclusion or a decimal certificate.

## 1. The center control — independently COMPUTED

`two_lap_oracle.py` derives normalization from whole positional integers,
extracting digits by quotient/remainder. It independently replays all 24
center edges 和 their doubled 48-edge list. The carry exits at 1-e, every
prescribed symmetric trim is legal, 和 the original center returns exactly.
The lengths [7,6,7,7,7,7,6,6,6,7,7,7] repeat four times. Total overflow is16;
total symmetric center trim is8. Complete phase words are reproducible with

```bash
python3 -O calculation/agent-115/two_lap_oracle.py target --laps 2
```

Each center edge also has an ordinary integer fixture using its own small B;
these separate fixtures are not a connected exterior cycle or certificate.

## 2. Common-width reduction — PAPER PROOF

Credit: Agent7's padding theorem in
[PR315](https://github.com/taco-jpg/p196-algorithm/pull/315), the subsequent
Agent114 exterior transports, 和 the common-width applications by Agents107/109.
Agent114's subsequent [PR400](https://github.com/taco-jpg/p196-algorithm/pull/400)
formally verifies the width equivalence; it does not verify our solver code.
The main repository's `calculation/neutral_band/structure/bcp.py` already
contains a generic CP-SAT exterior formulation. No novelty of that model or
the padding identity is claimed here.

Fix base b>=2, h=b-1. Let F(B) be the raw exterior successor when the center
changes incoming carry e to 1-e. Neutral suffix padding satisfies

\[
F(B\mathbin{+\!+}h^a)=F(B)\mathbin{+\!+}h^a.
\]

It preserves e 和 g: a neutral run transmits its entering carry, emitting
h(1-e) on the forward side 和 he on the reverse side. Paired padded digits
sum h, including the shifted overflow join. Empty B is included: e=0, g=1,
和 F([])=[b].

Given any closed legal exterior cycle with phase lengths n_t<=W, W>=1,
write a_t=W-n_t. The exact length identity is

\[
n_t+g_t=n_{t+1}+u_t,
\qquad a_t+u_t=a_{t+1}+g_t.
\]

Padding phase t by a_t therefore turns
F(B_t)=B_(t+1)++h^(u_t) into

\[
F(A_t)=A_{t+1}\mathbin{+\!+}h^{g_t},\qquad |A_t|=W.
\]

All original natural trim schedules are covered. The center, center trims,
streams, and phase count remain unchanged. Conversely, a fixed-W solution
is itself a legal exterior cycle. Thus solving at W is **equivalent to
existence with every original exterior width at most W**. In particular,
UNSAT at W excludes every smaller bound; each smaller width need not be run.

All-neutral padded rows must remain allowed, since they represent empty
original phases. Nonempty zero-head rows are forbidden by actual Hyp. Width
zero alone has no closed exterior cycle: [b] cannot be removed as a neutral
suffix. No maximal-trim or nonneutral-ended condition is added to the model.

## 3. Exact bounded column model — PAPER PROOF

For phase t and units-first position j, x_(t,j) is a coefficient, D its
forward digit, R its reverse-normalized digit aligned to the same position,
and f/r the forward/reverse-aligned carries. Bounds: 0<=x<=2b-2, x[t,0]>=1,
0<=D,R<=b-1, f,r in{0,1}. The equations are

\[
x_j+f_j=D_j+bf_{j+1},\qquad
x_j+r_{j+1}=R_j+br_j,
\]
\[
f_0=0,\quad f_W=e_t,\quad r_W=1-e_t,\quad r_0=g_t.
\]

These bounds make each equation the unique ordinary quotient/remainder
normalization. Without overflow, x'_(j)=D_j+R_j. With overflow,

\[
x'_0=D_0+1,\qquad x'_j=D_j+R_{j-1}\quad(1\le j<W),
\]

and the final trimmed symbol imposes **R_(W-1)=(b-1)e_t**. It is exactly
the raw-top equation (b-1)(1-e_t)+R_(W-1)=b-1. Omitting that condition would
admit a false free-boundary model. Temporal successors are indexed modulo48.

The bounded unsigned encoding uses k=bit_length(2b-1), so 2^k>2b-1.
Every column side is at most2b-1; successor sums are at most2b-2, with
overflow head at mostb. Thus no encoded addition can wrap. The integer
encoding expresses the same equations. Solver UNSAT is a **COMPUTED**
bounded conclusion, not kernel verification.

## 4. Forced first coefficient — PAPER projection + COMPUTED support

Credit Agent4's scalar-head projection: for positive head x and inward carry
c in{0,1}, g=floor((x+c)/b). The next head is x%b+(x+c)%b when g=0,
and x%b+1 when g=1.

Make nodes (t,x), require the prescribed g_t, 和 advance t modulo48.
Every full exterior cycle projects to a closed walk, so iterative removal
of sinks preserves every possible cycle. Generic retained nodes need not
themselves lie on cycles; only a necessary support restriction is used.

Independent synchronous and queue peels agree:864 nodes,704 unique edges,
848 carry-labelled edges; retained counts864,448,268,152,100,84,68,56,52,48
then stabilize: the unique heads are [9,10,1,2,5,11,2,5,10,1,2,4] repeated4.

The solver constrains only these first coefficients. It does not identify
the rest of the words across12 or24 phases. Queue/synchronous comparisons
also agree on one/two laps of all eight known source drivers:17 graphs,
with all168 source head occurrences retained.

## 5. Necessary last-coefficient domains

For tail x and incoming forward carry a, e=floor((x+a)/b). At g=0 its
successor is (x+a)%b+(x+1-e)%b. At g=1, the neutral trim forces x=b-1,a=e,
with successor in(b-1)(1-e)+{0,...,b-1}, also covering width1. An actual
P-cycle projects to a P-step closed walk; `two_lap_tail_projection.py`
computes these necessary domains without a half-period equality.

For the target,912 vertices/500 edges reduce to108 states; sink peeling 和
exact48-step return give identical domains. All16 overflow phases force9;
the other domains have2..4 values. Every phase retains9, so this projection
alone cannot exclude any driver. It is not enabled in the reported searches.
Independent checks exhaust9,664 words/4,832 legal edges in bases2..5,
widths1..4, with ordinary-integer fixtures, plus112 known/padded cycle edges.

## 6. Independent controls

All eight Lean-source certificates (bases2,4,8,11,16,17,26,32) are parsed
directly, padded to common exterior widths, 和 checked with u=g. The SMT
model accepts pinned coefficients with free digits/carries; resulting words
pass independent positional arithmetic, unchanged-mirror exterior replay,
和 full cycleOK after coupling with their known centers. A tiny unpinned
base2 search also finds an independently replayed full certificate.

`two_lap_equations_check.py` is independent of the solver. Normal 和
optimized Python agree on7,354 small words,29,416 padding identities,
24,219 arbitrary-trim transports,7,350 fixed-width equivalences, 和3,675
rejected incorrect overflow boundaries. It replays224 rotated/repeated/
padded known-source certificates, totaling2,688 full edges.

`two_lap_solver_checks.py` compares the solver with exhaustive ordinary
integer enumeration in13 complete boxes: base2 widths1..3/periods2..4,
和 base3 widths1..2/periods2..3. Every one of1,168 e/g pairs is checked in
four variants: bit vectors/integer arithmetic, each with/without head support.
All4,672 calls agree:32 SAT,4,640 UNSAT, zero mismatches/unknowns. All32 SAT
witnesses couple to known centers, checking128 full edges. Runtime32.493s,
peak74,736KiB. Injected UNKNOWN, false SAT, 和 expired-budget controls fail
closed under `python -O`.

The separate oracle checks7,406 normalization cases 和104 integer/mirror
fixtures:48 target-center plus56 known-source edges. These named test counts
are not one disjoint aggregated population.

## 7. Complete P48 spatial exhaustion

The unchanged [Agent108/#423](https://github.com/taco-jpg/p196-algorithm/pull/423)
engine represents the complete correlated spatial frontier for16 temporal
blocks, lengths[1,4,3,4] repeated4. Its terminal test alone fixes e; no
intermediate-state e pruning occurs. Coefficient ports close only after
all16 blocks. Left rotation1 of BOTH streams changes only the temporal cut.
Four cuts0/1/5/8 reproduce every frontier size through10; cut1 uses161,752
nodes there versus315,361 at cut0. No temporal period is shortened.

The decisive run checks every F0..F79, each with zero prescribed-e terminals,
and ends `EXHAUSTED_NO_B_FOR_E / empty_layer / depth=79 / exit=0`.
Selected exact cardinalities:

| Width | Complete frontier size |
|---:|---:|
|0|1|
|1|4,096|
|6|44,118,136,832|
|36|166,879,149,312|
|44 (maximum)|753,581,526,272|
|75|15,917,896,064|
|76|3,918,372,864|
|77|991,801,344|
|78|16,252,928|
|79|0|

The80 layers contain12,265,536,267,537 state occurrences, not distinct B
words. All37 sizes0..36 agree exactly with a previous history-mode run;
the k2 counts through7 also agree with116/#428's independent block language.
Resource receipt:3,161,664,080 operations;491.642s native/494.741s with
build;1,483,100KiB peak. Limits were900 native seconds,6B operations,
6M resident nodes,4GiB. None was reached. Peak resident nodes1,984,374;
20,837,947 allocated,20,586,710 reclaimed across79 collections. Remaining
251,237 nodes retain checkpoints; the CURRENT frontier is exactly empty.

**Why ANY e follows:** the prescribed e changes only terminal counts, never
images. Every neutral terminal for every e has an all9 self-loop. Therefore
any earlier accepting word for any e would persist to F79; any longer path
must pass F79. Its emptiness excludes both. This is a PAPER consequence of
the computed empty language, not a claim to have enumerated all e words.
Common-width padding then covers arbitrary finite widths/natural trims.

Before live collection, historical-node caps left width17,24,36 complete;
those pilot statuses remain UNDECIDED at arbitrary width and are superseded
by the completed run. The separate bounded solver outcomes are:

| Backend | W | Completed result | Seconds | Peak MiB |
|---|---:|---|---:|---:|
| Z3 direct bit blast |8|UNSAT|1.186|93.785|
| Z3 direct bit blast |16|UNDECIDED, timeout|120.037|166.645|
| Z3 generic BV |8|UNDECIDED, timeout|120.100|1887.629|
| Z3 generic BV |16|UNDECIDED, memory|19.367|1920.699|
| Z3 integer |4|UNDECIDED, timeout|30.032|75.574|
| Independent CP-SAT |8|UNDECIDED, wall cap|120.048|not captured|

Z3 package5.3.2.0 reports5.3.2; direct mode is simplify/bit-blast/sat.
CP-SAT uses OR-Tools9.15.6755, one worker. Its normal 和 optimized unpruned
selftests each pass8 pinned sources,1 free positive,4 exhaustive negatives,
和 target W1/2/4. The final supervisor records failed-worker memory 和
reserves an audit window; its1ms cap returns UNDECIDED. No long run was
repeated after that metadata-only change. CP W16 和 SMT W32 were deferred
after109's stronger width16/all-lap result 和 the exact MDD became available.

## 8. Reproduction 和 repository gate

The running binary hash was49bb997c25efef247d2935ac40b88d93e0419ec31b0af2835b21a30cbc23f677,
identical to108's audited release. Both optimized dependency suites pass:
259,160 tiles/363 complete sets, then975 live sets/6,267,273 records,
138 positive B edges/828 integer steps, structural/Brent/replay/cap guards.
Our P48 seam control independently checks x0=4,x24=8,x48=4; both separately
closed halves reject it. A second-lap carry mismatch at31 is rejected.
These synthetic local controls do not claim physical reachability.

`two_lap_mdd_run.py` pins dependency hashes, restores phase, derives natural
trims, 和 requires48 coupled integer/mirror edges before candidate output.
Normal/-O controls:8 sources,56 canonical/224 rotated edges,21 parser cases,
2 dependency guards,1 real timeout-output preservation control. Interrupted
output keeps complete witnesses; missing offline metadata gives no bound.
From repo root, with unchanged credited dependency code:

```bash
python3 -O calculation/agent-115/two_lap_oracle.py selftest
python3 -O calculation/agent-115/two_lap_equations_check.py
python3 -O calculation/agent-115/two_lap_tail_projection.py selftest
python3 -O calculation/agent-115/two_lap_mdd_controls.py --seconds 45 --memory-mib 1024
python3 -O calculation/agent-115/two_lap_mdd_run.py selftest
PYTHONPATH=/tmp/p196-agent115-python python3 -O calculation/agent-115/two_lap_solver_checks.py --seconds 58
PYTHONPATH=/tmp/p196-agent115-python python3 calculation/agent-115/two_lap_solver.py solve --width 8 --encoding bv-direct --seconds 120 --memory-mib 3072
PYTHONPATH=/tmp/p196-agent115-cpsat python3 -O calculation/agent-115/two_lap_cp_solver.py selftest --seconds 120 --memory-mib 3072 --no-head-prune
python3 -O calculation/agent-108/exterior_run.py selftest
python3 -O calculation/agent-108/exterior_run.py live-selftest
python3 calculation/agent-108/exterior_run.py run 100010010001100010010001100010010001100010010001 --e 101001101001010110010110101001101001010110010110 --witness --live --nodes 6000000 --operations 6000000000 --seconds 900 --gib 4
python3 calculation/agent-115/two_lap_mdd_run.py run --phase-shift 1 --live --nodes 6000000 --operations 6000000000 --seconds 1200 --gib 4
```

Install the separately pinned solvers using `python3 -m pip install --target`
with `/tmp/p196-agent115-python z3-solver==5.3.2.0` or
`/tmp/p196-agent115-cpsat ortools==9.15.6755`, respectively.
The Agent108 run command reproduces the exact native budget; the own wrapper
offers the same decision with a1200s total budget and preserved timeout data.
Actual `python3 tools/verify.py --changed` PASS:5,217 Lean files/301 projects;
0 changed modules/0 endpoints,38.913s/50,868KiB. No new Lean result is claimed.
No additional center lap, different overflow word, global one-band
impossibility, or decimal Lychrel conclusion follows from this result.
