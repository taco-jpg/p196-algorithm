# Agent 110 — Wider fixed-period backward exterior MDD

## Scope 和 attribution

**COMPUTED tool extension + PAPER representation audit.** This extends the
exact backward exterior engine in
[PR419](https://github.com/taco-jpg/p196-algorithm/pull/419), which is the
explicit dependency/base of this PR. The supported temporal representation
now reaches P=64 subject to the checked cut-space bound below. Each input
still specifies **one complete temporal period**; no smaller seam is imposed
because the prescribed e/g labels repeat.

The priority application is TWO copies of the actual decimal C24 driver:

```
E24 = 010100110100101011001011
G24 = 110001001000110001001000
V24 = 100001000000100001000000
C0  = [9,14,13,18,13,14,9]
E48 = E24 ++ E24
G48 = G24 ++ G24
```

Agent115 retains primary P48 completion. This work supplies a separate
backward-engine capability 和 independent finite-period application.
Agent108 retains the forward live-memory engine (#423); Agents106/116
forward regular languages,113 backward all-lap languages,111 invariant
verification, 和109 bounded-width/all-lap decisions remain distinct.
Agent101 owns the C24 witness;117/#409 和108/#405 own the earlier one-lap
exterior results. Agent105's real multiple-lap control is
[PR417](https://github.com/taco-jpg/p196-algorithm/pull/417).

No general driver-period descent, arbitrary-lap reduction, decimal
certificate, or global neutral-band impossibility is claimed.

## 1. Exact representation change

For temporal period P, overflow count G, 和 base b, an exterior cut records
P forward bits, P reverse bits, 和 G lag digits in0..b−1. Therefore

\[
|\mathcal S|=2^{2P}b^G
\le 2^{q},\qquad q=2P+\lceil\log_2 b\rceil G.
\]

The old guard required q<=120 和 P<=32. The new guard requires q<=240 和
P<=64. Base2..32, positive overflow count, 和 overflow gaps1..6 remain the
supported geometry. Unsupported inputs return UNDECIDED; representable
inputs can still exceed explicit time, node, operation, or memory limits.
P48 has q=160, so the old count-space guard correctly rejected it.

Counts use four least-significant-first uint64 limbs. Addition uses at most
65 temporary bits per limb 和 rejects a carry past limb4; subtraction checks
order first 和 rejects underflow. Neither failed operation mutates its input.
Decimal conversion performs long division by10; the uint128 temporary is
only a limb arithmetic workspace, never the complete count. Division by a
uint32 divisor needs at most96 temporary bits. The maximum permitted set
cardinality2^240 takes241 value bits, safely inside the256-bit representation.
MDD labels partition represented words, so every partial cardinality sum
is at most the complete cut-space bound. Checked arithmetic also rejects an
unexpected implementation overflow instead of wrapping.

Carry masks remain uint64. Every individual phase shift is unsigned 和 at
most63. The old out-of-range test `mask >> P` is performed only when P<64;
at P=64 every uint64 mask already fits. Values beyond uint64 are rejected
during decimal input parsing. Block symbols, immutable node IDs, exact
interning/union, coefficient ports, FIRST positivity, terminal construction,
preimage recursion 和 witness equations are unchanged.

The inherited proof obligations remain those of #419: common-width padding
preserves the full driver 和 replaces arbitrary natural trims by u=g;
positive-FIRST paths to the neutral terminal are exactly the fixed-period
exterior returns. A backward fixed point is compared by complete canonical
root equality. A capped image gives no fixed-point conclusion.

## 2. Full temporal seam controls

Agent105's base6 canonical words are

```
[4,7,7,8,3]
[9,3,4,5,8]
[4,7,7,10,2,2]
[9,3,4,9]
```

They form a genuine four-step exterior cycle with e=g=0101 和 natural
u=[0,0,2,0]. The label word has primitive period2. Padding every B to width6
gives u=g, preserving the four distinct phases. The new engine returns
EXHAUSTED for the one-lap input e=g=01, with terminal predecessor closure
R6 of12 states 和 FIRST4 disjoint. For e=g=0101 it returns ACCEPT at width6,
R5=65 和 FIRST8, with all four B words independently replayed. This is an
exterior-only base6 control, not a base6 cycleOK certificate.

Artificial interior columns separately test the whole48/64-step seam 和
high mask bits. They are arithmetic relation fixtures, not physical B words.
For base2, g=all1, choose x with ones only at P/2 和 P−1; set old L/H 和
new L/H' to the x bits, old Y_t=x_(t+1), 和 new Y=0. The complete target
preimage has four states. It closes at P, has x_(P/2)!=x_0, 和 exercises
bits47/63. A separate decimal P48 fixture with the actual G48 uses
x24=x25=x26=1,x27=2,x28=4,x29=8,x30=9, all other x=0;
old L has bits23,29,30, new H' has bit30, 和 old Y=0. Direct literal
arithmetic verifies x48=x0=0 but x24=1. A12-phase rotation exercises bits
above31 while preserving the priority overflow pattern.

The independent arithmetic suite passes17,400 Count256 cases against Python
integers under UBSan, including maximum256-bit decimal output, boundaries
near64/128/192/240/256 bits, alias operations, 727 checked addition overflows,
2,922 subtraction underflows, 和180 divisions by zero. Failed operations
leave operands unchanged. Old/new complete sets agree on24 frontiers,
eight FIRST sets, 和55 preimages, with the whole-column oracle also checking
those preimages. All14 explicit guards return UNDECIDED/exit2, including
actual64MiB exhaustion; q=240 is accepted 和 q=242 rejected.

Actual P33/base4 和 P64/base8 searches reconstruct width2 exterior cycles,
with FIRST counts2,048 和65,536, exercising bits32 和63. A separately
authored whole-integer checker joins the P33 B witness to the known base4
center after66 steps, using the least common multiple of their periods;
the P64/base8 join closes after64. Both pass full mirror cycleOK. Base6
remains exterior-only. Ten other repeated known complete cycles contribute
408 full mirror edges. Five artificial wide columns, including both complete
four-state preimage sets, are checked independently. None is a decimal
candidate. Normal 和 optimized-Python control counts agree.

## 3. Priority P48 computation

**UNDECIDED, node cap, exit2. No candidate.** Complete reverse layers are:

| Depth | Complete state count |
|---:|---:|
| 0 | 1 |
| 1 | 5,308,416 |
| 2 | 3,844,124,001 |
| 3 | 67,414,436,737 |
| 4 | 1,344,747,058,657 |
| 5 | 5,873,017,249,113 |
| 6 | 23,814,316,376,793 |
| 7 | 101,175,231,335,657 |
| 8 | 220,745,634,903,877 |
| 9 | 383,731,445,469,622 |

All complete layers are disjoint from the complete FIRST frontier of4,096
states. Construction of R10 hits2,000,000 historical nodes after14.424860s,
peak1,257,212KiB. Final counters:47,437 local tiles, 256,287,614 operations,
17,493,790 image-cache entries, 和686,273 union-cache entries;
`last_complete_depth=9`, `image_complete=false`. Partial R10 supplies no
further conclusion. R8 used482,003 nodes; R9 used1,149,353. Increasing only
the wall allowance would not remove this node/history bottleneck, so no
duplicate near-memory-limit run was performed.

The P48 R3 count is1,089,288 smaller than the square of the P24 count259,645.
The search does not square one-lap sets or impose a24-step seam.
These finite slices can cross-check exact all-lap DFA computations, but
they establish no arbitrary-width or arbitrary-lap exclusion. Agent115's
forward scope 和 stronger completed finite widths remain credited.

The actual center repeats after24, so its48-edge replay has total G=16,
V=8 和 widths6/7. A compatible B must close after the complete48 phases;
the existing one-lap negative does not exclude it. Any reconstructed B is
replayed through literal whole-integer exterior arithmetic, joined to the
correct repeated C/v, 和 checked by the unchanged Python cycleOK before a
decimal candidate can be announced. Lean verification remains an additional
required step before any decimal proof claim.

## 4. Reproduction 和 limits

Compile the new engine 和 the exact pinned parent baseline:

```sh
g++ -O3 -std=c++17 -Wall -Wextra -Wconversion -Wshadow -pedantic \
  calculation/agent-110/p24_reverse_mdd.cpp -o /tmp/agent110-wide-reverse-mdd
git show 85ea6c91eda54559ac85241b6d77629d7279d8ce:calculation/agent-110/p24_reverse_mdd.cpp \
  > /tmp/agent110-wide-narrow-baseline.cpp
g++ -O3 -std=c++17 /tmp/agent110-wide-narrow-baseline.cpp \
  -o /tmp/agent110-wide-narrow-baseline
python3 calculation/agent-110/wide_reverse_controls.py --seconds 180 \
  --witnesses /tmp/agent110-wide-witnesses.json
python3 -O calculation/agent-110/wide_reverse_controls.py --seconds 180
python3 calculation/agent-110/wide_reverse_literal_controls.py \
  --witnesses /tmp/agent110-wide-witnesses.json
```

The arithmetic/set suite returns PASS in1.288s (optimized Python2.255s);
the independent literal/witness suite returns PASS in0.078043s (optimized
Python0.056325s). Its two captured joins add130 full mirror edges,538 total.
The witness
file contains scientific finite words/preimage sets, not an execution log.
Compiler warnings are empty. UBSan also checks P64 maximum-mask acceptance,
P63 out-of-range rejection, 和 P64 parser overflow, with empty diagnostics.

Reproduce the exact priority pilot (expected exit2, UNDECIDED/node_cap):

```sh
/tmp/agent110-wide-reverse-mdd 10 \
  010100110100101011001011010100110100101011001011 \
  110001001000110001001000110001001000110001001000 \
  --layers 1000 --seconds 60 --memory-mib 4096 \
  --nodes 2000000 --operations 2000000000
```

Frozen source SHA256 values:

```
p24_reverse_mdd.cpp 9861e0e9f07a414deee449b8bf3aa772b3d3f9f276ad71eb3f5bd3a19d9a8eab
count256.hpp c82c72b8965c0793670887919626e8ca75de1d140be6706bebb2454e7680507e
```

Runs are individually capped at1500s 和 at most4GiB. FIRST is still
explicitly enumerated: for example, some dense-overflow P64 inputs have
billions of FIRST states despite fitting the bit representation. The wider
type is a correctness/capability change, not a promise of efficient
completion on every input. No silent truncation, wraparound, horizon-limited
negative, or inference from a stable count is allowed.

Literal `python3 tools/verify.py --changed`: **ALL CHECKS PASSED**,5217 Lean
files/301 projects;0 changed Lean modules 和0 audited endpoints.
The only modified parent source is Agent110's own
engine; all other files are new Agent110 code/report. No baseline, README,
RESULTS, registry, Lean module, or other-agent source is modified.
