# Agent 118 — T4.segment-MDD / T3.P48

## Result 和 exact scope

**COMPUTED:** no center cycle of any finite length exists for the decimal driver
`e=(101010010101)^4`, `g=(100010001000)^4`, period48, total overflow12.
The exact computation uses the binary trim schedule `v=(00001000)^6`.
The credited arbitrary-schedule padding theorem extends this negative to every
nonnegative trim schedule for this driver. The three documented p12 streams
are time rotations of one B-cycle, so the statement covers their fourfold
repetitions after corresponding time rotation.

This resolves the P48 case left UNDECIDED by the explicit Cartesian frontier in
[PR340](https://github.com/taco-jpg/p196-algorithm/pull/340).
It does 不 exclude other decimal drivers or unrestricted repetition counts,
does 不 establish global one-band impossibility, 和 supplies no decimal
certificate or new Lean theorem. All new files are computation/report files.

**PAPER PROOF:** the new representation computes the exact same frontier image
as the existing local segment transitions, preserving all input correlations.
The computation is subject to ordinary implementation review; an independent
external implementation is separately claimed by Agent111.

Dependency: this PR stacks on PR340, commit
`7e4d7449e63154404b14ce083281ec5ed62d96d0`, for `build_center.py` 和
`check_center.py`. Baseline main:
`eafbbbfd6b5b857597f95f68268c56dbd96b6bcb`.
[Claim](https://github.com/taco-jpg/p196-algorithm/issues/289#issuecomment-6432936525),
[preliminary progress](https://github.com/taco-jpg/p196-algorithm/issues/289#issuecomment-6433010727).

## Credited ingredients

The local arithmetic generator, segmented state semantics, 和 all-length
generic-frontier/terminal-tail reduction come from the existing
`calculation/neutral_band/structure/cauto_fast.cpp`.
Agent7 owns neutral padding covariance; Agent107's
[PR336](https://github.com/taco-jpg/p196-algorithm/pull/336) gives arbitrary
equal-total trim-schedule transport; Agent110 owns balanced-profile corollaries.
Agent10 identified earlier capacity limitations. Agent113 owns reusable runtime
infrastructure. Agent101's cumulative individual-state reachability is a
different representation/reduction. Agent111 retains P33 和 independent MDD
validation. The present claim is exact MDD frontier representation 和 P48.

## Exact relational image

For segment s, the unchanged local table maps its old state ID q_s to choices
`(y_s,c_s)`. Here c_s is a coefficient in `0..2b-2`, or inactive sentinel -1.
The explicit Cartesian engine emits the cyclic tuple

`q'_s = getLid(s, y_s, c_(s+1))`, with `c_NS=c_0`.

A frontier is a finite language of complete old-state tuples. It is represented
by an ordered multi-valued decision DAG: every level is one segment, arcs carry
local state IDs, node0 is the empty language, 和 node1 accepts only the empty
suffix after the final level. No variable level is skipped. Interning compares
the full `(level, sorted arcs)` after hashing, so collisions cannot merge
different languages. Equal-label arcs combine suffixes by exact language union.

Fix initial coefficient a=c_0. For an old suffix node q at level s, define
`I_s(q,c,a)` by union over each old arc `ell -> q'`, each local choice
`(y,c)` in `T_s(ell)`, 和 every next coefficient d:

`[getLid(s,y,d)] . I_(s+1)(q',d,a)`.

At the final segment require d=a. At the terminal node accept iff c=a.
Union `I_0(root,a,a)` over every permitted a.

Induction on the remaining levels proves exactness: each produced path selects
one whole original input path 和 compatible local choices; conversely every
such choice appears in the union. Retaining q' is essential. Replacing the
old frontier by its coordinate marginals would introduce spurious tuples;
the independent test contains an explicit 2-versus-4 counterexample.

The implementation uses immutable `deque` nodes, persistent IDs, fresh image
memoization per layer, 和 the full key `(old node, required c, initial a)`.
Local choices are copied before recursion, avoiding invalidation when original
local pools grow. Canonical root equality therefore certifies equality of the
complete represented frontiers. Counts are auxiliary unsigned128 values with
an explicit saturation flag; neither equality nor acceptance uses those counts.

## All-length coverage

The special first layer is handled separately. From layer1 onward, generic
local signatures are stationary. Exact equality `F6=F7` thus proves a fixed
generic frontier at every later layer.

For this selected schedule every phase center length is m or m+1. For either
initial parity, exactly two layers remain after the common generic prefix.
Increasing m by2 shifts every half-length index by1, preserving both terminal
signatures. Widths1..12 cover transient prefixes; widths13 和14 cover the two
stationary tails. All these tails are empty.

The general implementation conservatively scans widths below mlo=97 plus
two eventual representatives, with memoization by initial parity 和 generic
frontier index. It reports14 distinct tails, period1, two classes, zero hits.
Empty centers are impossible under the required complementary entering/exiting
carry condition, so excluding positive lengths covers every permitted center.

For schedule transport, if an original cycle uses trims u 和 target schedule v,
choose padding offsets satisfying `a_(t+1)=a_t+u_t-v_t`, shifted so all are
nonnegative. Equal totals permit cyclic offsets. The credited identity
`F_t(P_a C)=P_a(F_t C)` produces a cycle with schedule v. Therefore its absence
at all widths excludes the original trims as well. No bounded-width assertion
is transported through this argument.

## Reproduction 和 measured output

Build the pinned core 和 independent checks from repository root:

```bash
python3 calculation/agent-118/build_center.py --out-dir /tmp/p196-agent118-center
python3 calculation/agent-118/build_mdd.py --out-dir /tmp/p196-agent118-mdd
python3 calculation/agent-118/test_mdd.py --binary /tmp/p196-agent118-mdd/center_mdd --baseline /tmp/p196-agent118-center/cauto118
python3 calculation/agent-118/run_mdd.py /tmp/p196-agent118-mdd/center_mdd --ops 20000000 --seconds 120
```

The final command uses one process,4GiB address-space limit,120s wall limit,
1,000,000 DAG-node budget,20,000,000 charged operations,120 generic layers.
Measured wall0.567s, peak child RSS15,588KiB. Exact generic frontier counts:

| Layer | Complete tuples | Cumulative DAG nodes |
|---:|---:|---:|
| 1 | 1,000,000 | 95 |
| 2 | 935,560,192 | 1,401 |
| 3 | 8,574,299,136 | 3,588 |
| 4 | 8,868,958,208 | 4,228 |
| 5 | 9,157,137,472 | 5,234 |
| 6 | 9,312,887,872 | 5,806 |
| 7 | 9,312,887,872 | 5,806 |

Terminal marker:
`MDD_DONE status=none scope=allm jstar=6 period=1 mlo=97 classes=2 hits=0 tails=14 nodes=5883 ops=15947757 comparisons=0`.
Wrapper JSON status is `NONE`, returncode0. The77 extra terminal nodes are
included in the final total5,883; generic totals already include intermediate
union nodes, so they are conservative representation-size counts.

The pre-existing P24 result is reproduced with:

```bash
python3 calculation/agent-118/run_mdd.py /tmp/p196-agent118-mdd/center_mdd --e 101010010101101010010101 --g 100010001000100010001000 --v 000010000000100000001000 --seconds 120
```

It returns `NONE`, `jstar=6`, period1,mlo49,classes2,tails14,nodes1449.
All original generic counts agree:
`1000,30592,93376,116128,140104,152584,152584`.
This is a regression of established work, 不 a new P24 exclusion.

## Independent validation 和 guarded failure

`test_mdd.py` contains a separately authored Python explicit Cartesian oracle
和 Python decision-DAG image. Its abstract suite checks135 models,485 input
words,2,082 output words, including cyclic closure, merged suffixes, dead rows,
one segment, inactive -1, duplicate choices, empty frontier, 和 rejected zero
segments. Exact finite sets 和 canonical roots agree in every case.

Production validation compares decoded complete C++ MDD frontiers against
the original explicit `Fast::step`, preserving actual local state IDs.
Seven complete all-length controls give264 whole-frontier equalities,
including P24 balanced, rotated, 和 concentrated schedules. A separate P48
first-layer check matches all1,000,000 tuples before deliberately stopping
with `UNDECIDED` at the one-layer detection budget. Sixty-six positive witnesses,
310 edges, are independently replayed by the integer arithmetic in
`check_center.py`; all seven baseline decisions/metadata/feasible-width sets
agree, with zero discrepancies. Three resource/scope guards reject safely.

Sanitizer reproduction:

```bash
ASAN_OPTIONS=detect_leaks=0 python3 calculation/agent-118/build_mdd.py --sanitize --out-dir /tmp/p196-agent118-mdd-asan
ASAN_OPTIONS=detect_leaks=0 /tmp/p196-agent118-mdd-asan/center_mdd 10 101010010101101010010101101010010101101010010101 100010001000100010001000100010001000100010001000 1 1 -v 000010000000100000001000000010000000100000001000 -allm -nodes 1000000 -ops 25000000 -layers 120
```

ASan/UBSan gives the same complete P48 output in5.016s, with no diagnostics.
Separate sanitized finite runs at widths13,14,15 also exhaust their tails.
Insufficient node/memo/operation budgets, no detected generic period, unsupported
zero trims, malformed input, failed witness reconstruction, timeouts, 和 memory
failures remain `UNDECIDED`. A cap never produces an empty frontier result.
Requested witnesses must pass the original independent center replay before
printing; optional Python replay uses a separate positional-integer formulation.

The builder verifies original source SHA256
`eb2e6b18b09fdfcae0a5b6b818d23291123ed6a76b59fb6e531589e7f6d00fff`.
MDD C++ source SHA256
`c28ab048aa557363f5bfafe3d15063f76cc867143fa7a8631d56abc991b453b8`.
Generated headers 和 binaries stay outside the repository.

### Separate finite-width arithmetic model

`check_mdd_tail.py` independently states integer coefficient/digit/carry
equations, symmetry, exact neutral trims, 和 cyclic phase closure. It imports
no MDD or local transition code. Using a Python environment with SciPy:

```bash
"$CODEX_PRIMARY_RUNTIME_PYTHON" calculation/agent-118/check_mdd_tail.py --width 13
"$CODEX_PRIMARY_RUNTIME_PYTHON" calculation/agent-118/check_mdd_tail.py --width 14
"$CODEX_PRIMARY_RUNTIME_PYTHON" calculation/agent-118/check_mdd_tail.py --control
```

Each worker uses one solver thread,3GiB address-space limit,120s solver limit.
Widths13 和14 both return **UNDECIDED** at that limit: HiGHS status13,
SciPy status1, no primal solution. Width13:1,584 integer variables,1,308
equations,4,416 nonzeros,120.015s,85,776KiB RSS. Width14:1,704 variables,
1,404 equations,4,752 nonzeros,120.006s,86,812KiB RSS. Neither is a negative
result or independent corroboration of the complete P48 exclusion.

The base26 positive control uses42 integer variables/38 equations, returns
FEASIBLE in0.021s, 和 passes exact Python-integer replay of all four edges.
Its center starts `[32,20,20,32]`. Any numerical infeasibility returned by this
auxiliary model would be labeled `NUMERICAL_INFEASIBLE`, separate from the exact
MDD decision; this experiment produced no such result.

## Verification 和 next question

Repository gate: `python3 tools/verify.py --changed` passes:5,217 registered
Lean files,301 projects,0 changed Lean modules,0 endpoint audits.
Output: `ALL CHECKS PASSED (changed files only, against origin/main)`.
No Lean source changes are proposed. A zero-module gate pass checks repository
rules, 不 the computational exclusion as a kernel theorem.

The next useful question is whether the repeated local segment relations admit
a proof uniform in the number of temporal repetitions. A finite P48 negative
alone does 不 answer that question; any new all-k claim requires a separate
argument 和 assignment.
