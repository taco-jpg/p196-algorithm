# Agent 101 — D7 center-driver catalog and exterior triage

## Scope and attribution

**COMPUTED** finite graph analysis and scoped exterior trials, with a
**PAPER PROOF** of the reductions described below. This is not a Lean result.
The task is [T1.D7-new-driver-catalog](https://github.com/taco-jpg/p196-algorithm/issues/289#issuecomment-6433532960).
It follows our bounded-model report [#410](https://github.com/taco-jpg/p196-algorithm/pull/410).

Agent 6 owns the primary decimal prefix/center hierarchy. This PR is stacked
on Agent 101's separately authored and reviewed R3,D7 product implementation
[#381](https://github.com/taco-jpg/p196-algorithm/pull/381); that frozen factor
source is imported unchanged. The present contribution examines its exact
strongly connected components and extracts additional complete center drivers.
It does not claim that the product relation is new or that a finite exterior
has been found merely because a projected loop survives. The new exterior
checkpoint is the exact formerly capped SQ1 overflow word at period 18, with
Agent 4 retaining primary census attribution; no complete p18 theorem is
claimed from this single-word verification.

The known P24 center remains Agent 101's discovery; its one-lap arbitrary-width
exterior exclusion is credited to Agent 117/#409 and Agent 108/#405. Agent 117
also owns the P42 driver lift and its repeated-lap extension. The catalog
excludes every rotation and repetition of these paired e/g words. Other agents'
P24 repeated-lap searches, regular-language methods, and invariant checkers
remain separate. No driver-period descent is assumed.

## 1. Exact graph and cycle preservation

The frozen graph has an exterior prefix of exactly three coefficients, with
positive first coefficient, coupled to a symmetric center of length at most
seven. Coefficients are in 0..18, and the middle coefficient of an odd center
is even, as necessarily holds on a cycle after a raw center update. A center
has its unique complementary entering carry e. The unresolved reverse carry
at the exterior prefix boundary is free. An edge joins factor edges with
the same overflow g and retains the actual center trim v.

The sentinel used to realize an exterior-prefix transition is an auxiliary
finite word. Its own entering carry is not constrained to equal the center's
e. Keeping that distinction is necessary: this graph is an overapproximation
of full exterior/center dynamics, not a certificate checker.

Iterated sink removal preserves every directed cycle. The implementation
reuses the dead peeling queue as an original-to-compact vertex index, builds
the complete residual adjacency, then releases both full-size arrays. It
checks live outdegrees and the independent total live-arc identity. Iterative
Tarjan traversal partitions this residual into exact strongly connected
components; no recursion depth or hash equality is used for the partition.
Every closed walk lies entirely within one such component. Consequently an
exhaustive component classification is a statement about this finite projected
graph, even when a later driver sampler is deliberately nonexhaustive.

## 2. Driver periods and exact witnesses

Every retained witness contains all projected prefix and complete center
edges, with source/target words, e, g, v, and the chosen unresolved cut carry.
Independent positional-integer normalization replays both factors and every
seam. The closed center length identity gives sum(g)=2sum(v).

For a witness of length P, the *paired-label period* is the least divisor d
of P for which both e and g repeat. This d need not be the literal center
return period. An exterior exclusion at d therefore does not by itself rule
out a center that closes only at P. The triage runner always queries the full
witness period and never replaces it by its paired-label period.

Cyclic rotations of a full paired e/g word represent equivalent exterior
questions: rotate B and C together. Keeping one actual C/v witness for that
word is sufficient for a one-lap existence test, but does not classify other
periods or every center. The known-driver exclusion uses paired words, never
g alone, and does not infer that repeated labels force repeated B.

## 3. Exterior engine and candidate gate

The optional triage backend is Agent 108's published nonuniform block MDD,
[#405](https://github.com/taco-jpg/p196-algorithm/pull/405), pinned at
`b30d1d5a71d9be24fa28c5e05c76302919a322e6`. This is an attributed external
dependency, not a newly authored engine. Its exact terminal e/g language
covers every finite exterior width and arbitrary natural suffix trims via
credited common padding. A terminal witness is reconstructed, not inferred
from a positive count alone.

Only a successful terminal result with `empty_layer` or `exact_layer_repeat `
can be reported as a scoped exterior exclusion. Unsupported patterns, memory,
operation, depth, CPU, or wall limits remain UNDECIDED. Every subprocess has
hard limits, and a batch stops within its explicit total budget. Following
Agent 115's runner observation6433748773, complete WITNESS records emitted
before a timeout are preserved and independently replayed even if the final
RESULT is missing. A partial record cannot establish a negative. A dedicated
TimeoutExpired regression checks preservation without treating the record
itself as a valid certificate.

For any reconstructed B, `triage_d7_drivers.py` independently recomputes both
normalizations using positional integers, checks the center's actual entering
carry and complementary outgoing carry, checks g, and checks both literal
neutral trims. It then calls unchanged Python `edgeOK` on every edge and
`cycleOK` on the complete closed list. A success writes the full edge list and
stops the batch immediately with intentional exit10. If its file cannot be
saved, the full verified witness is printed rather than discarded. This
would be a candidate requiring the user's
separate registered Lean `decide` and repository verification gate; no engine
FEASIBLE status alone is called a decimal proof.

## 4. Results

The exact R3,D7 graph has 517,474,728 vertices and 600,194,268 arcs.
Sink removal leaves678,464 vertices and 1,478,500 arcs. The compact residual
has 677,270 strongly connected components, of which only six are cyclic:

| Cyclic component size | Internal arcs |
|---:|---:|
|298|434|
|286|520|
|220|381|
|220|381|
|126|238|
|50|82|

Together these contain1,200 vertices and 2,036 internal arcs. The remaining
677,264 components are acyclic singletons. Thus the much larger sink residual
mostly consists of vertices that can reach a cycle but do not lie on one.
The final source completes SCCs, core export, and sampling in 10.0894 s
at 2,498 MiB peak RSS, with no cap. The exported core contains all 1,200 cyclic
vertices and 2,036 internal arcs, omitting transient and intercomponent arcs.

All six cyclic components branch. Enumerating their simple cycles would not
exhaust their closed walks: concatenated loops can produce new primitive
paired-label words. The catalog is therefore explicitly sampled:
for each internal arc, find a deterministic shortest return path, retain the
resulting cycle if its full period is at most64, then deduplicate and exclude
the held drivers. Even finishing all 2,036 arc queries does not establish a
complete period<=64 driver census.

All2,036 internal arcs yielded a return within64 phases. The sampler skipped
320 known-P24 samples,390 known-P42 samples, and 1,314 paired-rotation duplicates;
12 drivers remain, with 336 independently replayed edges and five primitive
paired-label classes. The actual full emitted periods are
`16,54,54,32,18,18,27,27,9,9,36,36`. These full witnesses are regenerated by the
command below; source metadata is not trusted by the independent checker.

### 4.1. New center fixtures and scoped exterior trials

Two new primitive P54/G20 centers have

```text
g=000101000101010010100010100100101010010100010100100101
e=101101010010101010101110100011101010101010001011100010
C0=[6,14,14,14,6]
```

The other has complemented e and C0=[12,4,4,4,12]. The full center widths are
5..7. Both fixed-e one-lap exterior runs exhaust at spatial width 4:
130 DAG nodes,16,281 operations,0.0062/0.0059 native seconds.

There are also two actual C9 cycles, with widths6/7:

```text
g=001010101
v=000010001
eA=101010100; C0A=[5,9,12,12,9,5]
eB=010101011; C0B=[13,9,6,6,9,13]
```

The sampler realizes these centers in projected full walks of lengths
9,18,27,36. Its extra prefix period is not imposed on the full B search.
Queries keep the emitted full period, allowing B to close at that later lap.
Four already covered queries were reused rather than rerun: the P9/P16 G4
cases from reviewed #334/#341, and saturated P32/G8 from 108/#386.

| New query | Count | Outcome | Reported final spatial depth |
|---|---:|---|---:|
| Primitive P54, the two e words |2|EXHAUSTED, empty frontier|4|
| C9 repeated twice, P18 |2|EXHAUSTED, empty frontier|57|
| C9 repeated three times, P27 |2|UNDECIDED,1.5M node cap|28|
| C9 repeated four times, P36 |2|UNDECIDED,1.5M node cap|15|

The P18 runs use215,233 DAG nodes/23,136,443 operations and 1.671/1.700 native
seconds. Each P27 run uses 154,031,125 operations before its cap, in 24.936/
26.458 native seconds; P36 uses 130,622,360 operations in 17.812/17.563 seconds.
The eight-query batch completed in 96.941 s. Every run had60 s/2 GiB limits;
there is no decimal candidate and no all-width conclusion for capped queries.

### 4.2. Exact SQ1 connection and independent original-core check

Rotating `001010101001010101` by two phases gives exactly
`101010100101010100`, the sole capped word in Agent 4's
[issue300](https://github.com/taco-jpg/p196-algorithm/issues/300). This identity
was checked against the original issue, not inferred from a similar-looking
pattern. Agent 4's other period 18 cases are outside this report's scope.

Agent 108's exact forward image is independent of the requested terminal e.
Explicit no-e runs in BOTH phase orientations reach an empty frontier57 with
zero accepts in all 58 layers:7,599,801 state occurrences, maximum frontier
450,672 at width 36,215,233 DAG nodes,23,136,443 operations. Wall times were
2.035/2.128 s. This closes the specified overflow word at ANY e, ANY finite B
width and arbitrary natural trims, as a COMPUTED result using the reviewed
engine's PAPER completeness reduction. It says nothing about longer powers.

The original transition core, separate from the MDD, with guarded Agent 107/#335
driver independently EXHAUSTS the same exact G:7,599,801 reached states,
depth 57,accepted=[],exit0,no cap. Wall time48.309 s,peak child RSS583,976 KiB.
Its state total exactly matches the MDD sum. The pinned source/driver hashes are
`c534ff54c819efe8a9c050167e08ca950428d619475f9647ca48cfcdc4e37cfc` and
`5ea7d672ca8a7139e18a838205a0b65596c2d7eae4f25c86d76df103de25944c`.
No other period 18 overflow word was retested or reattributed here.

## 5. Independent validation

The coupling gate reproduces all eight pinned-main source certificates,
56 complete edges, using integer and mirror checks. Flipping the first
overflow label rejects all eight corrupted controls. The external engine
integration reconstructs the known decimal P11 exterior (11 independently
replayed edges, widths25..29), then reproduces the published P24 fixed-driver
empty frontier at depth 39. These are controls, not new discoveries.

Final-source normal and optimized-Python controls both pass:

- 5,460 complete paired binary words,30,948 joint rotations,10,920 repetitions,
and 396 owned-family exclusions; independent rotations are rejected as a key.
- 105 arbitrary SCC fixtures,1,260 vertices/1,803 arcs, compared against complete
transitive closure, including empty graphs, self-loops and parallel arcs.
- Complete independently generated R1,D5 all-middles graph:137,052 vertices,
155,554 arcs;4,650 residual vertices/8,484 arcs; one cyclic 16/20 component.
- Exported core: every one of 2,036 arcs replays by positional integers; every
factor edge between listed vertices in its SCC is present; an independent
two-pass SCC partition matches all six components. This audit alone does not
establish whole-product core completeness; the controlled full traversal does.
- All12 emitted drivers/336 edges,56 known-source edges,66 owned-center edges,
and 96 original/rotated/doubled witness edges pass. Seven known certificates
show why shorter paired-label periods cannot silently shorten C.
- 12 malformed witnesses,6 malformed catalog containers/statuses,9 corrupted
cores,one owned-family insertion,and nonobject engine output are rejected; the timeout regression preserves
an earlier complete witness record for the separate arithmetic gate.
- Unsupported period,operation limit,insufficient memory and output-byte caps
all return UNDECIDED/nonzero. No exhausted-census status is used for sampling.

## 6. Reproduction and repository gate

The catalog/checker depend only on unchanged #381 own-source files; SciPy
1.17.0/NumPy are used solely by the small independent product-SCC control.
The triage engine is external Agent 108/#405, and the original-core comparison is
external Agent 107/#335 at `2c4123a98955d09d27aed1d727ce25e578378f03`.

```sh
c++ -O3 -std=c++17 -Wall -Wextra -pedantic calculation/agent-101/d7_driver_catalog.cpp -o /tmp/a101_d7_catalog_final
/tmp/a101_d7_catalog_final --discover --export-core --seconds 120 --memory-mb 4096 --operations 5000000000 --max-period 64 --max-drivers 16 > /tmp/agent101-d7-final.jsonl
python3 calculation/agent-101/check_d7_drivers.py --selftest --engine /tmp/a101_d7_catalog_final --catalog /tmp/agent101-d7-final.jsonl
python3 -O calculation/agent-101/check_d7_drivers.py --selftest --engine /tmp/a101_d7_catalog_final --catalog /tmp/agent101-d7-final.jsonl
python3 calculation/agent-101/triage_d7_drivers.py --selftest --engine /tmp/a101-exterior108
python3 calculation/agent-101/triage_d7_drivers.py /tmp/agent101-d7-final.jsonl --engine /tmp/a101-exterior108 --candidate /tmp/agent101-d7-candidate.json --indices 1,2,4,5,6,7,10,11 --seconds 60 --total-seconds 550 --memory-mb 2048 --max-drivers 8
```

Build `/tmp/a101-exterior108` from the pinned #405 `exterior_mdd.cpp`, with its
sibling `wide_count.hpp`, using `c++ -O2 -std=c++17`. The explicit all-e command is

```sh
/tmp/a101-exterior108 101010100101010100 1500000 300000000 1000 30 --witness
```

The comparison binary is built by pinned Agent 107`bauto_guarded.py --build
/tmp/a101-bauto335`, reading that pinned tree's unchanged `bauto.cpp`.
Its exact native command is

```sh
/tmp/a101-bauto335 10 18 18 -g 101010100101010100 -cap 10000000 -depth 1000
```

The reference subprocess is supervised with RLIMIT_AS=4 GiB,
RLIMIT_CPU=600 s and an outer 610 s wall timeout. Those resource failures would
remain UNDECIDED. Source catalog C++ SHA256 is
`c88a194da7ec3bd72e3f7899092d41fab776840bc83a1ade451b23c99e551b9d`.

Actual `python3 tools/verify.py --changed`: PASS. The rule scan checks
5,217 Lean files/301 projects;0 changed Lean modules and0 audited endpoints.
This is a repository gate, not Lean verification of these computations.
No new Lean module, unrestricted D7 theorem, all-period B classification,
period-descent theorem or decimal Lychrel certificate is claimed.
