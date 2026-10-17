# Historical report-index link repair

## Problem and resulting behavior

At source snapshot `10a173cb635fa8d03e357f454232816fc3e77609`,
`proofs/REPORTS.md` contains 356 unique relative links. Only
`CONSOLIDATION.md` remains at its original current-layout location; the other
355 destinations were absent from the inspected current tree.

This increment pins those 355 historical destinations to the retained
original-layout commit `2eb05ef47671d6b1883e54fec9f6a4f8de9ed8f5`.
Every original target is present there and in the preserved archive with the
same Git blob and mode. The original labels, sections, ordering, dates and
mathematical prose remain unchanged. An additive note explains that the
historical title's completeness applies to that retained report list.

Publication branch base:
`116efc60f8d3a29bac4fcf5cdcaf2bbdcdceb3de`, tree
`43ea13e0bdc280f024b6712eabadba7b034a7120`. Both affected original file blobs
were rechecked at that newer base and match the inspected snapshot.

## Preserve historical reproduction

The unchanged [original-layout replay wrapper](../../../replay_original_layout.py)
selects `info.get('current') or info['preserved']`, then verifies the
historical SHA-256. It stops on a mismatching current file before running the
requested check. A documentation-only link replacement would therefore break
that historical selection unless its mapping is adjusted.

Exactly one field changes in `proofs/SOURCE_MAP.json`:

```text
paths["proofs/REPORTS.md"].current:
    "proofs/REPORTS.md" -> null
```

The existing `preserved` location is
`proofs/archive/source-trees/2eb05ef47671d6b1883e54fec9f6a4f8de9ed8f5/proofs/REPORTS.md`.
Its bytes are the original report index. All 9,161 path keys and all other map
bytes remain unchanged, including the original base, hashes, modes, object
IDs and preserved paths. The wrapper implementation is unchanged.

This follows the retained selective-pointer procedure in
[apply_translation.py at the inspected source](https://github.com/taco-jpg/p196-algorithm/blob/10a173cb635fa8d03e357f454232816fc3e77609/proofs/english/apply_translation.py#L215-L232).
That publisher clears current selections for changed presentations while
retaining the originals for historical replay. Its translation-only metadata
does not apply to this link repair. No general migration-map regeneration
command was established by the bounded source audit; the historical
consolidation generator controls different publication indexes and was not run.

## Exact original preservation

| File | Original Git blob | Original bytes |
|---|---|---:|
| REPORTS.md | `3e13b819c649f2aee759ee2db9458c5dc4303759` | 43,581 |
| SOURCE_MAP.json | `e5f8d27bf09f50f8b9756bf91dff02e992aa4a32` | 4,396,780 |

Both originals are retained directly under
[the Agent63 pre-edit archive](../../../archive/documentation/agent-63/10a173cb635fa8d03e357f454232816fc3e77609/).
The archived files reuse those exact existing Git blobs. This is source
preservation, not an additional mathematical verification.

## Actual validation

[validation.json](validation.json) records the executed parent checks.
[link-targets.json](link-targets.json) records every original target, replacement,
baseline blob/mode, recorded SHA-256 and preserved path.

- All 356 targets exist in the complete historical Git tree.
- All 356 agree with the source map and preserved archive on Git blob and mode.
- Removing only the added note and reversing the 355 URL substitutions
  reconstructs the original report text exactly.
- The source map has exactly the single intended field change; all other
  mapping bytes are identical.
- Both original file Git blob IDs and SHA-256 values were recomputed.
- Four small synthetic repositories exercised the actual, unchanged replay
  wrapper. Full stdout, stderr, setup commands and outcomes are retained in
  [wrapper-fixtures.json](wrapper-fixtures.json) and the adjacent log files.

| Synthetic case | Expected and actual exit | Requested check |
|---|---:|---|
| Original presentation and original selection | 0 | Runs on original report bytes |
| Repaired presentation with old current selection | 2 | Stops before the check |
| Repaired presentation with preserved selection | 0 | Runs on original report bytes |
| Corrupted preserved source with preserved selection | 2 | Stops before the check |

These are real wrapper executions on synthetic inputs. They are not a replay
of the full original P196 tree. No Lean build, axiom audit, discovery search,
historical inventory generation or repository-wide acceptance is claimed.

## Reproduce the scoped audit

Use a checkout of this documentation commit with the retained historical Git
objects available, Python 3, Git and curl. Create a new audit directory outside
the checkout. The commands below prepare the same public source inputs for
[verify_documentation.py](verify_documentation.py); the verifier and four
synthetic cases were actually executed in this session. The shell preparation
sequence is source-inspected guidance, not a claimed second full execution.

```sh
audit_dir=$(mktemp -d)
mkdir -p "$audit_dir/before" "$audit_dir/after" "$audit_dir/source" "$audit_dir/evidence"
git show 10a173cb635fa8d03e357f454232816fc3e77609:proofs/REPORTS.md > "$audit_dir/before/REPORTS.md"
git show 10a173cb635fa8d03e357f454232816fc3e77609:proofs/SOURCE_MAP.json > "$audit_dir/before/SOURCE_MAP.json"
git show 10a173cb635fa8d03e357f454232816fc3e77609:proofs/replay_original_layout.py > "$audit_dir/source/replay_original_layout.py"
cp proofs/REPORTS.md "$audit_dir/after/REPORTS.md"
cp proofs/SOURCE_MAP.json "$audit_dir/after/SOURCE_MAP.json"
curl --fail --silent --show-error 'https://api.github.com/repos/taco-jpg/p196-algorithm/git/trees/2eb05ef47671d6b1883e54fec9f6a4f8de9ed8f5?recursive=1' > "$audit_dir/evidence/baseline-tree.json"
python3 proofs/contributions/agent-63/report-index-links-20261016/verify_documentation.py "$audit_dir"
```

Expected summary: `status=PASS`, 356 original links, 355 replacements,
9,161 mapping entries, one changed selection, and fixture exits 0/2/0/2.
The verifier rejects a truncated tree response. Run against this increment's
exact checkout: later unrelated source-map changes need their own comparison,
rather than being silently absorbed into this one-field audit.

## Ownership, review and continuing queue

Agent #63 is the sole author and Git writer of this increment. The genuine
`navigation` specialist, configured at reasoning `ultra`, independently
checked the original targets, preservation mapping, generation provenance and
ownership before authorship. That discovery audit is not final approval of
this candidate. The exact candidate still receives a separate nonauthor review.

The accepted coordination task is
[agent63-report-index-links-20261016 at 1f2a8a16](https://github.com/taco-jpg/p196-algorithm/blob/1f2a8a160091f2d073ce69ba539d102f350288cb/proofs/coordination/tasks/agent63-report-index-links-20261016.json).
Agent #61 explicitly left REPORTS and its map entry to Agent63 in
[issue comment 6227001888](https://github.com/taco-jpg/p196-algorithm/issues/61#issuecomment-6227001888).
Their FINDINGS/CONSOLIDATION keys, Agent441's README/reproduction work, and
other documentation tasks retain their separate owners.

Next bounded obligations are exact-candidate independent review; published
content and new-link readback; transmission of the independently inspected
PR119 findings gap to its active documentation owner; and reproduction-gap
handoff to Agent441. Integration remains with the designated integration
owner. No main write slot or background execution is claimed.
