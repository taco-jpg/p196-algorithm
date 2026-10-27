# Agent 116 — independent P24 block-language tool checkpoint

## Status, scope, 和 attribution

**PAPER PROOF + COMPUTED tool validation; target search UNDECIDED.** This is
an independent implementation of the regular exterior-language approach.
Agent106 retains [**PRIMARY** attribution](https://github.com/taco-jpg/p196-algorithm/issues/289#issuecomment-6433401663). No all-width/all-repetition P24
negative, decimal certificate, decimal Lychrel number, or general one-band
impossibility is established by this checkpoint. No new Lean result is claimed.

This checkpoint publishes the exact engine, constructive witnesses, independent
oracles, guarded runner, 和 explicitly incomplete target computations.

Claim: [issue #289, comment 6433406194](https://github.com/taco-jpg/p196-algorithm/issues/289#issuecomment-6433406194).
The fixed decimal streams are

```text
E = 010100110100101011001011
G = 110001001000110001001000
overflow starts = 0,1,5,8,12,13,17,20
block lengths   = 1,4,3,4,1,4,3,4
```

The question includes every repetition k>=1, with streams E^k/G^k, every
finite exterior width, 和 every natural neutral-suffix trim schedule.
It does not cover other streams or arbitrary nonperiodic evolution.

Related work keeps its separate attribution: [Agent109's width-16/all-laps
result](https://github.com/taco-jpg/p196-algorithm/issues/289#issuecomment-6433464638);
Agent117/[108's one-lap results](https://github.com/taco-jpg/p196-algorithm/issues/289#issuecomment-6433338180);
[Agent115's period-48 work](https://github.com/taco-jpg/p196-algorithm/issues/289#issuecomment-6433592724); Agent101's
P24 center in [PR381](https://github.com/taco-jpg/p196-algorithm/pull/381),
head `f29759a359d923c7d8c1a22d7e7aecde462d565a`. One-lap cardinalities are
attributed to [Agent117, comment 6433395207](https://github.com/taco-jpg/p196-algorithm/issues/289#issuecomment-6433395207).
The common-width bridge follows A120's definitions 和 the padding argument
audited in Agent116 PR375, retaining Agent7/Agent114's padding attribution.

## Exact reduction — PAPER PROOF

Write h=b-1 和 F_b(B) for A120's exterior successor with reverse incoming
carry 1-e, where e is the low normalization's outgoing carry. Neutral
coefficients transmit either incoming carry unchanged. Therefore

```text
F_b(B ++ h^a) = F_b(B) ++ h^a,
```

preserving e 和 overflow g, including B empty. If arbitrary-width exterior
edges satisfy F_b(B_t)=B_(t+1)++h^(u_t), choose common N>=1 at least every
phase width 和 put Q_t=B_t++h^(N-|B_t|). The length identity
|B_(t+1)|+u_t=|B_t|+g_t gives F_b(Q_t)=Q_(t+1)++h^(g_t).
Every padded first coefficient is positive; an originally empty exterior
gets positive neutral padding. Thus equal-width search loses no finite cycle.

At a spatial cut, a block of length ell records its low incoming carries L,
required reverse outgoing carries H, 和 one lag digit Y at its first phase.
The block begins with g=1, followed by ell-1 zero overflow bits. Its letter is
typed by its actual starting phase, so equal gap lengths at different phases
remain distinct. Encoding is cfg=Lmask|(Hmask<<ell)|(Y<<(2ell)).

For entering coefficient x_0 和 guessed reverse incoming bits q_j, require

```text
floor((x_j+q_j)/b) = H_j
d_j = (x_j+L_j) mod b; r_j = (x_j+q_j) mod b
x_(j+1) = d_j+Y at j=0, otherwise d_j+r_j
L'_j = floor((x_j+L_j)/b); H'_j=q_j; Y'=r_0.
```

Coefficients lie in 0..2h. FIRST requires every coefficient used inside a
block to be positive; INTERIOR permits zero. An exiting zero is allowed
locally, but cannot survive a complete FIRST word: the next block rejects it,
or final closure would contradict the positive initial coefficient.

Tiles preserve letter types 和 concatenate by matching outgoing/incoming
coefficients. Choose one anchor coefficient c 和 require equality with c
only at the end of the complete accepted word. Do not impose closure after
each 24-step unit. An accepting input-unit boundary retains all outgoing
paths, including those whose live coefficient has not yet returned to c.
This permits a genuine multi-lap response to a shorter prescribed clock.

Let S be the eight-letter initial unit: L=0, H=g, Y=1 at overflow phases.
Let T be the fixed terminal unit: L=E, H=1-E, Y=hE at overflow phases.
The initial 和 target languages are S^+ 和 T^+, never just a finite list of k.
Let FIRST 和 R denote the first-column 和 interior cyclic transductions:

```text
A_0=S^+; A_1=FIRST(A_0); A_(n+1)=R(A_n) for n>=1.
```

Induction shows A_n contains exactly the boundary words reached after n
spatial columns, simultaneously for every k>=1. Transduction preserves each
letter's type 和 hence the same repetition count. Acceptance A_n intersect
T^+ != empty is equivalent to a width-n exterior return for some k.
The terminal equations supply reverse incoming carry 1-e 和 make the extra
overflow coefficient h(1-e)+Y equal h. They are sufficient as well as necessary.
Depth zero is excluded: in this decimal target, initial overflow lag1 is
different from terminal lag0 or9. The padding argument includes empty phases.

## Whole-language algorithms 和 sound stopping

Each image NFA records (input DFA state, anchor coefficient, live coefficient).
Its final bit requires both input acceptance 和 live=anchor. Trimming retains
all accepting continuations; subset construction gives the exact output
language. A separate flat-union code path audits every constructed subset's
final bit 和 full transition set, including absent labels. DFA quotient audits
check final bits 和 all present/absent transitions before canonical numbering.

Optional strong NFA bisimulation refines final-bit classes using the old
class 和 the SET of (label,target class) pairs. At stability, every transition
from either representative is matched into the same class. Induction on word
length proves equal right languages, including epsilon. The quotient maps
the initial set to its classes. The implementation audits the exact transition
set 和 final bit for every original state; multiplicities are irrelevant.
Populated initial class counts handle all-final automata correctly.

Optional anchor streaming constructs each fixed-c image separately, then
joins all completed images. Their union equals the ordinary image exactly.
Per-anchor 和 joined bisimulation quotients preserve that union. A complete
next layer is emitted only after every anchor finishes; a partial union
cannot establish absence. Both optimizations are independently crosschecked.

For target intersection, follow T repeatedly in the DFA. Acceptance gives k;
a repeated unit-boundary state before acceptance proves no future k accepts.
This is an exact whole-language test, not inspection of k=1,2,3 counts.

An empty A_n (n>=1) proves every later image empty. An exact repeated language
A_n=A_m, n>m>=1, makes the future repeat already checked layers. The engine
requires complete terminal checks 和 confirms structural repetition by exact
DFA product equivalence. Depth0 is not compared because FIRST differs from R.
Alternatively an invariant I suffices if FIRST(S^+) subset I, R(I) subset I,
和 I intersect T^+ is empty, all established by exact language operations.

Finite alphabets do not guarantee termination: k is unbounded. Stable state
counts, finite-k controls, depth bounds, 和 resource caps are not exhaustion.
The printed k=1,2,3 cardinalities are exact diagnostics, not an all-k argument.

## Independent controls — COMPUTED

`exterior_regular_oracle.py` imports no primary engine. Local tiles enumerate
every reverse-carry bit word. Generic language comparison traverses the exact
Python-NFA-subset/C++-DFA product over all words. Layer controls enumerate
unblocked full-time tuples 和 independently replay whole-integer exterior maps.
Every validation uses explicit exceptions, not removable Python assertions.

| Control | Completed result |
|---|---:|
| Decimal gaps1..5; bases2/3 gaps1..3; FIRST/INTERIOR | 22 exhaustive queries |
| Local tiles, including every coefficient witness | 478,796 comparisons |
| NFA fixtures, two numberings, four optimization modes | 30 fixtures / 240 queries |
| Cyclic-image models, four optimization modes | 19 models / 76 queries |
| Exact generic language-product pairs | 1,820 |
| Canonical image equalities across optimization modes | 57 |
| Strong-bisimulation quotient-size regressions | 8 checks |
| Spatial-layer engine queries | 20 |
| Exact finite-k layer cardinality comparisons | 228 |
| Independent whole-integer acceptance checks | 49 |
| Canonical spatial-layer equalities across modes | 57 |

The four modes cross anchor streaming off/on with NFA bisimulation off/on.
Two/three-control toggles require closure only after two/three accepted input
units. Shared-anchor, duplicate-edge, 和 same-label nondeterminism cases pass.
A seven-state fixture reduces to four bisimulation classes only with correct
set semantics; another retains seven despite equal languages at two states.
All-final chain/cycle regressions cover the repaired fail-closed minimizer bug.
Observed tile/generic/layer suite times: 13.691321/0.510334/0.057043 seconds.

`p24_regular_controls.py` separately parses known Lean certificate DATA 和
uses whole positional integers to replay B edges, C edges, 和 ordinary
reverse-and-add equalities. It supplies common-width k1/k2 witnesses with
every spatial cut 和 checks membership in emitted DFAs. It also replays
Agent101's P24 center; no exterior existence follows from that center alone.
Completed arithmetic controls cover nine known certificates (including the
optional PR356 base20 data): 64 B/C/ordinary-step edges, 18 padded k1/k2
exterior fixtures, 和 351 padded B edges. Small controls check 419 words,
838 padding equalities, 和 468 all-trim equalities. The P24 center has 48
checked edges 和 96 symmetric-padding checks; four malformed witnesses fail.
Every one of 89 arithmetic cut words is retained in completed engine DFAs;
89 wrong-phase words 和 48 empty-word checks reject. Bases2/4/8/16 reach
positive targets; 11/17/20/26 remain capped. Base32's gap6 is explicitly
unsupported by this engine. These controls agree under ordinary/optimized
Python 和 remain independent of tiles 和 regular operations.
Agent105's physical base6 two-lap control is attributed to
[comment 6433504667](https://github.com/taco-jpg/p196-algorithm/issues/289#issuecomment-6433504667);
unit E=G=10 returns at k2/width6, while exact-k1 repeats layer8=7 without
acceptance. Its four natural 和 four padded B edges replay independently;
this is one additional B-only fixture, not a new primary period-descent claim.
The guarded runner passes 43 normal/optimized-Python controls, with 17 emitted
B witnesses independently replayed using positional integers. Missing or
corrupt witnesses, resource stops, malformed output, signals, 和 false-negative
exit protocols are rejected. The base6 all-k run returns its actual k2 witness.

## Partial P24 computation — no global negative

Complete layers0..7 have been constructed. Their k1 counts are
1,64,256,1088,16752,44368,249216,202564,
agreeing with Agent117's independently attributed one-lap counts.
The latest supplied complete row is:

| Layer | DFA states | DFA edges | k1 words | k2 words | k3 words |
|---:|---:|---:|---:|---:|---:|
| 7 | 68,124 | 303,275 | 202,564 | 24,043,530,512 | 3,555,232,868,067,904 |

The baseline 500,000-NFA-state cap stopped after complete layer6.
Streaming with that cap completed layer7 before an NFA cap. Streaming with
NFA cap2,000,000 和 DFA cap1,000,000 stopped at a DFA cap after layer7.
Final-source isolated-checkout receipts (engine time, excluding compilation):

| Mode | Last complete layer | Stop | Seconds | Peak MiB |
|---|---:|---|---:|---:|
| Default 500k/500k | 6 | NFA cap | 1.03251617 | 89.6914062 |
| Streaming 500k/500k | 7 | NFA cap | 8.39167697 | 177.582031 |
| Streaming 2M/1M | 7 | DFA cap | 20.1465576 | 458.925781 |

The streamed bisimulation pilot also stopped after complete layer7:
`OPERATION_CAP_UNDECIDED` at 500,000,000 operations, 135.810439 seconds,
peak RSS332.902344MiB. At layer7 it had 91,863 quotient-NFA states/408,305
edges, 68,165 subset states/303,357 edges, 和 the same final DFA above.
Aggregate raw counts were 1,003,551/3,998,190; maximum materialized anchor
counts were 77,998/311,033. Bisimulation is optional/default-off; this run
adds work without proving a deeper layer. Every pilot remains UNDECIDED.

## Interface, reproduction, 和 resource semantics

The engine accepts bases2..32, equal binary E/G lengths1..256, G starting
with1, 和 every overflow gap in1..5. Default input is all k>=1;
`--finite-k K` restricts to exactly K (1..1000), never certifying all k.
Defaults: 80 layers, 60 seconds, 2GiB address space, 500,000 NFA 和 DFA
states, 20,000,000 edges, 和 150,000,000 operations. Configurable wall time
is at most1190 seconds 和 memory at most8GiB. State/edge limits are explicit.
For streaming, the NFA cap applies to a materialized anchor 和 to the joined
trimmed image; aggregate raw-state statistics can exceed a per-anchor cap.

NFA/DFA/EDGE/OPERATION/TIME/MEMORY/DEPTH cap statuses remain `*_UNDECIDED`;
exceptions are `ERROR_UNDECIDED`. Completed-layer 和 peak-RSS fields preserve
the scope of partial output. `--ignore-target` is diagnostic only: it cannot
produce a negative research verdict. Positive output requires explicit
preimage reconstruction 和 direct exterior replay; it is not a paired B/C
certificate or a Lean proof. No cap or failed control becomes a negative.
`--dump-dfa` labels exports `p196-exterior-block-dfa-v1`, includes base/E/G,
finite-k scope 和 depth, 和 identifies the object as an exact frontier, not
an invariant. Typed symbol=(actual phase<<32)|cfg; omitted DFA edges reject.

```bash
c++ -O3 -std=c++17 -Wall -Wextra -pedantic calculation/agent-116/exterior_blocks.cpp -o /tmp/agent116-exterior-blocks
c++ -O3 -std=c++17 -Wall -Wextra -pedantic calculation/agent-116/exterior_regular.cpp -o /tmp/agent116-exterior-regular
python3 calculation/agent-116/exterior_regular_oracle.py tiles --block-tool /tmp/agent116-exterior-blocks
python3 calculation/agent-116/exterior_regular_oracle.py regular --regular-tool /tmp/agent116-exterior-regular
python3 calculation/agent-116/exterior_regular_oracle.py layers --regular-tool /tmp/agent116-exterior-regular
```

```bash
python3 calculation/agent-116/p24_regular_run.py guards
python3 -O calculation/agent-116/p24_regular_run.py guards
python3 calculation/agent-116/p24_regular_run.py run
python3 calculation/agent-116/p24_regular_run.py run --stream-anchors
python3 calculation/agent-116/p24_regular_run.py run --stream-anchors --nfa-cap 2000000 --dfa-cap 1000000 --memory-mib 4096 --seconds 180 --edge-cap 50000000 --ops-cap 500000000
```

The last three commands return exit2 with the scoped UNDECIDED statuses above.
Adding `--nfa-bisim` to the last command reproduces the separate operation-cap
pilot. `--output /tmp/result.json` optionally saves mathematical result data;
no output file is created by default. All runs stay below three minutes.
The runner records compilation source hashes and independently replays every
emitted B witness. Optional external PR356 `cert20.json` adds the ninth full
certificate via `p24_regular_controls.py --cert20 /path/to/cert20.json`;
the default eight-baseline run has 56 full edges and 17 total B fixtures.

Engine SHA256: `7558118dec0cfc73ee49a640eaaed8879b99c05f0c4159e4454d62f6bb7dad61`.
Local-tile header SHA256: `5b98eab00fb5697c299c896755d61b64c6808d5c35a2cc80b4bf6c2119e9b19b`.
Main parent: `eafbbbfd6b5b857597f95f68268c56dbd96b6bcb`; no unmerged code dependency.
Publication requires literal `python3 tools/verify.py --changed`; its actual
receipt and the exact checked/published tree are recorded in the PR description.
No new Lean file or registered endpoint is introduced.
