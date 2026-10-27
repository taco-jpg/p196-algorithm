# Agent 118 — regular languages for the saturated exterior family

**PAPER exact reduction + COMPUTED tool/partial exploration; UNDECIDED.**
The new regular-language engine represents arbitrary temporal block counts
exactly. Bounded runs complete forward width7, unfiltered backward Q3,
and residue-filtered backward Q2, then hit explicit resource limits.
No uniform saturated-family classification, new B driver, center match,
decimal certificate, or Lean theorem is claimed.

## Question and scope

Task `T2.saturation-regular-language`, claimed in
[#289, comment 6433439217](https://github.com/taco-jpg/p196-algorithm/issues/289#issuecomment-6433439217),
asks for every finite decimal exterior return with overflow word
`g=(1000)^G`, for arbitrary positive G, arbitrary finite width, and free
carry word e. This is the equality family of the exterior clock bound
`P<=4G`. A time rotation gives the equivalent `(0001)^G` convention.

The intended classification concerns **terminal carry words**, not every
possible exterior coefficient word. Known period12 exteriors are positive
controls. Repetition of g never implies repetition of B or e.

## Prior work and attribution

The positional equations are the existing
[`bauto.cpp`](https://github.com/taco-jpg/p196-algorithm/blob/eafbbbfd6b5b857597f95f68268c56dbd96b6bcb/calculation/neutral_band/structure/bauto.cpp).
Agent7's [#315](https://github.com/taco-jpg/p196-algorithm/pull/315)
supplies neutral padding; Agent114's
[#400](https://github.com/taco-jpg/p196-algorithm/pull/400) formalizes the
uniform exterior width representative at unchanged A120.

Agent108's [#337](https://github.com/taco-jpg/p196-algorithm/pull/337)
classifies the relaxed two-column saturation coding. Its arbitrary binary
block itinerary does not settle finite neutral-tail closure.
Agent108's [#386](https://github.com/taco-jpg/p196-algorithm/pull/386)
introduces the exact four-phase tile representation and completes the
fixed-G8 negative. Agent103 retains the separate fixed-G6 census and its
forward/backward completion. Those fixed slices are controls here, not new
primary results. The present question has no bound on G.

Agent118's [#399](https://github.com/taco-jpg/p196-algorithm/pull/399)
excludes centers for every positive repetition of the known p12 e/g
driver. A complete exterior classification by that driver would therefore
exclude the whole saturated certificate family. No such implication is
asserted from a finite number of layers or finite-G controls.

## Exact language model (PAPER reduction)

At one spatial cut, group times into G blocks of four. A letter
`S=(L,H,Y)` consists of four binary lower carries L, four required reverse
carries H, and one digit Y at the overflow time. Its stable encoding is
`sid=Lmask+16*Hmask+256*Y`, giving 2560 letters. Temporal words have any
positive length; the empty word is excluded.

The physical initial language is `{272}^+`, since L=0, H=1, Y=1 in every
block. The first column must have strictly positive coefficients at every
time. Subsequent columns may use all coefficients 0 through18.

The credited saturation clock also gives the closed form
`F1={65,337}^+`: the first coefficients in each block are10,1,2,5,
and its new letters have `L=1,H=4+a,Y=a` for independent bits a.
Indeed three nonoverflow steps force the postoverflow head to be1 or2;
the value2 leads to a next postoverflow head at least7, which cannot
survive three more nonoverflows. Closure therefore forces1 in every
block, then10 before the overflow and reverse-carry bits `(a,0,1,0)`.
This does not restrict the later columns to a four-step return.

A tile from S to `S'=(L',H',Y')` carries two coefficient ports x0,x4.
Its four-time trace is uniquely specified by

```text
x0 = 10*H0 + Y' - H'0
x1 = x0 + L0 - 10*L'0 + Y
x(r+1) = 2*xr + Lr + H'r - 10*(L'r+Hr), r=1,2,3.
```

For r=0,1,2,3 require `0<=xr<=18` and the exact normalization inequalities
`10*L'r <= xr+Lr <= 10*L'r+9`,
`10*Hr <= xr+H'r <= 10*Hr+9`. Ports also lie in0..18.
Neighboring letters share `x4(j)=x0(j+1)`, including the final-to-first
join. The first-column variant additionally requires x0,x1,x2,x3>0.
These are the credited exact block equations; no blockwise temporal return
is imposed separately.

Given an input DFA, the image NFA retains its input state, the current
coefficient port, and the first coefficient port. An output arc follows
one complete input arc and one compatible tile. Acceptance requires both
input acceptance and equality of the current and first coefficient ports.
Intermediate accepting states retain all outgoing arcs, allowing longer
words that close only at the final boundary.

Let F0 be the physical language, F1 its positive first-column image, and
`F(n+1)=Image(Fn)` for n>=1. These are exact full-word languages, not
products of coordinate projections. The special F0 transition is never
silently reused at later widths. Equality between two later whole
languages would imply eventual repetition of every subsequent frontier.

## Terminal-language target

A neutral terminal letter has

```text
Hmask = 15 XOR Lmask
Y = 9*(Lmask AND 1).
```

Let T be this16-letter alphabet. Finite exterior returns are precisely
the terminal words encountered in `Fn intersect T^+`, with their complete
e words given by the four L bits of each letter. Common neutral padding
transfers arbitrary original widths/trims to this representation.
Explicitly choose `N>=max(1,max_t |B_t|)` and append `9^(N-|B_t|)` to
each B_t. Suffix covariance preserves e/g, and
`|B_(t+1)|=|B_t|+g_t-u_t` makes the new trim exactly g_t. An empty
source becomes `9^N`, so it also satisfies the positive first-column
condition; no separate nonempty-B assumption is hidden in this reduction.

The known p12 stream is `1010|1001|0101`; its L masks are5,9,10, and
its terminal letters are2469,2409,90. Define

```text
K = (2469 2409 90)^+ union (2409 90 2469)^+
    union (90 2469 2409)^+.
```

The classification sought is that every reachable terminal word belongs
to K. The known p12 witnesses already supply the opposite inclusion by
repetition. Odd G must remain in the exterior model; only a subsequent
full-certificate argument may use the center parity restriction.

There is also an exact backward formulation. Put `Bad=T^+ minus K` and
take generic tile preimages. Every terminal word has the all-9 spatial
self-loop, so `Bad subset Pre(Bad)`. Monotonicity then gives
`Pre^j(Bad) subset Pre^(j+1)(Bad)`. Equality of consecutive whole languages
would establish the entire backward closure. Its intersection with F1
tests all positive exterior widths. K is subtracted only in the initial
terminal seed: removing it from intermediate preimages could discard a
path that passes through a known terminal before reaching a different one.

## Optional credited residue filter

Agent2's prior [digit-sum result](https://github.com/taco-jpg/p196-algorithm/issues/289#issuecomment-6432397102)
gives `sB'=2*sB+1-2*e (mod9)` on every exterior edge. Four phases with
L mask give `s -> 7*s+6-2*a (mod9)`, where
`a=8*L0+4*L1+2*L2+L3`. A complete word composes to `s -> alpha*s+beta`,
with alpha in{1,7,4}. It has a cyclic residue iff
`gcd(1-alpha,9)` divides beta. This is a necessary terminal-language
condition, not sufficient exterior or center existence.

An optional backward seed intersects Bad with this27-state affine-map
language. Starting from(1,0), append a terminal letter by
`(alpha,beta) -> (7*alpha,7*beta+6-2*a) mod9`. State(1,0) remains accepting
after positive identity compositions; the separate positive-word language
excludes epsilon. Only the seed is restricted. No digit-sum condition is
imposed on arbitrary intermediate cuts. Every retained terminal still has
the all-9 self-loop, so the same ascending-closure proof applies.

Independent residue counts before subtracting K for G=1..8 are
`6,86,456,21846,349526,1864136,89478486,1431655766`, reproducing Agent2's
previous finite-period counts where they overlap. Subtract exactly three
known terminal words when3 divides G. In particular the G6 seed decreases
from16,777,213 to1,864,133. This is reuse of the established digit-sum test,
not a new invariant discovery or a new G6 classification.

## Computation and validation

Every pilot below ends with exit2 and `UNDECIDED`, not an exhausted result.
State/edge limits apply to each complete construction; an interrupted image
is never used as a frontier. Time and address-space guards also fail closed.

| Mode | State/edge caps | Last complete layer | DFA states/edges there | Next obstruction |
|---|---:|---:|---:|---|
| Forward | 500k/5M | width6 | 24,827/158,964 | width7 NFA state cap |
| Forward | 2M/20M | width7 | 186,270/1,277,754 | width8 NFA state cap |
| Backward | 500k/5M | Q3 | 15,851/772,000 | Q4 NFA edge cap |
| Backward, residue seed | 500k/5M | Q2 | 4,628/165,149 | Q3 NFA edge cap |

Root's final-source forward replays used1.04s/111,420KiB and10.81s/
407,096KiB. Backward baseline used1.36s/166,880KiB; residue-seeded backward
used1.10s/142,364KiB, partly concurrently. These profiles do not predict
of completion. The residue filter reduces admitted words but increases
automaton complexity at these depths; it does not improve the bounded pilot.

Complete forward DFA state counts at widths0..7 are
`2,2,17,230,1317,3737,24827,186270`. At widths6/7, exact finite-slice sizes
for G1..8 are respectively
`0,8,1338,208,0,389396,62944,9280` and
`0,32,3186,480,0,1272908,116928,27904`.
All completed forward terminal intersections and backward FIRST
intersections are empty. These partial depth facts are not advertised as
new global width bounds; Agent109's separate bounded all-driver work is
already stronger. Finite-G counts never establish whole-language equality.

### Independent validation

The Python oracle imports no production arithmetic helper. Direct quotient/
remainder arithmetic agrees on all48,640 tiles, including41,856 positive
FIRST tiles; all16 terminal masks have the exact all-9 self-loop.
An independent NFA verifies the full FIRST language `{65,337}^+`.
69 complete finite frontiers/121,689 records agree, including every known
G3 frontier through first acceptance at width53. Six additional singleton
positive-path images agree. The reconstructed p12 B witness passes all12
edges by independently written whole-integer normalization in both directions.

Seven complete reverse images/139 words and six Bad-seed/preimage sets/
4,547 words agree with the independently transposed relation. Tests detect
swapped temporal ports, lost whole-word closure, premature boundary closure,
lost input correlations, wrong K concatenation, repeated subtraction of K,
and epsilon inclusion. A temporary harness exercises the actual backward
witness routine on the known p12 path; its12 edges independently replay.
Residue seeds for G1..3 have exactly6,86,453 words, compared as full sets
against nine-start simulation of the original one-step recurrence.
Known identity compositions and epsilon/translation countercontrols pass.

The implementation reuses pinned PR399 automata operations and verbatim
PR386 tile arithmetic in temporary generated includes. Subset construction,
quotient homomorphisms, and separate DFA-product equality checks remain
exact. Two source/proof reviews found no logical defect. A wrapper gate
gap found during review was fixed: success now requires matching mode,
scope, fixed-G control status, recurrence/closure receipts, and a matching
replayed witness for a new-driver status. Caps cannot satisfy that gate.
The published wrapper regression has13 synthetic protocol fixtures:
three valid controls pass and ten incomplete/wrong-scope cases reject.

The fixed-G3 control also reproduces credited `F74=F71`, period3, after
75 terminal checks:11,306,953 guarded operations,0.21s/13,100KiB. This
tests the non-adjacent recurrence gate; it is not an all-G conclusion.
ASan/UBSan pass the actual G3 positive witness, backward throughQ3 and
residue-backward throughQ2 with no diagnostics; the latter runs stop at
their requested layer limits. Peak child RSS was761,388KiB. Leak scanning
was disabled for the sandbox ptrace limitation; no leak audit is claimed.

### Reproduction

From the repository root, C++17 and Python standard library:

```sh
python3 calculation/agent-118/build_exterior_regular.py
python3 calculation/agent-118/test_exterior_regular.py --binary /tmp/p196-agent118-exterior-regular/exterior_regular --full-p12 --backward --residue-seed
python3 calculation/agent-118/check_exterior_wrapper.py
python3 calculation/agent-118/run_exterior_regular.py /tmp/p196-agent118-exterior-regular/exterior_regular
python3 calculation/agent-118/run_exterior_regular.py /tmp/p196-agent118-exterior-regular/exterior_regular --states 2000000 --edges 20000000 --ops 500000000 --seconds 120 --memory-gib 4
python3 calculation/agent-118/run_exterior_regular.py /tmp/p196-agent118-exterior-regular/exterior_regular --backward
python3 calculation/agent-118/run_exterior_regular.py /tmp/p196-agent118-exterior-regular/exterior_regular --backward --residue-seed
python3 calculation/agent-118/run_exterior_regular.py /tmp/p196-agent118-exterior-regular/exterior_regular --fixed-blocks 3
python3 tools/verify.py --changed
```

The builder fetches pinned108 source at commit
`9b3f0c26d3482b93e4f13a6fe9194e8d3dcb1a5f`, SHA256
`3463604f5332e2d2bd60686de7f5fac0f3770b2ab09ccc3baa3a96a2615034c3`.
Offline use `--tiles-source /absolute/path/to/saturation_mdd.cpp`.
PR399 core SHA256 is
`8b7c00df5282f156bb027dfb5709d4ad82f7af614dec355fc8b6d93a86f27d19`.
This task's exterior source SHA256 is
`86092950d08e6b7b2d3562da6b12f0fb007b30f3c8ada466d88c0130ec673054`.

Sanitizer reproduction: build with `--sanitize --out-dir /tmp/breg118-asan`,
then run that binary with `ASAN_OPTIONS=detect_leaks=0:halt_on_error=1`
and `UBSAN_OPTIONS=halt_on_error=1`. Arguments are respectively
`--fixed-blocks 3 --stop-at-known --witness --layers 60`,
`--backward --layers 3`, and `--backward --residue-seed --layers 2`.
Use a120-second outer timeout; do not impose a small ASan virtual-memory cap.

### Optional larger bounded run

One process/core,8GiB address-space ceiling and900-second wall ceiling:

```sh
python3 calculation/agent-118/run_exterior_regular.py /tmp/p196-agent118-exterior-regular/exterior_regular --layers 120 --states 10000000 --edges 100000000 --ops 5000000000 --seconds 900 --memory-gib 8
```

This ready command is unexecuted. At the measured2M-state cap the process
used about398MiB, but later subset construction and retained layers can
require much more. Budget at most15minutes/8GiB; completion is not promised.
This optional job ranks below the campaign's priority repeated-P24 work.

The reusable forward and backward solvers preserve arbitrary positive G,
but none of the completed runs reaches a uniform stopping certificate.
Further computation requires an exact invariant or a completed language
return, not an extrapolation from these profiles.
