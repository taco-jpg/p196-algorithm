# Agent 111 — guarded long-period center decisions

Task: T3.p11.k3-allwidth / T4.compiled-long-period, issue #289.
Source baseline: `eafbbbfd6b5b857597f95f68268c56dbd96b6bcb`.

## Result 和 scope

**COMPUTED:** a source-pinned extension of the existing exact center automaton
compiles with period/segment limits 48, explicit input/packing/index guards,
immediate state-cap enforcement, 和 process resource limits. Independent
ordinary-integer arithmetic checks agree with its finite decisions 和 extracted
positive witnesses. The shared solver remains unchanged.

**UNDECIDED:** the base-10 driver `e=10100110011`, `g=11100010000`, repeated
three times (P=33, G=12), remains unresolved at unrestricted center width.
The minimum-first-layer schedule below reaches the explicit 4,000,000-state cap.
No finite failure, cap, or timeout is interpreted as absence.

**PAPER PROOF + COMPUTED:** an exact cyclic partition algorithm minimizes the
FIRST generic frontier over every binary trim schedule of the required weight.
For P33 it reduces this objective from 42,875 to 1,728 states. It does **not**
minimize later frontiers or total runtime; the second frontier can be larger.

No new Lean theorem, decimal certificate, all-k obstruction, or universal
one-band impossibility is claimed. A repository-gate PASS with zero changed
Lean modules supplies repository compliance, not a mathematical verification.

## Prior results retained

- `calculation/neutral_band/structure/cauto_fast.cpp` supplies the exact layer
  equations, factorized segment transitions, frontier equality, 和 all-length
  tail construction. This contribution does not reattribute that algorithm.
- Agent10's static limit audit is issue #292. This contribution supplies the
  compiled guard implementation, sanitizer checks, 和 independent arithmetic.
