# Independent stored-partition and rank diagnostic

Agent #1 specialist `/root/research_status/cap4_existing_theorems`, under claim
`efe6d4b95f53ad8fbcebf113f8da0616dfa67b22`.

**PASS:** the original stored partition covers all 878 catalog nodes exactly
once. Every one of the 1,458 archived labelled edges has nondecreasing component
index. Thus the proposed positive rank `132 - component_index` is nonincreasing,
and decreases by at least one across different components. These are checked
local data conditions, not a new SCC computation or an accepted Lean theorem.

## Exact provenance

Original artifact:

`proofs/archive/source-trees/2eb05ef47671d6b1883e54fec9f6a4f8de9ed8f5/proofs/research/main_existence_attempt/continuation_pass/periodic_bulk_followup/outer_filtered_graph.json.gz`

- Git blob: `c7bcc931f3cb36bd6845abeade0f7fd7b9723e08`.
- Compressed SHA256: `c3eb0a4bd4bc8e390d7681746e66300851035dff1b102412e2d14977ed1088e5`.
- Decoded SHA256: `cbd5c62ac2af58d0d0ce1cbb6f0cf9199ac49c75291d062179caf15f96e1ad50`.

`run-001/provenance.json` also pins the unchanged source of `catalogOrderKey`
and the existing `CondensationBound` definitions. The latter's `RankCertificate`
requires `weight(component) ≤ rank(component)` at each visited node. Therefore
weight one is compatible with `132 - component_index`, whose values are 1..132;
the otherwise monotone expression `131 - component_index` would have rank zero
at component 131 and fail that requirement. A positive clamped total extension
may be used outside the stored labels, but its values there are not part of the
original partition claim.

## Checked component facts

The stored 132 component lists form a disjoint exact partition, with 128
singletons, three blocks of 18 nodes, and one block of 696 nodes. Internal edges
occur **only** in the following four stored components:

| Index | Nodes | Exact membership description | Internal labelled edges |
| --- | ---: | --- | ---: |
| 8 | 696 | Nonconstant phases; 56 distinct indexed phases | 1,040 |
| 129 | 18 | `([9,9,9,9], p)` for `p = 1..18` | 54 |
| 130 | 18 | `([18,18,18,18], p)` for `p = 1..18` | 27 |
| 131 | 18 | `([0,0,0,0], p)` for `p = 1..18` | 27 |

The other 310 labelled edges cross components and strictly lower the positive
rank. Every one of the 128 singleton components has no internal edge. The
proposed nonzero return core, components 8, 129, and 130, has 732 nodes.

The zero component retains its 27 abstract internal edges. Removing it from a
**full tuple return** needs the separate existing zero-state no-cycle theorem;
this diagnostic does not delete zero edges or infer ordinary termination.

For the 18 original initial nodes `([14,14,4,4],p)`, the exact stored labels are:

| Outside coefficient | Component index |
| --- | --- |
| `p = 1..8` | `129 - p` |
| `p = 9` or `p = 10` | `8` |
| `p = 11..18` | `18 - p` |

Consequently the only initial outside values lying in the proposed nonzero
return core are 9 and 10. The new full-tuple return theorem remains the author's
formal obligation; no existence of a return for either survivor follows here.

## Retained data and matching tables

All outputs are under `run-001/`:

- `verification.json` and `run.log`: result, exact input and script hashes,
  Python version, counts, and no source drift.
- `components.json`: the complete original ordered partition.
- `edge-rank-checks.json`: every original row/edge index, complete labelled
  edge, source/target components, and both positive ranks.
- `component-transitions.json`: exact labelled-edge multiplicities between
  different components; `component-summary.json`: each block's size and rank.
- `node-component-table.json`: every original catalog index, node, existing
  base-19 key, component label, and positive rank.
- `component-by-catalog-index.json`: 878 labels in original catalog order.
- `key-component-table.json`: 878 ordered `(catalogOrderKey, component)` pairs.
- `phase-component-table.json`: 59 phase rows, with component entries indexed
  by outside value 0..18. `null` means no node in the stored catalog; it must
  not be interpreted as a new state or assigned a component by this evidence.
- `transient-overrides.json`: precisely the 128 singleton nodes outside
  components 8, 129, 130, and 131, for a compact matching-table implementation.
- `initial-classification.json`: all 18 initial memberships and survivor flags.

The numeric bridge author received the exact orientation, counts, initial
classification, and matching-table paths. No files owned by that author were
written. A total Lean component function using default label 8 away from known
cases is an implementation choice; its interpretation as this original
partition must be restricted to catalog nodes.

## Reproduction and limits

```sh
python3 proofs/contributions/agent-1/periodic-return-core-20261016/data-review/review.py \
  --source-root . --output-dir /tmp/agent1-return-core-data-review
```

Use a new output directory. The first and only diagnostic run passed under
Python 3.12.14. The script reads the existing component lists and edges; it never
runs SCC, BFS, path, cycle, or reachability discovery. It checks every local
inequality needed by the proposed rank certificate but does not claim SCC
minimality, interval residence bounds, a full-tuple return theorem, or any
ordinary numeric orbit result. No Lean execution, mathematical-source edit,
Git mutation, or external issue post was performed. All work was confined to
this `data-review/` directory.
