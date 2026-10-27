# Agent 116 — P25/G8 exterior census, one unresolved word

## Result 和 scope

**PAPER coverage + COMPUTED PARTIAL:** the complete decimal period-25,
eight-overflow domain contains 43,263 overflow necklaces. Exactly 303 pass
the necessary head filter. Two implementations independently exhaust the
same **302** full-width exterior graphs, with identical state 和 depth
counts. They contain **190,494 state records** in total.

One word remains **UNDECIDED**:

```text
g = 0001000100011000100100011
```

The explicit-tuple implementation reaches 4,000,000 states at spatial
depth 22 before its cap. No acceptance has appeared. This is neither an
exhaustive negative for the remaining word nor a complete P25/G8 exclusion.
No B/C certificate, decimal Lychrel number, or new Lean theorem is claimed.

The scope is return after exactly 25 listed steps with eight overflows,
arbitrary finite B widths 和 arbitrary natural neutral-suffix trims.
Other weights at period 25 和 longer responses after 50,75,... steps to
repetitions of these clocks are outside the result.

Claim: issue #289, comment 6433182465. Initial progress: comment 6433284071.
This task uses the independently audited exterior engine in
[PR375](https://github.com/taco-jpg/p196-algorithm/pull/375); that PR preserves
Agent4's primary period-20/filter attribution. The present period-25 input
slice had no prior claimed census in the reviewed discussion.

## Complete fixed-weight coverage — PAPER PROOF + COMPUTED

A weight-pruned recursive generator emits the least rotation of every
length-25, weight-8 necklace. Each output is checked for its exact length
和 weight, uniqueness, lexical minimality, 和 all 25 cyclic rotations.
An independent Burnside fixed-rotation sum gives the same class count.

Every target word is primitive: a repetition multiplicity would divide
both 25 和 8, whose greatest common divisor is one. Each orbit therefore
contains 25 distinct words. The checked disjoint orbits contain

```text
43,263 * 25 = 1,081,575 = binomial(25,8)
```

labelled words, proving complete coverage without trusting the generator's
internal recursion. Imprimitive words are retained by the general code;
they simply cannot occur in this particular domain.

The credited head relation uses x=B[0], or x=9 for empty B, 和 an inward
carry c in {0,1}: g=floor((x+c)/10), followed by 2x+c if g=0 or
(x mod10)+1 if g=1. All natural suffix trims preserve this effective head.
Thus a rejected clock cannot support a B return. Exactly **303** survive.

Sorted LF-terminated list hashes:

```text
all 43,263: e65cf45d044ffccbce793d2d52cda6b3830f91f2208af8ba9d8bdc9612dc35bd
selected303: efdb63315df953b1a88e2e6a25f895b4e706bd5cf5fc89ff43a8a970c3ba3a5e
```

Controls: 65 small fixed-weight cases /261 necklaces agree with independently
enumerated labelled subsets; two explicit imprimitive examples are retained.
The head relation passes 361 direct B states /392 all-trim edges, including
empty B, plus every rotation of the known p11/p12 positive drivers.
Ordinary 和 optimized Python agree on both target hashes 和 counts.
An insufficient necklace budget exits with `UNDECIDED`.

## Full-width computation

The tuple engine's all-width proof 和 implementation are unchanged from
PR375: neutral suffix padding converts every variable-width exterior cycle
into a common-width one with trim u_t=g_t. A finite spatial path accepts
exactly when its terminal low/reverse carries are complementary 和 its
overflow lag digits equal 9e_t. Complete reachable-state exhaustion rules
out every finite width. Initial 和 interior modes are distinct; all e
streams are retained. Hash equality compares complete arrays.

P25 uses indices 0..24 within the existing 32-slot arrays. The decimal
coefficients remain 0..18, carries are bits, 和 lag digits remain 0..9.
No new packed-key or arithmetic assumption enters this implementation.

| Run | Exact result | Wall time | Peak RSS |
|---|---|---:|---:|
| Tuple, all303, state cap2M | 302 exhausted; last word capped at depth18 | 18.460504s | 1,076.87891 MiB |
| Adapted Agent4, all303, cap2M/5s | Same302 exhausted; last word timed out | 6.890465s | 4 GiB process limit |
| Tuple, last word only, cap4M | Capped at exactly4,000,000 states/depth22 | 28.420589s | 2,152.69531 MiB |

The tuple timings include coverage 和 positive controls. The adapted-source
batch timing excludes compilation 和 its two positive controls.
All 302 completed words agree in both **state counts 和 maximum depth**;
there are zero mismatches. No claim uses a capped or timed-out frontier
as a negative. The complete initial tuple run contains 2,190,494 state
records, including the capped word's first 2,000,000.

Five established positive queries replay 18 carry streams /143 B edges
with independent whole-integer arithmetic. A further period-25 array/wrap
control uses base16, g=e=(10000)^5, common width2. Its B phases repeat

```text
[16] -> [1,0] -> [2,1] -> [4,3] -> [8,7] -> [16].
```

Every one of the 25 edges replays exactly, with u=(00001)^5.
The bounded query returns `BOUNDED_WIDTH_ONLY`, retaining this positive;
that status is never accepted as an all-width negative.

## Independently corroborating implementation 和 provenance

The second implementation is Agent4's existing solver, explicitly adapted
in a **new temporary copy**. It is not presented as a newly authored engine.
Pinned original source:

```text
commit: 6e06c860bc658af484355725d26232c9fa3f285f
path: calculation/agent-4/fixed_g_B_probe.cpp
Git blob: 178ef3669c78c68a1b18886afafa68f56a4c5a9f
SHA256: e83add38e34cadb701395a9fd1600f601e70727187afdcd438ff6730ddaffe66
```

`agent4_guarded_replay.py` verifies both hashes 和 changes exactly the single
admission guard `p>24` to `p>25`; original bytes remain untouched.
Adapted SHA256:

```text
1a11e7bd4ba5eb34320956a0a3735988b5857f984aad79b1f46f163ef3e8e3af
```

P25/G8 needs 2*25+4*8=82 of its 128 key bits 和 25 of 32 array slots.
The original period restriction therefore required an explicit extension,
even though the representation already had sufficient capacity.
The wrapper imposes 4 GiB address space 和 wall limits. Its depth argument
is 10^9, beyond any simple discovery path before the 2M state cap.
The original p11 和 p12 controls still accept their documented e streams.

The legacy implementation stops at its first accepting state. Its evidence
here corroborates completed negatives; it does not enumerate every possible
e on a positive g. No Agent4 repository source is modified or vendored.

## Reproduction

This PR is stacked on PR375. From the complete combined checkout:

```bash
python3 calculation/agent-116/fixed_weight_coverage.py --selftest --output /tmp/agent116-p25-g8.txt
python3 calculation/agent-116/p25_g8.py --output /tmp/agent116-p25-g8-initial.json
python3 calculation/agent-116/p25_g8.py --only 0001000100011000100100011 --states 4000000 --seconds 90 --batch-seconds 120 --output /tmp/agent116-p25-g8-isolated4m.json
```

Both search commands deliberately return exit2 while the selected scope
remains incomplete. The second command's per-word result is a state cap;
it cannot turn the other 302 completed decisions into a full negative.

For the second implementation, save the pinned original source above as
`/tmp/agent116-agent4-fixed-g-original.cpp`, then run:

```bash
python3 calculation/agent-116/agent4_guarded_replay.py --source /tmp/agent116-agent4-fixed-g-original.cpp --words /tmp/agent116-p25-g8.txt --states 2000000 --seconds 5 --batch-seconds 900
```

The wrapper rejects any source-pin mismatch. Every result retains its exact
status; the summary reports 302 exhausted 和 one timeout, not a theorem.

## Ready-to-run Studio continuation

Defer this lower-priority continuation until the concrete P24 center target's
assigned work. No Studio job has been executed for this task.
Compile the unchanged tuple source from the combined checkout:

```bash
c++ -O3 -std=c++17 -Wall -Wextra -pedantic calculation/agent-116/exterior_tuple.cpp -o /tmp/agent116-exterior-tuple
python3 - <<'PY'
import subprocess
subprocess.run(['/tmp/agent116-exterior-tuple', '10',
    '0001000100011000100100011', '--states', '8000000', '--seconds', '900',
    '--memory-mib', '6144', '--witness'], check=True, timeout=930)
PY
```

One process /one core; hard address-space cap6 GiB, internal wall cap15min,
outer timeout15.5min. Based on the measured 4M run, planning estimates are
roughly 1–3min 和 4.5–6GiB to reach 8M, not promises of exhaustion.
Every cap/timeout remains UNDECIDED. An acceptance must preserve full B/e/g
data 和 pass integer replay before seeking a compatible C; only a paired
mirror-accepted cycle enters the user's CANDIDATE/Lean protocol.

## Repository gate 和 next scope

The literal `python3 tools/verify.py --changed` passed on the combined tree:

```text
[rules] 5217 Lean files, 301 projects, OK
[changed] against origin/main: 0 new/changed Lean file(s); building 0 module(s); auditing 0 project(s)
[build] OK
[axioms] 0 endpoints checked
ALL CHECKS PASSED (changed files only, against origin/main)
```

No new Lean module, registry change, README/RESULTS change, or other-agent
source edit is part of this result. The two complete implementations
corroborate only the 302 finished negatives. The unresolved word remains
listed explicitly, 和 the concrete P24 center-completion priority takes
precedence over further unrelated period expansion.
