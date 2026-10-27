# Agent 118 — T3.p12-k4-all-length

## Result 和 scope

**COMPUTED:** the guarded period-48 experiment remains **UNDECIDED**.
The documented decimal driver
`e=(101010010101)^4`, `g=(100010001000)^4`
reaches the 2,000,000-state frontier cap before generic-frontier periodicity
is established. Neither tested schedule supplies a center witness or an
all-length negative. Arbitrary repetition counts also remain unresolved.

The deliverable is a reproducible, source-pinned experiment with independently
checked arithmetic, explicit resource outcomes, 和 supported long-period
positive controls. It changes no Lean module. Repository verification passes
with zero changed Lean modules; this does 不 establish a new Lean theorem.

Baseline: main `eafbbbfd6b5b857597f95f68268c56dbd96b6bcb`.
Coordination: [claim](https://github.com/taco-jpg/p196-algorithm/issues/289#issuecomment-6432821294),
[progress](https://github.com/taco-jpg/p196-algorithm/issues/289#issuecomment-6432879655).

## Credited reductions 和 independent audit

Agent7 proved neutral padding covariance; Agent107 owns the general trim-schedule
transport theorem, 和 Agent110 owns the balanced-profile corollary.
Agent10 identified the original capacity limits. Agent113 owns reusable runtime
infrastructure; the present small pinned build serves this concrete experiment.
The original exact segment-transfer solver remains the arithmetic engine.

For fixed driver bits, write `P_a(C)=9^a ++ C ++ 9^a`.
Given original trims v 和 desired trims w with equal total, choose
`a_(t+1)=a_t+v_t-w_t`, shifted by a common constant to make every a nonnegative.
The credited identity `F_t(P_a(C))=P_a(F_t(C))` transports the closed center
cycle to schedule w. The entering/exiting carries remain valid. Consequently,
an all-length negative for a single prescribed schedule would exclude arbitrary
original trims at this exact driver period. Equal finite-width caps generally
do 不 transfer under an arbitrary schedule change.

The selected balanced schedule is `w=(00001000)^6`. It has total trim6,
six segments of length8, 和 relative phase lengths0 or1. Selected overflow
steps can trim in padded representatives. A second tested schedule puts its
six trim bits at indices3..8, giving maximum segment length43.

Independent inspection of `setup_instance`, `Fast::sigFor/step/detect/sameSet`,
`decide`, 和 `allm_pattern` supports the existing all-length reduction:

- Generic layers after the initial layer use a stationary transition.
- Period detection compares complete state sets; fingerprints only filter comparisons.
- Increasing m0 by2 shifts every phase length by2 和 every half-length index by1.
- Hence the finite terminal part depends only on parity 和 the generic-frontier phase.
- Every shorter width plus `2*period` long-width representatives covers all widths.

The runner accepts an all-length `NONE` only with exit0, exactly1 `DONE none`,
positive detected period, `classes=2*period`, `mlo>2P`, 和 no
`FEASIBLE`, `CAPPED`, `NOPERIOD`, or `UNDECIDED` output.
Failure to establish a repeated frontier within120 generic layers remains
`UNDECIDED`; elapsed search alone supplies no exclusion.

## Guarded source reuse

`build_center.py` reads the existing `neutral_band/structure/cauto_fast.cpp`.
Upstream SHA256:
`eb2e6b18b09fdfcae0a5b6b818d23291123ed6a76b59fb6e531589e7f6d00fff`.
It verifies exact patch anchors 和 creates generated C++ only outside the repo.
Generated C++ SHA256:
`902dfbe0de1987da55ab40a5f1cc8f0d46f951307647a842ddd2260a7a9e5b9d`.

Changes: MAXP/MAXL48; strict binary stream, trim-total, option 和 range guards;
256-bit packing checks; local ID/pool/witness-choice capacity checks;
an immediate frontier-cap check inside the Cartesian product;
failure on a missing all-length threshold; verified fallback witnesses;
explicit `UNDECIDED`/exit2 for unsupported or incomplete outcomes.
Transition equations 和 complete-set equality remain unchanged.
The target needs `2P+6G+7V=210` packed bits.

## Exact reproduction

From repository root, build 和 run independent checks:

```bash
python3 calculation/agent-118/build_center.py --out-dir /tmp/p196-agent118-center --selftest
python3 calculation/agent-118/check_center.py --solver /tmp/p196-agent118-center/cauto118
ASAN_OPTIONS=detect_leaks=0 python3 calculation/agent-118/build_center.py --out-dir /tmp/p196-agent118-center-asan --sanitize --selftest
```

The new target run:

```bash
python3 calculation/agent-118/run_center.py /tmp/p196-agent118-center/cauto118 --cap 2000000 --seconds 120 --no-witness
python3 calculation/agent-118/run_center.py /tmp/p196-agent118-center/cauto118 --v 000111111000000000000000000000000000000000000000 --cap 2000000 --seconds 120 --no-witness
```

Both commands exit2 with JSON status `UNDECIDED`. Address-space ceiling:4GiB;
wall ceiling:120 seconds; process count1 per command. Measured outcomes:

| Schedule | Complete generic layer1 | Next layer status | Peak frontier | Wall | Peak RSS |
|---|---:|---|---:|---:|---:|
| `(00001000)^6` | 1,000,000 | capped | 2,000,001 | 0.684s | 94MiB |
| six trims at3..8 | 49,136 | capped | 2,000,001 | 0.610s | 106MiB |

Both runs stop before any complete all-length classification. These are
measured implementation limits, with no inference of absence.

Existing-result regression, reproduced to validate the extended solver:

```bash
python3 calculation/agent-118/run_center.py /tmp/p196-agent118-center/cauto118 --e 101010010101101010010101 --g 100010001000100010001000 --v 000010000000100000001000 --cap 1000000 --seconds 120 --no-witness
```

Output: `NONE`, `jstar=6`, `period=1`, `mlo=49`, `classes=2`,
`maxstates=152584`, `tails=14`. Generic frontier sizes:
`1000,30592,93376,116128,140104,152584,152584`.
This is the pre-existing p12/k2 negative, with attribution retained.

## Independent validation

`check_center.py` implements the center transition via positional integers:
`N=e+val_b(C)`, require `N//b^m=1-e`, extract exactly m low digits,
append `(b-1)*e` iff g=1, pair with reversal, then check/remove exactly v
neutral outer pairs. It imports no solver or mirror transition implementation.

Completed checks, with zero disagreements:

- Eight existing certificate bases;56 original center edges.
- 1,344 transported edges, including nonbinary concentrated trim schedules.
- 10,000 independent full-template integer center extractions.
- 1,048 finite-width exhaustive/seeded comparisons;186 are feasible positives.
- Eight original-source solver positives 和 a repeated base32 P48 positive.
- Guard tests:10 malformed/capacity rejections, cap1 explicitly undecided,
  和27 original-vs-extended all-length comparisons.
- A base32 P48 positive with a45-step segment; independent48-edge replay.
  The same test 和 guard suite pass ASan/UBSan without diagnostics.

A repeated base2 P48 case needs324 legacy bits 和 is deliberately rejected.
The helper supports only the stated guarded capacity, regardless of period alone.
`check_center.py --replay-stdin` independently validates future printed witnesses.

Repository gate: `python3 tools/verify.py --changed` prints
`ALL CHECKS PASSED (changed files only, against origin/main)`;
5217 registered Lean files,301 projects,0 changed Lean modules.

## Next concrete question

The balanced first layer already contains1,000,000 Cartesian product states.
An exact compressed representation of segment-state tuples may avoid expanding
every combination. Cumulative individual-state reachability is separately
owned by Agent101. The next Agent118 scope will investigate exact decision-DAG
compression for this P48 experiment, with independently enumerable controls.
