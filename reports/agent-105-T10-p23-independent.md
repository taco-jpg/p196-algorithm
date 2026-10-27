# Agent 105 — T10: independent period-23 exterior audit

## Result 和 exact scope

**COMPUTED:** an independent census enumerates all 364,724 binary overflow
necklaces of length 23, including every weight 0..23. A necessary head-cycle
filter retains 1,502. The independent full tuple-state search exhausts all 1,502,
with zero accepting states, caps, timeouts, errors, or unprocessed words.

**PAPER PROOF:** the head projection is necessary, 和 common-width neutral
padding reduces every finite exterior cycle to the exact finite transfer graph.
Consequently, subject to the stated mathematical argument 和 finite computations,
there is no base-10 exterior B-cycle closing after 23 steps, at any finite
exterior width or with any allowed neutral trimming pattern.

This confirms Agent 4's period-23 result independently. It does 不 exclude other
periods, repeated-driver cycles whose B-state closes only after more than 23
steps, arbitrary center cycles, or every decimal route. 没有 decimal certificate
or new Lean theorem is supplied; these claims are 不 LEAN-VERIFIED.

## Prior work, source pins, 和 independence

Primary credit remains with [Agent 4, PR #342](https://github.com/taco-jpg/p196-algorithm/pull/342).
The audited primary head is `d415b7089a5265f1d90a1042199955eeb476638b`;
its parent PR #323 is pinned at `6e06c860bc658af484355725d26232c9fa3f285f`.
The [primary source](https://github.com/taco-jpg/p196-algorithm/blob/d415b7089a5265f1d90a1042199955eeb476638b/calculation/agent-4/fixed_g_B_probe.cpp)
has Git blob `178ef3669c78c68a1b18886afafa68f56a4c5a9f`.

[Agent 106's author-source rerun](https://github.com/taco-jpg/p196-algorithm/issues/289#issuecomment-6433207984)
reports 74.884 seconds 和 640,580 KiB for the primary full batch. Those are
measurements of the primary implementation, separate from the results below.
The primary prose references `test_low_digit.py`, absent at the pinned head;
this is a narrow reproducibility gap. Our corresponding head checks are
published in `census_controls.py`; it does 不 import primary filter code.

The new C++ implementation uses explicit carry/digit arrays 和 separate root
handling. Its state equality compares all 72 bytes; a hash is used only for
lookup. The census, tuple implementation, direct Cartesian-product Python
control, 和 integer-arithmetic whole-word control use separate algorithms.
The original [mirror](../calculation/neutral_band_search.py) remains the shared
specification, corresponding to the established Lean template definitions.

## Necessary first-coordinate projection

Let `h=b-1`; coefficients lie in `0..2h`. A nonempty B has positive first
coefficient x. In base 10, `1<=x<=18`. Let c be the inward carry entering x
when normalizing reverse(B). It is a bit. Directly from `nextB`,

`g=(x+c)//10`,

`x'=2x+c` if `g=0`; `x'=(x mod10)+1` if `g=1`.

This gives 18 states 和 27 distinct labelled edges. In particular, the boundary
case `x=9,c=1` gives overflow edge `9 -> 10`; replacing every overflow by
`x-9` would be incorrect. Non-overflow steps may use `2x+1` as well as `2x`.

Empty B is represented by virtual head 9. Its actual mirror values are
`e=0,g=1,nextB=[10]`, exactly the graph edge `9 -> 10`. A trim to empty B
removes an all-9 raw exterior, so its projected successor head is 9 as well.
Hence the graph is necessary even for cycles visiting empty exteriors.

If `G=sum(g)=0`, every projected step strictly increases the positive head:
`x'=2x+c>x`. Thus no cyclic head path exists. This handles weight zero directly.
No minimum-weight assumption is used in the enumeration.

## Complete necklace census

The recursive generator extends a binary prefix together with its candidate
period, first repeating the periodic digit 和 then taking each larger digit.
At length p it emits exactly when the candidate period divides p. Representatives
are lexicographically least cyclic rotations; both constant words are included.
The independent controls compare this enumeration with explicit rotations of
every raw binary word for periods 1..12.

For weight w, Burnside's count is

`N(p,w)=(1/p)*sum_{d|gcd(p,w)} phi(d)*binom(p/d,w/d)`.

For prime p=23 the total is `(2^23+22*2)/23=364724`. All 24 weight counts
are checked independently. Cyclic relabelling preserves exterior feasibility,
so one representative per necklace suffices. The survivor manifest contains
1,502 distinct 23-bit strings, ordered by `(weight,string)`, without a header.

| G | All necklaces | Head survivors |
|---:|---:|---:|
| 0..5 | 1,938 | 0 |
| 6 | 4,389 | 1 |
| 7 | 10,659 | 64 |
| 8 | 21,318 | 463 |
| 9 | 35,530 | 731 |
| 10 | 49,742 | 239 |
| 11 | 58,786 | 4 |
| 12..23 | 182,362 | 0 |
| Total | 364,724 | 1,502 |

Manifest SHA-256:
`ae06e8e4db03a76c493e0d62c5cca93e2945d1a8ca290af739aa353ff4147fc6`.

## Common width 和 exact tuple transfer

Neutral suffix padding 和 canonical stripping retain
[Agent 7's prior attribution](https://github.com/taco-jpg/p196-algorithm/pull/315)
和 [canonical-quotient proof](https://github.com/taco-jpg/p196-algorithm/pull/326).
The reduction below audits those facts for this particular search.

Under `Hyp`, the 两 normalization carries are distinct bits, so `e2=1-e1`.
Write F(B) for the autonomous exterior update, using reverse entry carry
`1-e(B)`. Appending j neutral coefficients preserves e 和 g, 和

`F(B ++ h^j) = F(B) ++ h^j`.

Indeed, normalizing a neutral coefficient preserves its carry; the 两 emitted
padding digits add to h. This also holds for empty B, where `F([])=[b]`.
For any cycle `F(B_t)=B_(t+1) ++ h^u_t`, choose
`N>=max(1,max_t |B_t|)` 和 `W_t=B_t ++ h^(N-|B_t|)`.
Since `|B_(t+1)|=|B_t|+g_t-u_t`,

`F(W_t)=W_(t+1) ++ h^g_t`.

Thus arbitrary widths 和 trimming counts reduce to a common width N; N is 不
bounded in the graph search. Conversely, stripping maximal neutral suffixes
from an accepted padded cycle gives actual canonical exterior words; the
reconstructed words are checked against the finite-word update.

At a cut after j coefficients, retain per phase t the forward carry L, reverse
boundary carry H, 和 previous reverse digit Y for overflowing phases. Initial
values are `L=0,H=g,Y=g`; Y is zero for non-overflow phases.
Choose a coefficient x in `0..2h` 和 inward carry k in `{0,1}`. Set

`D=(x+L) mod b`, `L'=(x+L)//b`,
`R=(x+k) mod b`, requiring `(x+k)//b=H`, 和 `H'=k`.

The next phase's coefficient must equal `D+R` if g=0, or `D+Y` if g=1.
Set `Y'=R` for g=1, otherwise zero, 和 require closure across all p phases.
The first coefficient is positive at every phase; subsequent coefficients may
be zero. A cut accepts exactly when `L_t+H_t=1` for every phase 和, for
g=1, `Y_t=h*L_t`. These are the reverse-entry 和 extra-neutral-output conditions.

Every real padded cycle supplies such a path. Every accepting path supplies
complete words satisfying the displayed finite-word identities. Carry bits
remain bits because coefficients are bounded by 2h. The finite state space is
at most `4^p*b^G`, plus the separately flagged root. Breadth-first exhaustion
therefore decides all finite widths for a fixed overflow word, without a depth
cutoff. Repeated states may be merged after the special first-column step.

## Root handling 和 resource semantics

The implementation keeps the restricted first-column root separate from generic
visited states. Additionally, for positive G, no positive-width reachable cut
can have `L_t=0` at every phase. To prove this, put
`A_t=sum_{i<j} x_(t,i)*b^i` for a cut j>=1. Zero final forward carries imply
`A_t=sum D_(t,i)*b^i`. Exact temporal equations give

`A_(t+1)=A_t+sum R_(t,i)*b^i >= A_t` when g=0;

`A_(t+1)=A_t+1+b*sum_{i<j-1}R_(t,i)*b^i >= A_t+1` when g=1.

Cyclic summation contradicts G>0. Thus merging a generic return with the
primary root cannot lose a reachable positive-G path; the independent solver
nevertheless makes the distinction explicit. A primary depth option of 110
does 不 invalidate a case that actually exhausts at depth 65.

`exterior_tuple.cpp` stores three `uint8_t[24]` arrays: 72 bytes per state,
with full-array equality. It accepts bases 2..62 和 periods 1..24. The published
p23 run uses a 12,000,000-state cap, a 4-GiB `RLIMIT_AS`, 和 a 1,100-second
per-word guard; `run_p23.py` also enforces a 1,200-second whole-batch timeout.
There is no depth cutoff. Allocation failure, a cap, timeout, malformed output,
missing word, or incomplete graph is UNDECIDED. Only complete exhaustion with
no acceptance is a negative. Positive witnesses are replayed as full words.

## Independent controls 和 completed p23 batch

Head controls realize all 36 `(x,c)` cases through the original mirror using
`B=[x,10c]`, giving all 27 graph edges. All 6,858 positive-head exteriors of
lengths 1..3 project correctly, 和 empty B has an explicit control. The separate
small-necklace census checks 8,190 binary words / 801 necklaces at periods 1..12.

The integer-evaluation whole-word implementation checks 21,754 canonical raw
steps against the original mirror, including empty B. Counts at bases 2..6,
width bound 4, are 54, 500, 2,058, 5,832, 13,310. Its bounded-cycle results are
only controls, 不 an all-width obstruction. The eight source certificates at
bases 2,4,8,16,32,11,17,26 pass the mirror; their overflow words 都 produce
an accepted exterior. There are 56 source 和 56 returned B-edge integer replays.
These are overflow controls: at base 11 the source e is `011011`, while the
first returned e is `001001`; equality of these e-streams is 不 required.

A separate Python transfer enumerates every inward-carry vector directly.
For all 60 graphs at bases 2..5, periods 1..4, all binary necklaces, it exactly
matches the C++ visited state sets, accepting streams, minimum accepting widths,
transition multiplicities, 和 maximum depth: 301 vertices, 257 transitions,
4 accepting streams, zero mismatches. Every extracted positive word is also
replayed by the independent integer-evaluation update.

The full p11 control exhausts 18,061 states 和 finds `e=10100110011`, with
minimum accepting common width 29.
The p12 control exhausts 136,653 states 和 finds exactly
`100101011010`, `010110101001`, `101010010101`. These controls include complete
accepting-state enumeration 和 reconstructed full-word checks; all three p12
streams first accept at common width 53.

| G | Words exhausted | Sum states | Largest graph | Max depth |
|---:|---:|---:|---:|---:|
| 6 | 1 | 65 | 65 | 1 |
| 7 | 64 | 70,304 | 62,497 | 9 |
| 8 | 463 | 817,005 | 252,273 | 21 |
| 9 | 731 | 378,659 | 43,897 | 6 |
| 10 | 239 | 9,229,819 | 8,455,917 | 65 |
| 11 | 4 | 120,324 | 117,249 | 4 |
| Total | 1,502 | 10,616,176 | 8,455,917 | 65 |

All 1,502 graphs report `EXHAUSTED`, `complete=true`; zero accepts, caps,
timeouts, errors, or unprocessed words. Solver wall time is 50.519899 seconds;
including compilation 和 census, 53.475735 seconds. Process peak RSS is
1,744,864 KiB, 和 the largest frontier is 566,544 states. These are measurements
of this independent run, with state counts including the flagged root.

The hard canonical word `00001010101010100100111` has 8,455,917 states,
depth 65, 和 search time 38.355754 seconds. In the primary word's phase,
`10101010101001001110000`, its only closed initial head is 17 和 its head
sequence is unique; there are 512 local inward-carry assignments. These local
assignments are 不 full exterior solutions; the full graph exhausts without one.

## Reproduction 和 repository gate

From the repository root after these files are installed:

```bash
python3 calculation/agent-105/run_p23.py
python3 calculation/agent-105/census_controls.py --mirror calculation/neutral_band_search.py
python3 calculation/agent-105/wholeword_controls.py --solver calculation/agent-105/exterior_tuple
python3 calculation/agent-105/compare_small_graphs.py --solver calculation/agent-105/exterior_tuple.cpp
python3 tools/verify.py --changed
```

`run_p23.py` rebuilds both independent C++ programs, regenerates 和 validates
the manifest, 和 runs the complete batch. The final JSON event is `RESULT`,
with aggregate `outcome="PASS"`.
No raw logs or transcript artifacts are required.

Solver SHA-256: `063369a245add9be4a9ff2e4d64a091ea3d3c4ae9f86eff396e9b6ecc43306e8`.
Driver SHA-256: `1ba96ba63d91a2fbd19dfccff612d1b8ea8b84e9a925e2641e89f3e984fba559`.
Recompiling the final repository source produces a byte-identical binary to the
one used for the complete audit; SHA-256 is
`35a6a83bfe776d09787b70cb05d67df6010664803d8e11c20949f6e774a1467e`.

**Repository gate:** literal `python3 tools/verify.py --changed` returned
`ALL CHECKS PASSED (changed files only, against origin/main)`: 5,217 Lean
files / 301 projects satisfy repository rules; 0 Lean modules changed,
built, or axiom-audited. The final checked tree equals the published tree.
The gate does 不 convert these paper arguments or Python/C++ computations
into Lean-verified mathematical theorems.
