# Agent 108 — exact nonuniform exterior block MDD

## Result 和 scope

**COMPUTED, with a PAPER PROOF of the exact block reduction.** For base 10,
the fixed 24-step overflow word
`g=110001001000110001001000` has no finite exterior B return, with arbitrary
carry word e 和 arbitrary finite exterior width. Its exact spatial frontier
becomes empty at width 39; every earlier all-e terminal count is zero.
Cyclic phase shifts are equivalent. This is an independent engine result
for SQ5, following the scoped T4/T10 claim in
[comment 6433266167](https://github.com/taco-jpg/p196-algorithm/issues/289#issuecomment-6433266167).

In particular, the supplied center control with
`e=010100110100101011001011`, `v=100001000000100001000000`, 和
`C0=[9,14,13,18,13,14,9]` cannot acquire a matching finite B return in one
24-step lap. The center is itself a valid projected center cycle: its
24 transitions are independently replayed below. No contradiction is
claimed for repeated laps with longer exterior period, other g words,
other periods, or the unrestricted neutral-band route. There is no new
Lean theorem or decimal Lychrel certificate.

The complete original transition core independently corroborates exhaustion
with the same 8,575,477 state occurrences. All 40 layer sizes also agree
with Agent117's separate explicit traversal
[6433395207](https://github.com/taco-jpg/p196-algorithm/issues/289#issuecomment-6433395207).

## Attribution 和 dependencies

This extends Agent108's uniform four-step implementation in
[PR #386](https://github.com/taco-jpg/p196-algorithm/pull/386), on which this
PR is stacked. The exact positional equations originate in
`calculation/neutral_band/structure/bauto.cpp`. Agent118's center-MDD work
motivated correlated symbolic compression; Agent103 retains the distinct
G6/P24 B-MDD application. Agent7's neutral-padding theorem supplies the
common-width reduction; Agent107's guarded driver #335 supplies completion
semantics 和 the independent scalar reference.

Agent101 discovered the center control 和 owns its complementary bounded
SAT lift; Agent117 retains the primary fixed-e, arbitrary-width SQ5 lift;
Agent4 retains the primary all-e SQ5 census. This artifact supplies a
separately implemented fixed-driver symbolic engine 和 independent checks.
It does not transfer their discovery or primary-task attribution.
Agent114's subsequently published [#400](https://github.com/taco-jpg/p196-algorithm/pull/400)
formalizes the credited common-width/u=g reduction; this computation does
not import or claim to verify that Lean development.

## Variable-length temporal blocks

Rotate the supplied cyclic g word to begin with 1. Split at every 1 into
blocks `1,0,...,0` of lengths r. This implementation supports r=1..5;
the fifth length is needed by the known p11 positive control. An average
period bound does not justify omitting individual length-five gaps.

At a spatial cut, a block symbol is `S=(L[r],H[r],Y)`, with binary carry
masks L,H 和 a decimal digit Y. Its alphabet has `10*4^r` symbols. Encode
`S=Lmask + 2^r*Hmask + 2^(2r)*Y`; the physical initial symbol is
`2^r + 2^(2r)`. Different MDD levels may therefore have different alphabets.

For target `T=(L',H',Y')`, a tile contains the temporal coefficient trace
`x0,...,xr`, satisfying `0<=xj<=18` 和

```text
x0 = 10*H0 + Y' - H'0
10*L'j <= xj+Lj  <= 10*L'j+9                (0<=j<r)
10*Hj  <= xj+H'j <= 10*Hj+9                 (0<=j<r)
x1 = x0 + L0 - 10*L'0 + Y
x(j+1) = 2*xj + Lj + H'j - 10*(L'j+Hj)     (1<=j<r).
```

These are exactly forward/reverse quotient-and-remainder equations. A
source/target symbol pair determines its trace uniquely. Join the right
port xr of each block to the next block's left port x0, including the final
cyclic join. Every port has 19 values. On the first spatial column require
all r source coefficients positive; later columns allow zero. Positivity
of a right port is imposed by the next block's left coefficient.

Completeness also gives a closed tile count: choose x0 in 0..18, input Y
in 0..9, input L, 和 output H' freely. Ordinary normalization determines
H,L',Y' 和 the complete trace; each new coefficient is a sum of two digits.
The reverse reconstruction above proves injectivity. Thus the universal
number of tiles is exactly `19*10*4^r`.

| r | Symbols | Live inputs | Tiles | First-positive tiles |
|---:|---:|---:|---:|---:|
| 1 | 40 | 40 | 760 | 720 |
| 2 | 160 | 160 | 3,040 | 2,864 |
| 3 | 640 | 560 | 12,160 | 10,896 |
| 4 | 2,560 | 2,000 | 48,640 | 41,856 |
| 5 | 10,240 | 7,120 | 194,560 | 160,512 |

The independently authored `exterior_tiles.py` compares the quotient-based
reconstruction against direct normalization for every tile, then compares
all 259,160 C++ export rows, including every coefficient 和 positivity bit.
A separate 19-state coefficient transfer checks first-positive totals.

## Exact language image, terminal boundary, 和 stopping

An MDD node represents a complete suffix language, not independent symbol
marginals. Exact image recursively follows each source-language arc,
composes local tiles, 和 remembers both required current 和 initial cyclic
coefficient ports. Its memoization key is `(source node,current port,initial
port)`. Suffix languages with the same output label are united exactly.
Nodes are immutable 和 interned by level plus their complete ordered arcs;
hash collisions receive a full equality comparison.

A block is neutral-terminal exactly when

```text
Hmask = ((1<<r)-1) XOR Lmask
Y = 9*(Lmask AND 1).
```

Precisely these symbols have an unchanged-symbol tile whose entire trace
is 9; all `2^r` cases are checked for each r. Every initial symbol fails this
predicate. The low-carry bits at a terminal cut recover the complete e
word. Optional `--e` intersects the terminal set with that exact requested
word, after the same temporal rotation as g. It never prunes image states.
Witness reconstruction reverses the rotation before reporting B/e.

The common-width padding theorem transports any finite B cycle with natural
trims to this exact physical-to-neutral spatial language. Conversely an
accepting path reconstructs every coefficient 和 therefore a finite B
return; removing terminal 9s recovers canonical exteriors, with natural
trim counts checked by the independent arithmetic oracle.

Let F0 be the physical singleton, F1 its first-positive image, 和
F(n+1)=Image(Fn) for n>=1. Each Fn is the full correlated exact-width set.
An empty Fn proves every later set empty. Alternatively, equality Fi=Fj
for 1<=i<j proves all later layers repeat; all intervening terminal
intersections must have been checked. F0 is excluded from generic repeat
detection. A cap or unsupported pattern returns UNDECIDED, never a negative.
For positive input, `FEASIBLE` stops at the first matching terminal: it
does not claim to classify all other e streams.

## Complete SQ5 symbolic run

Both the prescribed-e run 和 an unrestricted-e run reach `empty_layer` at
depth 39. The unrestricted run reports `EXHAUSTED_NO_B`, 113,007 immutable
DAG nodes, 和 12,650,429 operations. These 40 layers contain 8,575,477
state occurrences in total; maximum layer size is 599,296 at width 22.
Every all-e terminal count is zero.

| Width | Size | Width | Size |
|---:|---:|---:|---:|
| 0 | 1 | 20 | 422,000 |
| 1 | 64 | 21 | 573,536 |
| 2 | 256 | 22 | 599,296 |
| 3 | 1,088 | 23 | 339,168 |
| 4 | 16,752 | 24 | 177,672 |
| 5 | 44,368 | 25 | 295,192 |
| 6 | 249,216 | 26 | 339,000 |
| 7 | 202,564 | 27 | 235,128 |
| 8 | 276,380 | 28 | 136,016 |
| 9 | 286,144 | 29 | 261,224 |
| 10 | 220,196 | 30 | 306,616 |
| 11 | 187,392 | 31 | 208,224 |
| 12 | 151,668 | 32 | 214,768 |
| 13 | 256,644 | 33 | 166,208 |
| 14 | 245,568 | 34 | 40,592 |
| 15 | 244,208 | 35 | 48,288 |
| 16 | 369,040 | 36 | 31,232 |
| 17 | 444,672 | 37 | 13,248 |
| 18 | 535,936 | 38 | 2,560 |
| 19 | 433,352 | 39 | 0 |

The final 256-bit implementation took 0.607 s wall / 36,108 KiB peak RSS
in a fresh process (a later replay: 0.812 s / 35,820 KiB). Independently,
the unchanged original bauto transition core plus the corrected #335
guarded driver exhausted in 119.477 s / 650,400 KiB, with 8,575,477 states,
depth39, zero accepted e, and no cap. Its command was:

```bash
/tmp/agent108-bauto335 10 24 24 -g 110001001000110001001000 -cap 15000000 -depth 1000
```

This external reference used #335 commit
`2c4123a98955d09d27aed1d727ce25e578378f03`, with one extra final newline
in the temporary driver; it is not a runtime dependency of this PR.
Core SHA256: `c534ff54c819efe8a9c050167e08ca950428d619475f9647ca48cfcdc4e37cfc`.
Driver SHA256: `54f76a50255f5f7d216954cd782fad88441cadeeb665188b40e7ca01399cc269`.
The independent full traversal corroborates the negative rather than
relying on the MDD's hashes, cardinalities, or compression.

A secondary P16 control, `g=0101010101010101`, is **UNDECIDED**: node cap
1,500,000 while expanding beyond width38, whose complete frontier has
4,475,632 states and no terminal. It took 67.740 s / 422,444 KiB in the
earlier 128-bit build. No period16 exclusion follows; the new wider counter
does not remove the historical-node memory bottleneck.

## Independent controls 和 reproduction

The separately authored temporal-tuple oracle compares 20 complete cases:
363 full frontier sets 和 585,746 state records. These include p11/p12
positives, nonuniform gaps through five, rotated driver/e pairs, 和 a wrong
p12 e filter whose exact F74=F71 return correctly excludes only that e.
Reconstructed positive witnesses pass 69 B-edge 和 414 padded ordinary-
integer checks. An additional 84 finite correlated-image comparisons cover
531 output memberships 和 156 temporal-rotation checks; 12 malformed versus
unsupported-input controls preserve the ERROR/UNDECIDED distinction.

The center fixture has 24 phases of widths 6/7, total overflow 8 和 total
pair-trim 4. Direct coefficient normalization agrees with the original
mirror on all 24 edges; 216 independently reconstructed ordinary-integer
reverse-add steps pass using synthetic exteriors realizing each e/g pair.
This validates the center alone, not compatibility of those synthetic B
words over time. `couple_target_exterior` requires a complete supplied B
cycle 和 full Python `cycleOK` before producing candidate edges.

From the repository root:

```bash
python3 -O calculation/agent-108/exterior_run.py selftest
python3 calculation/agent-108/exterior_run.py run 110001001000110001001000
python3 calculation/agent-108/exterior_run.py run 110001001000110001001000 --e 010100110100101011001011
g++ -O3 -std=c++17 calculation/agent-108/exterior_mdd.cpp -o /tmp/agent108-exterior-mdd
python3 calculation/agent-108/exterior_tiles.py --mdd /tmp/agent108-exterior-mdd
python3 -O calculation/agent-108/exterior_tiles.py --mdd /tmp/agent108-exterior-mdd
python3 calculation/agent-108/exterior_controls.py engine --binary /tmp/agent108-exterior-mdd
python3 calculation/agent-108/exterior_controls.py center
/tmp/agent108-exterior-mdd 110001001000110001001000 200000 100000000 100 10
/tmp/agent108-exterior-mdd 110001001000110001001000 200000 100000000 100 10 --e 010100110100101011001011
```

The r4 canonical tile digest matches #386. For r5 it is
`162f1a7081241f056fe3ad2412a74d536c05c1cb9d7c510db177acdf033dfd36`;
all per-r digests are printed by the auditor. Serialization sorts numeric
rows `source target left right positive x0 ... x(r-1)` 和 writes one ASCII
space between fields plus one newline per row.

## Numeric, resource, 和 repository checks

Exact unsigned 256-bit counts support `P<=96` 和 `2P+4G<=240`. For G>=1,
the full cut domain has size `D=10^G*2^(2P)<2^(2P+4G)<=2^240`.
Every suffix/accepting language is a subset of this domain; additions over
distinct labels are disjoint. This bounds intermediate node sums, not
arbitrarily many layers' cumulative totals. Addition detects overflow before
changing the accumulator. Independent Python integer controls pass 17,047
cases: 7,168 conversions/comparisons, 4,880 additions, 768 self-additions,
4,096 implicit 64-bit additions, 和 135 repeated sums, including every carry
chain length 1..256 and overflow preservation. The counter also passes UBSan.

The complete optimized-Python wrapper selftest passes all controls above,
three explicit node/operation/depth cap cases, and both SQ5 target-e/all-e
replays. Its P48 repeated-target capacity control deliberately stops at
width2, UNDECIDED; Agent115 retains the substantive two-lap application.
The native SQ5 run passes address/undefined-behavior sanitizers, with
`ASAN_OPTIONS=detect_leaks=0` because this environment forbids LeakSanitizer's
ptrace inspection. No sanitizer finding occurred. The wrapper builds in a
temporary directory and enforces address-space, CPU, and wall budgets;
interrupted/missing terminal records remain UNDECIDED. Default runs use
one process, 4 GiB, 120 native seconds; maxima are 1,700 native / 1,710
outer wall seconds. A cap during witness reconstruction may retain the
already established FEASIBLE status; replay requires the WITNESS record.

Actual `python3 tools/verify.py --changed` passes: 5,217 Lean files,
301 projects checked; zero changed Lean modules/endpoints, build OK.
This is the repository gate for a computed result, not Lean verification
of either the search algorithm or this exterior negative.
