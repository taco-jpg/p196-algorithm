# Agent 113 — Guarded P48 center runtime

## Scope 和 status

**COMPUTED:** a compiled, source-pinned extension of the existing exact
`calculation/neutral_band/structure/cauto_fast.cpp`, with independent arithmetic,
packing, sanitizer, positive-control 和 interruption regressions.
**没有 new mathematical center exclusion or Lean theorem.**

Task: `T4.P48-compiled-runtime`, coordination #289, claim6432820954,
scope split6432861568. Agent10's static audit #292 identified period, segment
和 packing limits. Agent111 retains the concrete decimal P33 decision;
Agent118 retains P48. Agent101 owns cumulative generic-state reachability.
Agent107 owns general trim-schedule equivalence; Agent110 owns balanced profiles.
Agent7's padding theorem supplies the common mathematical foundation.

The helper supports bases2..62, periods1..48, 和 one explicitly supplied binary
trim schedule satisfying `2*sum(v)=sum(g)`. Its definitive answers preserve the
upstream arithmetic transition equations. Resource-limited runs remain
`UNDECIDED`; increasing capacity does 不 establish any decimal result.

## Source 和 implementation

Baseline main: `eafbbbfd6b5b857597f95f68268c56dbd96b6bcb`.
Upstream source SHA256:
`eb2e6b18b09fdfcae0a5b6b818d23291123ed6a76b59fb6e531589e7f6d00fff`.

`extend_cauto.py` checks that digest 和 every replacement anchor, generates a
temporary C++ source, 和 compiles it. The upstream file remains unchanged.
A changed upstream digest requires a fresh review; the helper refuses to guess.

| Defect / limitation | Guarded behavior |
|---|---|
| `MAXP=32`, `MAXL=32`, `MAXNS=16` | Bounds48,48,24, with explicit segment checks |
| Legacy packed key256 bits | Nine64-bit words; checked individual field writes |
| Malformed streams, trim strings or missing option operands | Native argument rejection before indexing |
| Full Cartesian product formed before checking cap | Check after every inserted successor |
| Local cached relations can grow independently | Configuration/state/transition guards 和 process memory limit |
| Witness choices truncated to16 bits |32-bit choices |
| Legacy witness fallback ignored failure | Every printed requested witness must pass `verify_cycle`, including direct legacy mode |
| Fixed120 generic-layer horizon | Explicit `-jgen`; unfinished detection remains `UNDECIDED` |
| Arbitrary100000 bound when finding long-width threshold | Exact algebraic threshold below |
| `-vall` materializes combinatorially many patterns | Require one explicit `-v`; reject enumeration/skip/partition modes |
| Process timeout/allocation/startup failure | Structured `UNDECIDED`, never an exhausted verdict |

For `P<=48`, `G<=48`, `K=G/2<=24`, the legacy key requires
`2P+6G+7K<=552<576` bits. For base62, `Rd+1<=62` fits6 bits 和
`Z+1<=123` fits7 bits; coefficients/sentinels fit the existing signed8-bit fields.
These are capacity arguments, independently tested by the bit oracle below.

Let `delta_t=sum_(i<t)(g_i-2v_i)`, `dmin=min(delta_t)`.
Since `J_t=ceil((m0+delta_t)/2)`,
`min(J_t)-1>=jstar` iff `m0>=2*jstar+1-dmin`.
Thus `mlo=max(2P+1,2*jstar+1-dmin)` exactly replaces the finite scan.
The generic frontier still uses full set equality after fingerprint filtering;
the original two-parity tail reduction is retained.

## Reproduction

Run from the repository root. Dependencies: Python3 standard library, a C++17
compiler, 和 POSIX resource limits. Optional sanitizer checks use GCC/Clang ASan
和 UBSan. Every research execution remains within the campaign time budget.

```bash
python3 calculation/agent-113/extend_cauto.py --build-only
c++ -O2 -std=c++17 calculation/neutral_band/structure/cauto_fast.cpp -o /tmp/a113-baseline
```

Use the printed executable path as `BINARY` in:

```bash
python3 calculation/agent-113/test_center_runtime.py --binary BINARY --baseline /tmp/a113-baseline
python3 calculation/agent-113/test_runtime_guards.py
python3 calculation/agent-113/test_runtime_guards.py --packing
python3 tools/verify.py --changed
```

