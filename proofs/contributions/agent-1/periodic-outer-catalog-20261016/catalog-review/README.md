# Independent original outer-product catalog review

Agent #1 specialist `/root/research_status/cap4_existing_theorems`, under claim
`db88a5c78fd5f67ac134031d8486c26df9201799` (issue61 receipt6226182566).

**Diagnostic PASS:** all878 archived states and all1,458 complete labelled edges
match the original `bulk_phases.outputs` plus `outer_filter.outer`, and also the
proposed `outerImages`/`outerOutputs` formulas. Equality includes source order,
outgoing edge order, target coordinates, clocks, and all optional carry labels.
There were no mismatches or failed diagnostic attempts.

This is artifact/formula and literal-source-data review. It is not Lean
acceptance, a new reachability/SCC computation, or a whole-word realization.

## Original provenance

Archive directory:

`proofs/archive/source-trees/2eb05ef47671d6b1883e54fec9f6a4f8de9ed8f5/proofs/research/main_existence_attempt/continuation_pass/periodic_bulk_followup/`

| Artifact | Git blob | SHA256 |
| --- | --- | --- |
| `outer_filtered_graph.json.gz` | `c7bcc931f3cb36bd6845abeade0f7fd7b9723e08` | `c3eb0a4bd4bc8e390d7681746e66300851035dff1b102412e2d14977ed1088e5` |
| `outer_filtered_results.json` | `29ff1888439d8be43f3161dbdb59846d82063d7f` | `b444d8bcea8fb07368638b2f52cea57f2b4647dd385864313c12c9d0c4498506` |
| `outer_filter.py` and identical flattened `proofs/outer_filter__4b3d159990f5e177.py` | `ca0fe5e4cf9f6df4528d1e1375c9bfc404ad04f6` | `6c336a1b7d1d71e6525bec42a001572bfd7ee98115c2991b961d10c455f30d9c` |
| `bulk_phases.py` and identical flattened `proofs/bulk_phases__50a5613b2ee6f003.py` | `46a1ad0bbd6491685f98f6dc9201c9c16775a50c` | `5bdd7d03f0e29f081dddde9ad6e00223f3acc19a26db8d8baca2c41e0be848d4` |

Decoded outer graph SHA256:
`cbd5c62ac2af58d0d0ce1cbb6f0cf9199ac49c75291d062179caf15f96e1ad50`.
The original phase graph, original `Agent8.overflow`/`nextExterior` source, and
final phase catalog source are also pinned in `run-001/provenance.json`.
The literal phase catalog SHA256 is
`44445a343635503c940ea125727d0bbb75bbf7dce24be62c28a660241363f9f9`;
its124 complete edges were parsed independently and matched to the original
phase graph before they were used in the proposed product calculation.

## Outer arithmetic and order

All36 scalar cases `1 ≤ p ≤ 18`, `g ∈ {0,1}` were checked directly. The
original formula loops over incoming bits0,1, retains those with
`(p+e)//10 = g`, and sorts the set of corresponding outer targets. The proposed
formula filters the same two bits by `Agent8.overflow p e = g`, maps
`Agent8.nextExterior p e`, and erases duplicates. Their resulting lists agree
exactly, including order:

| Outside coefficient | Clock0 images | Clock1 images |
| --- | --- | --- |
| `1 ≤ p ≤ 8` | `[2*p, 2*p+1]` | `[]` |
| `p = 9` | `[18]` | `[10]` |
| `10 ≤ p ≤ 18` | `[]` | `[p % 10 + 1]` |

For high outside coefficients both incoming bits have the same image. The
original graph intentionally forgets this incoming bit and deduplicates the
outer target **before** forming product edges. Keeping each bit as a separate
edge would produce1,864 edges, with406 repeated copies; the archived and
proposed deduplicated formulas both produce1,458. `scalar-checks.json` records
every bit case, raw target list, and deduplicated list.

The product comparison separately uses the original generator's phase outputs
and the literal Lean `phaseEdges.filter` by source phase. Each phase edge is
combined, in order, with its compatible deduplicated outer images. All878
outgoing lists match exactly through both routes. There is no phase rotation,
source reindexing, clock replacement, or reordering hidden in this comparison.

## Labels, initial states, and finite checks

- The878 state tuples are distinct, in the original sorted order. Each phase
  belongs to the retained59-phase catalog; every outside coefficient is in1..18.
- The18 initial tuples are exactly `([14,14,4,4],p)` for `p=1,...,18`, in that
  order; all occur in the catalog.
- All1,458 complete labelled edges are distinct, and every target is in the
 878-state catalog. Outgoing lists contain every compatible original phase
  label and deduplicated outer target, with no missing or extra entries.
- Exactly108 product edges have the all-nine source phase. They retain the
  original two boundary-carry labels, distinct from the forgotten outer
  incoming bit. Their phase targets all equal the constant `18-9*(a+b)`.
- The stored component lists partition the878 states without repetition and
  have recorded sizes:128 singletons, three components of18, and one of696.
  This verifies the stored partition and counts only; no SCC algorithm runs.

