# Agent117 — every repetition of the P42 center overflow is obstructed

## Result and exact scope

**PAPER PROOF of the reduction + COMPUTED complete finite obstruction.**
Let `w=101000101001001010100` (21 bits). There is no decimal exterior B
cycle with overflow word a cyclic rotation of `w^k`, for **any k>=1**,
any carry word e, arbitrary finite exterior widths, and arbitrary natural
neutral-suffix trims. Consequently, Agent6's actual P42 center from
[#361](https://github.com/taco-jpg/p196-algorithm/pull/361) has no matching
finite exterior after one lap or any positive number of its laps.

This excludes one specific overflow family. It is not a no-go theorem for
all centers of width7, other overflow words, the unrestricted A120 route,
or decimal Lychrel existence. No new Lean theorem or certificate is claimed.
Nonempty intermediate prefix graphs are only necessary relaxations.

The task was claimed in
[6433515606](https://github.com/taco-jpg/p196-algorithm/issues/289#issuecomment-6433515606)
and explicitly extended to repetitions in
[6433542904](https://github.com/taco-jpg/p196-algorithm/issues/289#issuecomment-6433542904).
This PR is stacked on our [#409](https://github.com/taco-jpg/p196-algorithm/pull/409),
which supplies unchanged integer oracles and the frozen narrower solver.

## Prior work and the actual center

Agent6 supplied the projected P42 witness and the exterior-prefix relation.
[#367](https://github.com/taco-jpg/p196-algorithm/pull/367) excludes that
particular three-coefficient exterior itinerary at coefficient4. Our search
does not prescribe that itinerary: alternative prefixes survive through
coefficient4, and the complete family fails at coefficient5.
Agent7's neutral-suffix covariance, subsequently formalized by Agent114
([#366](https://github.com/taco-jpg/p196-algorithm/pull/366),
[#400](https://github.com/taco-jpg/p196-algorithm/pull/400)), handles arbitrary
widths/trims. These mathematical attributions are unchanged.

The center fixture, pinned to Agent6 commit
`0ac61037baa3a6ac8a560c4bd6057e7bbb4c6180`, is:

```text
E  = 010100010111000101010101011101000111010101
G  = 101000101001001010100101000101001001010100 = w^2
V  = 000000010000200000010000000010000200000010
C0 = [18,13,13,18]
```

`p42_center_target.py` contains all42 centers and independently replays every
raw image, carry flip, natural pair trim, and closing edge by whole integers.
Widths are3..7, total g=16, total v=8; the second21 centers are coefficientwise
18-complements of the first21. This validates only the center.
Its candidate assembler requires complete B words and the unchanged Python
`cycleOK` before emitting full candidate edges. No candidate was found.

## PAPER PROOF: a sound finite prefix relation

Write h=b-1. For R>=1 define the finite R-word Pi_R(B)=take_R(B ++ h^infinity).
A valid B is empty or has positive first coefficient;
therefore Pi_R(B) always has positive first coefficient, including empty B.

For source prefix a=(a0,...,a[R-1]), retain BOTH possible unresolved inward
reverse carries z[R] in{0,1}. Compute backwards and forwards:

```text
z[j]   = floor((a[j]+z[j+1])/b),    g=z[0]
l[0]   = 0
d[j]   = (a[j]+l[j]) mod b,        l[j+1]=floor((a[j]+l[j])/b)
r[j]   = (a[j]+z[j+1]) mod b
g=0:   a'[j]=d[j]+r[j]
g=1:   a'[0]=d[0]+1; a'[j]=d[j]+r[j-1] for j>=1.
```

These are the ordinary normalization equations for the actual exterior
update. The carry e is imposed at the eventual finite terminal boundary,
not at every spatial prefix. The projected relation imposes no e constraint.

For every actual exterior edge F(B)=B' ++ h^u, with any natural u,

```text
(g, Pi_R(B')) belongs to projected(b, Pi_R(B)).
```

For R<=|B| choose the actual inward carry at the cut. For larger R, append
enough neutral coefficients first. Suffix covariance preserves e/g and gives
F(B ++ h^a)=F(B) ++ h^a. Its first R output coefficients equal Pi_R(B'),
because deleting or appending a neutral suffix leaves Pi_R unchanged.
This includes empty/short source and target words. No minimum B width,
maximal-trim restriction, or uniform temporal width is assumed here.

## PAPER PROOF: refinement retains every number of laps

The phase graph uses t modulo21 and edges t->t+1 with prescribed g=w[t].
A B cycle whose overflow word is w^k projects to a closed walk of length21k.
The graph permits every such walk; it does not impose closure after21 steps
or use a driver-period-descent theorem. Rotating a cycle aligns its first phase.

At R=1 enumerate every phase and head1..18. Retain all projected transitions
with the prescribed overflow and an existing target. Repeatedly delete
vertices of indegree0 or outdegree0. Every vertex on a closed walk survives:
the first deleted vertex of that walk would still have its predecessor and
successor. Call the retained graph the in/out-degree core.

At each next R append every coefficient0..18 to every retained shorter
prefix. A real projected closed walk uses only retained shorter prefixes,
so all its extensions and edges remain candidates. Deletion again preserves
the walk. Induction proves that an empty core at any finite R excludes every
actual finite B cycle, for every k. This is a necessary projection argument;
surviving vertices or paths alone do not construct a finite B return.

## Complete computed obstruction

`p42_prefix_audit.py` uses the digit-carry relation above and finite graph
deletion. The complete decimal21-phase computation is:

| R | Candidate vertices | Unique arcs | Retained vertices | Retained arcs |
|---:|---:|---:|---:|---:|
|1|378|301|21|21|
|2|399|407|46|51|
|3|874|940|57|65|
|4|1,083|1,230|39|42|
|5|741|754|**0**|**0**|

Only the first coefficient is forced:
`[14,5,10,1,3,7,15,6,12,3,6,13,4,8,16,7,15,6,12,3,7]`.
The nonunique higher prefixes explain why simply reusing Agent6's fixed
three-prefix obstruction would not establish this broader result.

Using the42-phase doubled G independently doubles every vertex/arc count
and again empties at R=5. The741-vertex final lifted graph has longest path22;
this statistic concerns only that filtered domain, not unrestricted B
trajectories or the full Cartesian width5 graph.

## Separately authored whole-integer graph check

`p42_full_prefix_check.py` constructs the FULL Cartesian phase graphs through
R=3, without using shorter-prefix pruning. A local edge is obtained from the
ordinary integers sum(a[j]*b^j) and sum(a[j]*b^(R-1-j))+z, not the production
digit-carry recurrence. It deletes all sources, then all remaining sinks;
sink removal cannot lower a remaining vertex's indegree. Exact surviving
vertex AND edge sets agree with the production computation:

| R | Full vertices | Full arcs | Retained vertices/arcs |
|---:|---:|---:|---:|
|1|378|301|21 /21|
|2|7,182|5,719|46 /51|
|3|136,458|108,661|57 /65|

It then skips the R=4 refinement entirely. All57 independently obtained
R=3 vertices receive all19^2 two-coefficient extensions. This separate
width5 graph has **20,577 vertices and23,370 arcs**. A complete source-only
topological deletion removes every vertex. This independently proves the
same all-repetition obstruction without trusting the production R4 core.
Its longest path28 again applies only to its stated candidate domain.
The complete independent check took approximately1.01s.

Agent105's base6 example
[6433504667](https://github.com/taco-jpg/p196-algorithm/issues/289#issuecomment-6433504667)
is a genuine four-step B orbit over the two-step e=g=01 driver. All4 actual
integer edges and16 projected edges at widths1..4 survive our phase graphs.
At width4 the four projected states are explicitly distinct; the shorter
prefixes alone would collapse to period2. This tests genuine multiple laps,
not a new period-descent claim.

## Independent exact one-lap engines

`wide_driver_exterior.cpp` extends the frozen #409 solver to four64-bit
limbs. It supports P<=63, bases2..62, positive overflow and
2P+ceil(log2 b)*G<=256. L occupies bits0..P-1, H the next P bits, followed
by one digit field per overflow. Equality compares all limbs. Cross-limb
fields avoid shift64; the P42 cut requires148 bits, beyond the old127-bit cap.
The forward transition core is the unchanged `bauto.cpp`; exact inverse,
forward, and bidirectional modes retain fail-closed resource semantics.

The complete P42 forward traversal with no prefix-itinerary restriction gives
frontiers **[1,65536,331776,147456,23104,0]**,567,873 records including the
physical provenance root,567,872 emitted transitions, and zero accepting e.
All records are expanded; `all_e_audit_complete=true`. Runtime4.394629s
internal/4.502263s wall, peak146,460KiB, exit0; no limit fired.

Pinned Agent108 [#405](https://github.com/taco-jpg/p196-algorithm/pull/405),
commit `b30d1d5a71d9be24fa28c5e05c76302919a322e6`, independently gives exactly
the same six frontiers using its correlated nonuniform block MDD. Our
unrestricted-e replay reports `EXHAUSTED_NO_B`,258 nodes,11,705 operations,
0.006834s native/0.011176s wall. A separate prescribed-e replay agrees.
Its decimal p11 positive control reconstructs a width29 exterior and all11
edges pass our independent whole-integer replay. These engine runs establish
only the one42-step case; the phase-prefix proof supplies the all-k result.

## Arithmetic, numeric, and resource controls

The production prefix selftest passes7,832 complete local source words in
bases2/3/4/10 against whole-integer normalization;7,859 complete B words,
8,514 legal trims and51,084 neutral-padded projections include empty/short
words. All8 existing source-certificate bases preserve112 explicit graph
vertex/edge checks. Normal and optimized Python agree. A state cap or an
unexhausted prefix bound returns UNDECIDED. The first-layer cap is checked
before allocation. The full-graph checker also caps allocation in advance.

Wide controls recover all8 source exterior cycles in each of forward,
reverse and bidirectional modes. All8 bidirectional witnesses independently
replay actual B words, cuts and each column. The frozen128-bit and new256-bit engines agree on
1,409 complete small forward cuts and2,304 reverse cuts for the P24 control.
Independent Python integers verify36 limb cases spanning3,148,154,189,192,
252 and256 bits;6 invalid numeric inputs are rejected. A genuine repeated
base17 P42 positive with154-bit cuts has exactly128 independently matched
predecessors. The independent P42 physical first frontier has65,536 cuts,
every column replays; its sorted32-byte-key SHA256 is
`f957bc4321e50da389ccfc9c35f8ddf4f699085036e44a9b9378a5af02506627`.
The exhaustion metadata checker labels itself as such, not a second full
explicit traversal. All runs stay well below the30-minute task budget.

## Reproduction

Run from this PR's repository root:

```bash
python3 calculation/agent-117/p42_center_target.py
python3 calculation/agent-117/p42_prefix_audit.py --selftest
python3 -O calculation/agent-117/p42_full_prefix_check.py
python3 calculation/agent-117/p42_prefix_audit.py --g 101000101001001010100101000101001001010100 --max-width 5
c++ -O2 -std=c++17 calculation/agent-117/wide_driver_exterior.cpp -o /tmp/agent117-wide
/tmp/agent117-wide --mode forward --cap 1000000 --seconds 120 --memory-mb 1024 --ops 100000000
python3 calculation/agent-117/wide_driver_verify.py --key-controls /tmp/agent117-wide --wide-control /tmp/agent117-wide --known-controls /tmp/agent117-wide --first-frontier
python3 tools/verify.py --changed
```

Optional MDD reproduction at the pinned external #405 checkout:

```bash
python3 calculation/agent-108/exterior_run.py run 101000101001001010100101000101001001010100 --seconds 120 --gib 4
```

The primary result needs only the small prefix scripts and credited integer
oracle from #409; the wide engine and external MDD are corroboration.
Use `--max-width 4` or `--states 1` on the prefix script to exercise explicit
UNDECIDED exits. No resource-limited run is counted as a negative result.

## Repository gate

Code/report-only change; no Lean modules or registry changes. The actual
`python3 tools/verify.py --changed` gate passes:5,217 Lean files/301 projects
checked,0 changed modules/0 endpoints, build OK, ALL CHECKS PASSED.
This gate does not convert the finite computation into a Lean theorem.
Only Agent117 files are added; source Agent6/108 files and README/RESULTS
remain unchanged. The broader decimal route and other drivers remain open.
