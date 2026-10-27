# Agent 114 — complete exterior cycle and trim-schedule transport

## Result, dependencies, and attribution

**LEAN-VERIFIED:** compatible natural exterior padding offsets preserve the
unchanged A120 `chainOK` checker in both directions. Closed offsets preserve
the complete `cycleOK` checker, including nonemptiness, endpoint closure,
overflow, and gain. Every prescribed nonnegative exterior-trim schedule with
the same number of edges and total trim has an explicit transported cycle.
The center words and center trims remain fixed.

This result depends on the verified local exterior-padding API in
[PR 366](https://github.com/taco-jpg/p196-algorithm/pull/366), commit
`7ccb2d3fbc04a9cfb15d56f2d1528707361219d8`.
The proposed review branch stacks on that parent, not directly on main.
The tested main baseline is `eafbbbfd6b5b857597f95f68268c56dbd96b6bcb`.

Prior mathematics is credited: Agent 7's padding and normalization
[PR 315](https://github.com/taco-jpg/p196-algorithm/pull/315) and
[PR 326](https://github.com/taco-jpg/p196-algorithm/pull/326);
Agent 107's schedule argument
[PR 336](https://github.com/taco-jpg/p196-algorithm/pull/336) and exterior
retiming controls in [PR 363](https://github.com/taco-jpg/p196-algorithm/pull/363).
The all-natural prefix-plus-suffix construction was explicitly announced by
[Agent 104](https://github.com/taco-jpg/p196-algorithm/issues/289#issuecomment-6433077061)
for the separate center-schedule formalization. No retiming discovery is claimed.

Agent 104's whole-center transport and Agent 119's local-center foundations
remain separate. This contribution modifies exterior `B/u` and preserves `C/v`.

## Arbitrary compatible offsets

Write `S_a(B) = B ++ (b-1)^a`. The inductive relation
`PadChain b a z es fs` records a sequence of original and transported edges,
initial padding `a`, and terminal padding `z`. Every edge uses natural offsets
and replacement trim satisfying

```text
a_i + u_i = w_i + a_(i+1).
```

The target offset of one edge is the source offset of the next. No source
acceptance or base restriction is hidden in the relation. The empty plan is
valid with equal endpoint offsets.

The registered endpoints prove:

| Endpoint in `PadChain` | Exact conclusion |
| --- | --- |
| `length_eq` | `fs.length = es.length` |
| `endB_eq` | `endB fs (S_a B) = S_z (endB es B)` |
| `endC_eq` | `endC fs C = endC es C` |
| `chainOK_iff` | `chainOK b fs (S_a B) C = true` iff `chainOK b es B C = true` |
| `gain_balance` | `a + sumGain es = sumGain fs + z` |
| `sumGain_eq` | Closed offsets imply equal total gain |
| `sumGam_eq` | An accepted source chain has equal overflow totals |
| `streams_eq` | An accepted source chain has identical `(e1,e2,gam)` streams |
| `cycleOK_iff` | Closed offsets preserve the complete cycle check in both directions |

Endpoint and gain identities hold even for disconnected or rejected edge lists.
Carry/overflow identities use source acceptance to obtain each edge's actual
`Hyp`. The full cycle equivalence handles a rejected chain separately, so it
does not assume either certificate succeeds.

The proof imports the original `edgeOK` and the local transport theorem.
Common suffix cancellation preserves each source-link comparison and exterior
closure. Gain telescopes by natural arithmetic; no subtraction is used.

## Prescribing a complete exterior schedule

For original trims `u_0,...,u_(P-1)` and requested natural trims
`w_0,...,w_(P-1)`, define

```text
a_i = reserve + sum_(j<i) u_j + sum_(j>=i) w_j.
```

Each local balance equation holds directly. The initial offset is
`reserve + sum w`, and the final offset is `reserve + sum u`; equal totals
therefore close the offsets. No minimum-prefix computation is needed.

`retimeEdges` is an explicit recursive construction. Its registered endpoints
prove the `PadChain` relation, exact output trim list, unchanged center words
and center trims, complete cycle-check equivalence under equal totals, and
existence of a transported accepted cycle with precisely the requested list.
The existence endpoint takes `reserve=0` and pads the starting exterior by
exactly `sum w`.

Every certified use requires equal list lengths. The raw recursive function
stops when either list ends; no theorem interprets a truncated mismatched-list
result. The Python control wrapper rejects mismatched lists explicitly.

## Lean validation

New registered project: `Agent114NeutralExteriorCycle`, two modules and 14
endpoints, all in namespace `Agent114.NeutralExteriorCycle`:

```text
P196.Agent114NeutralExteriorCycle.CycleTransport
P196.Agent114NeutralExteriorCycle.ScheduleTransport
```

Commands, with Lean 4.19.0 on `PATH`, from the repository root:

```bash
export LEAN_NUM_THREADS=1
ulimit -v 8388608
cd lean
timeout 1200 lake build P196.Agent114NeutralExteriorCycle.ScheduleTransport
cd ..
timeout 1200 python3 tools/verify.py --changed
```

Actual combined gate against main, including the unmerged PR 366 dependency:

```text
[rules] 5221 Lean files, 303 projects, OK
[changed] against origin/main: 4 new/changed Lean file(s); building 4 module(s); auditing 2 project(s)
[build] OK
[kernel replay] 4 module(s) re-checked by lean4checker
[axioms] 28 endpoints checked
ALL CHECKS PASSED (changed files only, against origin/main)
```

The 28 audited endpoints are 14 from the parent and 14 new here. All use only
the allowed axioms. No prohibited proof mechanism is used.
Separate one-thread `lake env lean` builds, each with an 8 GiB address-space
limit and 1,200-second timeout:

| New module | Exit | Wall seconds | Peak RSS KiB |
| --- | ---: | ---: | ---: |
| `CycleTransport.lean` | 0 | 0.540 | 450960 |
| `ScheduleTransport.lean` | 0 | 0.602 | 444480 |

Resource measurements use `time.monotonic` and per-child `os.wait4` because
`/usr/bin/time` is absent. Both files meet the repository budget.

## Independent arithmetic controls — COMPUTED

The new script explicitly reuses the parent's independent whole-integer
normalization and edge arithmetic. It separately implements chain acceptance,
endpoints, cycle closure/gain, guarded transport, and two independent formulas
for the natural offsets. The original mirror supplies source fixtures and
differential cycle decisions.

```bash
python3 calculation/agent-114/exterior_cycle_controls.py
python3 -O calculation/agent-114/exterior_cycle_controls.py
```

Both exact final runs produce identical counters and end with
`ALL EXTERIOR CYCLE CONTROLS PASSED`. Fixed seed: `114002`.

| Control | Exact count |
| --- | ---: |
| Existing source bases / edges | 8 / 56 |
| All equal-total requested schedules for those certificates | 252 |
| Retimed cycles at extra reserves 0 and 5 / edges | 504 / 4464 |
| Additional cycles with extra reserve 1024 | 8 |
| Full chain equivalences, accepted / rejected | 2009 / 5520 |
| Empty-chain cases | 118 |
| Endpoint / gain / overflow-total identities | 7529 each |
| Per-edge complete carry/overflow stream identities | 29580 |
| Original-mirror cycle comparisons | 15058 |
| Accepted / rejected closed-offset cycle equivalences | 518 / 881 |
| Rotated source prefixes / seeded chains | 504 / 992 |
| Seeded empty-exterior sources | 124 |
| Rejected malformed checker / schedule / transport inputs | 15 / 9 / 18 |

All 252 weak compositions of the known exterior trim budget two are covered,
with a combinatorial count and duplicate check. The seeded chains span bases
2–32. Negative cases include wrong start words, disconnected individually valid
edges, and corrupted targets. Both tuple and list word representations pass.
Arithmetic-only controls include counters of size `10^80` and reserves
`10^120`. Explicit branch checks remain enabled under optimized Python.

## Scope limits

This proves transport of an existing accepted certificate and exact checker
equivalence. It does not create acceptance from an unaccepted input. The
number of listed edges is preserved; no claim concerns the least period of
the interface sequence.

Padding may increase exterior widths. No width-preserving reduction,
minimal-padding bound, maximal-suffix canonicalization, center retiming,
new base-10 certificate, unbounded search exclusion, or decimal Lychrel
existence theorem is claimed.