Neither abstract phase labels nor the outer incoming bit are asserted to be
freely realizable together for a fixed whole word. The exact arithmetic bridge
and the finite Lean theorem audits remain separate author/reviewer work. The
catalog is a necessary projection, not a realizability certificate or an
affirmative finite-interface return.

## Retained results

`run-001/verification.json` and `run-001/run.log` record the successful result,
Python version3.12.14, input identities, script hash, and source-drift check.
`original-payload.json` retains the exact decoded artifact;
`original-functions.txt` retains the two exact executed function bodies.
`row-checks.json` and `edge-checks.json` index every stored source/edge and retain
the matching phase-edge index, deduplicated targets, and all witnessing incoming
bits. The full node and edge exports are not summarized away.

| Export | SHA256 |
| --- | --- |
| `states.json` | `cc488b212f8fd622b47db4f0da91fd396127090fbb2097debaf8ec938341bff1` |
| `initial.json` | `b6b9cd4d95e0e4ce6e6a2709b70a9dcb35dd93679be7291747035ad650f6aeb5` |
| `labelled-edges.json` | `3c93c099cd4cb1eaf21db8709746e121379ea693ac446dae0febe6ced249622b` |
| `scalar-checks.json` | `c56b590d72ec0712af491cf4aebb631610a65ecba3c4016a9f55adc3ec7b9d9c` |
| `edge-checks.json` | `6aaf20efdf330ca6df72c6ee6531abd27a330728884779f785471e6c7c4a6444` |

## Literal Lean snapshot comparison

`lean-data-001/` retains the exact inspected source snapshots and a separate
PASS receipt. All878 literal `outerCatalog` nodes and all1,458 literal
`outerEdges` entries match the archive in full and in exact order. The
`outerImages` and `outerOutputs` definition bodies match the formulas checked
by the diagnostic, including `eraseDups` and preservation of `e.carries`.

- `Agent1PeriodicOuterCatalog.lean` snapshot SHA256:
  `6fdd1a6850553ecd56fe4663be3f9f9541e5315a1f3b489c4c9fa782b4c017d4`.
- `Agent1PeriodicOuterChoices.lean` snapshot SHA256:
  `9bd84fb0c22b2252fb71f0310fe763e6a07192ef0fb80299763459ab48fb76ad`.

The subsequent chunked-source rebind is retained in `lean-data-002/`, for Catalog
SHA256 `d2733f0f4373969985e91e969e7c76e2f32e9bf20483b696d6bb186c2b846365`.
The Choices source is unchanged. The independent parser expands the **actual
public append expressions**, in their written order, using their59 named
literal node blocks and59 named literal edge blocks. It rejects repeated,
missing, undefined, unused, or mixed-phase blocks. It does not trust the
author's chunk generator or assume a numeric block ordering.

The expanded878-node and1,458-labelled-edge arrays equal both the original
archive and the preserved `lean-data-001/` source, with exact ordering and all
labels. Their serialized SHA256 values remain exactly
`cc488b212f8fd622b47db4f0da91fd396127090fbb2097debaf8ec938341bff1` and
`3c93c099cd4cb1eaf21db8709746e121379ea693ac446dae0febe6ced249622b` respectively.
`lean-data-002/append-expansion.json` retains every actual block reference,
block size, and phase order. Both source snapshots, both verification receipts,
and the exact comparison script for each version are preserved. No1,458-edge
formula replay was repeated for this representation-only rebind.

The final frozen-source rebind is `lean-data-003/`, Catalog SHA256
`1e6ebcc4e47df94162467d52826cee4e64c5707a622ac775008671d3fb0391e2`.
Here the public definitions use `outerNodeBlocks.flatten` and
`outerEdgeBlocks.flatten`. The parser follows those exact public references,
reads each named list's59 block references in its written order, and expands
the literal blocks. The result again equals the original archive and **both**
prior reviewed source snapshots, preserving every878 node and1,458 complete
labelled edge. The two expanded array hashes above remain unchanged.

`lean-data-003/verification.json` records the exact final source hash, both
baseline source hashes, actual named-list assembly, array hashes, and no source
drift. `append-expansion.json` retains the declared block order, and the exact
third parser version is saved alongside the final source snapshot. All earlier
receipts, sources, and parser snapshots remain intact. Only data parsing and
comparison ran; the original1,458-edge diagnostic was not repeated.

Only literal data and definition bodies are compared; Lean compilation, theorem
adequacy, and axioms remain outside this diagnostic review.

## Reproduce without graph discovery

From the worktree root, with new output directory names:

```sh
python3 proofs/contributions/agent-1/periodic-outer-catalog-20261016/catalog-review/replay.py \
  --source-root . --output-dir /tmp/agent1-outer-catalog-review
python3 proofs/contributions/agent-1/periodic-outer-catalog-20261016/catalog-review/compare_lean_data.py \
  --source-root . --output-dir /tmp/agent1-outer-literal-data-review
```

Only the original `outputs` and `outer` function ASTs are executed. Neither
generator's `main`, BFS, SCC, or cycle-search code is run. The replay iterates
the existing finite artifact and36 scalar arithmetic cases; it does not discover
new graph states or reestablish reachability/minimality. All work was confined
to this review directory: no Lean execution, mathematical-source edits, Git
mutation, or external issue post was performed.
