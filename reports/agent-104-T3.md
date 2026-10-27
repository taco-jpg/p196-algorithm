# Agent 104 — complete neutral trim-schedule transport

**Status: LEAN-VERIFIED.** The concrete theorem 和 existence equivalence pass
the complete changed-file gate, including the declared local-padding dependency.

## Scope 和 attribution

The target result is a constructive theorem for the unchanged
`Agent120.Neutral.cycleOK`: given a checked certificate 和 any list of natural
center trims of the same length 和 total, construct another checked certificate
with exactly that schedule. Preserve every exterior source/target, exterior
trim, lower carry, overflow, period, 和 total gain. Only centers change.

This formalizes existing mathematics: Agent7 established neutral padding,
Agent107's [PR336](https://github.com/taco-jpg/p196-algorithm/pull/336) gives
general equal-total schedule transport, 和 Agent110's
[PR338](https://github.com/taco-jpg/p196-algorithm/pull/338) gives balanced
width-preserving consequences. Agent119 owns the separate Lean local-padding
covariance 和 one-edge transport foundation in
[PR374](https://github.com/taco-jpg/p196-algorithm/pull/374); this project imports it.
The new contribution is the complete-chain/cycle integration in Lean.

The theorem concerns unrestricted center widths. It does not preserve a
specified width cap, optimize padding, prove a new decimal period exclusion,
or construct a decimal certificate. It does not establish the sharp padding
bound from Agent107's minimum-offset construction. Listed edge count is
preserved; least period need not be.

The concrete endpoint is:

```lean
theorem Agent104.NeutralTrimTransport.cycleOK_retime
    (b : Nat) (es : List Agent120.Neutral.Edge) (ws : List Nat)
    (B C : List Nat) (hc : Agent120.Neutral.cycleOK b es B C = true)
    (hl : es.length = ws.length) (hs : ws.sum = sumV es) :
    Agent120.Neutral.cycleOK b (retimeCenter b es ws) B
      (Agent119.NeutralCenterPadding.padC b ws.sum C) = true
```

Names `sumV` 和 `retimeCenter` are in the Agent104 namespace above.

## Constructive offsets

For source trims v_t 和 target trims w_t, both of length P 和 total K, set

\[
a_t=\sum_{j<t}v_j+\sum_{j\ge t}w_j.
\]

Every offset is a natural number. Direct addition gives

\[
a_t+v_t=w_t+a_{t+1},\qquad a_0=K=a_P.
\]

Thus the source center at phase t is padded by a_t neutral pairs. The local
one-edge theorem changes its trim from v_t to w_t 和 pads the target by
a_(t+1). Adjacent targets 和 sources coincide because their offsets coincide.
Equal totals make the final padding agree with the initial padding.

There is no binary-trim restriction: zeros 和 arbitrary natural entries are
permitted. No center symmetry, nonempty exterior, primitive period, or extra
carry hypothesis is introduced. The original checker supplies each source's
`Hyp` through `edgeOK_sound`.

PAPER observation, also checked in the executable controls: the elementary
bound a_t<=2K gives at most 4K added coefficients per center.
This coarser construction avoids signed prefix minima. The mathematical
existence reduction is the same as the established sharper construction.

## Lean organization

`Structure.lean` defines `sumV` 和 `retime pad q es ws`. The padding function is
a parameter; this module only transforms edge records. At a cons step E,w,
the new source reserve is q+w+sum(ws), the target reserve is
q+E.v+sum(ws), 和 recursion advances q to q+E.v.

Its structural theorems show exact target trims, unchanged exterior fields
和 period, unchanged final B, the precise final C padding, 和

\[
\operatorname{sumGain}(\mathrm{new})+\operatorname{sumV}(\mathrm{old})
=\operatorname{sumGain}(\mathrm{old})+\sum w.
\]

`Chain.lean` packages the two needed local facts as ordinary theorem
hypotheses: checked-edge transport under the offset equation 和 overflow
preservation under padding. These hypotheses are not axioms. Induction
through the exact `chainOK` definition proves checked-chain transport 和
preservation of the full lower-carry/overflow stream.

The cycle argument then proves all five original Boolean clauses:
nonemptiness, checked chaining, B closure, C closure, 和 the gain inequality.
The gain identity above 和 equal totals preserve total gain exactly; the
overflow identity preserves the other side of the gain comparison.

`Schedule.lean` fixes the initial exterior, all per-edge (B,B2,u) triples,
the lower-carry/overflow streams, 和 a schedule. Its `ScheduleRealizable`
predicate quantifies existentially over centers. It proves an existence
equivalence for any two equal-length/equal-total schedules, by applying
forward padding independently in each direction. No inverse-padding theorem
is assumed.

`Main.lean` instantiates all local hypotheses with Agent119's checked
`edgeOK_transport` 和 `gam_padC`. Its `cycleOK_retime` 和
`schedule_realizable_iff` have no unproved local-law premise. The base
parameter is arbitrary: any accepted original edge enforces b>=2 itself.

## Independent executable controls

The supporting script `calculation/agent-104/trim_transport.py` follows this
specific additive-offset construction 和 replays transported certificates
through the unchanged Python mirror. It treats invalid length/total/natural
number inputs as errors even under optimized Python. It depends only on the
baseline mirror 和 its eight baseline certificate fixtures, not another
Agent104 computation script. These fixtures exclude the later base20 result.

```bash
python3 calculation/neutral_band_search.py selftest
python3 calculation/agent-104/trim_transport.py
python3 -O calculation/agent-104/trim_transport.py
```

All three commands passed. Both transport runs report the same exact counts:

| Control | Count |
|---|---:|
| Baseline bases / source edges | 8 / 56 |
| Complete natural schedules, K=1/2, every distinct rotation | 8928 |
| Return-schedule controls with a source trim2 | 56 |
| Total complete cycle replays | 8984 |
| Transformed edge replays | 169872 |
| Arithmetic source/target schedule pairs | 698 |
| Malformed inputs rejected | 20 |

The maximum observed added center width is8 at K2. Each output is replayed
through actual mirror `edgeOK` 和 `cycleOK`; checks also cover unchanged
exterior fields, center carry/overflow, total gain, 和 offset equations.
A separate reviewer derived all counts independently from the eight fixture
periods 和 composition counts, 和 checked the guard behavior under `-O`.

## Verification

All four new modules are registered in `lean/registry.json`, with21 endpoints
under `Agent104.NeutralTrimTransport.`. The dependency is PR374 at commit
`f182aa81cdb4040f6237401bced19fbb863adf4f`, tree
`382415036ed07c5a7cb12e3a6b2ced447dcd54dd`. This branch is stacked directly
on that exact commit; no dependency source is edited. Main is
`eafbbbfd6b5b857597f95f68268c56dbd96b6bcb`.

Stock Lean4.19.0, commit `6caaee842e94`, core + Std. Required gate:

```bash
LEAN_NUM_THREADS=1 python3 tools/verify.py --changed
```

The gate ran in an isolated checkout of the exact parent plus this result:

```text
[rules] 5224 Lean files, 303 projects, OK
[changed] against origin/main: 7 new/changed Lean file(s); building 7 module(s); auditing 2 project(s)
[build] OK
[kernel replay] 7 module(s) re-checked by lean4checker
[axioms] 39 endpoints checked
ALL CHECKS PASSED (changed files only, against origin/main)
```

The total comprises four own modules/21 endpoints 和 three dependency
modules/18 endpoints. Every audited endpoint uses only permitted `propext`,
`Classical.choice`, 和 `Quot.sound`. Official Lean4Checker v4.19.0 source is
commit `e11f65c651edd58d68ba260015d2bfde5102cd7f`.

The portable `measure_lean.py` is unchanged from Agent104's PR364 helper 和
included here for standalone reproduction. Example, from the repository root
with stock Lean/Lake on PATH:

```bash
python3 calculation/agent-104/measure_lean.py lean/P196/Agent104NeutralTrimTransport/Main.lean --hard-as
```

| File | Wall seconds | CPU seconds | Peak RSS (KiB) | Result |
|---|---:|---:|---:|---|
| Structure.lean | 1.126871 | 0.941556 | 453684 | PASS |
| Chain.lean | 0.624641 | 0.613401 | 451384 | PASS |
| Schedule.lean | 0.376909 | 0.297468 | 434856 | PASS |
| Main.lean | 0.525502 | 0.520122 | 434352 | PASS |

Each measurement used one CPU affinity, `LEAN_NUM_THREADS=1`, hard 8 GiB
address-space 和 1,200-second CPU/wall limits, with exit0. Independent source
review covered the structural reserve equations, original-checker chain
induction, gain cancellation, existential quantifiers, concrete local-law
instance, exact assumptions, 和 finite test coverage.
