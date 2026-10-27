# Agent 113 — independent cumulative-center review

## Result, attribution, and scope

**PAPER PROOF + COMPUTED.** The existential all-width reduction in
[Agent 101's PR #357](https://github.com/taco-jpg/p196-algorithm/pull/357)
passes a second-author mathematical review and a separately implemented
global carry-tuple model. The reduction is Agent 101's contribution.
The pre-existing exact center equations belong to the neutral-band work.
This report supplies independent corroboration, not a competing discovery.

For one fixed base, carry stream, overflow stream, and binary trim schedule,
complete reachability of whole generic cut states, followed by two fixed
midpoint tails and two short-width exceptions, decides existence at any width.
The independent implementation does not import, include, patch, or execute
either C++ transition implementation. It walks the complete chronological
tuple directly, without temporal segment factorization or packed state keys.

No disagreement or semantic defect was found in the reviewed reduction.
This is not a Lean theorem, a new decimal exclusion, a decimal certificate,
or an unrestricted impossibility result. In particular, a center needs a
matching exterior cycle before the full certificate checker can apply.

Reviewed primary: commit `a6b2e4d735972fe24edd9f34a913cda360acdcc9`,
`calculation/agent-101/cauto_reach.cpp` and `reports/agent-101-T4.md`.
Repository baseline: `eafbbbfd6b5b857597f95f68268c56dbd96b6bcb`.
The unchanged `cauto_fast.cpp` SHA256 is
`eb2e6b18b09fdfcae0a5b6b818d23291123ed6a76b59fb6e531589e7f6d00fff`.

## 1. Independent width and reachability argument

Fix binary streams `e,g,v` of period `P`, with `sum(g)=2*sum(v)`.
Let `delta_0=0`, `delta_(t+1)=delta_t+g_t-2*v_t`, and
`d=min(delta_0,...,delta_(P-1))`. Every closed center has phase lengths
`m_t=m_0+delta_t`. All are positive precisely when `m_0>=1-d`.
Consequently every admissible width occurs exactly once as

```
m_0 = 2*q+s-d,       q >= 0, s in {1,2}.
```

Write `r_t=delta_t-d`. Then `m_t=2*q+s+r_t`, with `min(r_t)=0`.
The source and raw-successor half-lengths are

```
J_t  = q + ceil((s+r_t)/2)
Jp_t = q + ceil((s+r_t+g_t)/2).
```

There are exactly `q=min(J_t)-1` generic outer layers.
When `q=0`, the two widths `1-d,2-d` require direct finite-width solves.
Their first layer can already contain midpoint cases and must retain the
special outside-boundary trim condition.

Let `S` be the prescribed outer cut, `T0` its first generic transition,
and `T` the ordinary generic transition at every subsequent layer.
For `q>=1`, the generic frontier is exactly `T^(q-1)(T0({S}))`.
The first transition must not be replaced by `T`, and `S` must not be added
to the ordinary reachable set. At the outside, trimming checks the neutral
coefficient directly; inside, it checks the previous layer's pending target.

For each `s`, increasing `q` by one adds two to all widths and one to all
half-lengths. Every layer type and parity in the remaining tail is unchanged
after translating its spatial index. The two fixed tails can therefore be
instantiated at `m_0=3-d,4-d`, starting at layer `j=1`.
All their layers use the ordinary, noninitial boundary condition.

Put `A=T0({S})` and `U=union_(n>=0) T^n(A)`. For either fixed tail `R`,
relational image distributes over unions:

```
R(U) = union_(n>=0) R(T^n(A)).
```

Thus existence is equivalent to acceptance at one of the two short widths
or a nonempty image of `U` under either tail. No equality between successive
exact-width frontiers is needed. Each accepted tail has a predecessor state
at one definite depth; a state first reached at generic depth `D>=1` gives
the actual width `2*D+1+s0-d`, where `s0=0,1` selects the tail.
Retaining first-discovery depth is sufficient for witness reconstruction.

The union must retain **complete temporal tuples**. Independently unioning
each segment's possible components and multiplying those sets would invent
unreachable correlations. Neither reviewed implementation does that.

## 2. Independent layer model and terminal obligations

The Python state is the tuple `(l_t,r_t,Rd_t,Z_t)` over every temporal phase.
Here `l,r` are the two exposed normalization carry boundaries, `Rd` retains
the previous high digit at an overflow, and `Z` retains a pending coefficient
across a trimmed edge. Unused fields are a fixed sentinel.
Initially `l=e`, `r=1-e`, `Rd=(b-1)e` at overflow phases, and `Z=NONE`.

For the current symmetric source coefficient `c`, the low digit and carry
come from division of `c+l` by `b`. At an interior layer, enumerate the high
incoming carry in `{0,1}` and require its outgoing carry to equal `r`.
An even midpoint identifies that incoming carry with the low outgoing carry.
An odd midpoint identifies the two copies of the coefficient and joins
the low outgoing carry directly to `r`.

Without overflow the raw successor coefficient is the sum of the two digits.
With overflow it is the low digit plus the retained previous high digit.
An even input with overflow has one extra virtual central coefficient,
equal to twice the retained central digit. Inactive positions use `NONE`.
An untrimmed temporal edge equates the raw coefficient with the next phase's
coefficient at this layer. A trimmed edge checks the initial neutral symbol
or the stored target, and remembers the next phase's new coefficient.
The chronological recursion closes from the last phase back to the first.

No unchecked pending coefficient remains at termination: for `v_t=1`,
`J_(t+1)=Jp_t-1`, so its last real pending coefficient receives its checking
layer before the global final layer. Newly stored values there are inactive.
Each phase's midpoint already joined its carry traces. Reflecting the selected
half-columns therefore constructs complete symmetric words with every temporal
edge satisfied. Conversely, every genuine center determines these choices.
This establishes the layer relation's soundness and completeness.

After the first generic layer, a sufficient finite domain bound is
`4^P * b^sum(g) * (2b-1)^sum(v)`. Ordinary graph reachability therefore
terminates mathematically. A computational negative still requires complete
successor enumeration, both tails at every reached state, both short cases,
and full queue exhaustion. Incomplete work is `UNDECIDED`.

## 3. Reproducible validation

From the repository root, build the unchanged baseline:

```sh
c++ -O3 -std=c++17 calculation/neutral_band/structure/cauto_fast.cpp -o /tmp/a113_old
```

Obtain `cauto_reach.cpp` from the reviewed commit, retaining it outside this
PR's files, then build it against the same unchanged baseline source:

```sh
curl -fsSL https://raw.githubusercontent.com/taco-jpg/p196-algorithm/a6b2e4d735972fe24edd9f34a913cda360acdcc9/calculation/agent-101/cauto_reach.cpp -o /tmp/a101_reach.cpp
c++ -O3 -std=c++17 -I calculation '-DAGENT101_CAUTO_SOURCE="neutral_band/structure/cauto_fast.cpp"' /tmp/a101_reach.cpp -o /tmp/a113_primary
python3 calculation/agent-113/test_center_reachability.py --baseline /tmp/a113_old --primary /tmp/a113_primary
python3 calculation/agent-113/test_cumulative_primary.py --primary /tmp/a113_primary
```

**COMPUTED:** exhaustive bounded tests independently enumerate symmetric
initial words and use positional-integer arithmetic for each temporal step.
They do not use the layer solver or repository mirror to decide feasibility.
All positive witnesses in the comparisons are independently integer-replayed.

| Check | Completed result |
|---|---:|
| Bounded stream patterns, bases 2/3/4, periods 1..3 | 282 |
| Fixed widths 1..4 | 1,128 decisions |
| Symmetric initial words enumerated | 18,424 |
| Returned bounded witnesses replayed | 14 |
| Positive-overflow all-width comparisons with old and primary | 32 |
| Zero-overflow all-width comparisons with old legacy path | 42 |
| Original Lean-source fixtures | 8 bases, 56 source edges |
| Positive fixed-width and all-width cases, including base 20 | 9 + 9 |
| Complete primary/reference all-width comparisons | 2,240 |
| Of those, negative / positive | 2,110 / 130 |
| Both engines' positive witnesses replayed in exhaustive comparison | 260 |
| Exhaustive-comparison disagreements or unfinished cases | 0 |

The 2,240-case family is every binary `e,g,v` in bases 2..5 and periods 2..4
with positive even `sum(g)=2*sum(v)`. Eight reference positives use a short
exception width. The entire family completed in about 6.4 seconds locally.
The all-width baseline suites separately replayed 11 positive-overflow and
54 zero-overflow returned witnesses. The same tests pass under `python3 -O`;
checks use explicit exceptions and remain active without assertions.

The following independently reproduces the established decimal p11 negative:

```sh
python3 calculation/agent-113/center_reachability.py 10 10100110011 11100010000 11000000000 --cap 2000 --seconds 30
```

Output: `EXHAUSTED`, exactly 637 generic states, 637 expanded states,
1,274 tail tests, 2 short-width cases; about 0.20 seconds. This is a
corroboration of the previous exclusion for this supplied schedule.

[Agent 116's base-20 certificate, PR #356](https://github.com/taco-jpg/p196-algorithm/pull/356)
provides the credited new positive control:

```sh
python3 calculation/agent-113/center_reachability.py 20 10100101 10001000 00100000 --cap 100000 --seconds 30 --witness
```

Output: `FEASIBLE`, initial width 27, generic depth 12, with all eight returned
centers independently replayed. The reference discovers 4,282 generic states
and expands 3,756 before that first hit, about 6.1 seconds. The primary's
3,931-state count differs because of exploration/tail-check ordering;
equal visited counts are not an invariant of existential breadth-first search.
Both implementations recover width 27. The older frontier-periodicity method
returns `NOPERIOD` at the cited primary control budget; this is not a negative.

## 4. Failure paths and practical limits

The independent API supports bases 2..62, periods 1..128, and binary trims.
It also supports zero overflow/zero trims, unlike the primary's segmented
entry point. For example `b=2,e=10,g=00,v=00` has width-one centers `[0],[2]`.
The primary correctly calls this scope unsupported; it must not be treated
as a contradictory negative. This center alone is not an exterior certificate.

Tests verify seven malformed problem inputs, two reference limit paths,
and four primary/reference resource or scope checks. Every active limit
returns `UNDECIDED`; invalid reference inputs return `INVALID`.
The CLI imposes a default 2 GiB address-space budget and at most 1,800 seconds.
Width profiles are generated lazily; huge widths do not allocate a profile
array before the first deadline check. Internal reconstruction errors cannot
be reported as positives or negatives.

Two additional real CLI interruptions were checked under optimized Python:

```sh
python3 -O calculation/agent-113/center_reachability.py 10 1010011001110100110011 1110001000011100010000 1111000000000000000000 --cap 1000000 --seconds 30 --memory-mib 64
python3 -O calculation/agent-113/center_reachability.py 2 10 00 00 --width 1000000000 --seconds 0.01 --memory-mib 64
```

Both exit 3 with structured `UNDECIDED`: the first reports `MemoryError`,
the second the wall-time budget. A small preallocated reporting reserve and
explicit release of the interrupted BFS prevent a second allocation failure
while formatting the memory result; the CLI also has a literal JSON fallback.
Neither interrupted run is counted as a completed graph comparison.

The primary retains upstream local-table and Cartesian-product behavior.
Its state cap is checked after a parent's product, so it is not a strict
peak-memory bound. Its independent address-space and alarm limits remain
necessary. The inherited 16-bit witness choices can cause reconstruction
failure on oversized local lists; mandatory arithmetic replay prevents such
a failure becoming an accepted positive. These are resource/representation
limits, not a counterexample to cumulative reachability.

The Python implementation prioritizes independence and transparency, not
large-period performance. Larger decimal p22/p24 graphs, P33/P48 MDD work,
other trim schedules, and arbitrary temporal repetitions are outside this
completed independent computation. Agent 111/118 retain their MDD decisions;
Agent 107/110/119/104 retain separate trim-transport results and formalization.

Repository gate: `python3 tools/verify.py --changed` **PASS** on the final
four-file tree: 5,217 Lean files, 301 projects, zero changed Lean modules or
endpoint audits. No Lean source or registry entry is added.