- Agent7's neutral-padding covariance is in PR #315 / issue #301.
- Agent107 owns arbitrary equal-total trim-schedule transport
  [6432786581](https://github.com/taco-jpg/p196-algorithm/issues/289#issuecomment-6432786581).
  Agent110 owns its balanced-width corollary
  [6432826635](https://github.com/taco-jpg/p196-algorithm/issues/289#issuecomment-6432826635).
  These results justify choosing any one schedule for **unbounded** widths.
  Padding does not preserve a specified width cap.
- Agent118 retains the concrete P48 decimal decision; P48 examples here are
  boundary/positive controls only. Agent101 retains cumulative-reachability
  tooling. Agent113 is invited to independently validate this compiled extension.

## Exact build transformation

`long_center.py` reads the original C++ source, checks its SHA-256, applies
literal substitutions with exact occurrence counts, 和 compiles a temporary
source file. It rejects an altered upstream source before building.

```
upstream: eb2e6b18b09fdfcae0a5b6b818d23291123ed6a76b59fb6e531589e7f6d00fff
generated: 01077a522265dbaa2e6428b352b2497ffea8bcc163cce903fcf69c1e32582bfc
```

Changes: MAXP/MAXL become 48; MAXNS remains 16. Explicit binary streams/trims,
base 2..62, positive bounded width arguments, sum(g)=2sum(v), key width<=256,
numeric caps, supported options, 和 finite IDs are checked. Witness choices use
uint32 instead of uint16. The key requires `2P+6G+7K` bits: 180 for P33/G12/K6,
210 for P48/G12/K6. A 324-bit case is explicitly rejected.

The old fast path checked its cap only after a complete per-input Cartesian
product. The new guard stops immediately after the first insertion above the
cap, records that frontier, 和 prints an explicit UNDECIDED diagnostic.
Address-space, CPU, 和 wall limits cover allocations outside that frontier.
No transition equation or completed-result acceptance criterion changes.

## All-length coverage audit

Fix a binary schedule v with total K=G/2. Put
`d_t=sum_{s<t}(g_s-2v_s)` 和 `m_t=m0+d_t`. Increasing m0 by 2h increases every
half-width J_t/Jp_t, the first nongeneric layer j0, 和 the final layer by h.
The parity 和 relative tail signatures are unchanged.

The generic transfer is stationary after its special first layer. Repetition
requires equality of the complete frontier sets; fingerprints are only a
prefilter. If a repeat starts at jstar with period q, all sufficiently large m0
are covered by residue classes modulo 2q. The finite smaller widths are checked
separately. Memoization by `(m0%2, generic-frontier index)` is therefore sound.
Failure to establish a repeat within 120 layers, or any cap, remains UNDECIDED.

## First-frontier optimization

At time t in the first generic layer, the low incoming carry is e_t, the
required high outgoing carry is 1-e_t, 和 the overflow partner is (b-1)e_t.
For a coefficient c in 0..2b-2 和 inward high carry h in {0,1}, require

```
floor((c+h)/b) = 1-e_t
c' = (c+e_t)%b + ((c+h)%b if g_t=0 else (b-1)*e_t).
```

A segment starts with arbitrary c0 和 ends at a trim requiring c'=b-1.
A small coefficient DP counts its paths. Distinct `(c0, inward-carry vector)`
produce distinct local configurations: the configuration retains every inward
carry, so c0 reconstructs all intermediate coefficients. The assembled global
state retains every local configuration 和 the next segment's c0. Assembly is
injective, hence the first-frontier count is exactly the product of segment
counts. A minimum-product interval DP over every cyclic anchor enumerates
every K-segment partition, proving global optimality for this objective.

For P33 the selected optimum is
`v=001000000000010000000011100000001`, with segment factors
`12,12,1,1,12,1`, product 1728. The balanced schedule has product 42875.
No implication about later frontiers follows from this comparison.

## Reproduction 和 observed outputs

From the repository root, using Python3 和 a C++17 compiler:

```bash
python3 calculation/agent-111/long_center.py build /tmp/agent111_cauto
python3 calculation/agent-111/long_center.py guard-selftest /tmp/agent111_cauto
python3 -O calculation/agent-111/center_controls.py --binary /tmp/agent111_cauto
python3 calculation/agent-111/schedule_optimizer.py --selftest --solver /tmp/agent111_cauto
python3 calculation/agent-111/p33_trial.py /tmp/agent111_cauto --schedule min-first --cap 4000000 --timeout 60 --memory-mb 4096
```

The last command intentionally exits 2 on an unresolved run. Observed output:

```
UNDECIDED state_cap frontier=4000001 cap=4000000
detect sizes: 1728 2548480
DONE ... status=noperiod ... maxstates=4000001 tails=0 ... sec=2.01 rssMB=188
STATUS=UNDECIDED engine_status=noperiod
```

This is a capped generic-frontier computation; no all-length center verdict was
reached. Timing/RSS describe this machine, not a future larger-run forecast.

Validation totals:

| Independent check | Exact coverage / outcome |
|---|---|
| Existing mirror selftest | Eight known bases accepted |
| Lean-source integer arithmetic | 56 original edges, eight bases |
| Prescribed-schedule arithmetic | 1,264 padded cycles  / 25,760 edges; pass |
| Finite direct-center oracle | 664 patterns  / 3,218 initial widths  / 130,974 centers; 34 feasible, 3,184 infeasible; zero discrepancies |
| Extended-period positive controls | 10 P36/P40/P48 cases; 416 extracted witness edges independently replayed |
| Malformed-input guards | 23 direct-binary rejections; source-tamper 和 324-bit refusal |
| Optimizer brute comparison | 1,860 stream/base cases  / 11,280 schedules; same minima |
| Optimizer first-layer comparison | 24 existing-solver cases; exact counts agree |
| Independent-reference invalid cases | 14 rejected; arithmetic also passes under Python -O |

Sanitizer reproduction:

```bash
python3 calculation/agent-111/long_center.py build /tmp/agent111_cauto_san --sanitize
ASAN_OPTIONS=detect_leaks=0 python3 calculation/agent-111/long_center.py boundary-smoke /tmp/agent111_cauto_san --sanitizer
python3 tools/verify.py --changed
```

AddressSanitizer/UndefinedBehaviorSanitizer passed fast 和 legacy P33/P48
boundary runs, longest segments 28/43, with exact frontier 2 / cap 1 diagnostics.
LeakSanitizer alone was disabled because this host's ptrace environment blocks
its process inspection. These capped runs validate bounds, not nonexistence.

Repository gate: `ALL CHECKS PASSED`, 5,217 registered Lean files  / 301 projects,
zero new/changed Lean modules, zero theorem endpoints audited in changed scope.

## Next exact question

Can an exact compressed representation of the same generic-frontier sets
reach a repeat for P33 without explicitly enumerating millions of tuples?
Any such implementation needs supported-case differentials, extracted positive
witness controls, 和 honest resource-limit handling before a new exclusion.
