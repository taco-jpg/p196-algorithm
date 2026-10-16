# Independent review of the retained phase catalog

Agent #1 specialist `/root/research_status/cap4_existing_theorems`, under claim
`6db01dafab1ec876d24c9964bc6086440ed21266` (issue61 receipt6226044951).

**Diagnostic PASS:** all59 archived indexed phases and all124 complete labelled
edges are retained exactly. Every original generator output agrees, row for row,
with the stored graph and with the proposed list-normalizer/zipper arithmetic.
No mismatch was found. This is artifact and source-data review, not a Lean proof.

## Exact source provenance

Archive directory:

`proofs/archive/source-trees/2eb05ef47671d6b1883e54fec9f6a4f8de9ed8f5/proofs/research/main_existence_attempt/continuation_pass/periodic_bulk_followup/`

| Original artifact | Git blob | SHA256 |
| --- | --- | --- |
| `bulk_phase_graph.json.gz` | `ef81b2d214f37e79d04cd8c8aa9bc764c227a54e` | `a22b2e39e4b2ed31d00b0c69694cd25b29f63135cd2378a16e3a434781855bb2` |
| `bulk_phase_results.json` | `4a161c89c61706da3c80387e27f204239896b1a7` | `9cef6aaf456d4b39e4ed7965401f2aba40d29553b0b2241ec4dad53926d4613f` |
| `bulk_phases.py` and identical flattened `proofs/bulk_phases__50a5613b2ee6f003.py` | `46a1ad0bbd6491685f98f6dc9201c9c16775a50c` | `5bdd7d03f0e29f081dddde9ad6e00223f3acc19a26db8d8baca2c41e0be848d4` |

Decoded graph payload SHA256:
`4100f332c808b277d8d3052fc6b16aef0637aa185c45bd3525ddac5267ebc3c6`.
`run-001/provenance.json` also pins the unchanged original Lean primitive sources
`ActualWordBridge` and `Agent1PeriodicGuard`; their fixed-digit, terminal-carry,
and zipper definitions are interpreted directly by the independent diagnostic.
No archived file was modified.

## Orientation and all-nine exception

For every non-nine recorded phase `w`, set

```
U = fixedDigits w (terminalCarry w 0)
V = fixedDigits w.reverse (terminalCarry w.reverse 0)
```

All58 non-nine phases satisfy `U = low` and `V.reverse = high`, where the
original cyclic formula obtains each incoming carry from the nearest non-nine
coefficient in the respective direction. For clock0 the zipper uses `high`;
for clock1 it uses `[high[3], high[0], high[1], high[2]]`. Therefore its indexed
target is exactly

```
low[i] + high[(i-clock) mod 4]
```

The116 non-nine labelled edges all agree with this formula. There is no change
of initial index, rotation equivalence, reflected source, or clock sign.

The all-nine source is a separate branch. Its eight labels are exactly the
ordered triples `(clock,left_carry,right_carry)` in `{0,1}³`, in the original
lexicographic product order. The two digit blocks are constant `9-9*a` and
`9-9*b`; both clocks give the constant target `18-9*(a+b)`. All eight labels
match independently. Per clock, carries00 yield18, carries01 and10 yield9,
and carries11 yield0. Applying the zero-entry `phaseImage` to all-nine without
this exception would retain only the target18 branch.

These are abstract possibilities. The review does not assert that the two
boundary carries and clock may be selected independently for a fixed full word.

## Complete finite data checks

- Exactly59 phases, all distinct, in the archived sorted indexed order; every
  phase has four entries in0..18. Initial `(14,14,4,4)` is present.
- Exactly124 complete labelled edges, all distinct. Every non-nine phase has
  exactly clocks0 and1 and no carry fields. All-nine has exactly all eight
  clock/carry triples. Original `outputs()` reproduces every complete edge
  dictionary and its order with no missing or extra labels.
- Every target lies in the59-phase catalog. Constants are exactly0,9,18.
- Forgetting carry labels leaves122 distinct `(source,clock,target)` triples;
  forgetting clocks as well leaves117 distinct `(source,target)` arcs. Thus
 124 is a labelled edge count and must not be replaced by a simple-graph count.
- The stored component lists partition all59 phases without repetition and
  have sizes1,1,1,56. This check does not recompute strongly connected components.

`run-001/phases.json` retains the full59-phase list, and
`run-001/labelled-edges.json` retains all124 complete edge dictionaries.
`run-001/edge-checks.json` gives each original zero-based row/edge index, label,
stored and generator target, low/high digit arrays, zipper result, and carry
data. Hashes of these deterministic data exports:

| Export | SHA256 |
| --- | --- |
| `phases.json` | `e57821a4098b57db043b87e9c613f04cc0c1b09e8bf1789923d5860957670513` |
| `labelled-edges.json` | `5f3424b9cc1da37d1bca1dfca76b8dc16913cb1d1f9ae7efdb7aa62e25967fa1` |
| `edge-checks.json` | `315e2086b89b6ffad644fa148e89b95952d440162088ca6252999b03877a231d` |

## Literal Lean data comparison

`lean-data-001/` separately retains the exact inspected source snapshots.
The literal `phaseCatalog` and `phaseEdges` definitions match the archived data
in full, including order and every optional carry label. The inspected
`phaseImage` definition matches the exact zipper expression reviewed above.

- Catalog snapshot SHA256:
  `a1f4c4a8ceb90b26bc7885e647b314d3acf8951b1ae14d9c2113fa280342d269`.
- Phase snapshot SHA256:
  `705c139614ffd4f9f20a305f7c4bff20059da0c7fa127ca180ff8a88397a51ce`.

These snapshots may precede the authors' final proof freeze. This comparison
accepts literal data only; final Lean compilation, theorem statements, and axiom
review belong to the separate independent reviewer. The comparison can be rerun
against a later frozen source without changing the original archive replay.

## Reproduction and scope

The successful run used Python3.12.14. `replay.py` pins all original input hashes,
extracts and executes only the unchanged generator's `outputs()` function by AST,
then compares it to an independently implemented direct zipper calculation.
The generator's `main`, graph discovery, SCC algorithm, and cycle search are
never called. Checks iterate only the already recorded59 phases and124 labels;
reachability is not recomputed. Original reachability claims remain attributed
to the retained artifact. No ordinary trajectory search or infinite-orbit claim
is made, and no Lean process, Git mutation, or external issue post was performed.

From the worktree root, with new output directory names:

```sh
python3 proofs/contributions/agent-1/periodic-phase-catalog-20261016/catalog-review/replay.py \
  --source-root . --output-dir /tmp/agent1-phase-catalog-review
python3 proofs/contributions/agent-1/periodic-phase-catalog-20261016/catalog-review/compare_lean_data.py \
  --source-root . --output-dir /tmp/agent1-phase-literal-data-review
```

The first and only diagnostic run passed. `run-001/verification.json` and
`run-001/run.log` retain the final result and script hash; no failed replay or
superseded computational claim is omitted.
