# Agent 110 — Sparse period-12 center graphs at widths 15–17

## Scope 和 attribution

**PAPER PROOF + COMPUTED.** No center cycle for the documented p12 driver
exists at any repetition count with every center width at most17.
This task concerns the documented decimal streams
`e=101010010101`, `g=100010001000`, their joint four-step rotations,
**every repetition count**, 和 arbitrary natural center trims under a
uniform width cap. It extends the exact return-graph method of
[PR370](https://github.com/taco-jpg/p196-algorithm/pull/370).

Agent 3 owns the odd-center alternating-residue/even-midpoint invariant
([issue303](https://github.com/taco-jpg/p196-algorithm/issues/303),
[PR318](https://github.com/taco-jpg/p196-algorithm/pull/318)). This work applies
that existing invariant to a sparse, independently checked enumeration.
Agent 110's balanced cap theorem is
[PR338](https://github.com/taco-jpg/p196-algorithm/pull/338), using Agent 7's
padding covariance 和 Agent 107's schedule transport. Agent 6's earlier
all-repetition width10 bound remains credited
([issue296](https://github.com/taco-jpg/p196-algorithm/issues/296)).

No unrestricted-width center obstruction, other-driver negative, decimal
Lychrel existence theorem, or new Lean theorem is claimed.

## 1. Exact reduction to a sparse partial function

For a legal center edge,

\[
m_{t+1}=m_t+g_t-2v_t,
\quad F_t(C_t)=9^{v_t}\,C_{t+1}\,9^{v_t}.
\]

The entering/exiting normalization carries are `e_t,1-e_t`.
A closed p12 itinerary has `3k=2 sum(v)`, so k is even. Write
`r_t=(sum(g_j,j<t)) mod2`. For every cap W>=2, padding each source to the
largest width<=W with its original parity constructs one of the profiles
`W-1+r_t` or `W-r_t`, without changing e/g or the period. Padding amounts
`a_t=(L_t-m_t)/2` satisfy `a_(t+1)=a_t+v_t-w_t`, so covariance
`F_t(9^a C 9^a)=9^a F_t(C) 9^a` proves every transformed edge.

A12-step shift swaps the profiles because it preserves e/g 和 adds three
overflows. Choose the floor profile, with trims at original phases4,12,20
mod24. Anchor at phase4, where the width is W 和 e=g=v=1. The required
raw endpoint9 forces the source endpoint9; source symmetry supplies both
ends. Thus every candidate cycle gives a directed cycle in the partial
24-step return map on `C=[9] ++ D ++ [9]`, with symmetric D. Conversely,
a cycle of that map is a center cycle under the same cap. All intermediate
widths are W or W-1. This treats original width-one phases 和 arbitrary
nonmaximal trims through the same cap lift.

The unfiltered source encoding is

\[
\mathrm{id}=\sum_{j=0}^{H-1} D_j19^j,
\qquad H=\lfloor(W-1)/2\rfloor,
\qquad N=19^H.
\]

The first H entries determine D by reflection. Source IDs use uint64,
which is essential at W17: N=16,983,563,041 exceeds2^32.

Failed returns have no outgoing edge 和 cannot lie on a cycle. Storing
only successful return edges preserves the exact graph. Vertices outside
all retained edge endpoints are isolated; they require no per-vertex
allocation. This removes the old dense O(N) storage without treating any
unexamined source as failed. Every enumerated candidate is still evaluated.

## 2. Credited odd-width pruning 和 its proof obligation

For every odd center in an overflow-containing closed cycle, Agent 3 proves

\[
A(C):=\sum_i(-1)^i C_i\equiv9\pmod{11},
\qquad C_{(m-1)/2}\text{ is even}.
\]

The p12 driver has positive overflow. Its balanced transformed cycle is
itself a legal cycle, so the invariant applies directly to every odd-W
anchor. Pruning can remove transient states, but it retains **every** cycle
state. Consequently an acyclic induced graph excludes all original cycles;
transient counts 和 path lengths describe the restricted graph only.

For W odd, put `d=(W-3)/2` 和 write D using the outer half
`x_0,...,x_(d-1)` 和 middle x. Since `A(C)=18-A(D)`, the source conditions are

\[
2\sum_{j<d}(-1)^j x_j+(-1)^d x\equiv9\pmod{11},
\qquad x\in\{0,2,4,6,8,10,12,14,16,18\}.
\]

Given the outer half, at most one middle is possible: two distinct even
numbers in0..18 cannot differ by a nonzero multiple of11. The exact table is

| Residue of x modulo11 | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Permitted even x | 0 | 12 | 2 | 14 | 4 | 16 | 6 | 18 | 8 | none | 10 |

Enumerating each19-ary outer half once 和 taking this unique middle is a
bijection onto the invariant-admissible source domain. The middle's place
value is19^d; the prefix occupies lower places. Every retained target is
also checked for domain membership. W16 uses the complete source domain.

An independent11-residue counting recurrence supplies expected domain sizes:
start with mass1 at residue0, then convolve by the19 possible signed
`2*x_j` contributions. Sum masses whose required middle residue is not9.
No carry or temporal transition enters this count.

| W | Unfiltered IDs N | Outer prefixes scanned | Candidate sources before carry | Initial carry flips |
|---:|---:|---:|---:|---:|
| 15 | 893,871,739 | 47,045,881 | 42,768,908 | 21,384,454 |
| 16 | 893,871,739 | 893,871,739 | 893,871,739 | 446,935,869 |
| 17 | 16,983,563,041 | 893,871,739 | 812,610,866 | 406,305,433 |

The initial-flip counts above are predicted independently: coefficient
complementation `x -> 18-x` exchanges exit carries. At odd widths it
preserves the invariant domain 和 has no fixed point because the middle
must be even. At even widths the unique all9 fixed point transmits the
entering carry1 和 fails the required exit0.

## 3. Completed computations

Both independent implementations completely exhausted the following domains.
All counters exclude no source except the explicitly proved odd-width filter.

| W | Complete 24-step paths | Retained return edges | Cyclic states | Max path in searched graph | Sorted-edge FNV1a64 |
|---:|---:|---:|---:|---:|---|
| 15 | 187 | 174 | 0 | 1 | `e7a329174d6ad08d` |
| 16 | 4,985 | 4,683 | 0 | 1 | `9af50d135beef154` |
| 17 | 3,624 | 3,357 | 0 | 1 | `62482c4f38ad2034` |

W15 has13 completed images outside the required neutral-endpoint return
domain; W16 has302 和 W17 has267. No remaining target is rejected by the
invariant filter.
Primary carry-normalization timings: W15 5.974 seconds; W16 124.221 seconds,
both8704KiB peak RSS. Independent positional-integer timings: W15
3.33315896 seconds; W16 53.2760303 seconds. Every completed run exited0,
evaluated exactly its independently predicted candidate count, 和 reported
a complete cycle scan with zero cyclic states.

The W17 comparator ran each implementation once 和 compared the **entire
sorted edge list**, beyond checking the digest. Every edge agrees exactly.
Its independent set check finds **no target that is also a retained source**;
therefore there is no path of length2 in this restricted graph, independently
of either cycle-detection implementation. It also replays256 retained edges
through the baseline mirror, with no mismatch. W17 took126.342 seconds in
the primary implementation (11392KiB peak RSS) 和53.024546 seconds in the
integer reference; the complete comparison took179.478 seconds.

The final W17 counts are exact:16983563041 unfiltered IDs;893871739 scanned
outer prefixes;812610866 admissible sources, all evaluated;406305433 initial
carry flips;3624 completed24-step paths;3357 retained edges;zero cycles.
The odd-width filter is cycle-preserving, so this excludes **all** center
cycles under cap17, including original cycles that require the other balanced
profile before reindexing. The lower-cap results are separate reproducible
controls; cap17 alone supplies the strongest stated exclusion.

## 4. Independent checks 和 reproduction

Three self-contained files are added under `calculation/agent-110/`:

- `p12_sparse_graph.cpp`: ordinary coefficient carry propagation, explicit
  symmetric words, sparse sorted edges, 和 functional-graph traversal.
- `p12_sparse_integer.cpp`: separately authored whole-integer evaluation 和
  repeated decimal quotient/remainder, an odometer enumerator, 和 sparse
  Kahn indegree peeling. It imports no primary implementation.
- `p12_sparse_controls.py`: independent residue/first-nonneutral counting,
  rank/unrank checks, baseline-mirror arithmetic, 和 complete edge comparison.

The reference integer never exceeds the uint64 range at supported widths:
each normalized source has at most17 coefficients in0..18, hence positional
value at most `2*(10^17-1)`. Both programs validate W in2..17 before any
fixed-width allocation or indexing. Source IDs 和 counters are uint64.
Per-run wall limits cannot exceed1500 seconds. The primary explicitly caps
RSS below1GB; the reference uses a conservative sparse-allocation bound
with a default512MiB allowance. Checked resource caps emitUNDECIDED.
Invalid input 和 generic consistency errors are rejected; a killed process
or any missing successful terminal result remains inconclusive. In the
integer reference, generic errors exit1; checked caps 和 allocation failure
exit2. No such outcome supports a negative.

`--map W` deliberately computes the **unfiltered** anchor return for any
valid source ID. In contrast, a census filters odd source/target invariants.
This distinction is tested by16 old W11 successful return sources with odd
midpoints: they remain positive map controls while excluded from the census.
The primary's `--unfiltered` regression mode is restricted to W<=14.

```bash
g++ -O3 -std=c++17 -Wall -Wextra -pedantic \
  calculation/agent-110/p12_sparse_graph.cpp -o /tmp/p196-agent110-p12-sparse
g++ -O3 -std=c++17 -Wall -Wextra -pedantic \
  calculation/agent-110/p12_sparse_integer.cpp -o /tmp/agent110_p12_sparse_integer
/tmp/p196-agent110-p12-sparse 15 --seconds 1500
/tmp/p196-agent110-p12-sparse 16 --seconds 1500
/tmp/agent110_p12_sparse_integer 15 --seconds 1500
/tmp/agent110_p12_sparse_integer 16 --seconds 1500
python3 calculation/agent-110/p12_sparse_controls.py \
  --primary /tmp/p196-agent110-p12-sparse \
  --independent /tmp/agent110_p12_sparse_integer --safeguards
```

The baseline checker finishes with `status=PASS`, exit0. Its defaults are
10000 samples, seed1101715, 和 complete regression graphs W2..10.
The final W17 comparison used this exact separate command, which avoids
repeating the baseline controls:

```bash
python3 - <<'PY'
import json,random,sys
from pathlib import Path
sys.path.insert(0,'calculation/agent-110')
from p12_sparse_controls import compare_graphs
result=compare_graphs([Path('/tmp/p196-agent110-p12-sparse'),Path('/tmp/agent110_p12_sparse_integer')],17,1500,random.Random(1101715))
print(json.dumps(result,sort_keys=True),flush=True)
if result['status']!='COMPLETE_IDENTICAL_ACYCLIC_GRAPHS': raise SystemExit(2)
PY
```

Exit0, `status=COMPLETE_IDENTICAL_ACYCLIC_GRAPHS`, edges3357,
digest`62482c4f38ad2034`, replayed_edges256, cycles0, max_path_edges1,
targets_that_are_sources`[]`. The complete comparison took179.4780883 seconds.

The controls already reproduce275121 exhaustive small-domain membership
decisions,145957 rank/unrank checks, 和 all56 existing positive center edges.
Both C++ executables agree with the Python oracle on27623 raw maps each
(55246 total), including64 successful padded fixtures 和10 W17 fixture IDs
above2^32. The72 padding fixtures comprise64 successful partial returns
和8 terminal targets; there is also one seeded W17 raw-map success.
Six generic cycle-detector fixtures pass. Complete sorted edge sets at
W2..10 agree; both forced one-second W17 runs yieldUNDECIDED, 和 invalid
map IDs are rejected.

The independent Python positional oracle additionally enumerated every
filtered odd source through W13: W13 has2251028 candidates,1125514 initial
flips,16 completed returns 和16 edges, all exactly matching the C++ reference.
This is a different domain from the old unfiltered W13 graph. Prior complete
Python even-width controls through W14 retain their exact counts.

## 5. Verification 和 limits

Literal `python3 tools/verify.py --changed` returned:

```text
[rules] 5217 Lean files, 301 projects, OK
[changed] against origin/main: 0 new/changed Lean file(s); building 0 module(s); auditing 0 project(s)
[build] up to 1 Lean file(s) at a time
[build] OK
[axioms] 0 endpoints checked
ALL CHECKS PASSED (changed files only, against origin/main)
```

This report/code change adds no Lean module. The repository gate does 不
provide kernel verification of the paper argument or finite computational
exclusion. Unrestricted widths remain open; this result only requires that
any center cycle for this specific driver encounter a width of at least18.
