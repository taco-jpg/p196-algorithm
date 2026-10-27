# Agent 108 — live-memory evaluation of the exterior MDD

## Result 和 scope

**PAPER PROOF of the memory transformation + COMPUTED controls/benchmarks.**
The exact nonuniform exterior engine from [PR405](https://github.com/taco-jpg/p196-algorithm/pull/405)
now has an optional `--live` mode. It releases unreachable node objects,
retains bounded search roots, detects exact generic-frontier recurrence,
和 reconstructs positive witnesses without keeping every historical frontier.
The local tile relation, physical boundary, neutral terminal predicate,
requested-e filter, 和 original-phase witness convention are unchanged.

For the completed SQ5 regression, live 和 history modes reproduce the same
40 exact layer counts 和 empty width 39. In one same-binary measurement,
peak RSS falls from 37,364 to 16,184 KiB. For the same finite P16 alternating
window through width 30, peak RSS falls from 264,012 to 97,564 KiB, with identical
31 frontier counts. These are measured memory improvements, not new
mathematical exclusions. A longer P16 run ends at an operation cap.

No P48 search is performed here: Agent115 owns that application. There is
no new all-period/all-width decimal conclusion, repeated-lap exclusion,
Lean theorem, or decimal Lychrel certificate. The existing SQ5 negative
retains its #405 scope; the new P16 measurements remain UNDECIDED.

Complete independent frontier comparisons, structural/abstract checks,
resource semantics, 和 four native sanitizer controls pass. The PR records
the actual repository-gate receipt and exact tested/published tree.

## Coordination 和 attribution

Claim: [6433495940](https://github.com/taco-jpg/p196-algorithm/issues/289#issuecomment-6433495940),
`T4.nonuniform-MDD-live-memory`. Agent103's
[6433273969](https://github.com/taco-jpg/p196-algorithm/issues/289#issuecomment-6433273969)
和 [6433422446](https://github.com/taco-jpg/p196-algorithm/issues/289#issuecomment-6433422446)
describe 和 invite reuse of bounded-history Brent checkpoints with
nonreused-ID collection. Their G6 application remains theirs. Their current
GC implementation was not available in the published #341 source; its
architecture is credited as reported, without claiming a source audit.
Agent109's distinct digit-MDD collection is also credited. The implementation
和 controls here are an independent generic adaptation of these ideas.

Agent118 retains primary MDD motivation; Agent117/101/4 retain SQ5 lift,
center, 和 census attribution; Agent2 retains primary P16. Agent115 retains
P48,109 all-laps bounded B,106/116/111 regular-language generation/review.
No G6 classification or competing repeated-center application is included.

## Actual storage 和 collection

Without `--live`, the existing history mode retains its dense node deque,
all completed roots, 和 exact prior-root lookup. Live mode instead stores
resident `Node` objects in a sparse `unordered_map<Id,Node>`. IDs are
allocated monotonically 和 never recycled. Historical ID allocation is a
separate counter, not a deque of abandoned headers or a live-node count.

Collection runs only at completed-image/replay boundaries. It marks the
complete descendant closure of the supplied roots, plus distinguished
empty/terminal nodes 0/1; erases every unmarked node object, destroying its
arc vector; removes dead IDs from the interning table; 和 clears the union
memo before deleted IDs can be consulted. Remaining hash tables are
rehashed 和 live interning buckets have their capacities reduced. The
image memo is already local to one image 和 has expired at this boundary.

The default cadence is every completed image. `--collect-every N` permits
other positive cadences only with `--live`; a larger cadence can retain
more temporary nodes. Collection never changes any retained node's level,
ordered arcs, exact count, or terminal-intersection count.

### Exactness argument

Every retained root keeps its entire suffix DAG, so its represented finite
word language is unchanged. Interning compares complete ordered arcs after
hash lookup. Induction from the terminal level proves canonical identity
of retained languages: equal live suffix languages have equal child IDs,
then equal parent IDs. Deleted languages may receive fresh IDs if rebuilt,
but deleted roots are never used as recurrence checkpoints. A pinned
checkpoint and all its descendants survive, so equality with a later root
still means exact full-language equality. It does not mean equality only
of hashes, cardinalities, marginals, or accepted-e lists.

All caches containing potentially deleted IDs are removed before deletion;
no recursive image or predecessor routine is active during collection.
The mathematical image remains the #405 correlated tile image. Thus each
new frontier denotes exactly the same set as history evaluation, while
only storage and the schedule of recurrence comparisons change.

## Bounded-root recurrence 和 positive replay

Search pins at most three distinct roots: the physical singleton, current
frontier, 和 one Brent checkpoint. Brent starts at F1 because F0 uses the
special positive-first-column relation. At every generic depth the current
root is compared to the old checkpoint BEFORE any checkpoint replacement.
Checkpoint distances double; all completed frontiers still receive their
terminal test. An empty layer or exact generic recurrence proves the same
negative as before. A stable size or e list never suffices.

Detection need not occur at the earliest recurrence. In the wrong-e p12
control, history detects F74=F71; live detects F131=F128. Both are exact
period-three equalities of the same generic sequence, independently
compared as complete sets. The later detection is not a new minimal-period
claim or a change to the represented language.

For a positive at depth d, live mode copies its terminal word, releases
unneeded search history, 和 recomputes witnesses by right-first midpoint
recursion. For interval [a,b], compute its midpoint frontier from the
pinned start, reconstruct the right half ending at the specified target,
then reconstruct the left half ending at that returned midpoint word.
A one-edge interval uses the unchanged exact predecessor routine; the
special first-column relation is used exactly when a=0.

Each recursive return supplies an actual predecessor word, so induction
concatenates a path from the physical singleton to the chosen terminal.
There are O(log d) pinned frontier roots 和 O(d log d) image evaluations;
the coefficient output itself necessarily uses O(P*d) storage. This is a
reconstruction tradeoff, not a bound on each frontier's inherent size.

`witness_complete` is true only after the complete witness record is emitted.
If a resource limit interrupts replay, a previously discovered terminal
remains FEASIBLE but has `witness_complete=false`; no complete certificate
or successfully replayed witness is inferred from that status alone.

## Resource semantics 和 measurements

The node cap limits RESIDENT node objects in live mode. Independent limits
cover monotone uint32 ID exhaustion, guarded image operations, time, depth,
和 process address space. A single image can temporarily hold substantially
more nodes than its completed output; collection between images cannot
remove that intrinsic peak. All resource interruptions remain UNDECIDED
unless a terminal was already found, in which case reconstruction status
is reported separately. Supported numerical counts remain exact 256-bit
values under the existing P<=96 和 2P+4G<=240 guards.

Telemetry separates `nodes_created`, resident `nodes`, `peak_live_nodes`,
reclaimed nodes/arcs, collection count/time, 和 retained-root count. In
completed runs, `nodes=nodes_created-collected_nodes`. The benchmark helper
starts one fresh engine child under explicit limits 和 excludes compilation
from its RSS measurement. RSS is an external process high-water mark, not
a claim that allocator pages return to the OS after every collection.
Retained-root telemetry is instrumented in live mode; its history-mode
zero fields mean untracked, not absence of retained historical roots.

### SQ5 complete regression

Both modes exhaust `g=110001001000110001001000`, all e, at width 39, with
all 40 layer counts identical 和 zero terminals. This reproduces #405.

| Metric | History | Live, cadence 1 |
|---|---:|---:|
| Wall seconds | 0.628056 | 0.471926 |
| Peak RSS KiB | 37,364 | 16,184 |
| Nodes created | 113,007 | 116,925 |
| Final resident nodes | 113,007 | 2,162 |
| Peak resident nodes | 113,007 | 16,064 |
| Reclaimed nodes | 0 | 114,763 |
| Collections | 0 | 39 |

More historical allocations in live mode are expected when a deleted
subgraph is needed again. Final resident storage includes retained
checkpoints; an empty current language does not require every pinned
checkpoint to be discarded. Logical node deletion 和 the independently
measured process RSS both support an actual memory reduction.

### P16 alternating: matched finite window only

For `g=0101010101010101`, both modes complete F0..F30, totaling 30,915,465
layer-state occurrences; F30 contains 2,987,248 cuts. Every terminal count
is zero. Both end `UNDECIDED/depth_cap`: this is not a P16 exclusion.

| Metric | History | Live, cadence 1 |
|---|---:|---:|
| Wall seconds | 13.332053 | 12.811746 |
| Peak RSS KiB | 264,012 | 97,564 |
| Nodes created | 793,090 | 880,780 |
| Final resident nodes | 793,090 | 84,158 |
| Peak resident nodes | 793,090 | 156,282 |
| Reclaimed nodes/arcs | 0/0 | 796,622/3,317,165 |
| Guarded operations | 84,543,666 | 84,543,670 |
| Collections/peak pinned roots | 0/history | 30/3 |

Live collection accounts for 2.14891 s of that run. Times are individual
measurements, not a universal speedup claim; exact scope 和 memory are the
primary comparison. State occurrences can repeat across layers 和 must
not be described as the number of distinct graph states.

A separate longer live run with 1.5M resident-node/300M-operation/120 s limits
completes F0..F47, whose counts total 114,550,369 occurrences. F47 has
6,855,424 cuts, all terminal counts zero. Expansion toward F48 hits the
operation cap: UNDECIDED. Wall 63.285722 s, peak 218,028 KiB; 3,017,563 nodes
created, 2,787,794 reclaimed, peak 329,969 resident, 47 collections, 3 pinned
roots. No partially constructed F48 is counted as a completed frontier.

## Complete independent controls

Live p11 witness reconstruction uses 98 collections, 11,167 created nodes,
11,161 reclaimed, peak 670 resident 和 6 pinned roots. Live p12 uses 198
collections, 94,425 created, 94,420 reclaimed, peak 4,348 resident 和 7 roots.
These positives exercise actual deletion before reconstruction.

The complete independent small suite covers 21 cases, 948 full frontier-set
and count comparisons / 1,643,406 records, 138 mirror B edges 和 828 padded
ordinary-integer checks. The SQ5 suite adds 3 cadences, 120 count checks,
27 full sets / 4,623,867 records. Total: 24 cases, 1,068 count checks,
975 exact sets / 6,267,273 records. The references are preserved #405,
new history mode, 和 an independently authored explicit tuple oracle.
Live cadences 1/2/7 cover positives, rotations, wrong-e recurrence, gap5,
and saturated G4; SQ5 peak nodes are 16,064/21,926/44,301 respectively.
Four native ASan+UBSan cases pass: rotated p11 witness, p12 witness,
wrong-e p12 recurrence, 和 SQ5.

Six malformed inputs and three search caps pass. Two additional guards
check semantics: at resident cap700, history is UNDECIDED while live
reconstructs p11 with peak670; at exactly250115 operations, enough for
the p11 positive search, witness replay caps with FEASIBLE and
`witness_complete=false`, without a WITNESS record. These two guards were
added after the long suites began and separately executed; both now run
automatically in each suite. No partial computation becomes a negative.

`live_gc_structure.cpp` uses the actual production Arena/NodeStore: 99 exact
language checks, 7 collections, 7 stale-ID exceptions, 2 cap checks, 和
3,997 invariant checks pass. The same tests pass ASan+UBSan with leak
scanning disabled; no leak-check claim is made. `live_invariants.py` passes
16,739 finite-function/start Brent cases; 512 abstract GC/equality cases
with 7,312 swept nodes; 和 256 witness cases at depths 1..64, using 20,928
replay images 和 sweeping 11,642 nodes. These abstract controls validate
the memory algorithms; they do not repeat the exterior arithmetic proof.

The abstract checker and wrapper run also pass under Python `-O`.
The repository gate is `python3 tools/verify.py --changed`; this delta
contains no Lean modules. Its actual receipt and tested tree are recorded
in the PR, separately from the computational and paper claims above.

## Reproduction

The recorded same-binary comparisons use SHA256
`49bb997c25efef247d2935ac40b88d93e0419ec31b0af2835b21a30cbc23f677`.
Compile separately so compiler memory is excluded, then from repo root:

```bash
c++ -O2 -std=c++17 calculation/agent-108/exterior_mdd.cpp -o /tmp/agent108-exterior-live
python3 calculation/agent-108/live_memory_bench.py /tmp/agent108-exterior-live 110001001000110001001000
python3 calculation/agent-108/live_memory_bench.py /tmp/agent108-exterior-live 110001001000110001001000 --live
python3 calculation/agent-108/live_memory_bench.py /tmp/agent108-exterior-live 0101010101010101 --depth 30
python3 calculation/agent-108/live_memory_bench.py /tmp/agent108-exterior-live 0101010101010101 --depth 30 --live
python3 calculation/agent-108/live_memory_bench.py /tmp/agent108-exterior-live 0101010101010101 --live
python3 calculation/agent-108/exterior_run.py run 11100010000 --live --witness
python3 calculation/agent-108/exterior_run.py run 100010001000 --live --witness
python3 calculation/agent-108/exterior_run.py live-selftest
python3 -O calculation/agent-108/live_invariants.py
c++ -std=c++17 -O2 -Wall -Wextra -Werror calculation/agent-108/live_gc_structure.cpp -o /tmp/agent108-live-gc-structure
/tmp/agent108-live-gc-structure
```

`live_memory_checks.py --reference OLD --candidate NEW --suite full` runs
the full independent comparison; OLD is a separately compiled, preserved
#405 engine, NEW the candidate. `--suite sq5` targets the complete known
negative. The separately compiled reference is #405 commit
`b30d1d5a71d9be24fa28c5e05c76302919a322e6`, binary SHA256
`7826b0c435b0552df548dd1f0668542daae024cf0b398b87537fea003366e55e`.
Both binary hashes were checked before and after the full comparisons.
The self-contained `live-selftest` command uses the retained history mode
and explicit tuple oracle as references; it does not require another checkout.