Example single-schedule all-length run reproducing an existing p11 negative:

```bash
python3 calculation/agent-113/extend_cauto.py --seconds 120 --memory-mib 2048 -- \
  10 10100110011 11100010000 1 1 -v 11000000000 -allm -w -cap 100000
```

Observed: `DONE ... status=none jstar=4 period=1 mlo=23 classes=2
feasible_classes=0 maxstates=637 tails=10`; structured status `EXHAUSTED`.
This reproduces prior work; it is 不 a new exclusion.

Default wrapper limits:120 seconds,2048MiB address space, one process.
`--seconds` accepts at most1800. Compilation is separately bounded by120 seconds.
`--sanitize` disables the address-space limit because ASan reserves a large
virtual address space; use only the small regression cases in that mode.

## Actual validation

The independent center reference evaluates the entire coefficient word as a
Python integer, normalizes by division by `b^m`, then forms exact reflected
digit sums. It imports 没有 arithmetic from the repository mirror.

| Completed check | Actual output / scope |
|---|---|
| Exhaustive small direct arithmetic |282 stream/trim cases;18424 symmetric initial words |
| Fast/legacy/baseline comparisons |564 comparisons;0 disagreements;42 independently replayed witnesses |
| All-length differential regression |32 patterns;0 disagreements;0 undecided;27 replayed witnesses |
| Existing source controls |56 edges across bases2,4,8,11,16,17,26,32 |
| Positive solver controls |15 cases, including periods33,36,40,48;15 returned witnesses independently replayed |
| Long segment |P48 base32 control, one segment of length45, accepted |
| Expanded legacy key |P40 base26 control needing270 bits accepted with direct `-legacy`,2GiB/30-second limits |
| Invalid input |19 cases rejected before search |
| Known-positive cap regression |P48 base26 source repetition at500000 states returns `CAPPED-UNDECIDED` |
| Forced resource/completion paths |6 cases: local cap, generic horizon, wall timeout, malformed trim, in-product cap, address-space failure; 都 classified conservatively |
| In-product cap evidence |Requested10000, reported `maxstates=10001`, `noperiod`; expansion stops during the product |
| Independent packed-key oracle |100000 random layouts;552 basis bits;553 distinct basis/zero keys;4011 field placements;7 invalid writes rejected |

Packed-key oracle output:

```text
KEY_PROBE PASS random=100000 basis_bits=552 unique_basis_keys=553 field_placements=4011 rejected_invalid=7
```

ASan/UBSan also passed all282 small cases,32 all-length cases,19 invalid inputs,
the known-positive cap regression, 和 three long controls: base4 P36, base32 P48,
base32 P48 with segment45. Address 和 undefined-behavior instrumentation stayed
enabled. LeakSanitizer was disabled because this container's `/proc`/ptrace
restrictions prevent its task inspection; 没有 leak-check claim.

The packing test includes the generated implementation with renamed `main`,
then compares it with a separately written bit-at-a-time oracle. It exercises
every active bit of the maximal552-bit layout, not merely the decimal210-bit case.

Literal repository gate on this code/report-only change:

```text
[rules] 5217 Lean files, 301 projects, OK
[changed] against origin/main: 0 new/changed Lean file(s); building 0 module(s); auditing 0 project(s)
[build] OK
[axioms] 0 endpoints checked
ALL CHECKS PASSED (changed files only, against origin/main)
```

## Interpretation 和 limits

`EXHAUSTED` with `-allm` covers every positive initial center length for the
supplied schedule. Without `-allm`, it covers only the requested length interval.
Generalizing to every trim schedule requires the separately proved transport
theorem in Agent107 PR336; the runtime does 不 assume a bounded-width transport.

`FEASIBLE` is a center result. It supplies 没有 exterior B witness. A decimal
certificate still requires compatible B/C edges, exact mirror `cycleOK`, 和
the registered Lean gate requested by the campaign.

The P48 base26 repeated source control remains undecided at500000 states despite
its known existence. This explicitly demonstrates why a cap is 不 evidence of
nonexistence. The decimal P33/P48 decisions belong to Agents111/118; this report
claims neither a new decimal center negative nor a decimal Lychrel certificate.
