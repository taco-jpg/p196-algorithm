# Agent 107 — dense indices for the neutral exterior residue class

## Scope and attribution

**PAPER PROOF + COMPUTED tool validation.** This provides a bijection,
dense rank/unrank and streaming enumeration for the necessary cycle-state
class proved in [PR363](https://github.com/taco-jpg/p196-algorithm/pull/363).
It is an indexing tool, not an exterior transition graph or a new cycle
exclusion. It does not modify another agent's search.

Coordination claim: issue #289 comment6433069487. Agent9 retains the explicit
width8 census in issue #295; Agent109 retains the compressed spatial-language
method. The alternating-residue theorem credits the prior Agent2/3/5
moment algebra and its explicit neutral adaptation. Agent108's PR360 supplies
the decimal Lean charge bridge under its stated positive-overflow premise.

The implementation is standalone C++17 and has no source dependency on
PR363 or another unmerged PR. Its mathematical cycle-pruning justification
is the paper result in PR363; no new Lean result is claimed here.

## Domain and encoding

Fix base `b>=2`, maximum width `M>=0`, alphabet size `a=2b-1`, and
modulus `m=b+1`. The domain consists of finite words B with:

- `|B|<=M`;
- coefficients in `0..2b-2`, listed least significant first;
- a positive first coefficient when B is nonempty;
- `R(B)=sum_j((-1)^j*B_j)-(-1)^|B| = 0 mod m`.

The empty word fails the last condition. Neutral suffixes are permitted;
the words are not identified under neutral suffix padding.

Encode B as the fixed-width tuple

\[
E_M(B)=0^{M-|B|}\mathbin{++}B.
\]

These zeros are added at the low-coefficient side **only as an encoding**.
Decode by removing all initial zeros. Actual carry transitions must run on
the decoded B, not on the padded tuple.
For example, decimal B=`[10]` emits overflow1, while its width2 encoding
`[0,10]` emits overflow0. The encoding does not preserve exterior dynamics.

Prepending k zeros multiplies both the alternating sum and length sign by
`(-1)^k`, so `R(0^k++B)=(-1)^k R(B)`. Thus the selected tuples are exactly

\[
x\in\{0,\ldots,a-1\}^M,
\qquad \sum_{i=0}^{M-1}(-1)^ix_i\equiv(-1)^M\pmod m. \tag{1}
\]

The all-zero tuple fails (1), since `m>=3`. Every other tuple has a unique
first nonzero coefficient; removing its zero prefix gives a legal B and
inverts the encoding. This proves the bijection, including M=0, whose
selected domain is empty.

## Exact rank and inverse

Order selected padded tuples lexicographically, comparing coefficient0
first. Let `D_i(r)` count suffixes at positions i through M-1 whose signed
sum is residue r modulo m. The recurrence is

\[
D_M(r)=[r=0],\qquad
D_i(r)=\sum_{d=0}^{a-1}D_{i+1}\bigl(r-(-1)^id\bigr). \tag{2}
\]

All residue arguments are reduced modulo m. The domain size is
`N_M=D_0((-1)^M)`.

For each position and required residue, precompute cumulative counts

\[
H_i(r,d)=\sum_{c=0}^{d-1}D_{i+1}\bigl(r-(-1)^ic\bigr),
\qquad 0\le d\le a. \tag{3}
\]

Rank starts with required residue `r=(-1)^M` and accumulated index0.
At digit d it adds `H_i(r,d)` and changes r to `r-(-1)^i*d`.
Every added block consists exactly of tuples agreeing with the prefix so
far and having a smaller next digit; the blocks are disjoint and exhaust
the lexicographically earlier selected tuples. The final required residue
must be zero. This proves the rank formula.

Unrank chooses the unique nonempty block with
`H_i(r,d)<=k<H_i(r,d+1)`, subtracts its lower endpoint, and updates r.
Equation (2) partitions every parent interval into those blocks. Induction
on the remaining width proves existence, uniqueness and mutual inversion
for every `0<=k<N_M`. Empty blocks are skipped, never selected.

Streaming enumeration advances to the next viable prefix branch and fills
its smallest viable suffix. A zero-count branch contains no selected
tuple by (2), so skipping it is exact. This does not enumerate all `a^M`
unfiltered tuples before discarding failures.

## IDs remain stable when the width cap increases

`E_(M+1)(B)=0++E_M(B)`. The initial zero branch is the first lexicographic
block, and its residue constraint reduces to (1) for width M after a sign
change. Therefore every word already present has the same ID at caps M
and M+1. Induction gives cap stability for any larger cap.

In particular, IDs `[0,N_L)` are exactly the words of width at most L.
This permits retaining existing IDs when an application increases its cap.
It does not assert that a word's successor stays below the old cap.

## Safe use in a cycle search

PR363 proves that every legal closed neutral exterior cycle lies wholly
inside this class, and that the class is forward invariant under every
legal neutral suffix trim. Thus a bounded B graph may restrict vertices
to the class, preserve every legal edge between retained words, and retain
exactly the same directed cycles as the full graph.

A caller must restore the actual coefficient word before applying its
existing arithmetic, enumerate every legal suffix trim, and separately
discard successors outside its width cap. A candidate full B/C certificate
still requires the original mirror and Lean checks. A cycle in a B-only
overapproximation still need not have a compatible center.

The restricted graph does not retain all transient paths. In particular,
its longest path is not the full graph's longest path. The independent
finite-time absorption theorem may bound the omitted prefix, but that is
a separate deduction requiring its hypotheses.

## Exact width8 payload sizes

The decimal domain has `N_8=1,543,960,696` words, fewer than `2^31`.
The unfiltered domain has `19^8=16,983,563,041` words, requiring34 bits.

| Payload | Full width8 universe, Agent9 layout | Selected class |
|---|---:|---:|
| One-byte state array | 16,983,563,041 bytes | 1,543,960,696 bytes |
| FIFO storing each state once | 84,917,815,205 bytes at5 bytes/ID | 6,175,842,784 bytes at4 bytes/ID |

These are arithmetic payload sizes, not measurements of a completed graph.
They exclude allocator, buffering and indexing-table overhead. Indegree
and queue bounds still need checked arithmetic in the caller. Rank/unrank
costs can offset some enumeration savings; no full-search speedup is claimed.

## Implementation, reproduction and validation

`charge_index.hpp` exposes `p196::agent107::ChargeIndex` with `count`,
`contains`, `rank`, `unrank`, `stream` and `for_each`. Construction supports
bases2 through62 and widths0 through64, provided every required residue
count fits `uint64_t`; each addition is checked before execution. Table
dimensions are bounded by those explicit constructor limits.

The full unconstrained universe need not fit `uint64_t`: the implementation
never sums all residue bins. Base2 width41 has exactly
`3^40=12,157,665,459,056,928,801` selected words and is supported, although
`3^41` is too large. Width42 rejects count overflow. Decimal width16 also
rejects count overflow.

After precomputation, rank takes O(M), unrank O(M log(2b-1)). A cursor holds
a reference to its index, which must remain alive and unmoved. Creating a
cursor from a temporary index is rejected at compile time; synchronous
`for_each` on a temporary remains valid. Streams explicitly clip a requested
range to the remaining IDs using subtraction, avoiding `start+limit`
overflow. The CLI reports requested and emitted counts separately; it has
no graph-completion or cycle verdict.

Exact commands from the repository root:

```bash
c++ -O3 -std=c++17 -Wall -Wextra -pedantic \
  calculation/agent-107/charge_index.cpp -o /tmp/agent107-charge-index
/tmp/agent107-charge-index 10 8 count
/tmp/agent107-charge-index 10 8 unrank 0
/tmp/agent107-charge-index 10 8 rank '[10]'
/tmp/agent107-charge-index 10 8 benchmark 771980348 1000000
/tmp/agent107-charge-index 10 8 roundtrip 100000 107
python3 -O calculation/agent-107/test_charge_index.py
python3 tools/verify.py --changed
```

The count is1,543,960,696; ID0 is `[10]`. Malformed commands produce an
explicit JSON error and nonzero exit status. Batch mode continues after an
error but retains a failing final exit status. CLI enumeration is limited
to100,000 emitted rows and benchmark loops to1,000,000 iterations; the
header provides the general streaming API.

Independent optimized-Python suite:9 tests pass. Complete brute enumeration
of17 domains checks all1,292 selected words, exact ranks, decoding,
membership and iterator output. Independent cyclic-polynomial completion
counts check60 decimal width8/12 random and boundary ranks. Cross-cap tests
include complete small domains and32 wider samples. A closed-form ternary
oracle checks high-bit base2 width41 ranks. Additional tests cover overflow,
invalid inputs, maximum-uint64 range clipping and cursor owner lifetime.
The test depends only on these C++ files and standard Python/C++ libraries.

Bounded Linux sandbox benchmarks, compiled with the exact O3 command above:

| Operation | Scope | Timed loop | Wall time | Checksum |
|---|---|---:|---:|---:|
| Streaming plus rank check | IDs771,980,348 through772,980,347 | 0.092343969s | 0.094808s | 12992478337700242689 |
| Random unrank/rank | 100,000 samples, seed107, full width8 domain | 0.032854721s | 0.035096s | 16184063656323175153 |

Both commands return `ok:true`; the streaming run reports exactly1,000,000
processed words. Every streamed word in that interval has width8. Loop
timings exclude construction and initial cursor positioning; Python's
`perf_counter` measured subprocess wall times. Its `RUSAGE_CHILDREN`
maximum across these two runs was8,704 KiB. Neither run generates graph
neighbors, constructs indegrees or peels vertices. No graph runtime is
extrapolated from these measurements.

Literal `python3 tools/verify.py --changed` returns `ALL CHECKS PASSED`:
5,217 Lean files/301 projects satisfy the repository rules;0 new Lean
modules and0 endpoints are selected. This is not a Lean proof of the index
or the cycle-pruning theorem.

## Limits

No width8 graph was run and no new decimal cycle was excluded or found.
The tool enumerates a necessary residue class exactly; its members need
not be on cycles. Supported integer/resource limits are explicit and
overflow is an error, not a truncated count. This does not supply a general
finite-state representation of the unbounded-width problem.
